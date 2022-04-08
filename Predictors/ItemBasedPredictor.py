from collections import defaultdict
from DataModels import Product
from Predictors.Predictor import Predictor
from DataProvider import DataProvider


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items

    def __init__(self,  dp: DataProvider, threshold: float = 0) -> None:
        self.threshold = threshold
        self.dp = dp
        self.productSimilarities = self.dp.getSimilaritiesFromPickle()
        self.bothProductPurchases = {}
        self.noneProductPurchases = {}
        self.oneProductPurchases = {}

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        '''
        Function returns list of N products not in users current basket using item-item CF
        '''
        basketProducts = self.dp.findProducts(basket)
        products = {}
        for x in self.dp.products:
            if len(products) < 10:
                products[self.dp.products[x].id] = self.dp.products[x]
            else:
                break

        if self.productSimilarities == None or len(self.productSimilarities.keys()) == 0:
            self.productSimilarities = {}
            for prod1 in basketProducts:
                for prod2 in products:
                    if prod1.id != prod2:
                        if (prod1.id, prod2) not in self.productSimilarities and (prod2, prod1.id) not in self.productSimilarities:
                            # calc sim
                            purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = self.getNumOfPurchases(
                                prod1.id, prod2)

                            # Youls' Q
                            a = ((purchasedBoth * purchasedNone) -
                                 (purchasedFirst*purchasedSecond))
                            b = ((purchasedBoth * purchasedNone) +
                                 (purchasedFirst*purchasedSecond))

                            similarity = 0

                            if b != 0:
                                similarity = a/b

                            # if similarity < self.threshold or similarity < 0:
                             #   similarity = 0

                            self.productSimilarities.update(
                                {(prod1.id, prod2): similarity})

                        elif (prod1.id, prod2) not in self.productSimilarities and (prod2, prod1.id) in self.productSimilarities:
                            self.productSimilarities.update(
                                {(prod1.id, prod2): self.productSimilarities[(prod2, prod1.id)]})
            self.dp.storeSimilaritiesToPickle(self.productSimilarities)

        # reccomend products
        a = self.productSimilarities

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

            self.bothProductPurchases.update({(prod1, prod2): countBoth})
            self.bothProductPurchases.update({(prod2, prod1): countBoth})
            self.noneProductPurchases.update({(prod1, prod2): countNone})
            self.noneProductPurchases.update({(prod2, prod1): countNone})
            self.oneProductPurchases.update({(prod1, prod2): countFirst})
            self.oneProductPurchases.update({(prod2, prod1): countSecond})

        return (countBoth, countNone, countFirst, countSecond)
