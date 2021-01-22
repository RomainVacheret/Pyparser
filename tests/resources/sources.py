# Functions
FUNCTION_EXAMPLE = 'def foo(toto:int, bd=12) -> [int, int]: pass'
NESTED_FUNCTIONS_EXAMPLE = "def a():\n\tdef b():\n\t\tdef c():\n\t\t\twhile 1: pass"

# Imports
IMPORT_EXAMPLE = 'from random import randint'

# Loops
FOR_EXAMPLE = 'for _ in range(4): print(toto)'
WHILE_EXAMPLE = 'while 1: print(toto)'

# Data structures
TUPLE_EXAMPLE = 'x = (1, 2, 3)'
LIST_EXAMPLE = 'x = [1, 2, 3]'
SET_EXAMPLE = 'x = {1, 2, 3}'
DICT_EXAMPLE = 'x = {"1": 1, "2": 2, "3": 3}'

# Comprehensions
LIST_COMP_EXAMPLE = 'x = [i for i in range(9)]'
SET_COMP_EXAMPLE = 'x = {i for i in range(9)}'
DICT_COMP_EXAMPLE = 'x = {i: i ** 2 for i in range(9)}'

# Calls and expressions
CALL_EXAMPLE = 'print(1)'
CALL_KEYWORD_EXAMPLE = 'print(1, end=" ")'
AUGASSIGN_EXAMPLE = 'x += 2'