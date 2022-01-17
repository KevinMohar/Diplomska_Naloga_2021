from Predictors.Predictor import Predictor
from Predictors.RandomPredictor import RandomPredictor


class Recommender:
    '''
    Reccomender class 
    '''

    predictor: Predictor
    data = None

    def __init__(self, predictor: Predictor):
        '''
        Inits a predictor to be used for recommending products

        :param predictor: (Predictor) predictor to be used
        '''
        self.predictor = predictor

    def recommend(self, userID: int, basket: list, N: int = 10):
        '''
        Function reccomends top N products for given user

        :param userID: (int) users id
        :param NumOfProducts: (int) number if products to return 
        :return: (list) returns list of products
        '''
        if N > 0:
            return self.predictor.predict(N, userID, basket)

    def fit(self, data):
        '''
        Sets data to be used by predictor

        :param data: (list) list of products
        '''
        self.data = data
        self.predictor.fit(data)