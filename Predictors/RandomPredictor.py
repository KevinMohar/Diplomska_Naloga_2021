import random
from Predictors.Predictor import Predictor


class RandomPredictor(Predictor):
    '''
    A random predictor class
    '''

    def __init__(self) -> None:
        super().__init__()

    def predict(self, N: int):
        '''
        Returns N random products from list of products

        :param N: (int) number of products to return
        :return: (list) list of numOfProducts recommended products
        '''
        return random.sample(self.data, N)

    def fit(self, data: list):
        '''
        Sets data to be used in predict method

        :param data: (list) list of products
        '''
        self.data = data
