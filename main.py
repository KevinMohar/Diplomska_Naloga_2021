from DataProvider import DataProvider
from Predictors.SimpleContextBasedPredictor import SimpleContextBasedPredictor
from Predictors.ItemBasedPredictor import ItemBasedPredictor
from Recommender import Recommender
from UI.UImanager import UImanager

recommendations = []

dp = DataProvider(True)
uiManager = UImanager()

'''
SCBpredictor =SimpleContextBasedPredictor(dp)
recommender = Recommender(SCBpredictor)
SCBrecommendations = recommender.recommend(uiManager.getUser(), uiManager.getBasket(), 5)

IBpredictor = ItemBasedPredictor(dp)
recommender = Recommender(IBpredictor)
IBrecommendations = recommender.recommend(uiManager.getUser(), uiManager.getBasket(), 5)

recommendations.extend(SCBrecommendations)
recommendations.extend(IBrecommendations)
'''
uiManager.outputRecommendations(list(dp.products.values()))



