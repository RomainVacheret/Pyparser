import ast

from pyparser.summary.body_summary import BodySummary
from pyparser.summary.function_summary import FunctionSummary
from pyparser.summary.minor_summaries import (
    ForSummary,
    WhileSummary
)

class BodyVisitor(ast.NodeVisitor):
    def body_visit(self, node):
        return BodySummary([self.visit(inner_node) for inner_node in node.body])

    def visit_Module(self, node: ast.Module): 
        """
            Node's fields:
                - body (list(ast.?)): every element in the module's body
                - type_comment (?): ?
        """
        return self.body_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
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
    
    def visit_arguments(self, node: ast.arguments):
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

    def visit_For(self, node: ast.For)-> ForSummary:
        """
            Node's fields:
                - target (ast.Name): name of the 
                - iter (object): values looped through
                - body (list(ast.?))
                - orelse (?)
                - type_comment (?)
        """
        target = self.visit(node.target)
        body_summary = self.visit(node)

        return ForSummary(target, body=body_summary)

    def visit_While(self, node: ast.While)-> WhileSummary:
        """
            Node's fields:
                - test (object): name of the 
                - body (list(ast.?))
                - orelse (?)
        """
        test = self.visit(node.test)
        body_summary = self.body_visit(node)

        return WhileSummary(test, body_summary)
    
    def visit_Name(self, node: ast.Name):
        """
            Node's fields:
                - id (str): node's name
                - ctx (?):
        """
        return node.id
    
    