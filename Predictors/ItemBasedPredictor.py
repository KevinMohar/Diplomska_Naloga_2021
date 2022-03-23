from DataModels import Product
from Predictors.Predictor import Predictor
from DataProvider import DataProvider


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items
    usersProducts = {}

    def __init__(self,  dp: DataProvider, threshold: float = 0) -> None:
        self.threshold = threshold
        self.dp = dp

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        '''
        Function returns list of N products not in users current basket using item-item CF
        '''

        for prod1 in self.data:
            for prod2 in self.data:
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
                        similarity = ((purchasedBoth * purchasedNone) - (purchasedFirst*purchasedSecond))/(
                            (purchasedBoth * purchasedNone)+(purchasedFirst*purchasedSecond))

                        if similarity < self.threshold or similarity < 0:
                            similarity = 0

                        self.productSimilarities.update(
                            {(prod1, prod2): similarity})

                    elif (prod1, prod2) not in self.productSimilarities and (prod2, prod1) in self.productSimilarities:
                        self.productSimilarities.update(
                            {(prod1, prod2): self.productSimilarities[(prod2, prod1)]})

        #
        for product in self.data:
            numOfWeights = 0  # vsota podobnosti
            sumOfWeights = 0  # vsota uteži
            for pair in self.productSimilarities:
                if pair[1] == product and self.productSimilarities[pair] > 0:
                    numOfWeights += self.productSimilarities[pair]
                    sumOfWeights += self.productSimilarities[pair] * \
                        self.movies[pair[0]][userID]
            self.ratings.update({product: sumOfWeights/numOfWeights})

    def fit(self, products: list):
        '''
        Function accepts data to be used for generating predictions 
        '''

        self.data = products
        self.productSimilarities = {}

    def getNumOfPurchasesOfBothItems(self, prod1: Product, prod2: Product) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased both
        '''
        pass

    def getNumOfPurchasesOfNone(self, prod1: Product, prod2: Product) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased none of the two
        '''
        pass

    def getNumOfPurchasesOfOnlyOne(self, prod1: Product, prod2: Product) -> int:
        '''
        Function accepts 2 products and returns the number of users that purchased prod1 but didnt purchase prod2
        '''
        pass
