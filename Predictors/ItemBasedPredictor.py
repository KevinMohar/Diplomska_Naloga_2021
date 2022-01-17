from Predictors.Predictor import Predictor


class ItemBasedPredictor(Predictor):
    '''
    Item based predictor class
    '''

    threshold: float  # minimal similartiy threshold between two items
    usersProducts = {}

    # Dict containing num of orders per product({"product1":numOfOrders,"product2":numOfOrders,...})
    orders = {}

    def __init__(self, min_values=0, threshold=0) -> None:
        self.min_values = min_values
        self.threshold = threshold

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        pass

    def fit(self, products: list):
        #
        self.data = products

        for x in self.views:
            for y in self.views:
                if x != y:
                    pass
