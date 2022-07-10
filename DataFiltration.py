import csv
import random
from sqlite3 import Time
import time
from ApplicationConstants import ApplicationConstants, DataPaths, Logging
from Telematry import Telematry


def writeDataToCSV(filename, csvStringArray, sampleSize=None):
    if sampleSize != None:
        filenameComponents = filename.split(".")
        filename = filenameComponents[0] + "_filtered_" + \
            str(sampleSize) + "." + filenameComponents[1]

    # write to file
    with open(filename, "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csvStringArray)


def prepareRecords(filename):
    with open(filename, "r", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header

        for row in reader:
            orderID = int(row[0])
            productID = int(row[1])

            if orderID in orderIds[len(orderIds)-1] and productID not in productIds:
                productIds.append(productID)


SAMPLE_SIZES_ORDERS = ApplicationConstants.SAMPLE_SIZES_ORDERS
SAMPLE_SIZES_PRODUCTS = ApplicationConstants.SAMPLE_SIZES_PRODUCTS
tel = Telematry()

print(Logging.INFO + "Started data filtration...")

tel.dataFiltr_startTime = time.time()
tel.DB_orders = SAMPLE_SIZES_ORDERS
tel.DB_products = SAMPLE_SIZES_PRODUCTS
orderIds = []
lastPassed = False

##############################
# prepare orders
##############################
csv_file_string_array = []
with open(DataPaths.ordersCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_string_array.append(next(reader))
    orders = []

    for row in reader:
        if row[2] == "train":
            csv_file_string_array.append(row)
            orders.append(int(row[0]))

            # stop if all sample sizes have been created
            if lastPassed:
                break

            try:
                listIndex = SAMPLE_SIZES_ORDERS.index(
                    len(csv_file_string_array)-1)
                writeDataToCSV(DataPaths.ordersCSV,
                               csv_file_string_array, SAMPLE_SIZES_ORDERS[listIndex])
                orderIds.append(orders.copy())

                if listIndex == len(SAMPLE_SIZES_ORDERS)-1:
                    lastPassed = True
            except:
                pass

print(Logging.INFO + "Orders prepared.")
##############################
# prepare products
##############################
csv_file_string_array = []
csv_file_header = ""

productIds = []
prepareRecords(DataPaths.orderProductsTrainCSV)
# prepareRecords(DataPaths.orderProductsPriorCSV)

print(Logging.INFO + "Prepared ordered products.")
nonOrderProducts = []

# find products for orders
with open(DataPaths.productsCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_header = next(reader)

    for row in reader:
        productID = int(row[0])

        if productID in productIds:
            csv_file_string_array.append(row)
        else:
            nonOrderProducts.append(row)


# write filtered products to csv
for x in range(len(SAMPLE_SIZES_PRODUCTS)):
    # save only products for orders
    if x == len(SAMPLE_SIZES_PRODUCTS)-1:
        data = random.sample(csv_file_string_array, SAMPLE_SIZES_PRODUCTS[x])
        data.insert(0, csv_file_header)
        writeDataToCSV(DataPaths.productsForOrdersCSV, data)

    # fill missing products if not enough products were found
    if len(productIds) < SAMPLE_SIZES_PRODUCTS[x]:
        NumbOfMissingSamples = SAMPLE_SIZES_PRODUCTS[x] - len(productIds)
        missingSamples = random.sample(
            nonOrderProducts, NumbOfMissingSamples)
        csv_file_string_array.extend(missingSamples)

    # save products by sample size
    data = random.sample(csv_file_string_array, SAMPLE_SIZES_PRODUCTS[x])
    data.insert(0, csv_file_header)
    writeDataToCSV(DataPaths.productsCSV, data, SAMPLE_SIZES_PRODUCTS[x])

print(Logging.INFO + "Products prepared.")
tel.dataFiltr_endTime = time.time()
print(Logging.INFO + "Data filtration completed!")
tel.PrintDataFiltrJobStats()
