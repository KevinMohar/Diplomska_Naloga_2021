from collections import defaultdict
import random
from DataModels import Product
from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import operator


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items
    isOptimized = False

    def __init__(self,  dp: DataProvider, isOptimized: bool) -> None:
        self.dp = dp
        self.bothProductPurchases = {}
        self.noneProductPurchases = {}
        self.oneProductPurchases = {}
        self.isOptimized = isOptimized

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        '''
        Function returns list of N recommended products not in users current basket using item-item CF
        '''

        if self.isOptimized:
            # read from db
            self.productSimilarities = self.dp.getSimilaritiesFromPickle()
        else:
            # calculate similarities for products in basket
            pass

        if self.productSimilarities == None or len(self.productSimilarities.keys()) == 0:
            return recommendedProducts

        # order by similartiy (contains only product pairs with similarity grater than 0)
        sortedDict = dict(sorted(self.productSimilarities.items(),
                          key=operator.itemgetter(1), reverse=True))

        recommendedProducts = {}

        # select "numOfProducts" most similar products to the ones in the basket
        for key in sortedDict:
            prod1 = key[0]
            prod2 = key[1]

            if prod1 in basket and prod2 not in basket:
                recommendedProducts[prod2] = self.dp.products[prod2]
            elif prod2 in basket and prod1 not in basket:
                recommendedProducts[prod1] = self.dp.products[prod1]

            if len(recommendedProducts) >= numOfProducts:
                break

        # if less than "numOfProducts" of products with similarities grater than 0 were found fill the empty spots with randomly
        #   selected products from list of prodcts that are not in basket
        while len(recommendedProducts) < numOfProducts:
            prod_id, prod = random.choice(list(self.dp.products.items()))
            if prod_id not in recommendedProducts:
                recommendedProducts.update({prod_id: prod})

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
