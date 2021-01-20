from pyparser.summary.summary import Summary

class FunctionSummary(Summary):
    def __init__(self, name, args=None, body=None):
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):
        return f'FunctionSummary[name: {self.name}, args: {self.args}, body: {self.body}]'

    def __repr__(self):
        return f'FunctionSummary[name: {self.name}]'