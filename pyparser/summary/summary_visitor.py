from collections.abc import Iterable
from pyparser.summary.summary import (
    Summary,
    all_attrs_predicate as all_pre,
    excluded_attrs_predicate as pre,
    select_method as sm
)

class SummaryVisitor:
    PARAMETERS_FIELDS = ['select_method', 'excluded_attrs', 'predicate']

    def __init__(self, parameters=None, defaults=None):
        """ 
            parameters -> {
                aSummaryClassName: {
                    select_method: function,
                    excluded_attrs: [],
                    predicate: lambda
                }
            }
        """
        self.parameters =  {
            'BodySummary': {
                'excluded_attrs': ['summary_list']
            }
        }

        if parameters is not None:
            self.parameters.update(parameters)

        self.defaults = defaults or {
            'select_method': sm,
            'predicate': pre,
            'excluded_attrs': []
        }

    def visit(self, summary):
        """ Visits a summary """
        method = f'visit_{summary.__class__.__name__.lower()}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(summary)

    def generic_visit(self, summary):
        """ Called if no explicit visitor function exists for a node """
        print(type(summary))
        if isinstance(summary, Summary):
            raise Warning(f'No method have been define for the class {summary.__class__.__name__}')
        else:
            raise TypeError(f'Summary or child class object expected, {summary.__class__.__name__} found')
    
    def _get_parameters(self, name):
        return self.parameters[name] if name in self.parameters else None
    
    def _auto_build(self, summary):
        """ Generates a basic summary """
        field_map = {}
        summary_name = summary.__class__.__name__

        for field in self.PARAMETERS_FIELDS:
            try:
                field_map[field] = self._get_parameters(summary_name)[field]
            except TypeError: # result can be None
                field_map[field] = self.defaults[field]
            except KeyError: # or incomplete
                field_map[field] = self.defaults[field]

        return summary.build(**field_map)
    
    def _safe_build(self, summary, output, attr):
        if attr in vars(summary):
            attribute = getattr(summary, attr)
            output[attr] = [self.visit(field) for field in attribute] \
                if isinstance(attribute, Iterable) else self.visit(attribute)
            
    def _visit_body(self, summary):
        """ Builds the basic summary and generates the body's summary """
        result  = self._auto_build(summary)
        self._safe_build(summary, result, 'body')
        return result
    
    def visit_bodysummary(self, summary):
        result = self._auto_build(summary)
        self._safe_build(summary, result, 'functions')
        self._safe_build(summary, result, 'fors')
        self._safe_build(summary, result, 'whiles')

        return result
    
    def visit_functionsummary(self, summary):
        return self._visit_body(summary)
    
    def visit_forsummary(self, summary):
        return self._visit_body(summary)
    
    def visit_whilesummary(self, summary):
        return self._visit_body(summary)