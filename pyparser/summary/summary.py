from json import dumps

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