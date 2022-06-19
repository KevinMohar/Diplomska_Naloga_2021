import csv
from ApplicationConstants import ApplicationConstants, DataPaths, Logging


def writeOrdersToCSV(csvStringArray, sampleSize):
    files = {1000: DataPaths.ordersCSV_filtered1k, 5000: DataPaths.ordersCSV_filtered5k,
             10000: DataPaths.ordersCSV_filtered10k, 15000: DataPaths.ordersCSV_filtered15k}

    # write to file
    with open(files[sampleSize], "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csvStringArray)


SAMPLE_SIZES = ApplicationConstants.SAMPLE_SIZES
lastPassed = False
csv_file_string_array = []

print(Logging.INFO + "Started data filtration...")

with open(DataPaths.ordersCSV, "r", encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile)
    csv_file_string_array.append(next(reader))
    for row in reader:
        csv_file_string_array.append(row)

        # stop if all sample sizes have been created
        if lastPassed:
            break

        try:
            listIndex = SAMPLE_SIZES.index(len(csv_file_string_array)-1)
            writeOrdersToCSV(csv_file_string_array, SAMPLE_SIZES[listIndex])

            if listIndex == len(SAMPLE_SIZES)-1:
                lastPassed = True
        except:
            pass

print(Logging.INFO + "Data filtration completed!")
