from collections import defaultdict
import bashlex
import os
import re


class wordvisitor(bashlex.parser.ast.nodevisitor):
    def __init__(self, words, evaluated_variables, assignments):
        self.words = words
        self.evaluated_variables = evaluated_variables
        self.assignments = assignments

    def visitcommand(self, n, parts):
        for i in range(len(parts)):
            if parts[i].kind == 'commandsubstitution':
                break
            words = set(map(os.path.basename, self._process_command(parts[i]))) if self._process_command(parts[i]) else {}
            if words in ({'eval'}, {'source'}) and len(parts) > i + 1:
                if self._process_command(parts[i+1]):
                    words.update(self._process_command(parts[i+1]))
            if words:
                self.words.update(set(words))
                break

    def _process_command(self, part):
        if part.kind == 'word':
            if len(part.parts) == 0:
                return {os.path.basename(part.word)}
            elif part.parts[0].kind == 'parameter':
                self.evaluated_variables.append(part.parts[0].value)
                #return _get_words(self.assignments[part.parts[0].value], self.words, self.assignments)

    def visitassignment(self, n, word):
        key, value = word.split('=', 1)
        self.assignments[key].append(value)


def parse(file_path):
    """
    Parses bash file and finds all word tokens that could be executables
    :param file_path: Bash file to parse
    :return: Set of all words found in script
    """
    evaluated_variables = []
    assignments = defaultdict(list)
    words = set()
    with open(file_path, 'r') as f:
        lines = f.readlines()
        single_line = _preprocess(lines)
        if single_line:
            _get_words(single_line, evaluated_variables, words, assignments)
    for eval_var in evaluated_variables:
        for value in assignments[eval_var]:
            _get_words(value, evaluated_variables, words, assignments)
    return words


def _get_words(line, evaluated_variables, words, assignments):
    """
    Parses bash line and finds all word tokens that could be executables
    :param line: Line to parse
    :return: Set of all words found in line
    """
    if not line:
        return
    trees = bashlex.parse(line)
    for tree in trees:
        visitor = wordvisitor(words, evaluated_variables, assignments)
        visitor.visit(tree)


def _preprocess(lines):
    # A lot of this stuff stems from bashlex not handling comments, multi-line functions, switch statements well
    # https://github.com/idank/bashlex/issues/23
    # https://github.com/idank/bashlex/issues/47

    # Strip comment lines from file
    lines = [line for line in lines if not re.match(r'^[\s]*#.+$', line)]

    # Remove any trailing comments from the script
    lines = [re.sub(r'(?<=[^$])#.*$', '', line) for line in lines]

    # Remove all case related lines
    lines = [line for line in lines if not re.match(r'^\s*esac\s*$', line)]
    lines = [line for line in lines if not re.match(r'^\s*case [\w${}\"]+ in\s*$', line)]
    lines = [line for line in lines if not re.match(r'^\s*\S+\)\s+$', line)]

    # Truncate script into a single line
    single_line = '; '.join([line.rstrip('\n') for line in lines])

    # Ensure there's no leading semicolons
    single_line = single_line.lstrip(';')

    # Should ensure there are no double semi-colons
    regex = re.compile(r';(\s*;)+')
    single_line = re.sub(regex, ';', single_line)

    # Need to remove semicolons between a function declaration + curly brace and first command of function
    # this is needed to ensure baslex can parse functions
    regex = re.compile(r'((function\s+){0,1}(\w+)\s+(\(\)\s+)*{\s*)(;)')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any trailing semicolons after thens
    regex = re.compile(r'(?<=;|\s)(then)\s*;')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any trailing semicolons after in (For case statements)
    regex = re.compile(r'(?<=;|\s)(in)\s*;')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any trailing semicolons after fors
    regex = re.compile(r'(?<=;|\s)(do)\s*;')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any trailing semicolons after open curly brackets
    regex = re.compile(r'(?<=;|\s)({)\s*;')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any trailing semicolons after elses
    regex = re.compile(r'(?<=;|\s)(else)\s*;')
    single_line = re.sub(regex, r'\1', single_line)

    # Need to remove any backslashes followed by a semicolon
    regex = re.compile(r'\\\s*;')
    single_line = re.sub(regex, r'', single_line)

    return single_line
