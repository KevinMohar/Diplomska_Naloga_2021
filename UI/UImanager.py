from ApplicationConstants import UserFiles, DataPaths
import json


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
    

    def outputRecommendations(self, products: list, printToConsole: bool = False):
        '''
        Function recives a list of recommended products and writes them in the output file.
        '''
        outProducts = []

        for product in products:
            tmp = {}
            tmp["product_id"] = product.id
            tmp["name"] = product.name
            tmp["aisle"] = json.dumps(product.aisle.__dict__)
            tmp["department"] = json.dumps(product.department.__dict__)
            outProducts.append(tmp)

        with open(UserFiles.recommenderOutput, "w") as outfile:
            outJSON = {}
            outJSON["recommendedProducts"] = json.dumps(outProducts)
            json.dump(outJSON, outfile)
