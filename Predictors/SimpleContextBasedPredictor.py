from Predictors.Predictor import Predictor
from DataProvider import DataProvider
import operator
import heapq


class SimpleContextBasedPredictor(Predictor):
    # Razred SimpleContextBasedPredictor predstavlja metodo, ki gleda katere artikle je dani kupec
    # kupoval v preteklosti. Metoda število izdelkov izdelkov posamezne kategorije ki jo je 
    # kupec v preteklosti kupil.

    def __init__(self, dp: DataProvider) -> None:
        self.dp = dp

    def predict(self, numOfProducts: int, user_id: int, basket: list):
        # Za podanega kupca vrne numOfProducts najpogostejših izdelkov ki jih je v preteklosti kupil.
        #
        # return: {prod_id: prod_obj}

        userOrderdProducts = self.__getUserOrderedProducts(user_id)
        topNProducts = heapq.nlargest(numOfProducts, userOrderdProducts, key=userOrderdProducts.get)

        result = {}
        for prod in  topNProducts:
            result[prod] = self.dp.products[prod]
        
        return result

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

    def __getUserOrderedProducts(self, user_id):
        # Za podanega uporabnika poišče in vrne izdelke ki jih je v preteklosti kupoval
        #
        # return : {product_id: numOfPurchases}

        orderdProducts = {}

        for order in self.dp.orders:
            if user_id == self.dp.orders[order].user_id:
                for product in self.dp.orders[order].product_list:
                    if product.id in orderdProducts:
                        orderdProducts[product.id] += 1 
                    else:
                        orderdProducts[product.id] = 1 
        
        return orderdProducts