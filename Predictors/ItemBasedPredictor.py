from collections import defaultdict
from math import prod
from DataModels import Product
from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import operator


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items

    def __init__(self,  dp: DataProvider) -> None:
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

        if self.productSimilarities == None or len(self.productSimilarities.keys()) == 0:
            self.productSimilarities = {}
            for prod1 in basketProducts:
                for prod2 in self.dp.products:
                    if prod1.id != prod2:
                        if (prod1.id, prod2) not in self.productSimilarities or (prod2, prod1.id) not in self.productSimilarities:
                            # calc sim
                            purchasedBoth, purchasedNone, purchasedFirst, purchasedSecond = self.getNumOfPurchases(
                                prod1.id, prod2)

                            # Yules' Q
                            a = ((purchasedBoth * purchasedNone) -
                                 (purchasedFirst*purchasedSecond))
                            b = ((purchasedBoth * purchasedNone) +
                                 (purchasedFirst*purchasedSecond))

                            similarity = 0

                            # value between -1 and 1
                            # Q = 0: no association between the variables.
                            # Q = 0 to ± 0.29: a negligible or very small association
                            # Q = from -0.30 to -0.49 or from 0.30 to 0.49: a moderate association between the variables.
                            # Q = 0.50 and 0.69 or -0.50 and -0.69: a substantial association between the variable
                            # Q > 0.70, or < -0.70: a very strong association.
                            # Q = 1 or -1 , there is a perfect association between the events
                            # A positive Q points to a positive correlation,  A negative Q points to a negative correlation
                            if b != 0:
                                similarity = a/b

                            self.productSimilarities[(
                                prod1.id, prod2)] = similarity
                            self.productSimilarities[(
                                prod2, prod1.id)] = similarity

            self.dp.storeSimilaritiesToPickle(self.productSimilarities)

        # reccomend products
        sortedDict = dict(sorted(self.productSimilarities.items(),
                          key=operator.itemgetter(1), reverse=True))

        recommendedProducts = []
        for key in sortedDict:
            prod1 = key[0]
            prod2 = key[1]

            if prod1 not in recommendedProducts and prod1 not in basket and len(recommendedProducts) < numOfProducts:
                recommendedProducts.append(prod1)

            if prod2 not in recommendedProducts and prod2 not in basket and len(recommendedProducts) < numOfProducts:
                recommendedProducts.append(prod2)

            if len(recommendedProducts) >= numOfProducts:
                break

        return recommendedProducts

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
