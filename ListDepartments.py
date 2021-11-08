from DataProvider import DataProvider

dataProdvider = DataProvider()

print("Listing aisles:")
for department in dataProdvider.departments:
    print(department)
