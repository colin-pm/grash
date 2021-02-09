from grash import graph
import os.path


def create_test_files(tmpdir):
    with open(os.path.join(tmpdir, 'foo.sh'), 'w') as f:
        f.write('echo "this is a test"')
    with open(os.path.join(tmpdir, 'bar.sh'), 'w') as f:
        f.write('echo "This is another test"\nfoo.sh 1 2 3')
    with open(os.path.join(tmpdir, 'baz.sh'), 'w') as f:
        f.write('#!/bin/bash\nfoo.sh 1 2 3\nbar.sh\necho "Done!"')


def test__get_all_files_from_paths(tmpdir):
    create_test_files(tmpdir)
    files = graph._get_all_files_from_paths([tmpdir])
    assert all([file in files for file in ['foo.sh', 'bar.sh', 'baz.sh']])


def test_graph(tmpdir):
    create_test_files(tmpdir)
    test_scripts = [os.path.join([tmpdir], script) for script in ['foo.sh', 'bar.sh', 'baz.sh']]
    g = graph.Graph(tmpdir, test_scripts)

    assert all([script in g.scripts for script in test_scripts])

    assert g['foo.sh'] == {'echo'}

    assert g['bar.sh'] == {'echo', 'foo.sh'}

    assert g['baz.sh'] == {'foo.sh', 'bar.sh', 'echo'}
