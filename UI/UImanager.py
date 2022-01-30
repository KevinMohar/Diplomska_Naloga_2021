from ApplicationConstants import UserFiles, DataPaths
from DataModels import Aisle, Department, Product, Order
import json
from JSONEncoder import Encoder


class UImanager():
    '''
    Class for managing user input and output.
    '''

    files: UserFiles
    user_id: int
    products: list

    def __init__(self) -> None:
        self.files = UserFiles

        f = open(UserFiles.basketInput)
        data = json.load(f)["order"]
        self.user_id = data["user_id"]
        self.products = data["products"]
        f.close()

    def getBasket(self):
        # Funkcija prebere podatke o kupcu in izdelkih v košarici iz datoteke z vhodnimi podatki
        return self.products
        
    def getUser(self):
        return self.user_id
    

    def outputRecommendations(self, products: dict, printToConsole: bool = False, outputType: str = "id"):
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


