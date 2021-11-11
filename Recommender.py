from Predictors.Predictor import Predictor
from Predictors.RandomPredictor import RandomPredictor


class Recommender:
    '''
    Uses predictor passed to constructor to reccomend products
    '''

    predictor: Predictor
    data = None

    def __init__(self, predictor):
        '''
        Inits a predictor to be used for recommending products

        :param predictor: (predictor) predictor to be used
        '''
        self.predictor = predictor

    def recommend(self, userID: int, NumOfProducts: int = 10):
        '''
        Reccomends products for given users

        :param userID: (int) users id
        :param NumOfProducts: (int) number if products to return 
        :return: (list) returns list of products
        '''
        if NumOfProducts > 0:
            return self.predictor.predict(NumOfProducts)

    def fit(self, data):
        '''
        Sets data to be used by predictor

        :param data: (list) list of products
        '''
        self.data = data
        self.predictor.fit(data)
