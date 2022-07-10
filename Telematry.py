from datetime import datetime
from sqlite3 import time


class Telematry:
    dataPrep_content_startTime: any
    dataPrep_content_endTime: any
    dataPrep_content_proccessingTime: any

    dataPrep_itemB_startTime: any
    dataPrep_itemB_endTime: any
    dataPrep_itemB_proccessingTime: any

    dataFiltr_startTime: any
    dataFiltr_endTime: any

    dataPrep_total_time: any
    dataFiltr_total_time: any

    itemBased_startTime: any
    itemBased_endTime: any
    itemBased_totalTime: any
    itemBased_RequestedProducts: int
    itemBased_RecommendedProducts: int
    itemBased_MissPercentage: float

    contentBased_startTime: any
    contentBased_endTime: any
    contentBased_totalTime: any
    contentBased_RequestedProducts: int
    contentBased_RecommendedProducts: int
    contentBased_MissPercentage: float

    DB_orders: int
    DB_products: int
    PerItemStoreSize: int
    PerUserStoreSize: int
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
        print("# Num of products: %s" % self.DB_products)
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
        print("# Num of products: %s" % self.DB_products)
        print("# Total data filtration time:         %ss" %
              self.dataFiltr_total_time)
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
