from ApplicationConstants import DataPaths
from DataModels import Aisle, Department, Product
import csv


class DataProvider():

    aisles = []
    departments = []
    products = []

    def __init__(self) -> None:
        self.__getAisles()
        self.__getDepartments()
        self.__getProducts()

    def __getAisles(self):
        with open(DataPaths.aislesCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                self.aisles.append(Aisle(int(row[0]), row[1]))

    def __getDepartments(self):
        with open(DataPaths.departmentsCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                self.departments.append(Department(int(row[0]), row[1]))

    def __getProducts(self):
        with open(DataPaths.productsCSV, "r", encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                aisle = self.__findAisle(int(row[2]))
                department = self.__findDepartment(int(row[3]))
                self.products.append(
                    Product(int(row[0]), row[1], aisle, department))

    def __findAisle(self, id):
        for aisle in self.aisles:
            if aisle.id == id:
                return aisle

    def __findDepartment(self, id):
        for department in self.departments:
            if department.id == id:
                return department
