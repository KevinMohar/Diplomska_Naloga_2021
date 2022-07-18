from DataProvider import DataProvider
import heapq
from Predictors.Predictor import Predictor

from Telematry import Telematry


class SimpleContentBasedPredictor(Predictor):
    '''
    Class SimpleContextBasedPredictor checks users past purchases and returns N most popular products 
    '''

    isOptimized = False
    storeItemSize: int

    def __init__(self, dp: DataProvider, isOptimized: bool, userProductStoreSize: int, telematy: Telematry) -> None:
        self.dp = dp
        self.isOptimized = isOptimized
        self.storeItemSize = userProductStoreSize
        self.tel = telematy

    def predict(self, N: int, user_id: int, basket: list):
        '''
        Function returns N most popular products not in users current basket purchased by given user in the past
        '''
        result = {}
        userOrderdProducts = None
        topNProducts = None

        self.tel.StartContentBased()
        self.tel.contentBased_RequestedProducts = N

        if self.isOptimized:
            # read users item purchases from db (products are ordered by num of purchases - first is most purchased)
            userOrderedProducts = self.dp.getUserItemPurchases(
                self.storeItemSize)

            # remove products already in the basket
            cleanList = [
                item_id for item_id in userOrderedProducts[user_id] if item_id not in basket]

            if len(cleanList) >= N:
                topNProducts = cleanList[:N]
                self.tel.contentBased_RecommendedProducts = N
            else:
                topNProducts = cleanList
                self.tel.contentBased_RecommendedProducts = len(
                    cleanList)

        else:
            # calculate users most purchased products
            userOrderdProducts = self.dp.getUserOrderedProducts(user_id)

            # remove products already in the basket
            cleanList = [
                item_id for item_id in userOrderdProducts if item_id not in basket]

            # select users N most purchased products
            if len(cleanList) >= N:
                topNProducts = cleanList[:N]
                self.tel.contentBased_RecommendedProducts = N
            else:
                topNProducts = cleanList
                self.tel.contentBased_RecommendedProducts = len(
                    cleanList)

        for prod in topNProducts:
            result[prod] = self.dp.products[prod]

        self.tel.EndContentBased()

        return result

    def fit(self, data):
        '''
        Function accepts data to be used for generating predictions 
        '''
        self.data = data
