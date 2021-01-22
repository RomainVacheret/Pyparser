from pyparser.summary.summary import Summary


class AssignSummary(Summary):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value 
    
    def __str__(self):
        return f'AssignSummary[targets: {self.targets}, value: {self.value}]'

    def __repr__(self):
        return f'AssignSummary[targets: {self.targets}]'
    

class AugAssignSummary(Summary):
    def __init__(self, target, value, op):
        self.target = target
        self.value = value 
        self._op = op # TODO must not me counted -> already in the body's counter
    
    def __str__(self):
        return f'AugAssignSummary[target: {self.target}, value: {self.value}, op: {self._op}]'

    def __repr__(self):
        return f'AugAssignSummary[target: {self.target}]'
    

class CallSummary(Summary):
    def __init__(self, func, args, keywords):
        self.func = func
        self.args = args 
        self.keywords = keywords 
    
    def __str__(self):
        return f'CallSummary[func: {self.func}, args: {self.args}, keywords: {self.keywords}]'

    def __repr__(self):
        return f'CallSummary[func: {self.func}]'