from ApplicationConstants import ApplicationConstants
from UI.UImanager import UImanager


IS_OPTIMIZED_ALGORITHEM = ApplicationConstants.IS_OPTIMIZED_ALGORITHEM

# num of products to recommend
N = ApplicationConstants.REQUESTED_NUM_OF_PRODUCTS

ITEM_SIMILARITY_STORE_SIZE = ApplicationConstants.ITEM_SIMILARITY_STORE_SIZE
USERS_PRODUCTS_STORE_SIZE = ApplicationConstants.USERS_PRODUCTS_STORE_SIZE

SAMPLE_SIZE_ORDERS = ApplicationConstants.ORDERS_SAMPLE_SIZE_TO_USE

uiManager = UImanager(IS_OPTIMIZED_ALGORITHEM,
                      SAMPLE_SIZE_ORDERS, ITEM_SIMILARITY_STORE_SIZE, USERS_PRODUCTS_STORE_SIZE)
recommendations = uiManager.recommendProducts(N)
uiManager.outputRecommendations(recommendations, printToConsole=True)
