from ApplicationConstants import DataPaths
from DataModels import Aisle, Department, Product
import csv


def findAisle(id):
    for aisle in aisles:
        if aisle.id == id:
            return aisle


def findDepartment(id):
    for department in departments:
        if department.id == id:
            return department


def ReadFile(path: str, type: int):
    global aisles
    global departments
    global products
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        yield next(reader)  # skip header
        for row in reader:
            if type == 1:
                aisles.append(Aisle(int(row[0]), row[1]))
            if type == 2:
                departments.append(Department(int(row[0]), row[1]))
            if type == 3:
                aisle = findAisle(int(row[2]))
                department = findDepartment(int(row[3]))
                products.append(
                    Product(int(row[0]), row[1], aisle, department))


aisles = []
departments = []
products = []

print("Reading aisles....")
with open(DataPaths.aislesCSV, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        aisles.append(Aisle(int(row[0]), row[1]))

print("Done!\nReading departments....")

with open(DataPaths.departmentsCSV, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        departments.append(Department(int(row[0]), row[1]))

print("Done!\nReading products....")

with open(DataPaths.productsCSV, "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # skip header
    for row in reader:
        print(row)
        aisle = findAisle(int(row[2]))
        department = findDepartment(int(row[3]))
        products.append(
            Product(int(row[0]), row[1], aisle, department))
print("Done!")


for product in products:
    print(product+"\n\n")
