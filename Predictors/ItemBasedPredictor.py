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

        pass

    def fit(self, products: list):
        '''
        Function accepts data to be used for generating predictions 
        '''

        self.data = products

    def getNeighbourSelection(self, neighbourSize=-1):
        '''

        '''

        pass

    def getPurchasedItems(self, user_id: int):
        '''
        Function returns a dictionary of given users purchased items
        '''

        orderedProducts = {}

        for order in self.dp.orders:
            if self.dp.orders[order].user_id == user_id:
                for product in self.dp.orders[order].product_list:
                    orderedProducts[product.id] = orderedProducts.get(
                        product.id, 0) + 1

        return orderedProducts
