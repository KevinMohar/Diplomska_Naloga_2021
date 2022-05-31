from UI.UImanager import UImanager

# true - uporablja opimizirani algoritem ki bere podatke iz baze in jih ne računa
# false - uporablja osnovni algoritem ki računa podakte ob runtime
IS_OPTIMIZED_ALGORITHEM = True

uiManager = UImanager(IS_OPTIMIZED_ALGORITHEM)

recommendations = uiManager.recommendProducts(10)

uiManager.outputRecommendations(recommendations, printToConsole=True)
