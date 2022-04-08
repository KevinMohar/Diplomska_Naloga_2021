from Predictors.Predictor import Predictor
from ApplicationConstants import Logging


class Recommender:
    '''
    Recommender class 
    '''

    predictor: Predictor
    data = None

    def __init__(self, predictor: Predictor):
        '''
        Inits a predictor to be used for recommending products
        '''
        self.predictor = predictor

    def recommend(self, userID: int, basket: list, N: int = 10) -> list:
        '''
        Function reccomends top N products for given user
        '''

        print(Logging.INFO + "Generating reccomendations...")
        if N > 0:
            return self.predictor.predict(N, userID, basket)

    def fit(self, data):
        '''
        Sets data to be used by predictor
        '''
        self.data = data
        self.predictor.fit(data)
