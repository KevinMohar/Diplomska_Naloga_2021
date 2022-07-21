from ApplicationConstants import DataPaths, Logging
from DataModels import Aisle, Department, Product, Order, Similarity
import csv
import os
import threading
import pickle


class DataProvider():

    aisles = {}
    departments = {}
    products = {}
    orders = {}
    users = []
    __emptyOrders = {}
    usersProducts = {}

    threads = []

    def __init__(self, clearCache: bool = False, sampleSizeOrders: int = None, removeEmptyOrders: bool = False) -> None:

        # delete .pickle files and re-read csv
        if clearCache:
            self.__deleteAllPickle()

        if not (os.path.isfile(DataPaths.ordersPickle) and os.path.isfile(DataPaths.aislesPickle)
                and os.path.isfile(DataPaths.departmentsPickle) and os.path.isfile(DataPaths.productsPickle)):

            print(Logging.INFO + "Started data parsing (to parse: aisles, departments, products, orders, ordered products)...")

            self.threads.append(threading.Thread(target=self.__getAisles))

            self.threads.append(threading.Thread(target=self.__getDepartments))

            self.threads.append(threading.Thread(
                target=self.__getProducts, args=(sampleSizeOrders,)))

            self.threads.append(threading.Thread(
                target=self.__getOrders, args=(sampleSizeOrders,)))

            for thread in self.threads:
                thread.start()

            for thread in self.threads:
                thread.join()

            self.__getOrderedProducts()

            # remove orders without products
            if removeEmptyOrders:
                for key in list(self.orders.keys()):
                    if len(self.orders[key].product_list) == 0:
                        self.__emptyOrders[key] = self.orders[key]
                        del self.orders[key]

            # store to pickle
            self.__storeDataToPickle(
                self.users, DataPaths.usersPickle)  # users
            self.__storeDataToPickle(
                list(self.orders.values()), DataPaths.ordersPickle)  # orders
            self.__storeDataToPickle(
                list(self.aisles.values()), DataPaths.aislesPickle)  # aisles
            self.__storeDataToPickle(
                list(self.departments.values()), DataPaths.departmentsPickle)  # departments
            self.__storeDataToPickle(
                list(self.products.values()), DataPaths.productsPickle)  # products
            self.__storeDataToPickle(
                self.usersProducts, DataPaths.usersProductsPicke)  # users products

        else:
            self.__getAislesFromPickle()
            self.__getDepartmentsFromPickle()
            self.__getProductsFromPickle()
            self.__getProductsFromPickle()
            self.__getOrdersFromPickle()
            self.__getUsersProductsFromPickle()
            self.__getUsersFromPickle()
            print(Logging.INFO + "Restored data from .pickle files!")

    def __getAisles(self):
        '''
        Function reads aisles from .csv file and stores them in dictionary in apropriate data model
        '''
        print(Logging.INFO + "Parsing aisles...")
        with open(DataPaths.aislesCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                aisle_id = int(row[0])
                aisle = str(row[1])
                self.aisles[aisle_id] = Aisle(aisle_id, aisle)
        print(Logging.INFO + "Finished parsing aisles!")

    def __getDepartments(self):
        '''
        Function reads departments from .csv file and stores them in dictionary in apropriate data model
        '''
        print(Logging.INFO + "Parsing departments...")
        with open(DataPaths.departmentsCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                department_id = int(row[0])
                department = str(row[1])
                self.departments[department_id] = Department(
                    department_id, department)
        print(Logging.INFO + "Finished parsing departments!")

    def __getProducts(self, sampleSize):
        '''
        Function reads products from .csv file and stores them in dictionary in apropriate data model
        '''

        fe = DataPaths.productsCSV.split(".")
        filename = fe[0] + "_filtered_" + str(sampleSize) + "." + fe[1]

        with open(filename, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                product_id = int(row[0])
                product = str(row[1])
                aisle = self.__findAisle(int(row[2]))
                department = self.__findDepartment(int(row[3]))

                self.products[product_id] = Product(
                    product_id, product, aisle, department)

        print(Logging.INFO + "Finished parsing products!")

    def __getOrders(self, sampleSize):
        '''
        Function reads orders from .csv file and stores them in dictionary in apropriate data model
        '''
        filename = DataPaths.ordersCSV.split(".")
        fullFilename = filename[0] + "_filtered_" + \
            str(sampleSize) + "." + filename[1]

        print(Logging.INFO + "Parsing orders...")

        with open(fullFilename, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                id = int(row[0])
                user_id = int(row[1])
                eval_set = str(row[2])
                order_number = int(row[3])
                order_dow = int(row[4])
                order_hour_of_day = int(row[5])
                days_since_prior_order = int(row[6]) if len(row) == 6 else 0
                self.orders[id] = Order(id, user_id, eval_set, order_number, order_dow,
                                        order_hour_of_day, days_since_prior_order, row)

                # add user to list of users
                if user_id not in self.users:
                    self.users.append(user_id)

    def __getOrderedProducts(self):
        '''
        Function reads ordered producs from .csv file and appends the list of products to corresponding order 
        '''
        # for easier selection
        files = []
        files.append(DataPaths.orderProductsTrainCSV)
        files.append(DataPaths.orderProductsPriorCSV)

        for file in files:
            with open(file, "r", encoding='UTF-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # skip header
                for row in reader:
                    order_id = int(row[0])
                    product = self.__findProduct(int(row[1]))
                    if product and order_id in self.orders:
                        self.orders[order_id].addProduct(product)

                        if(self.orders[order_id].user_id in self.usersProducts):
                            self.usersProducts[self.orders[order_id].user_id].append(
                                product.id)
                        else:
                            self.usersProducts[self.orders[order_id].user_id] = [
                                product.id]

        print(Logging.INFO + "Finished parsing orders!")

    def __getOrdersFromPickle(self):
        '''
        Function reads orders from .pickle file and stores them in dictionary in apropriate data model
        '''
        with open(DataPaths.ordersPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.orders[obj.id] = obj

    def __getAislesFromPickle(self):
        '''
        Function reads aisles from .pickle file and stores them in dictionary in apropriate data model
        '''
        with open(DataPaths.aislesPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.aisles[obj.id] = obj

    def __getUsersFromPickle(self):
        '''
        Function reads users from .pickle file and stores them to array
        '''
        with open(DataPaths.usersPickle, "rb") as reader:
            self.users = pickle.load(reader)

    def __getDepartmentsFromPickle(self):
        '''
        Function reads departments from .pickle file and stores them in dictionary in apropriate data model
        '''
        with open(DataPaths.departmentsPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.departments[obj.id] = obj

    def __getProductsFromPickle(self):
        '''
        Function reads products from .pickle file and stores them in dictionary in apropriate data model
        '''
        with open(DataPaths.productsPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.products[obj.id] = obj

    def __getUsersProductsFromPickle(self):
        '''
        Function reads user ordered product from pickle to corresponding dictionary
        '''
        with open(DataPaths.usersProductsPicke, "rb") as reader:
            data = pickle.load(reader)
            self.usersProducts = data

    def __findAisle(self, id: int):
        '''
        Function retrives an aisle with matching id from dictionary
        '''
        return self.aisles.get(id, None)

    def __findDepartment(self, id: int):
        '''
        Function retrives a department with matching id from dictionary
        '''

        return self.departments.get(id, None)

    def __findProduct(self, id: int):
        '''
        Function retrives a product with matching id from dictionary
        '''
        return self.products.get(id, None)

    def findProducts(self, ids: list):
        '''
        Function retrives products with matching ids from dictionary
        '''
        prods = [self.products.get(id, None) for id in ids]
        return prods

    def __storeDataToPickle(self, data, pickleFilePath):
        '''
        Function stores data from dictionaries to corresponding .pickle files
        '''

        with open(pickleFilePath, "wb") as outfile:
            pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)

    def __deleteAllPickle(self, deleteSimilarities=False):
        '''
        Function deletes all .pickle files
        '''

        if os.path.isfile(DataPaths.aislesPickle):
            os.remove(DataPaths.aislesPickle)
        if os.path.isfile(DataPaths.departmentsPickle):
            os.remove(DataPaths.departmentsPickle)
        if os.path.isfile(DataPaths.productsPickle):
            os.remove(DataPaths.productsPickle)
        if os.path.isfile(DataPaths.ordersPickle):
            os.remove(DataPaths.ordersPickle)
        if os.path.isfile(DataPaths.similaritiesPicke) and deleteSimilarities:
            os.remove(DataPaths.similaritiesPicke)
        if os.path.isfile(DataPaths.usersProductsPicke):
            os.remove(DataPaths.usersProductsPicke)
        if os.path.isfile(DataPaths.usersPickle):
            os.remove(DataPaths.usersPickle)

    def storeSimilaritiesToPickle(self, simDict):
        '''
        Function stores dict of similarities to .pickle file
        '''

        with open(DataPaths.similaritiesPicke, "wb") as outfile:
            pickle.dump(simDict, outfile, pickle.HIGHEST_PROTOCOL)

    def getSimilaritiesFromPickle(self):
        '''
        Function reads similarities from .pickle file and stores them in dictionary
        '''

        sim = {}
        if os.path.isfile(DataPaths.similaritiesPicke):
            with open(DataPaths.similaritiesPicke, "rb") as reader:
                try:
                    while True:
                        data = pickle.load(reader)
                        sim.update(data)

                except EOFError:
                    pass

        return sim

    def storeItemSimilaritiesToPickle(self, simDict, amount: int):
        '''
        Function stores dict of similarities to .pickle file
        '''

        file = DataPaths.itemSimilarities + str(amount) + ".pickle"

        with open(file, "wb") as outfile:
            pickle.dump(simDict, outfile, pickle.HIGHEST_PROTOCOL)

    def getUserOrderedProducts(self, user_id) -> dict:
        '''
        Function function finds and returnes users past purchases
        '''
        # {product_id(int) : nomOfPurchases(int)}
        orderdProducts = {}

        for order in self.orders:
            if user_id == self.orders[order].user_id:
                for product in self.orders[order].product_list:
                    if product.id in orderdProducts:
                        orderdProducts[product.id] += 1
                    else:
                        orderdProducts[product.id] = 1

        return orderdProducts

    def storeUserPurchasesToPickle(self, usersPurchases: dict, amount: int):
        '''
        Function stores dict of user purchases to .pickle file
        '''

        file = DataPaths.usersPurchases + str(amount) + ".pickle"

        with open(file, "ab") as outfile:
            pickle.dump(usersPurchases, outfile, pickle.HIGHEST_PROTOCOL)

    def getUserItemPurchases(self, storeItemSize):
        filename = DataPaths.usersPurchases + str(storeItemSize) + ".pickle"
        data = None

        with open(filename, "rb") as reader:
            data = pickle.load(reader)

        return data

    def getItemSimilaritiesPurchases(self, storeItemSize):
        filename = DataPaths.itemSimilarities + str(storeItemSize) + ".pickle"
        data = None

        with open(filename, "rb") as reader:
            data = pickle.load(reader)

        return data
