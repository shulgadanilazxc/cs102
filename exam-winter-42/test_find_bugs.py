import find_bugs

def test_load_tasks():
    print(find_bugs.load_tasks())
    assert [[('A', 'B'), ('B', 'C'), ('C', 'B')], [('A', 'A'), ('B', 'C'), ('C', 'A')], [('A', 'A'), ('B', 'B')]] == find_bugs.load_tasks()

def test_flat_letters():
    graph = find_bugs.load_tasks()[0]
    assert ['A', 'B', 'B', 'C', 'C', 'B'] == find_bugs.flat_letters(graph)

def test_traverse():
    graph = find_bugs.load_tasks()[0]
    assert ('C', 'A') == find_bugs.traverse(graph)

def test_check_broken_links():
    graph = find_bugs.load_tasks()[0]
    assert 1 == find_bugs.check_broken_links(graph)