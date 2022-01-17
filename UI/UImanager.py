from ApplicationConstants import UserFiles
import json


class UImanager():
    '''
    Class for managing user input and output.
    '''

    files: UserFiles

    def __init__(self) -> None:
        self.files = UserFiles

    def getBasket(self):
        # Funkcija prebere podatke o kupcu in izdelkih v košarici iz datoteke z vhodnimi podatki

        f = open(UserFiles.basketInput)
        data = json.load(f)["order"]
        f.close()
        return data

    def outputRecommendations(self):
        '''
        Function recives a list of recommended products and writes them in the output file.
        '''
        pass
