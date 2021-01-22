import ast
import inspect

from pyparser.summary.body_summary import BodySummary
from pyparser.summary.function_summary import FunctionSummary
from pyparser.summary.minor_summaries import (
    ForSummary,
    WhileSummary
)


def _increase_counter(counter, value):
    """ Increases the given counter using the given value """
    counter[value] = counter[value] + 1 if value in counter else 1


class BodyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.counters = {}

    def visit(self, node, arg=None):
        """ Visits a summary """
        flag = False
        parameters = [node, arg]
        method = f'visit_{node.__class__.__name__}'
        try:
            visitor = getattr(self, method)
        except AttributeError: # No specific method for the given class
            visitor = self.generic_visit
            flag = True

        # if the methods has not been overwitten (no `arg` parameter)
        flag = len(inspect.signature(visitor).parameters.values()) != 2
        # print(inspect.signature(visitor).parameters.values())

        if flag: # only pass `node` as parameter for the method call
            parameters = parameters[:1]
        
        return visitor(*parameters)

    def body_visit(self, node, arg=None):
        """ 
            Returns a BodySummary with the result of the visit of each 
            node in `node`'s body. `arg` represents a dict of counters.
            It is used for example for operators and data structurse
        """
        if arg is None:
            arg = {}
        return BodySummary([self.visit(inner_node, arg) for inner_node in node.body], arg)

    def visit_Module(self, node: ast.Module, arg=None): 
        """
            Node's fields:
                - body (list(ast.?)): every element in the module's body
                - type_comment (?): ?
        """
        return self.body_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef, arg=None):
        """
            Node's fields:
                - name (str): the function's name
                - args (ast.arguments): the function's arguments
                - body (list(ast.?)): every element in the function's body
                - decorator_list (list(ast.Name)): the decorators used on the function
                - returns (ast.?): the indicative information about the function's return
                - type_comment (?): ?
        """
        name = node.name
        body_result = self.body_visit(node)
        args_result = self.visit(node.args)

        return FunctionSummary(name, args_result, body_result)
    
    def visit_arguments(self, node: ast.arguments, arg=None):
        """
            Node's fields:
                - posonlyargs (?): 
                - args (list(ast.arg)): the list of arguments
                - vararg (ast.arg): the conventionally named `*args` variable
                - kwonlyargs (?): 
                - kw_defaults (?): 
                - kwargs (ast._arg): the conventionally named `**kwargs` variable
                - defaults (list(ast.?)): the optional default value of the arguments.
                    How are they linked to the correct arg in args ?
                    -> (len(args) - len(defaults)) gives the index of the 1st argument with default
        """
        return len(node.args)
    
    # ----- Loops ----- #

    def visit_For(self, node: ast.For, arg=None)-> ForSummary:
        """
            Node's fields:
                - target (ast.Name): name of the 
                - iter (object): values looped through
                - body (list(ast.?))
                - orelse (?)
                - type_comment (?)
        """
        target = self.visit(node.target, arg)
        body_summary = self.body_visit(node)

        return ForSummary(target, body=body_summary)

    def visit_While(self, node: ast.While, arg=None)-> WhileSummary:
        """
            Node's fields:
                - test (object): name of the 
                - body (list(ast.?))
                - orelse (?)
        """
        _increase_counter(arg, node.__class__.__name__)
        test = self.visit(node.test, arg)
        body_summary = self.body_visit(node)

        return WhileSummary(test, body_summary)
    
    # ----- Data structures ----- # 
    def visit_Tuple(self, node, arg=None):
        """
           Node's fields:
            - elts list(object): content of the tuple 
            - ctx (?)
        """
        _increase_counter(arg, node.__class__.__name__)
        return [self.visit(element, arg) for element in node.elts]

    def visit_List(self, node, arg=None):
        """
           Node's fields:
            - elts list(object): content of the list 
            - ctx (?)
        """
        _increase_counter(arg, node.__class__.__name__)
        return [self.visit(element, arg) for element in node.elts]
    
    def visit_Set(self, node, arg=None):
        """
           Node's fields:
            - elts list(object): content of the set 
        """
        _increase_counter(arg, node.__class__.__name__)
        return [self.visit(element, arg) for element in node.elts]
    
    def visit_Dict(self, node, arg=None):
        """
           Node's fields:
            - keys list(_ast.Name): 
            - values list(object):  
        """
        _increase_counter(arg, node.__class__.__name__)
        keys = [self.visit(key, arg) for key in node.keys]
        values = [self.visit(value, arg) for value in node.values]
        return list(map(list, zip(keys, values)))
    
    # ----- XX -----

    def visit_Name(self, node: ast.Name, arg=None):
        """
            Node's fields:
                - id (str): node's name
                - ctx (?):
        """
        return node.id
    
    def visit_Constant(self, node, arg=None):
        """
            Node's fields:
                - value (any type): the constant value
                - kind (?):
        """
        return node.value
    