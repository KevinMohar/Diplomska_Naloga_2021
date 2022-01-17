from Predictors.Predictor import Predictor
from DataProvider import DataProvider


class SimpleContextBasedPredictor(Predictor):
    # Razred SimpleContextBasedPredictor predstavlja metodo, ki gleda katere artikle je dani kupec
    # kupoval v preteklosti. Metoda ne uporablja učenja temveč le prešteje koliko izdelkov posamezne
    # kategorije je kupec v preteklosti kupil.

    def __init__(self, dp: DataProvider) -> None:
        self.dp = dp

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        # Za podanega kupca vrne numOfProducts najpogostejših izdelkov ki jih je v preteklosti kupil.
        return self.__GetUsersOrdersPerDepartment(user_id)

    def fit(self, data):
        self.data = data

    def __GetUsersOrdersPerDepartment(self, user_id: int):
        # za danega uporabnika poišče število kupljenih izdelkov po kategorijah in vrne slovar vrednosti

        ordersPerDepartment = {}

        for order in self.dp.orders:
            if order.user_id == user_id:
                for product in order.product_list:
                    ordersPerDepartment[product.department] += 1

        return ordersPerDepartment
