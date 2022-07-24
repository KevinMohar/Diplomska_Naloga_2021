import random
import json
from ApplicationConstants import ApplicationConstants, UserFiles, Logging
from DataProvider import DataProvider


SAMPLE_SIZE_ORDERS = ApplicationConstants.SAMPLE_SIZES_ORDERS[0]
NUM_OF_PRODUCTS_IN_BASKET = 20


dp = DataProvider(clearCache=True, sampleSizeOrders=SAMPLE_SIZE_ORDERS)

isOk = False
randProducts = []
randUser = -1
printProducts = False

while not isOk:
    # randomly select N products
    randProducts = random.sample(list(dp.products), NUM_OF_PRODUCTS_IN_BASKET)

    # select random user
    users = []
    for order_id in dp.orders:
        order = dp.orders[order_id]
        if order.user_id not in users:
            users.append(order.user_id)

    randUser = random.choice(users)

    # print baseket and wait for conformation
    print("Randomly generated basket: ")
    print("User: {}".format(randUser))
    if printProducts:
        print("Products: ")
        for prd in randProducts:
            print("  - {}".format(dp.products[prd]))

    userInput = ""
    while True:
        userInput = input("Is this basket ok? Y/N: ")

        if userInput == "Y" or userInput == "y" or userInput == "yes" or userInput == "Yes" or userInput == "YES":
            isOk = True
            break
        elif userInput == "N" or userInput == "n" or userInput == "no" or userInput == "No" or userInput == "NO":
            break
        else:
            print("Invalid input!")


# write to basket.json
filepath = UserFiles.basketInput
jsonOut = {"order": {"user_id": randUser, "products": randProducts}}
with open(filepath, 'w') as outfile:
    json.dump(jsonOut, outfile)

print(Logging.INFO + "Random basket generated and saved to json!")
