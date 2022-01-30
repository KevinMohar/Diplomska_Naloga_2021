from Predictors.Predictor import Predictor


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items
    usersProducts = {}

    # Dict containing num of orders per product({"product1":numOfOrders,"product2":numOfOrders,...})
    orders = {}

    def __init__(self, threshold:float = 0) -> None:
        self.threshold = threshold

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        #sestavi matriko 
        #izracunaj podobnost
        pass
        

    def fit(self, products: list):
        #
        self.data = products
