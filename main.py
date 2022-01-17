from DataProvider import DataProvider
from Predictors.SimpleContextBasedPredictor import SimpleContextBasedPredictor
from Recommender import Recommender
from UI.UImanager import UImanager



dp = DataProvider()
uiManager = UImanager()

#recommender = Recommender(SimpleContextBasedPredictor(dp))
# recommender.fit(dp.products)


#print(recommender.recommend(3, [], 2))
print(dp.aisles)


