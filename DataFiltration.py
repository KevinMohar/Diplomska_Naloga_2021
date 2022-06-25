import csv
import datetime
import random
from sqlite3 import Time
import time
from ApplicationConstants import ApplicationConstants, DataPaths, Logging
from Telematry import Telematry


def writeDataToCSV(filename, csvStringArray, sampleSize):
    filenameComponents = filename.split(".")
    new_filename = filenameComponents[0] + "_filtered_" + \
        str(sampleSize) + "." + filenameComponents[1]

    # write to file
    with open(new_filename, "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csvStringArray)


def prepareRecords(filename):
    with open(filename, "r", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header

        for row in reader:
            orderID = int(row[0])
            productID = int(row[1])

            for x in range(len(orderIds)):
                if orderID in orderIds[x-1] and productID not in productIds[x-1]:
                    productIds[x-1].append(productID)


SAMPLE_SIZES = ApplicationConstants.SAMPLE_SIZES
tel = Telematry()

print(Logging.INFO + "Started data filtration...")

tel.dataFiltr_startTime = time.time()
tel.DB_records = SAMPLE_SIZES
orderIds = []

##############################
# prepare orders
##############################
csv_file_string_array = []
with open(DataPaths.ordersCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_string_array.append(next(reader))
    orders = []

    for row in reader:
        csv_file_string_array.append(row)
        orders.append(int(row[0]))

        # stop if all sample sizes have been created
        if lastPassed:
            break

        try:
            listIndex = SAMPLE_SIZES.index(len(csv_file_string_array)-1)
            writeDataToCSV(DataPaths.ordersCSV,
                           csv_file_string_array, SAMPLE_SIZES[listIndex])
            orderIds.append(orders)
            orders = []

            if listIndex == len(SAMPLE_SIZES)-1:
                lastPassed = True
        except:
            pass

##############################
# prepare products
##############################
csv_file_string_array = []
csv_file_header = ""
[csv_file_string_array.append([]) for _ in range(len(SAMPLE_SIZES))]

productIds = []
[productIds.append([]) for _ in range(len(SAMPLE_SIZES))]

prepareRecords(DataPaths.orderProductsTrainCSV)
prepareRecords(DataPaths.orderProductsPriorCSV)

# find products for orders
with open(DataPaths.productsCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_header = next(reader)
    nonOrderProducts = []
    [nonOrderProducts.append([]) for _ in range(len(SAMPLE_SIZES))]

    for row in reader:
        productID = int(row[0])

        for x in range(len(productIds)):
            if productID in productIds[x-1]:
                csv_file_string_array[x-1].append(row)
            else:
                nonOrderProducts[x-1].append(row)

    # fill missing products
    for x in range(len(productIds)):
        if len(productIds[x-1]) < SAMPLE_SIZES[x-1]:
            NumbOfMissingSamples = SAMPLE_SIZES[x-1] - len(productIds[x-1])
            missingSamples = random.sample(
                nonOrderProducts[x-1], NumbOfMissingSamples)
            csv_file_string_array[x-1].extend(missingSamples)

# write filtered products to csv
for x in range(len(SAMPLE_SIZES)):
    sampSize = SAMPLE_SIZES[x-1]
    csv_file_string_array[x-1].insert(csv_file_header, 0)
    writeDataToCSV(DataPaths.productsCSV)


tel.dataFiltr_endTime = time.time()
print(Logging.INFO + "Data filtration completed!")
tel.PrintDataFiltrJobStats()
