from Predictors.Predictor import Predictor


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    def __init__(self) -> None:
        super().__init__()

    def predict(self, numOfProducts: int):
        pass

    def fit(self, data: list):
        '''
        Sets data to be used in predict method

        :param data: (list) list of products
        '''
        self.data = data
