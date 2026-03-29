from base_metric import BaseMetric
class ResponseLengthMetric(BaseMetric):
    def compute(self,response):
        return len(response)