class DataPaths():
    '''
    Class for holding paths to data files
    '''

    # CSV files
    aislesCSV = "Data/aisles.csv"
    departmentsCSV = "Data/departments.csv"
    productsCSV = "Data/products.csv"
    productsForOrdersCSV = "Data/products_for_orders.csv"
    ordersCSV = "Data/orders.csv"

    sampleSubmissionCSV = "Data/sample_submission.csv"
    orderProductsPriorCSV = "Data/order_products__prior.csv"
    orderProductsTrainCSV = "Data/order_products__train.csv"

    # pickle files
    aislesPickle = "Data/aisles.pickle"
    departmentsPickle = "Data/departments.pickle"
    productsPickle = "Data/products.pickle"
    productsForOrdersPickle = "Data/productsForOrders.pickle"
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
    # sample sizes for orders
    SAMPLE_SIZES_ORDERS = [1000, 5000, 10000, 15000]

    # number of users most purchased products stored for each user
    USERS_PRODUCTS_STORE_SIZES = [1, 10, 50, 100]

    # number of stored items most similar to each item
    ITEM_SIMILARITY_STORE_SIZES = [1, 10, 50, 100]

    # sample size to use for preparing orders
    ORDERS_SAMPLE_SIZE_TO_USE = SAMPLE_SIZES_ORDERS[0]

    # number of most purchased products per user to store
    USERS_PRODUCTS_STORE_SIZE = USERS_PRODUCTS_STORE_SIZES[0]

    # number of similarities per item to store
    ITEM_SIMILARITY_STORE_SIZE = ITEM_SIMILARITY_STORE_SIZES[0]
