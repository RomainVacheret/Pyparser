import ast
import os

def ast_from_string(string):
    """
        Parses a given string and returns its AST

        :param string: python source code
        :type path: str

        :returns: the AST of the parsed string
        :rtype: _ast.Module 
    """
    return ast.parse(string)

def string_from_ast(ast_):
    """
        Returns the string representation of an AST
        
        :param ast: the AST to convert to string
        :type ast: _ast.Module

        :rtypes: str
    """
    return ast.dump(ast_)


def ast_from_file(path):
    """
        Parses a given python file and returns its AST

        :param path: Path to the file to parse
        :type path: str

        :raises FileNotFoundException: The given path is incorrect

        :returns: AST of the parsed file
        :rtype: _ast.Module 
    """
    if os.path.isfile(path):
        with open(path, 'r') as file:
            tree = ast_from_string(file.read())
    else:
        raise FileNotFoundError()

    return tree


def ast_display(node):
    """
        Displays an AST with a indented format

        :param node: The node the ast to display
        :type node: _ast.Module 
    """
    string = string_from_ast(node)
    tabs = 0
    
    for index, char in enumerate(string):
        brackets = ['(', '[', ')', ']']
        try:
            bracket_index = brackets.index(char)
        except ValueError:
            bracket_index = None

        if bracket_index is not None:
            value = string[index + 1] if bracket_index < 2 else string[index - 1]
            if value == brackets[(bracket_index + 2) % 4]:
                print(char, end='')
                continue

        if char in brackets[:2] or char == ',':
            tabs += char != ','
            print('{0}\n{1}'.format(char, '   ' * tabs), end='')
        elif char in brackets[2:]:
            tabs -= 1   
            print('\n{0}{1}'.format('   ' * tabs, char), end='\n' \
                if string[(index + 1) % len(string)] not in brackets[2:] + [','] else '')
        elif char == ' ':
            continue
        else:
            print(char, end='')