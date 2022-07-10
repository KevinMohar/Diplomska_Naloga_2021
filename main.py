from ApplicationConstants import ApplicationConstants
from UI.UImanager import UImanager

# true - uporablja opimizirani algoritem ki bere podatke iz baze in jih ne računa
# false - uporablja osnovni algoritem ki računa podakte ob runtime
IS_OPTIMIZED_ALGORITHEM = True

# idx: 0 = for each item we store 1 most similar items; for each user we store 1 most frequently purchased product
# idx: 1 = for each item we store 10 most similar items; for each user we store 10 most frequently purchased products
# idx: 2 = for each item we store 50 most similar items; for each user we store 50 most frequently purchased products
# idx: 3 = for each item we store 100 most similar items; for each user we store 100 most frequently purchased products
ITEM_SIMILARITY_STORE_SIZE = ApplicationConstants.ITEM_SIMILARITY_STORE_SIZES[0]

# idx: 0 = for each user we store 1 most frequently purchased product
# idx: 1 = for each user we store 10 most frequently purchased products
# idx: 2 = for each user we store 50 most frequently purchased products
# idx: 3 = for each user we store 100 most frequently purchased products
USERS_PRODUCTS_STORE_SIZE = ApplicationConstants.USERS_PRODUCTS_STORE_SIZES[0]

# idx: 0 = 1k orders in database
# idx: 1 = 5k orders in database
# idx: 2 = 10k orders in database
# idx: 3 = 15k orders in database
SAMPLE_SIZE_ORDERS = ApplicationConstants.SAMPLE_SIZES_ORDERS[0]

# idx: 0 = 100 products in database
# idx: 1 = 500 products in database
# idx: 2 = 1000 products in database
# idx: 3 = 1500 products in database
SAMPLE_SIZES_PRODUCTS = ApplicationConstants.SAMPLE_SIZES_PRODUCTS[0]

uiManager = UImanager(IS_OPTIMIZED_ALGORITHEM,
                      SAMPLE_SIZE_ORDERS, SAMPLE_SIZES_PRODUCTS, USERS_PRODUCTS_STORE_SIZE, ITEM_SIMILARITY_STORE_SIZE)
recommendations = uiManager.recommendProducts(10)
uiManager.outputRecommendations(recommendations, printToConsole=True)
