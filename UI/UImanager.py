from ApplicationConstants import UserFiles
import json
from JSONEncoder import Encoder
from Predictors.Predictor import Predictor
from Predictors.SimpleContextBasedPredictor import SimpleContentBasedPredictor
from Predictors.ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender
from DataProvider import DataProvider


class UImanager():
    '''
    Class for managing user input and output.
    '''

    files: UserFiles
    user_id: int
    products: list
    dp = DataProvider(False)
    isOptimized = False

    def __init__(self, isOptimized: bool) -> None:
        '''
        Constructor reads users id and list of products in current basket from input file
        '''
        self.files = UserFiles

        f = open(UserFiles.basketInput)
        data = json.load(f)["order"]
        self.user_id = data["user_id"]
        self.products = data["products"]
        f.close()

        self.isOptimized = isOptimized

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

        SCBpredictor = SimpleContentBasedPredictor(self.dp)
        recommender = Recommender(SCBpredictor)
        SCBrecommendations = recommender.recommend(
            self.user_id, self.products, numOfProd)

        IBpredictor = ItemBasedPredictor(self.dp)
        recommender = Recommender(IBpredictor)
        IBrecommendations = recommender.recommend(
            self.user_id, self.products, numOfProd)

        recommendations.update(SCBrecommendations)
        recommendations.update(IBrecommendations)

        return recommendations
