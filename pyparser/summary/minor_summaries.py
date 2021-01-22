from pyparser.summary.summary import Summary


class ForSummary(Summary):
    def __init__(self, target, iter=None, body=None):
        self.target = target
        self.iter = iter
        self.body = body
    
    def __str__(self):
        return f'ForSummary[target: {self.target}, body: {self.body}]'

    def __repr__(self):
        return f'ForSummary[target: {self.target}]'
    

class WhileSummary(Summary):
    def __init__(self, test, body):
        self.test = test
        self.body = body
    
    def __str__(self):
        return f'WhileSummary[test: {self.test}, body: {self.body}]'

    def __repr__(self):
        return f'WhileSummary[test: {self.test}]'