import bashlex


class wordvisitor(bashlex.parser.ast.nodevisitor):
    def __init__(self, words, assignments):
        self.words = words
        self.assignments = assignments

    def visitcommand(self, n, parts):
        for i in range(len(parts)):
            if parts[i].kind == 'commandsubstitution':
                break
            words = self._process_command(parts[i])
            if words in ({'eval'}, {'source'}) and len(parts) > i + 1:
                if self._process_command(parts[i+1]):
                    words.update(self._process_command(parts[i+1]))
            if words:
                self.words.update(set(words))
                break

    def _process_command(self, part):
        if part.kind == 'word':
            if len(part.parts) == 0:
                return {part.word}
            elif part.parts[0].kind == 'parameter':
                return _get_words(self.assignments[part.parts[0].value])

    def visitassignment(self, n, word):
        key, value = word.split('=', 1)
        self.assignments[key] = value


def parse(file_path):
    """
    Parses bash file and finds all word tokens that could be executables
    :param file_path: Bash file to parse
    :return: Set of all words found in script
    """
    executables = set()
    with open(file_path, 'r') as f:
        while line := f.readline():
            executables.update(_get_words(line))
    return executables


def _get_words(line):
    """
    Parses bash line and finds all word tokens that could be executables
    :param line: Line to parse
    :return: Set of all words found in line
    """
    trees = bashlex.parse(line)
    words = set()
    assignments = {}
    for tree in trees:
        visitor = wordvisitor(words, assignments)
        visitor.visit(tree)
    return words
