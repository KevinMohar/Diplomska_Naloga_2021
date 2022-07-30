import threading
from DataModels import Similarity
from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import operator

from Telematry import Telematry


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float = 0 # minimal similarity between two items
    isOptimized = False
    storeItemSize: int
    dp: DataProvider
    itemSimilarities = []

    def __init__(self,  dp: DataProvider, isOptimized: bool, itemSimilarityStoreSize: int, telematy: Telematry) -> None:
        self.dp = dp
        self.bothProductPurchases = {}
        self.noneProductPurchases = {}
        self.oneProductPurchases = {}
        self.isOptimized = isOptimized
        self.storeItemSize = itemSimilarityStoreSize
        self.tel = telematy

    def predict(self, N: int, user_id: int, productsInBasket: list):
        '''
        Function returns list of N recommended products not in users current basket using item-item CF
        '''

        self.tel.itemBased_RequestedProducts = N
        self.tel.StartItemBased()
        recommendedProducts = {}
        basket = list(set(productsInBasket))


        if self.isOptimized:
            # read prepared similarites for each product
            self.productSimilarities = self.dp.getItemSimilaritiesPurchases(
                self.storeItemSize)

            # filter out similarities only for items in basket
            self.itemSimilarities = []
            for item in basket:
                if item in self.productSimilarities:
                    self.itemSimilarities += self.productSimilarities[item]

            # order by similarity
            sortedList = sorted(self.itemSimilarities,
                                key=lambda x: x.similarity, reverse=True)

            # remove products that are already in basket or are recommended
            topNProductSim = []
            for sim in sortedList:
                if sim.product2 not in topNProductSim and sim.product2 not in basket:
                    topNProductSim.append(sim.product2)

            # select N products to recommend
            if len(topNProductSim) >= N:
                topNProductSim = topNProductSim[:N]
                self.tel.itemBased_RecommendedProducts = N
            else:
                topNProductSim = topNProductSim
                self.tel.itemBased_RecommendedProducts = len(topNProductSim)

            for prod in topNProductSim:
                recommendedProducts[prod] = self.dp.products[prod]

        else:
            # calculate similarities for products in basket
            self.itemSimilarities = []
            threads = []
            global_lock = threading.Lock()

            for item_id in basket:
                thread = threading.Thread(target=self.CalcSimilaritiesForProduct, args=(item_id, self.dp.products, global_lock))
                threads.append(thread)

            [thread.start() for thread in threads]
            [thread.join() for thread in threads]

            # order by similarity (most similar first) and return N most similar items
            sortedSimDict = sorted(self.itemSimilarities,
                            key=lambda x: x.similarity, reverse=True)

            if len(sortedSimDict) >= N:
                self.tel.itemBased_RecommendedProducts = N
                for sim  in sortedSimDict:
                    if sim.product2 not in basket and sim.product2 not in recommendedProducts:
                        recommendedProducts[sim.product2] = self.dp.products[sim.product2]
                    if len(recommendedProducts) == N:
                        break
            else:
                self.tel.itemBased_RecommendedProducts = len(sortedSimDict)
                for sim in sortedSimDict:
                    if sim.product2 not in basket and sim.product2 not in recommendedProducts:
                        recommendedProducts[sim.product2] = self.dp.products[sim.product2]

        self.tel.EndItemBased()
        return recommendedProducts

    def CalcSimilaritiesForProduct(self, product_Id:int, products, globalLock):
        similarities = []

        for product2_id in products:
            sim = self.CalcSimWithYoulsQ(product_Id, product2_id, globalLock)
            similarities.append(Similarity(product_Id, product2_id, sim))

        while globalLock.locked():
            continue

        globalLock.acquire()

        for sim in similarities:
            self.itemSimilarities.append(sim)
        globalLock.release()

    def CalcSimWithYoulsQ(self, prod1, prod2, globalLock):
        '''
        Function accepts 2 products and returns similarity between given products calculated using Youls' Q
        '''
        purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = self.getNumOfPurchases(
            prod1, prod2, globalLock)

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

    def getNumOfPurchases(self, prod1: int, prod2: int, globalLock):
        '''
        Function accepts 2 products and returns values needed for Youls' Q calculation
        '''
        countBoth = 0
        countNone = 0
        countFirst = 0
        countSecond = 0

        for user_id in self.dp.usersProducts:
                # both
                if prod1 in self.dp.usersProducts[user_id] and prod2 in self.dp.usersProducts[user_id]:
                    countBoth += 1

                # none
                if prod1 not in self.dp.usersProducts[user_id] and prod2 not in self.dp.usersProducts[user_id]:
                    countNone += 1

                # first but not second
                if prod1 in self.dp.usersProducts[user_id] and prod2 not in self.dp.usersProducts[user_id]:
                    countFirst += 1

                # second but not first
                if prod1 not in self.dp.usersProducts[user_id] and prod2 in self.dp.usersProducts[user_id]:
                    countSecond += 1

        return (countBoth, countNone, countFirst, countSecond)
