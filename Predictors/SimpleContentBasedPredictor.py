from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import heapq


class SimpleContentBasedPredictor(Predictor):
    '''
    Class SimpleContextBasedPredictor represents a method that checks users past purchases and returns N
    most popular products 
    '''

    isOptimized = False
    storeItemSize: int

    def __init__(self, dp: DataProvider, isOptimized: bool, storeItemSize: int) -> None:
        self.dp = dp
        self.isOptimized = isOptimized
        self.storeItemSize = storeItemSize

    def predict(self, N: int, user_id: int, basket: list):
        '''
        Function returns N most popular products not in users current basket purchased by given user in the past
        '''
        result = {}

        if self.isOptimized:
            # read most purchased product from db
            # dp.getUserItemPurchases(storeItemSize)
            pass
        else:
            # calculate users most purchased products
            userOrderdProducts = self.dp.getUserOrderedProducts(user_id)

            for item_id in basket:
                userOrderdProducts.pop(item_id, None)

            topNProducts = heapq.nlargest(
                N, userOrderdProducts, key=userOrderdProducts.get)

            for prod in topNProducts:
                result[prod] = self.dp.products[prod]

        return result

    def fit(self, data):
        '''
        Function accepts data to be used for generating predictions 
        '''
        self.data = data
