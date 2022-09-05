from datetime import datetime
from sqlite3 import time


class Telematry:
    dataPrep_content_startTime: any = None
    dataPrep_content_endTime: any = None
    dataPrep_content_proccessingTime: any = None

    dataPrep_itemB_startTime: any = None
    dataPrep_itemB_endTime: any = None
    dataPrep_itemB_proccessingTime: any = None

    dataFiltr_startTime: any = None
    dataFiltr_endTime: any = None

    dataPrep_total_time: any = None
    dataFiltr_total_time: any = None

    itemBased_startTime: any = None
    itemBased_endTime: any = None
    itemBased_totalTime: any = None
    itemBased_RequestedProducts: int = None
    itemBased_RecommendedProducts: int = None
    itemBased_MissPercentage: float = None

    contentBased_startTime: any = None
    contentBased_endTime: any = None
    contentBased_totalTime: any = None
    contentBased_RequestedProducts: int = None
    contentBased_RecommendedProducts: int = None
    contentBased_MissPercentage: float = None

    DB_orders: int = None
    PerItemStoreSize: int = None
    PerUserStoreSize: int = None

    NumOfHypens = 100

    def PrintDataPrepJobStats(self):
        self.dataPrep_content_proccessingTime = self.dataPrep_content_endTime - \
            self.dataPrep_content_startTime
        self.dataPrep_itemB_proccessingTime = self.dataPrep_itemB_endTime - \
            self.dataPrep_itemB_startTime
        self.dataPrep_total_time = self.dataPrep_itemB_proccessingTime + \
            self.dataPrep_content_proccessingTime

        print()
        print("#" + ("-" * self.NumOfHypens) + "#")
        print("# Num of orders: %s" % self.DB_orders)
        print("# Content based data prep time: %ss" %
              self.dataPrep_content_proccessingTime)
        print("# Item based data prep time:    %ss" %
              self.dataPrep_itemB_proccessingTime)
        print("# Total data prep time:         %ss" %
              self.dataPrep_total_time)
        print("#" + ("-" * self.NumOfHypens) + "#")
        print()

    def PrintDataFiltrJobStats(self):
        self.dataFiltr_total_time = self.dataFiltr_endTime - self.dataFiltr_startTime

        print()
        print("#" + ("-" * self.NumOfHypens) + "#")
        print("# Num of orders: %s" % self.DB_orders)
        print("# Total data filtration time:         %0.2fs" %
              self.dataFiltr_total_time)
        print("#" + ("-" * self.NumOfHypens) + "#")
        print()

    def PrintReccomendations(self, products_content, products_item, printProducts = False):
        CB_missPercent = 0
        IB_missPercent = 0

        if self.contentBased_RecommendedProducts < self.contentBased_RequestedProducts:
            CB_missPercent = 100 - \
                ((self.contentBased_RecommendedProducts * 100) /
                 self.contentBased_RequestedProducts)

        if self.itemBased_RecommendedProducts < self.itemBased_RequestedProducts:
            IB_missPercent = 100 - \
                ((self.itemBased_RecommendedProducts * 100) /
                 self.itemBased_RequestedProducts)

        print()
        print("#" + ("-" * self.NumOfHypens) + "#")

        print("# Number of orders in DB: {}".format(self.DB_orders))
        print("# Item similarity store size : {}     User orders store size: {}".format(
            self.PerItemStoreSize, self.PerUserStoreSize))

        print("#" + ("-" * int(self.NumOfHypens/2)))

        if printProducts:
            print("# Content based recommendations: ")
            for product in products_content:
                print("#   - Product {}: {}".format(product.id, product.name))
        print("#")
        print("# CB requested products: {}        CB recommended products: {}".format(
            self.contentBased_RequestedProducts, self.contentBased_RecommendedProducts))
        print("# CB miss percentage: {}%        Processing time: {:0.4f}s".format(
            CB_missPercent, self.contentBased_totalTime))

        print("#" + ("-" * int(self.NumOfHypens/2)))

        if printProducts:
            print("# Item based recommendations: ")
            for product in products_item:
                print("#   - Product {}: {}".format(product.id, product.name))
        print("#")
        print("# IB requested products: {}        IB recommended products: {}".format(
            self.itemBased_RequestedProducts, self.itemBased_RecommendedProducts))
        print("# IB miss percentage: {}%        Processing time: {:0.4f}s".format(
            IB_missPercent, self.itemBased_totalTime))

        print("#" + ("-" * self.NumOfHypens) + "#")
        print()

    def StartItemBased(self):
        self.itemBased_startTime = time.time()

    def StartContentBased(self):
        self.contentBased_startTime = time.time()

    def EndItemBased(self):
        self.itemBased_endTime = time.time()
        self.itemBased_totalTime = self.itemBased_endTime - self.itemBased_startTime

    def EndContentBased(self):
        self.contentBased_endTime = time.time()
        self.contentBased_totalTime = self.contentBased_endTime - self.contentBased_startTime
