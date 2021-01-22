import ast
import unittest
import tests.resources.sources as sources


from pyparser.summary.body_summary import BodySummary
from pyparser.utils import  ast_from_string
from pyparser.parser.body_visitor import BodyVisitor, _increase_counter

class BodyVisitorTest(unittest.TestCase):
    def _get_visitor_and_result(self, source):
        visitor = BodyVisitor()
        result = visitor.visit(ast_from_string(source))
        return visitor, result

    def test__increase_counter(self):
        counter = {}
        _increase_counter(counter, 'Test')
        self.assertEqual(1, counter['Test'])

        _increase_counter(counter, 'Test')
        self.assertEqual(2, counter['Test'])

        _increase_counter(counter, 'Test2')
        self.assertEqual(2, len(counter))

    def test_visit_module(self):
        visitor, result = self._get_visitor_and_result(sources.CALL_EXAMPLE)
        self.assertTrue(isinstance(result, BodySummary))
        self.assertEqual(1, len(result.summary_list))
        
    # Data structures
    
    def test_visit_tuple(self):
        visitor, result = self._get_visitor_and_result(sources.TUPLE_EXAMPLE)
        # TODO -> add summary and test
        # self.assertEqual([1, 2, 3], result)
        self.assertEqual(1, result.counters['Tuple'])
    
    def test_visit_list(self):
        visitor, result = self._get_visitor_and_result(sources.LIST_EXAMPLE)
        # TODO -> add summary and test
        # self.assertEqual([1, 2, 3], result)
        self.assertEqual(1, result.counters['List'])
    
    def test_visit_set(self):
        visitor, result = self._get_visitor_and_result(sources.SET_EXAMPLE)
        # TODO -> add summary and test
        # self.assertEqual([1, 2, 3], result)
        self.assertEqual(1, result.counters['Set'])

    def test_visit_dict(self):
        visitor, result = self._get_visitor_and_result(sources.DICT_EXAMPLE)
        # TODO -> add summary and test
        # self.assertEqual([1, 2, 3], result)
        self.assertEqual(1, result.counters['Dict'])