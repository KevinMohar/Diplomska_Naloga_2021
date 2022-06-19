import glob
import heapq
import itertools
import operator
import os
from DataProvider import DataProvider
from ApplicationConstants import ApplicationConstants, DataPaths, Logging
import threading


def CalcSimWithYoulsQ(prod1, prod2):
    purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = getNumOfPurchases(
        prod1, prod2)

    similarity = 0

    # Yules' Q
    a = ((purchasedBoth * purchasedNone) -
         (purchasedFirst*purchasedSecond))
    b = ((purchasedBoth * purchasedNone) +
         (purchasedFirst*purchasedSecond))

    if b != 0:
        similarity = a/b

    if similarity < 0:
        similarity = 0

    return similarity


def getNumOfPurchases(prod1: int, prod2: int):
    '''
    Function accepts 2 products and returns values needed for Youls' Q calculation
    '''
    countBoth = 0
    countNone = 0
    countFirst = 0
    countSecond = 0

    found = [False, False, False, False]

    # both
    if (prod1, prod2) in bothProductPurchases or (prod2, prod1) in bothProductPurchases:
        countBoth = bothProductPurchases[(prod1, prod2)] if (
            prod1, prod2) in bothProductPurchases else bothProductPurchases[(prod2, prod1)]
        found[0] = True

    # none
    if (prod1, prod2) in noneProductPurchases or (prod2, prod1) in noneProductPurchases:
        countNone = noneProductPurchases[(prod1, prod2)] if (
            prod1, prod2) in noneProductPurchases else noneProductPurchases[(prod2, prod1)]
        found[1] = True

    # first but not second
    if (prod1, prod2) in oneProductPurchases:
        countFirst = oneProductPurchases[(prod1, prod2)]
        found[2] = True

    # second but not first
    if (prod2, prod1) in oneProductPurchases:
        countFirst = oneProductPurchases[(prod1, prod2)]
        found[3] = True

    if not all(found):
        for user_id in dp.usersProducts:
            # both
            if prod1 in dp.usersProducts[user_id] and prod2 in dp.usersProducts[user_id]:
                countBoth += 1

            # none
            if prod1 not in dp.usersProducts[user_id] and prod2 not in dp.usersProducts[user_id]:
                countNone += 1

            # first but not second
            if prod1 in dp.usersProducts[user_id] and prod2 not in dp.usersProducts[user_id]:
                countFirst += 1

            # second but not first
            if prod1 not in dp.usersProducts[user_id] and prod2 in dp.usersProducts[user_id]:
                countSecond += 1

        bothProductPurchases.update({(prod1, prod2): countBoth})
        bothProductPurchases.update({(prod2, prod1): countBoth})
        noneProductPurchases.update({(prod1, prod2): countNone})
        noneProductPurchases.update({(prod2, prod1): countNone})
        oneProductPurchases.update({(prod1, prod2): countFirst})
        oneProductPurchases.update({(prod2, prod1): countSecond})

    return (countBoth, countNone, countFirst, countSecond)


def PreProcessItemBasedData(products):
    for prod1 in products:
        for prod2 in dp.products:
            if prod1 != prod2:
                sim = 0

                if (prod1, prod2) in productSimilarities:
                    sim = productSimilarities[(prod1, prod2)]
                    if (prod2, prod1) not in productSimilarities:
                        productSimilarities[(prod2, prod1)] = sim
                elif (prod2, prod1) in productSimilarities:
                    sim = productSimilarities[(prod2, prod1)]
                    if (prod1, prod2) not in productSimilarities:
                        productSimilarities[(prod1, prod2)] = sim
                else:
                    sim = CalcSimWithYoulsQ(prod1, prod2)
                    productSimilarities[(prod1, prod2)] = sim
                    productSimilarities[(prod2, prod1)] = sim

                if sim > MIN_SIMILARITY_TRESHOLD:
                    dp.storeSimilaritiesToPickle(
                        {(prod1, prod2): sim}, global_lock)


def split_dict_equally(input_dict, chunks=2):
    "Splits dict by keys. Returns a list of dictionaries."
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k, v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks-1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


def CleanDBcache():
    for filename in glob.glob(DataPaths.itemSimilarities + "*"):
        os.remove(filename)

    for filename in glob.glob(DataPaths.usersPurchases + "*"):
        os.remove(filename)


SAMPLE_SIZE = ApplicationConstants.SAMPLE_SIZES[0]
USERS_PRODUCTS_STORE_SIZES = ApplicationConstants.USERS_PRODUCTS_STORE_SIZES
ITEM_SIMILARITY_STORE_SIZES = ApplicationConstants.ITEM_SIMILARITY_STORE_SIZES
NUM_OF_THREADS = 64
MIN_SIMILARITY_TRESHOLD = 0

dp = DataProvider(clearCache=False, sampleSize=SAMPLE_SIZE)

productSim = dp.getSimilaritiesFromPickle()
itemSimilarites = {}


CleanDBcache()

#############################################################################################
# calculate users most frequent purchases for content based
#############################################################################################
for N in USERS_PRODUCTS_STORE_SIZES:
    userItemPurchases = {}

    for user_id in dp.users:
        userOrderdProducts = dp.getUserOrderedProducts(
            user_id)  # get number of users product purchases
        topNProductsKeys = heapq.nlargest(
            N, userOrderdProducts, key=userOrderdProducts.get)
        userItemPurchases[user_id] = topNProductsKeys

    dp.storeUserPurchasesToPickle(userItemPurchases, N)


#############################################################################################
# calculate similarities for item based
#############################################################################################
bothProductPurchases = {}
noneProductPurchases = {}
oneProductPurchases = {}
productSimilarities = {}
prepData = split_dict_equally(dp.products, NUM_OF_THREADS)

threads = []
global_lock = threading.Lock()

for dataset in prepData:
    thread = threading.Thread(
        target=PreProcessItemBasedData, args=(dataset,))
    threads.append(thread)

print(Logging.INFO + "Starting preprocesing...")
[thread.start() for thread in threads]
[thread.join() for thread in threads]


# calculate similarities
for N in ITEM_SIMILARITY_STORE_SIZES:
    for product in dp.products:
        sim = {}

        for k1, k2 in productSim:
            if k1 == product:
                sim[k2] = productSim[(k1, k2)]

        sortedDict = dict(sorted(sim.items(),
                                 key=operator.itemgetter(1), reverse=True))

        itemSimilarites[product] = list(sortedDict)[:N]
    dp.storeItemSimilaritiesToPickle(itemSimilarites, N)


print(Logging.INFO + "DONE preprocesing data!!!")
