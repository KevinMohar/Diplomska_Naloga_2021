from DataProvider import DataProvider
from Predictors.RandomPredictor import RandomPredictor
from Recommender import Recommender

dp = DataProvider()

predictor = RandomPredictor()

recommender = Recommender(predictor)
recommender.fit(dp.products)

for prod in recommender.recommend(1, 3):
    print(prod)
