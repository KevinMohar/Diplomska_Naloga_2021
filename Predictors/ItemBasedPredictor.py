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
        self.firstButNotSecondProductPurchases = {}

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        '''
        Function returns list of N products not in users current basket using item-item CF
        '''
        products = self.dp.findProducts(basket)

        if self.productSimilarities == None or len(self.productSimilarities.keys()) == 0:
            for prod1 in products:
                for prod2 in self.dp.products:
                    if prod1 != prod2:
                        if (prod1, prod2) not in self.productSimilarities and (prod2, prod1) not in self.productSimilarities:
                            # calc sim
                            purchasedBoth = self.getNumOfPurchasesOfBothItems(
                                prod1, prod2)
                            purchasedNone = self.getNumOfPurchasesOfNone(
                                prod1, prod2)
                            purchasedFirst = self.getNumOfPurchasesOfOnlyOne(
                                prod1, prod2)
                            purchasedSecond = self.getNumOfPurchasesOfOnlyOne(
                                prod2, prod1)

                            # Youls' Q
                            a = ((purchasedBoth * purchasedNone) -
                                 (purchasedFirst*purchasedSecond))
                            b = ((purchasedBoth * purchasedNone) +
                                 (purchasedFirst*purchasedSecond))

                            similarity = 0

                            if b > 0:
                                similarity = a/b

                            if similarity < self.threshold or similarity < 0:
                                similarity = 0

                            self.productSimilarities.update(
                                {(prod1, prod2): similarity})

                        elif (prod1, prod2) not in self.productSimilarities and (prod2, prod1) in self.productSimilarities:
                            self.productSimilarities.update(
                                {(prod1, prod2): self.productSimilarities[(prod2, prod1)]})
            self.dp.storeSimilaritiesToPickle(self.productSimilarities)

        # reccomend products
        a = 1

    def getYQdata(self, prod1: int, prod2: int):
        '''
        Function accepts 2 products and returns dictionary containing user_id : touple key-value pairs.
        Touple contains 2 bools. First bool determines if user has purchased prod1 and second bool determines
            if user has purchased prod2
        '''

        userOrders = defaultdict(lambda: (False, False))

        for order in self.dp.orders:
            if prod1 in [x.id for x in self.dp.orders[order].product_list]:
                userOrders.update(
                    {self.dp.orders[order].user_id: (True, userOrders[self.dp.orders[order].user_id][1])})

            if prod2 in [x.id for x in self.dp.orders[order].product_list]:
                userOrders.update(
                    {self.dp.orders[order].user_id: (userOrders[self.dp.orders[order].user_id][0], True)})

        return userOrders

    def getNumOfPurchasesOfBothItems(self, prod1: int, prod2: int) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased both
        '''
        if (prod1, prod2) in self.bothProductPurchases:
            return self.bothProductPurchases[(prod1, prod2)]
        if (prod2, prod1) in self.bothProductPurchases:
            return self.bothProductPurchases[(prod2, prod1)]

        userOrders = self.getYQdata(prod1, prod2)

        count = 0
        for element in userOrders:
            if userOrders[element][0] and userOrders[element][1]:
                count += 1

        self.bothProductPurchases.update({(prod1, prod2): count})
        self.bothProductPurchases.update({(prod2, prod1): count})

        return count

    def getNumOfPurchasesOfNone(self, prod1: int, prod2: int) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased none of the two
        '''
        if (prod1, prod2) in self.noneProductPurchases:
            return self.noneProductPurchases[(prod1, prod2)]
        if (prod2, prod1) in self.noneProductPurchases:
            return self.noneProductPurchases[(prod2, prod1)]

        userOrders = self.getYQdata(prod1, prod2)

        count = 0
        for element in userOrders:
            if not userOrders[element][0] and not userOrders[element][1]:
                count += 1

        self.noneProductPurchases.update({(prod1, prod2): count})
        self.noneProductPurchases.update({(prod2, prod1): count})

        return count

    def getNumOfPurchasesOfOnlyOne(self, prod1: int, prod2: int) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased prod1 but didnt purchase prod2
        '''

        userOrders = self.getYQdata(prod1, prod2)

        count = 0
        for element in userOrders:
            if userOrders[element][0] and not userOrders[element][1]:
                count += 1

        return count
