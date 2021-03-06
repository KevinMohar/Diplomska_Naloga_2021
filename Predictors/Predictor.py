from DataProvider import DataProvider


class Predictor(object):

    '''
    A template class for a predictor
    '''

    data = None
    dp: DataProvider


def __init__(self) -> None:
    pass


def predict(self):
    '''
    A method for predicting best suitable products based on predictor type
    '''
    pass


def fit(self, data):
    '''
    A method for setting data to be used by predict method
    '''
    self.data = data
