from DataProvider import DataProvider

dataProdvider = DataProvider()

print("Listing aisles:")
for aisle in dataProdvider.aisles:
    print(aisle)
