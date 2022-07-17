import csv
import glob
import os
from sqlite3 import Time
import time
from ApplicationConstants import ApplicationConstants, DataPaths, Logging
from Telematry import Telematry
from DataModels import Order


def writeDataToCSV(filename, csvStringArray, sampleSize=None):
    if sampleSize != None:
        filenameComponents = filename.split(".")
        filename = filenameComponents[0] + "_filtered_" + \
            str(sampleSize) + "." + filenameComponents[1]

    # write to file
    with open(filename, "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csvStringArray)


def prepareRecords(filename, sampleSizes):
    with open(filename, "r", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header

        for row in reader:
            orderID = int(row[0])
            productID = int(row[1])

            # if products get stored to single file
            # if orderID in orderIds[len(orderIds)-1] and productID not in productIds:
            #     productIds.append(productID)

            for x in range(len(sampleSizes)):
                if orderID in orderIds[x]:
                    productIds[x].append(productID)


def ClearCache(clear: bool):
    if clear:
        # clear products
        fe = DataPaths.productsCSV.split(".")
        files = fe[0] + "_filtered_"
        for filename in glob.glob(files + "*"):
            os.remove(filename)

        # clear orders
        fe = DataPaths.ordersCSV.split(".")
        files = fe[0] + "_filtered_"
        for filename in glob.glob(files + "*"):
            os.remove(filename)


#---------------------------------------------------------------------------------------------------------------#
CLEAR_CACHE = True
SAMPLE_SIZES_ORDERS = ApplicationConstants.SAMPLE_SIZES_ORDERS
#---------------------------------------------------------------------------------------------------------------#

print(Logging.INFO + "Started data filtration...")
tel = Telematry()
tel.dataFiltr_startTime = time.time()
tel.DB_orders = SAMPLE_SIZES_ORDERS
orderIds = []
lastPassed = False
ClearCache(CLEAR_CACHE)

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
csv_file_string_array = [[] for x in range(len(SAMPLE_SIZES_ORDERS))]
csv_file_header = ""

productIds = [[] for x in range(len(SAMPLE_SIZES_ORDERS))]
prepareRecords(DataPaths.orderProductsTrainCSV, SAMPLE_SIZES_ORDERS)
# prepareRecords(DataPaths.orderProductsPriorCSV)

print(Logging.INFO + "Prepared ordered products.")

# find product csv strings
with open(DataPaths.productsCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_header = next(reader)

    for row in reader:
        productID = int(row[0])

        for x in range(len(SAMPLE_SIZES_ORDERS)):
            if productID in productIds[x]:
                csv_file_string_array[x].append(row)


# write filtered products to csv
for x in range(len(SAMPLE_SIZES_ORDERS)):
    data = csv_file_string_array[x]
    data.insert(0, csv_file_header)
    writeDataToCSV(DataPaths.productsCSV, data, SAMPLE_SIZES_ORDERS[x])


print(Logging.INFO + "Products prepared.")
tel.dataFiltr_endTime = time.time()
print(Logging.INFO + "Data filtration completed!")
tel.PrintDataFiltrJobStats()
