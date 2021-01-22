from pyparser.summary.summary import Summary
from pyparser.summary.function_summary import FunctionSummary
from pyparser.summary.minor_summaries import (
    ForSummary,
    WhileSummary
)

class BodySummary(Summary):
    def __init__(self, summary_list, counters=None):
        self.summary_list = summary_list
        self.counters = counters

        self.functions = []
        self.fors = []
        self.whiles = []

        self._sort_list()
    
    def _sort_list(self):
        """ Stores each summary in the list into the corresponding attribute """
        for summary in self.summary_list:
            if isinstance(summary, FunctionSummary):
                self.functions.append(summary)
            elif isinstance(summary, ForSummary):
                self.fors.append(summary)
            elif isinstance(summary, WhileSummary):
                self.whiles.append(summary)
        
    def __str__(self):
        return f'BodySummary[functions: {self.summary_list}]'