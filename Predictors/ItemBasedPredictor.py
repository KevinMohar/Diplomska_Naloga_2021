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

    def __init__(self,  dp: DataProvider, isOptimized: bool, itemSimilarityStoreSize: int, telematy: Telematry) -> None:
        self.dp = dp
        self.bothProductPurchases = {}
        self.noneProductPurchases = {}
        self.oneProductPurchases = {}
        self.isOptimized = isOptimized
        self.storeItemSize = itemSimilarityStoreSize
        self.tel = telematy

    def predict(self, N: int, user_id: int, basket: list):
        '''
        Function returns list of N recommended products not in users current basket using item-item CF
        '''

        self.tel.itemBased_RequestedProducts = N
        self.tel.StartItemBased()
        recommendedProducts = {}

        if self.isOptimized:
            # read prepared similarites for each product
            self.productSimilarities = self.dp.getItemSimilaritiesPurchases(
                self.storeItemSize)

            # filter out similarities only for items in basket
            itemSimilarities = []
            for item in basket:
                if item in self.productSimilarities:
                    itemSimilarities += self.productSimilarities[item]

            # order by similarity
            sortedList = sorted(itemSimilarities,
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
            itemSimilarities = {}

            for productId1 in basket:
                for productId2 in self.dp.products:
                    if productId2 not in basket:
                        if productId2 not in itemSimilarities:
                            itemSimilarities[productId2] = self.CalcSimWithYoulsQ(
                                productId1, productId2)

            # order by similarity (most similar first) and return N most similar items
            sortedSimDict = dict(sorted(itemSimilarities.items(),
                                        key=operator.itemgetter(1), reverse=True))
            if len(sortedSimDict) >= N:
                self.tel.itemBased_RecommendedProducts = N
                topNmostSimilarItems = list(sortedSimDict)[:N]
                for productId in topNmostSimilarItems:
                    recommendedProducts[productId] = self.dp.products[productId]
            else:
                self.tel.itemBased_RecommendedProducts = len(sortedSimDict)
                for productId in sortedSimDict:
                    recommendedProducts[productId] = self.dp.products[productId]

        self.tel.EndItemBased()
        return recommendedProducts

    def CalcSimWithYoulsQ(self, prod1, prod2):
        '''
        Function accepts 2 products and returns similarity between given products calculated using Youls' Q
        '''
        purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = self.getNumOfPurchases(
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

    def getNumOfPurchases(self, prod1: int, prod2: int):
        '''
        Function accepts 2 products and returns values needed for Youls' Q calculation
        '''
        countBoth = 0
        countNone = 0
        countFirst = 0
        countSecond = 0

        found = [False, False, False, False]

        # both
        if (prod1, prod2) in self.bothProductPurchases or (prod2, prod1) in self.bothProductPurchases:
            countBoth = self.bothProductPurchases[(prod1, prod2)] if (
                prod1, prod2) in self.bothProductPurchases else self.bothProductPurchases[(prod2, prod1)]
            found[0] = True

        # none
        if (prod1, prod2) in self.noneProductPurchases or (prod2, prod1) in self.noneProductPurchases:
            countNone = self.noneProductPurchases[(prod1, prod2)] if (
                prod1, prod2) in self.noneProductPurchases else self.noneProductPurchases[(prod2, prod1)]
            found[1] = True

        # first but not second
        if (prod1, prod2) in self.oneProductPurchases:
            countFirst = self.oneProductPurchases[(prod1, prod2)]
            found[2] = True

        # second but not first
        if (prod2, prod1) in self.oneProductPurchases:
            countFirst = self.oneProductPurchases[(prod1, prod2)]
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

            self.bothProductPurchases.update({(prod1, prod2): countBoth})
            self.bothProductPurchases.update({(prod2, prod1): countBoth})
            self.noneProductPurchases.update({(prod1, prod2): countNone})
            self.noneProductPurchases.update({(prod2, prod1): countNone})
            self.oneProductPurchases.update({(prod1, prod2): countFirst})
            self.oneProductPurchases.update({(prod2, prod1): countSecond})

        return (countBoth, countNone, countFirst, countSecond)
