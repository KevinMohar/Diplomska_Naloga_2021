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
    productsPickle= "Data/products.pickle"
    ordersPickle= "Data/orders.pickle"


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
