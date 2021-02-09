from grash import graph
import os.path
import os


def create_test_files(tmpdir):
    with open(os.path.join(tmpdir, 'echo'), 'w') as f:
        f.write("This isn't the echo you're looking for")
    with open(os.path.join(tmpdir, 'foo.sh'), 'w') as f:
        f.write('#!/bin/bash\necho "this is a test"')
    with open(os.path.join(tmpdir, 'bar.sh'), 'w') as f:
        f.write('#!/bin/bash\necho "This is another test"\nfoo.sh 1 2 3')
    with open(os.path.join(tmpdir, 'baz.sh'), 'w') as f:
        f.write('#!/bin/bash\nfoo.sh 1 2 3\nbar.sh\necho "Done!"')


def test__get_all_files_from_paths(tmpdir):
    test_scripts = [os.path.join(tmpdir, script) for script in ['foo.sh', 'bar.sh', 'baz.sh']]
    create_test_files(tmpdir)
    files = graph._get_all_files_from_paths([tmpdir])
    assert all([file in files for file in test_scripts])


def test_graph(tmpdir):
    create_test_files(tmpdir)
    test_scripts = [os.path.join(tmpdir, script) for script in ['foo.sh', 'bar.sh', 'baz.sh']]
    g = graph.Graph([tmpdir], test_scripts)

    assert all([script in g.scripts for script in test_scripts])

    assert g[test_scripts[0]].name == 'foo.sh'
    deps = [dep.name for dep in g[test_scripts[0]].dependencies]
    assert [script in deps for script in ['echo']]
    assert g[test_scripts[0]].type == 'Bourne-Again shell script, ASCII text executable'

    assert g[test_scripts[1]].name == 'bar.sh'
    deps = [dep.name for dep in g[test_scripts[1]].dependencies]
    assert [script in deps for script in ['echo', 'foo.sh']]
    assert g[test_scripts[1]].type == 'Bourne-Again shell script, ASCII text executable'

    assert g[test_scripts[2]].name == 'baz.sh'
    deps = [dep.name for dep in g[test_scripts[2]].dependencies]
    assert [script in deps for script in ['bar.sh', 'echo', 'foo.sh']]
    assert g[test_scripts[2]].type == 'Bourne-Again shell script, ASCII text executable'
