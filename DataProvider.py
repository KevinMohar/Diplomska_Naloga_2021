import imp
from ApplicationConstants import DataPaths, Logging
from DataModels import Aisle, Department, Product, Order
import csv
import json
import os
import threading
from collections import namedtuple
from JSONEncoder import Encoder
import pickle

class DataProvider():

    aisles = {}
    departments = {}
    products = {}
    orders = {}
    __emptyOrders = {}

    threads = []

    def __init__(self, clearCache: bool = False) -> None:

        if clearCache:
            self.__deleteAllPickle()

        if not (os.path.isfile(DataPaths.ordersPickle) andos.path.isfile(DataPaths.ordersPickle)):

            print(Logging.INFO + "Started data parsing (to parse: aisles, departments, products, orders, ordered products)...")

            t1 = threading.Thread(target=self.__getAisles)
            self.threads.append(t1)

            t2 = threading.Thread(target=self.__getDepartments)
            self.threads.append(t2)

            t3 = threading.Thread(target=self.__getProducts)
            self.threads.append(t3)

            t4 = threading.Thread(target=self.__getOrders)
            self.threads.append(t4)

            for thread in self.threads:
                thread.start()

            for thread in self.threads:
                thread.join()

            self.__getOrderedProducts()
            print(Logging.INFO + "Finished parsing ordered products")

            # clean orders
            for key in list(self.orders.keys()):
                if len(self.orders[key].product_list) == 0:
                    self.__emptyOrders[key] = self.orders[key]
                    del self.orders[key]

            # store to pickle
            self.__storeOrdersToPickle()
                    
        else:
            self.__getAislesFromPickle()
            self.__getDepartmentsFromPickle()
            self.__getProductsFromPickle()
            self.__getOrdersFromPickle()
            print(Logging.INFO + "Restored data from .pickle files!")

    def __getAisles(self):
        with open(DataPaths.aislesCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                aisle_id = int(row[0])
                aisle = str(row[1])
                self.aisles[aisle_id] = Aisle(aisle_id, aisle)
        print(Logging.INFO + "Finished parsing aisles")

    def __getDepartments(self):
        with open(DataPaths.departmentsCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                department_id = int(row[0])
                department = str(row[1])
                self.departments[department_id] = Department(
                    department_id, department)
        print(Logging.INFO + "Finished parsing departments")

    def __getProducts(self):
        with open(DataPaths.productsCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                product_id = int(row[0])
                product = str(row[1])
                aisle = self.__findAisle(int(row[2]))
                department = self.__findDepartment(int(row[3]))
                self.products[product_id] = Product(
                    product_id, product, aisle, department)
        print(Logging.INFO + "Finished parsing products")

    def __getOrders(self):
        with open(DataPaths.ordersCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                id = int(row[0])
                user_id = int(row[1])
                eval_set = str(row[2])
                order_number = int(row[3])
                order_dow = int(row[4])
                order_hour_of_day = int(row[5])
                days_since_prior_order = int(row[6]) if len(row)==6 else 0
                self.orders[id] = Order(id, user_id, eval_set, order_number, order_dow,
                                        order_hour_of_day, days_since_prior_order)
        print(Logging.INFO + "Finished parsing orders")
        
    def __getOrderedProducts(self):
        with open(DataPaths.orderProductsTrainCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                order_id = int(row[0])
                product = self.__findProduct(int(row[1]))
                if product:
                    self.orders[order_id].addProduct(product)

    def __getOrdersFromPickle(self):
        with open(DataPaths.ordersPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.orders[obj.id] = obj

    def __getAislesFromPickle(self):
        with open(DataPaths.aislesPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.aisles[obj.id] = obj

    def __getDepartmentsFromPickle(self):
        with open(DataPaths.departmentsPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.departments[obj.id] = obj

    def __getProductsFromPickle(self):
        with open(DataPaths.productsPickle, "rb") as reader:
            data = pickle.load(reader)
            for obj in data:
                self.products[obj.id] = obj

    def __findAisle(self, id: int):
        if id in self.aisles.keys():
            return self.aisles[id]
        else:
            return None

    def __findDepartment(self, id: int):
        if id in self.departments.keys():
            return self.departments[id]
        else:
            return None

    def __findProduct(self, id: int):
        if id in self.products.keys():
            return self.products[id]
        else:
            return None

    def __storeDataToPickle(self):
        threads = []
        threads.append(threading.Thread(target=self.__storeAislesToPickle))
        threads.append(threading.Thread(target=self.__storeDepartmentsToPickle))
        threads.append(threading.Thread(target=self.__storeProductsToPickle))
        threads.append(threading.Thread(target=self.__storeOrdersToPickle))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def __storeAislesToPickle(self):
        outData = list(self.aisles.values())
                
        with open(DataPaths.aislesPickle, "wb") as outfile:
            pickle.dump(outData, outfile, pickle.HIGHEST_PROTOCOL)

    def __storeDepartmentsToPickle(self):
        outData = list(self.departments.values())
                
        with open(DataPaths.departmentsPickle, "wb") as outfile:
            pickle.dump(outData, outfile, pickle.HIGHEST_PROTOCOL)

    def __storeProductsToPickle(self):
        outData = list(self.products.values())
                
        with open(DataPaths.productsPickle, "wb") as outfile:
            pickle.dump(outData, outfile, pickle.HIGHEST_PROTOCOL)

    def __storeOrdersToPickle(self):
        outOrders = list(self.orders.values())
                
        with open(DataPaths.ordersPickle, "wb") as outfile:
            pickle.dump(outOrders, outfile, pickle.HIGHEST_PROTOCOL)

    def __deleteAllPickle(self):
        if os.path.isfile(DataPaths.aislesPickle):
            os.remove(DataPaths.aislesPickle)
        if os.path.isfile(DataPaths.departmentsPickle):    
            os.remove(DataPaths.departmentsPickle)
        if os.path.isfile(DataPaths.productsPickle):
            os.remove(DataPaths.productsPickle)
        if os.path.isfile(DataPaths.ordersPickle):    
            os.remove(DataPaths.ordersPickle)   
    
