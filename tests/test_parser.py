from unittest import TestCase
from grash import parser


class Test(TestCase):
    def test__get_words(self):
        s = 'a b c'
        assert {'a'} == parser._get_words(s)

        s = 'a b "c"'
        assert {'a'} == parser._get_words(s)

        s = '2>/dev/null a b "c"'
        assert {'a'} == parser._get_words(s)

        s = 'a b>&1 2>&1'
        assert {'a'} == parser._get_words(s)

        s = 'a\nb'
        assert {'a', 'b'} == parser._get_words(s)

        s = 'a | b'
        assert {'a', 'b'} == parser._get_words(s)

        s = '! a | b'
        assert {'a', 'b'} == parser._get_words(s)

        s = 'a;'
        assert {'a'} == parser._get_words(s)

        s = 'a && b'
        assert {'a', 'b'} == parser._get_words(s)

        s = 'a; b; c& d'
        assert {'a', 'b', 'c', 'd'} == parser._get_words(s)

        s = 'a | b && c'
        assert {'a', 'b', 'c'} == parser._get_words(s)

        # I'm not sure about this test, probably should remove
        s = '$($<$(a) b)'
        assert {'a', '$'} == parser._get_words(s)

        s = 'a <(b $(c))'
        assert {'a', 'b', 'c'} == parser._get_words(s)

        s = 'FOO="echo foo"; eval $FOO'
        assert {'echo', 'eval'} == parser._get_words(s)

        s = 'eval foo'
        assert {'eval', 'foo'} == parser._get_words(s)

        # This is really gross and should never happen, foo.sh will not be recognized as a dep
        s = 'eval $(cat foo.sh)'
        assert {'eval', 'cat'} == parser._get_words(s)

        s = 'source foo.sh'
        assert {'source', 'foo.sh'} == parser._get_words(s)

