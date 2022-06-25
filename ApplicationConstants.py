class DataPaths():
    '''
    Class for holding paths to data files
    '''

    # CSV files
    aislesCSV = "Data/aisles.csv"
    departmentsCSV = "Data/departments.csv"
    productsCSV = "Data/products.csv"
    ordersCSV = "Data/orders.csv"

    sampleSubmissionCSV = "Data/sample_submission.csv"
    orderProductsPriorCSV = "Data/order_products__prior.csv"
    orderProductsTrainCSV = "Data/order_products__train.csv"

    # pickle files
    aislesPickle = "Data/aisles.pickle"
    departmentsPickle = "Data/departments.pickle"
    productsPickle = "Data/products.pickle"
    ordersPickle = "Data/orders.pickle"
    similaritiesPicke = "Data/similarityBetweenProducts.pickle"
    usersProductsPicke = "Data/usersProducts.pickle"
    usersPickle = "Data/users.pickle"

    # item similarites for each item
    itemSimilarities = "Data/itemSimilarities"

    # user purchases for each item
    usersPurchases = "Data/usersPurchases"


class UserFiles():
    '''
        Class for holding paths to user input and output files
    '''

    basketInput = "UI/currentOrder.json"
    recommenderOutput = "UI/recommenderOutput.json"


class Logging():
    '''
        Class for simple logging output
    '''

    INFO = "[SYSTEM_INFO]: "
    WARNING = "[SYSTEM_WARNING]: "
    ERROR = "[SYSTEM_ERROR]: "


class ApplicationConstants():
    '''
        Class for storing application constants
    '''
    # numer of orders in db
    SAMPLE_SIZES = [1000, 5000, 10000, 15000]

    # number of users most purchased products stored for each user
    USERS_PRODUCTS_STORE_SIZES = [1, 10, 50, 100]

    # number of stored items most similar to each item
    ITEM_SIMILARITY_STORE_SIZES = [1, 10, 50, 100]
