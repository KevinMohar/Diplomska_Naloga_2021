class DataPaths():
    '''
    Class for holding paths to data files
    '''

    aislesCSV = "Data/aisles.csv"
    departmentsCSV = "Data/departments.csv"
    productsCSV = "Data/products.csv"
    ordersCSV = "Data/orders.csv"
    sampleSubmissionCSV = "Data/sample_submission.csv"
    orderProductsPriorCSV = "Data/order_products__prior.csv"
    orderProductsTrainCSV = "Data/order_products__train.csv"

    aislesJSON = "Data/aisles.json"
    departmentsJSON = "Data/departments.json"
    productsJSON = "Data/products.json"
    ordersJSON = "Data/orders.json"


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
