from UI.UImanager import UImanager

# true - uporablja opimizirani algoritem ki bere podatke iz baze in jih ne računa
# false - uporablja osnovni algoritem ki računa podakte ob runtime
IS_OPTIMIZED_ALGORITHEM = True

# 1 - for each item we store 1 most similar item; for each user we store 1 most frequently purchased product
# 10 - for each item we store 10 most similar items; for each user we store 10 most frequently purchased products
# 50 - for each item we store 50 most similar items; for each user we store 50 most frequently purchased products
# 100 - for each item we store 100 most similar items; for each user we store 100 most frequently purchased products
STORED_ITEM_SIZE = 5

# 1000 - 1k orders in database
# 5000 - 5k orders in database
# 10000 - 10k orders in database
# 15000 - 15k orders in database
SAMPLE_SIZE = 1000

uiManager = UImanager(IS_OPTIMIZED_ALGORITHEM, STORED_ITEM_SIZE)

recommendations = uiManager.recommendProducts(10)

uiManager.outputRecommendations(recommendations, printToConsole=True)
