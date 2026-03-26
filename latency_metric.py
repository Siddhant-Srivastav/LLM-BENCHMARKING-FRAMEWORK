from base_metric import BaseMetric
class LatencyMetric(BaseMetric):
    def compute(self,start_time,end_time):
        return end_time-start_time
    
        