from ApplicationConstants import UserFiles
import json
from JSONEncoder import Encoder
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
    dp: DataProvider
    isOptimized: bool = False
    userProductStoreSize: int
    itemSimilarityStoreSize: int

    def __init__(self, isOptimized: bool, sampleSizeOrders: int, itemSimilarityStoreSize: int, userProductStoreSize: int) -> None:
        '''
        Constructor reads users id and list of products in current basket from input file
        '''
        self.dp = DataProvider(
            clearCache=True, sampleSizeOrders=sampleSizeOrders)

        self.telematry = Telematry()
        self.telematry.DB_orders = sampleSizeOrders
        self.telematry.PerItemStoreSize = itemSimilarityStoreSize
        self.telematry.PerUserStoreSize = userProductStoreSize

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

    def outputRecommendations(self, products: tuple, printToConsole: bool = False):
        '''
        Function recives a list of recommended products and writes them in the output file.
        '''
        outProducts = []

        products_content = products[0]
        products_item = products[1]

        products_content_obj = []
        products_item_obj = []

        for product in products_content:
            jsonOut = json.dumps(
                products_content[product].reprJSON(), cls=Encoder)
            outProducts.append(jsonOut)
            products_content_obj.append(self.dp.products[product])

        for product in products_item:
            jsonOut = json.dumps(
                products_item[product].reprJSON(), cls=Encoder)
            outProducts.append(jsonOut)
            products_item_obj.append(self.dp.products[product])

        with open(UserFiles.recommenderOutput, "w") as outfile:
            outJSON = {}
            outJSON["recommendedProducts"] = json.dumps(outProducts)
            json.dump(outJSON, outfile)

        if printToConsole:
            self.telematry.PrintReccomendations(
                products_item=products_item_obj, products_content=products_content_obj)

    def recommendProducts(self, numOfProd: int):
        '''
        Function returns a list of 2N recommended products using each method
        '''

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

        return (SCBrecommendations, IBrecommendations)
