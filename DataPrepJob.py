import glob
import heapq
import os
import time
from DataProvider import DataProvider
from ApplicationConstants import ApplicationConstants, DataPaths, Logging
from DataModels import Similarity
import threading
from Telematry import Telematry

newSimilarityCalculated = False


def CalcSimWithYoulsQ(prod1, prod2, globalLock):
    purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = getNumOfPurchases(
        prod1, prod2, globalLock)

    similarity = 0

    # Yules' Q
    a = ((purchasedBoth * purchasedNone) -
         (purchasedFirst*purchasedSecond))
    b = ((purchasedBoth * purchasedNone) +
         (purchasedFirst*purchasedSecond))

    if b != 0:
        similarity = a/b

    if similarity < MIN_SIMILARITY_TRESHOLD:
        similarity = MIN_SIMILARITY_TRESHOLD

    return similarity


def getNumOfPurchases(prod1: int, prod2: int, globalLock):
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

        while globalLock.locked():
            continue

        globalLock.acquire()

        bothProductPurchases.update({(prod1, prod2): countBoth})
        bothProductPurchases.update({(prod2, prod1): countBoth})
        noneProductPurchases.update({(prod1, prod2): countNone})
        noneProductPurchases.update({(prod2, prod1): countNone})
        oneProductPurchases.update({(prod1, prod2): countFirst})
        oneProductPurchases.update({(prod2, prod1): countSecond})

        globalLock.release()

    return (countBoth, countNone, countFirst, countSecond)


def PreProcessItemBasedData(products, productsFromOrders, globalLock):

    for prod1 in products:
        for prod2 in productsFromOrders:
            if prod1 != prod2:
                sim = 0

                # check if similarity was already calcualted for this product pair
                if (prod1, prod2) in productSimilarities:
                    sim = productSimilarities[(prod1, prod2)]
                    if (prod2, prod1) not in productSimilarities:
                        productSimilarities[(prod2, prod1)] = sim
                elif (prod2, prod1) in productSimilarities:
                    sim = productSimilarities[(prod2, prod1)]
                    if (prod1, prod2) not in productSimilarities:
                        productSimilarities[(prod1, prod2)] = sim
                else:
                    # similarity not calculated --> calculate it
                    sim = CalcSimWithYoulsQ(prod1, prod2, globalLock)
                    productSimilarities[(prod1, prod2)] = sim
                    productSimilarities[(prod2, prod1)] = sim
                    newSimilarityCalculated = True


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


SAMPLE_SIZE_ORDERS = ApplicationConstants.ORDERS_SAMPLE_SIZE_TO_USE

USERS_PRODUCTS_STORE_SIZES = ApplicationConstants.USERS_PRODUCTS_STORE_SIZES
ITEM_SIMILARITY_STORE_SIZES = ApplicationConstants.ITEM_SIMILARITY_STORE_SIZES

NUM_OF_THREADS = 64
MIN_SIMILARITY_TRESHOLD = 0

dp = DataProvider(clearCache=False, sampleSizeOrders=SAMPLE_SIZE_ORDERS)
tel = Telematry()
tel.DB_orders = SAMPLE_SIZE_ORDERS


# delete pickle files
CleanDBcache()

#############################################################################################
# calculate users most frequent purchases for content based [OK]
#############################################################################################
print(Logging.INFO + "Started content based data preprocessing...")
tel.dataPrep_content_startTime = time.time()

for N in USERS_PRODUCTS_STORE_SIZES:
    userItemPurchases = {}

    for user_id in dp.users:
        # get number of users product purchases
        userOrderdProducts = dp.getUserOrderedProducts(
            user_id)

        # select N most purchased products
        topNProductsKeys = heapq.nlargest(
            N, userOrderdProducts, key=userOrderdProducts.get)
        userItemPurchases[user_id] = topNProductsKeys

    # store N most purchased products for users
    dp.storeUserPurchasesToPickle(userItemPurchases, N)

tel.dataPrep_content_endTime = time.time()
print(Logging.INFO + "Content based data preprocessing completed!")

#############################################################################################
# calculate similarities for item based
#############################################################################################
print(Logging.INFO + "Starting item based data preprocesing...")
tel.dataPrep_itemB_startTime = time.time()

bothProductPurchases = {}
noneProductPurchases = {}
oneProductPurchases = {}
productSimilarities = dp.getSimilaritiesFromPickle()
itemSimilarites = {}
prepData = split_dict_equally(dp.products, NUM_OF_THREADS)

threads = []
global_lock = threading.Lock()

# calculate similarities between all items
for dataset in prepData:
    thread = threading.Thread(
        target=PreProcessItemBasedData, args=(dataset, dp.products, global_lock))
    threads.append(thread)

[thread.start() for thread in threads]
[thread.join() for thread in threads]

# store calulted similarities between all items for next time
if newSimilarityCalculated:
    dp.storeSimilaritiesToPickle(productSimilarities)

print(Logging.INFO + "Calculated similarities between all items")

# store N similar products for each item
for k1, k2 in productSimilarities:
    if k1 in itemSimilarites:
        itemSimilarites[k1].append(Similarity(
            k1, k2, productSimilarities[(k1, k2)]))
    else:
        itemSimilarites[k1] = [Similarity(
            k1, k2, productSimilarities[(k1, k2)])]

for N in ITEM_SIMILARITY_STORE_SIZES:
    tmp = {}

    for prod in itemSimilarites:
        sortedList = sorted(itemSimilarites[prod],
                            key=lambda x: x.similarity, reverse=False)
        data = []
        if N < len(sortedList):
            data = sortedList[:N]
        else:
            data = sortedList

        tmp[prod] = data
    dp.storeItemSimilaritiesToPickle(tmp, N)

print(Logging.INFO + "Stored N most similar items for each item.")

tel.dataPrep_itemB_endTime = time.time()
print(Logging.INFO + "Item based data preprocesing completed!")
tel.PrintDataPrepJobStats()
