import heapq
import itertools
import operator
from DataProvider import DataProvider
from ApplicationConstants import Logging
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


dp = DataProvider(clearCache=True)

NUM_OF_THREADS = 64
MIN_SIMILARITY_TRESHOLD = 0

productSim = dp.getSimilaritiesFromPickle()
itemSimilarites1 = {}
itemSimilarites10 = {}
itemSimilarites50 = {}
itemSimilarites100 = {}
userItemPurchases1 = {}
userItemPurchases10 = {}
userItemPurchases50 = {}
userItemPurchases100 = {}

#############################################################################################
# calculate users most frequent purchases for content based
#############################################################################################
for user_id in dp.users:
    # get number of users product purchases
    userOrderdProducts = dp.getUserOrderedProducts(user_id)

    top1Products = heapq.nlargest(
        1, userOrderdProducts, key=userOrderdProducts.get)
    top10Products = heapq.nlargest(
        10, userOrderdProducts, key=userOrderdProducts.get)
    top50Products = heapq.nlargest(
        50, userOrderdProducts, key=userOrderdProducts.get)
    top100Products = heapq.nlargest(
        100, userOrderdProducts, key=userOrderdProducts.get)

    userItemPurchases1[user_id] = top1Products
    userItemPurchases10[user_id] = top10Products
    userItemPurchases50[user_id] = top50Products
    userItemPurchases100[user_id] = top10Products

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
for product in dp.products:
    sim = {}

    for k1, k2 in productSim:
        if k1 == product:
            sim[k2] = productSim[(k1, k2)]

    sortedDict = dict(sorted(sim.items(),
                             key=operator.itemgetter(1), reverse=True))

    itemSimilarites1[product] = list(sortedDict)[:1]
    itemSimilarites10[product] = list(sortedDict)[:10]
    itemSimilarites50[product] = list(sortedDict)[:50]
    itemSimilarites100[product] = list(sortedDict)[:100]

#############################################################################################
# store data
#############################################################################################
dp.storeItemSimilaritiesToPickle(itemSimilarites1, 1)
dp.storeItemSimilaritiesToPickle(itemSimilarites10, 10)
dp.storeItemSimilaritiesToPickle(itemSimilarites50, 50)
dp.storeItemSimilaritiesToPickle(itemSimilarites100, 100)
dp.storeUserPurchasesToPickle(userItemPurchases1, 1)
dp.storeUserPurchasesToPickle(userItemPurchases10, 10)
dp.storeUserPurchasesToPickle(userItemPurchases50, 50)
dp.storeUserPurchasesToPickle(userItemPurchases100, 100)


print(Logging.INFO + "DONE preprocesing data!!!")
