import ast
import unittest
import tests.resources.sources as sources


from pyparser.summary.body_summary import BodySummary
from pyparser.utils import  ast_from_string
from pyparser.parser.body_visitor import BodyVisitor, _increase_counter

class BodyVisitorTest(unittest.TestCase):
    def test__increase_counter(self):
        counter = {}
        _increase_counter(counter, 'Test')
        self.assertEqual(1, counter['Test'])

        _increase_counter(counter, 'Test')
        self.assertEqual(2, counter['Test'])

        _increase_counter(counter, 'Test2')
        self.assertEqual(2, len(counter))

    def test_visit_module(self):
        visitor = BodyVisitor()
        result = visitor.visit_Module(ast_from_string(sources.CALL_EXAMPLE))
        self.assertTrue(isinstance(result, BodySummary))
        self.assertEqual(1, len(result.summary_list))