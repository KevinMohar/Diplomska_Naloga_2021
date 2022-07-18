from ApplicationConstants import ApplicationConstants
from UI.UImanager import UImanager

# true - uporablja opimizirani algoritem ki bere podatke iz baze in jih ne računa
# false - uporablja osnovni algoritem ki računa podakte ob runtime
IS_OPTIMIZED_ALGORITHEM = True

ITEM_SIMILARITY_STORE_SIZE = ApplicationConstants.ITEM_SIMILARITY_STORE_SIZE
USERS_PRODUCTS_STORE_SIZE = ApplicationConstants.USERS_PRODUCTS_STORE_SIZE

SAMPLE_SIZE_ORDERS = ApplicationConstants.ORDERS_SAMPLE_SIZE_TO_USE

uiManager = UImanager(IS_OPTIMIZED_ALGORITHEM,
                      SAMPLE_SIZE_ORDERS, ITEM_SIMILARITY_STORE_SIZE, USERS_PRODUCTS_STORE_SIZE)
recommendations = uiManager.recommendProducts(10)
uiManager.outputRecommendations(recommendations, printToConsole=True)
