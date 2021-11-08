from DataProvider import DataProvider

productListNum = 10
dataProdvider = DataProvider()

print(f"Listing first {productListNum} products:")
for product in dataProdvider.products:
    if productListNum == 0:
        break
    productListNum -= 1
    print(product)
