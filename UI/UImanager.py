from ApplicationConstants import UserFiles


class UImanager():
    '''
    Class for managing user input and output.
    '''

    files: UserFiles

    def __init__(self, files: UserFiles) -> None:
        self.files = files

    def getBasket(self):
        '''
        Function reads the input file containing user id and basket of products and returns a dictionary containing
            user id and products.
        '''
        pass

    def outputRecommendations(self):
        '''
        Function recives a list of recommended products and writes them in the output file.
        '''
        pass
