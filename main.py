from UI.UImanager import UImanager


uiManager = UImanager()

recommendations = uiManager.recommendProducts(10)

uiManager.outputRecommendations(recommendations, printToConsole=True)
