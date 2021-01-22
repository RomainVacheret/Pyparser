import inspect

from json import dumps

# Predicates
# All attributes
all_attrs_predicate = lambda : True
# Attributes which are not in `attrs`
excluded_attrs_predicate = lambda key, excluded_attrs: key not in excluded_attrs
# Attributes which are not None
attr_not_none_predicate = lambda value: value is not None
# Attributes which are nor None nor in `attrs`
excluded_not_none_predicate = lambda key, value, excluded_attrs: \
    excluded_attrs_predicate(key, excluded_attrs) and attr_not_none_predicate(value)
# Attributes which are not empty
# TODO
# Attributes which are not None, not in `attrs` and not empty
# TODO

class Summary:
    """ Base class or all summaries"""
    def build(self, select_method, predicate, **kwargs):
        """
            :param select_method: the method used to select the attributes
                used for the summary
            :type select_method: object
            :param excluded_attrs: the attributes that won't be part of the summary
            :type excluded_attrs: tuple(str)

            :returns: the object's summary
            :rtype: dict
        """
        return select_method(self, predicate, **kwargs)
    

def write_json(filename, summary):
    """
        Writes a JSON file using the given summary.

        :param filename: name of the json file
        :type filename: str
        :param summary: summary exported from a SummaryBuilder
        :type summary: dict
    """
    with open(filename, 'w') as file:
        file.write(dumps(summary, indent=4))


def select_method(summary, predicate, **kwargs):
    """
        Creates the summary's summary excluding parameters if necessary

        :param summary: summary from with the summary will be created
        :type summary: SummaryBuidlder
        :param predicate: predicate matching the attributes to collect
        :type predicate: lambda
        :param kwargs: parameters needed by the predicate

        :raises ?: attributes not in kwargs

        :returns: the summary matching the requirements
        :rtype: dict
    """
    
    if 'excluded_attrs' not in kwargs:
        kwargs['excluded_attrs'] = []
    # Parameters needed by the predicate
    needed_params = [param.name for param in inspect.signature(predicate).parameters.values()]

    def method(summary, predicate, params):
        """ Returns the summary's summary attributes matching the predicate """
        result = {}

        for (key, value) in vars(summary).items():
            tmp_params = params[:]

            if 'key' in needed_params:
                tmp_params.insert(needed_params.index('key'), key)
            if 'value' in needed_params:
                tmp_params.insert(needed_params.index('value'), value)

            if predicate(*tmp_params):
                result[key] = value

        return result

    # TODO case arg not in kwargs
    # Parameters `key` and `value` will be processed afterwards in the function `method`
    params = [kwargs[param] for param in needed_params if param not in ('key', 'value')]
    tmp  = method(summary, predicate, params)
    return tmp