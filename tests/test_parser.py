import pytest
from grash import parser
from collections import defaultdict


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
    ('eval foo', {'eval', 'foo'}),
    ('eval $(cat foo.sh)', {'eval', 'cat'}),
    ('source foo.sh', {'source', 'foo.sh'}),
    ('source /foo/bar.sh', {'source', 'bar.sh'}),
    ('foo # This is a comment and should return nothing', {'foo'}),
    ('function foo { echo test; }', {'echo'}),
    ('function foo { echo test; };', {'echo'}),
    ('foo () { echo test; }', {'echo'}),
    ('foo () { echo test; }; baz;', {'echo', 'baz'}),
    ('if [ "$1" == "-e" ]; then MSG="$2"; fi', {'['}),
    ('foo &', {'foo'})
]


@pytest.mark.parametrize("test_input,expected", get_words_inputs)
def test__get_words(test_input, expected):
    words = set()
    eval_vars = []
    assignments = defaultdict(list)
    parser._get_words(test_input, eval_vars, words, assignments)
    assert words == expected


parse_inputs = [
    ('''foo a b c\nbar d e f''', {'foo', 'bar'}),
    ('''FOO="echo foo"\neval $FOO''', {'echo', 'eval'}),
    ('''COMMAND_ONE="bar"\nCOMMAND_TWO="my_script foo | ${COMMAND_ONE}"\neval $COMMAND_TWO''', {'my_script', 'bar', 'eval'}),
    ('''foo () {\n  echo this is a test\n}\n''', {'echo'}),
    ('''#!/bin/bash\nfoo\n#This is a comment\n# This is another comment\n    #This is another comment''', {'foo'}),
    ('''if [ "$1" == "-e" ]; then\necho Test\nfi''', {'[', 'echo'}),
    ('''case ${test} in\nfoo)\necho test\n;;\nbar)\nbaz test\n;;\nesac''', {'echo', 'baz'}),
    ('''foo "this is a test" # And here is an inline comment\nbar baz''', {'foo', 'bar'}),
    ('''foo () {\n  eval $COMMAND\n}\nCOMMAND="bar"\nfoo\n''', {'eval', 'foo', 'bar'}),
    ('''foo () {\n  eval $COMMAND\n}\nif true; then\nCOMMAND="bar"\nelse\nCOMMAND="baz"\nfi\nfoo\n''', {'eval', 'true', 'foo', 'bar', 'baz'}),
    ('''echo "Starting eth0 carrier detect..."\n/usr/sbin/monitor-eth0-carrier.sh &\necho "Usage: $0 {start}"\nexit 1\nexit $?''', {'echo', 'monitor-eth0-carrier.sh', 'exit'}),
    ('''egrep '^#.*$' > /dev/null 2>&1 # this is a trailing comment''', {'egrep'})
]


@pytest.mark.parametrize("test_input,expected", parse_inputs)
def test_parse(tmpdir, test_input, expected):
    test_file = tmpdir / "test.sh"
    with open(test_file, 'w') as f:
        f.write(test_input)
    assert parser.parse(test_file) == expected

