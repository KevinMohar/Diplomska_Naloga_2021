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

    itemSimilarities1 = "Data/itemSimilarities1.pickle"
    itemSimilarities10 = "Data/itemSimilarities10.pickle"
    itemSimilarities50 = "Data/itemSimilarities50.pickle"
    itemSimilarities100 = "Data/itemSimilarities100.pickle"

    usersPurchases1 = "Data/usersPurchases1.pickle"
    usersPurchases10 = "Data/usersPurchases10.pickle"
    usersPurchases50 = "Data/usersPurchases50.pickle"
    usersPurchases100 = "Data/usersPurchases100.pickle"


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
