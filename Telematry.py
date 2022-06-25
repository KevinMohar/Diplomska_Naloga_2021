from datetime import datetime
from time import time


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

    DB_records: int
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
        print("# Num of records: %i" % self.DB_records)
        print("# Content based data prep time: %s s" %
              self.dataPrep_content_proccessingTime)
        print("# Item based data prep time:    %ss" %
              self.dataPrep_itemB_proccessingTime)
        print("# Total data prep time:         %s s" %
              self.dataPrep_total_time)
        print("#" + ("-" * self.NumOfHypens) + "#")
        print()

    def PrintDataFiltrJobStats(self):
        self.dataFiltr_total_time = self.dataFiltr_endTime - self.dataFiltr_startTime

        print()
        print("#" + ("-" * self.NumOfHypens) + "#")
        print("# Prepared data sample sizes: %s" % self.DB_records)
        print("# Total data filtration time:         %ss" %
              self.dataFiltr_total_time)
        print("#" + ("-" * self.NumOfHypens) + "#")
        print()
