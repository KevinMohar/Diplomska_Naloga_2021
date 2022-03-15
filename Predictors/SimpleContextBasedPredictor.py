from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import heapq


class SimpleContextBasedPredictor(Predictor):
    '''
    Class SimpleContextBasedPredictor represents a method that checks users past purchases and returns N
    most popular products 
    '''

    def __init__(self, dp: DataProvider) -> None:
        self.dp = dp

    def predict(self, N: int, user_id: int, basket: list):
        '''
        Function returns N most popular products not in users current basket purchased by given user in the past
        '''

        userOrderdProducts = self.__getUserOrderedProducts(user_id)

        for item_id in basket:
            userOrderdProducts.pop(item_id, None)

        topNProducts = heapq.nlargest(
            N, userOrderdProducts, key=userOrderdProducts.get)

        result = {}
        for prod in topNProducts:
            result[prod] = self.dp.products[prod]

        return result

    def fit(self, data):
        '''
        Function accepts data to be used for generating predictions 
        '''
        self.data = data

    def __getUserOrderedProducts(self, user_id) -> dict:
        '''
        Function function finds and returnes users past purchases 
        '''

        orderdProducts = {}

        for order in self.dp.orders:
            if user_id == self.dp.orders[order].user_id:
                for product in self.dp.orders[order].product_list:
                    if product.id in orderdProducts:
                        orderdProducts[product.id] += 1
                    else:
                        orderdProducts[product.id] = 1

        return orderdProducts
