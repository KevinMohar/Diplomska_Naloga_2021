from ApplicationConstants import UserFiles
import json
from JSONEncoder import Encoder
from Predictors.Predictor import Predictor
from Predictors.SimpleContentBasedPredictor import SimpleContentBasedPredictor
from Predictors.ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender
from DataProvider import DataProvider
from Telematry import Telematry


class UImanager():
    '''
    Class for managing user input and output.
    '''

    files: UserFiles
    user_id: int
    products: list
    dp = DataProvider(False)
    isOptimized: bool = False
    userProductStoreSize: int
    itemSimilarityStoreSize: int

    def __init__(self, isOptimized: bool, sampleSizeOrders: int, sampleSizeProducts: int, userProductStoreSize: int, itemSimilarityStoreSize: int) -> None:
        '''
        Constructor reads users id and list of products in current basket from input file
        '''
        self.dp = DataProvider(
            clearCache=False, sampleSizeOrders=sampleSizeOrders, sampleSizeProducts=sampleSizeProducts)
        self.telematry = Telematry()
        self.telematry.DB_orders = sampleSizeOrders
        self.telematry.DB_products = sampleSizeProducts

        # get data from basket
        f = open(UserFiles.basketInput)
        data = json.load(f)["order"]
        self.user_id = data["user_id"]
        self.products = data["products"]
        f.close()

        self.isOptimized = isOptimized
        self.itemSimilarityStoreSize = itemSimilarityStoreSize
        self.userProductStoreSize = userProductStoreSize

    def getBasket(self):
        '''
        Function returns list of products in users current basket
        '''
        return self.products

    def getUser(self) -> int:
        '''
        Function returns id of user
        '''
        return self.user_id

    def outputRecommendations(self, products: dict, printToConsole: bool = False):
        '''
        Function recives a list of recommended products and writes them in the output file.
        '''
        outProducts = []

        for product in products:
            jsonOut = json.dumps(products[product].reprJSON(), cls=Encoder)
            if printToConsole:
                print(jsonOut)
            outProducts.append(jsonOut)

        with open(UserFiles.recommenderOutput, "w") as outfile:
            outJSON = {}
            outJSON["recommendedProducts"] = json.dumps(outProducts)
            json.dump(outJSON, outfile)

    def recommendProducts(self, numOfProd: int):
        '''
        Function returns a list of 2N recommended products using each method
        '''

        recommendations = {}

        SCBpredictor = SimpleContentBasedPredictor(
            self.dp, self.isOptimized, self.userProductStoreSize, self.telematry)
        recommender = Recommender(SCBpredictor)
        SCBrecommendations = recommender.recommend(
            self.user_id, self.products, numOfProd)

        IBpredictor = ItemBasedPredictor(
            self.dp, self.isOptimized, self.itemSimilarityStoreSize, self.telematry)
        recommender = Recommender(IBpredictor)
        IBrecommendations = recommender.recommend(
            self.user_id, self.products, numOfProd)

        recommendations.update(SCBrecommendations)
        recommendations.update(IBrecommendations)

        return recommendations
