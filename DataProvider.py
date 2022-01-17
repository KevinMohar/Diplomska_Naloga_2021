from ApplicationConstants import DataPaths, Logging
from DataModels import Aisle, Department, Product, Order
import csv
import json
import os
import threading
from collections import namedtuple
from json import JSONEncoder


class DataProvider():

    maxNumOfRecords = 10000

    aisles = {}
    departments = {}
    products = {}
    orders = {}

    threads = []

    def __init__(self) -> None:
        if(False):
            print(Logging.INFO + "Startee data parsing (to parse: aisles, departments, products, orders, ordered products)...")

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

            # store to json
            self.__storeDataToJSON()

        else:
            self.__getAislesFromJSON()

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

    def __storeDataToJSON(self):

        t1 = threading.Thread(target=self.__storeAislesToJSON)
        t1.start()

        t2 = threading.Thread(target=self.__storeDepartmentsToJSON)
        t2.start()

        t3 = threading.Thread(target=self.__storeProductsToJSON)
        t3.start()

        t4 = threading.Thread(target=self.__storeOrdersToJSON)
        t4.start()

    def __storeAislesToJSON(self):
        with open(DataPaths.aislesJSON, "w") as outfile:
            outJSON = {}
            aisles = [json.dumps(self.aisles[aisle].__dict__) for aisle in self.aisles]
            outJSON["aisles"] = aisles
            json.dump(outJSON, outfile)

    def __storeDepartmentsToJSON(self):
        with open(DataPaths.departmentsJSON, "w") as outfile:
            outJSON = {}
            departments = [json.dumps(self.departments[department].__dict__) for department in self.departments]
            outJSON["departments"] = departments
            json.dump(outJSON, outfile)

    def __storeProductsToJSON(self):
        with open(DataPaths.productsJSON, "w") as outfile:
            json.dump({"products": self.products}, outfile)

    def __storeOrdersToJSON(self):
        with open(DataPaths.ordersJSON, "w") as outfile:
            json.dump({"orders": self.orders}, outfile)

    def __getAislesFromJSON(self):
        with open(DataPaths.aislesJSON, "r") as reader:
            jsonData = json.load(reader)
            for aisle in jsonData["aisles"]:
                aisleObj = Aisle(aisle)
                self.aisles[aisleObj.id] = aisleObj
        
    
