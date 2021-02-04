import pytest
from grash import parser


get_words_inputs = [
    ('a b c', {'a'}),
    ('a b "c"', {'a'}),
    ('2>/dev/null a b "c"', {'a'}),
    ('a b>&1 2>&1', {'a'}),
    ('a\nb', {'a', 'b'}),
    ('a | b', {'a', 'b'}),
    ('! a | b', {'a', 'b'}),
    ('a;', {'a'}),
    ('a && b', {'a', 'b'}),
    ('a; b; c& d', {'a', 'b', 'c', 'd'}),
    ('a | b && c', {'a', 'b', 'c'}),
    ('$($<$(a) b)', {'a', '$'}),
    ('a <(b $(c))', {'a', 'b', 'c'}),
    ('FOO="echo foo"; eval $FOO', {'echo', 'eval'}),
    ('eval foo', {'eval', 'foo'}),
    ('eval $(cat foo.sh)', {'eval', 'cat'}),
    ('source foo.sh', {'source', 'foo.sh'}),
    ('source /foo/bar.sh', {'source', 'bar.sh'}),
    ('foo # This is a comment and should return nothing', {'foo'}),
    ('function foo { echo test; }', {'echo'}),
    ('function foo { echo test; };', {'echo'}),
    ('foo () { echo test; }', {'echo'}),
    ('foo () { echo test; };', {'echo'}),
    ('if [ "$1" == "-e" ]; then MSG="$2"; fi', {'['})
]


@pytest.mark.parametrize("test_input,expected", get_words_inputs)
def test__get_words(test_input, expected):
    words = set()
    assignments = {}
    parser._get_words(test_input, words, assignments)
    assert words == expected


parse_inputs = [
    ('''foo a b c\nbar d e f''', {'foo', 'bar'}),
    ('''FOO="echo foo"\neval $FOO''', {'echo', 'eval'}),
    ('''COMMAND_ONE="bar"\nCOMMAND_TWO="my_script foo | ${COMMAND_ONE}"\neval $COMMAND_TWO''', {'my_script', 'bar', 'eval'}),
    ('''foo () {\n    echo this is a test\n}\n''', {'echo'}),
    ('''#!/bin/bash\nfoo\n#This is a comment\n# This is another comment\n    #This is another comment''', {'foo'}),
    ('''if [ "$1" == "-e" ]; then\necho Test\nfi''', {'[', 'echo'})
]


@pytest.mark.parametrize("test_input,expected", parse_inputs)
def test_parse(tmpdir, test_input, expected):
    test_file = tmpdir / "test.sh"
    with open(test_file, 'w') as f:
        f.write(test_input)
    assert parser.parse(test_file) == expected

