import Queue
import pprint
import string
import sys

def possible_neighbours_for_word(word):
    """Generate all words with edit-dist 1 from input word."""
    possible_neighbours = []
    for i, let in enumerate(word):
        for new_let in string.letters:
            if let == new_let or new_let.isupper():
                continue
            possible_neighbours.append(str(word[:i] + new_let + word[i+1:]))
    return possible_neighbours

def read_word_list(filename):
    """Open filename and return all words in it.

    Will also lowercase all words and strip whitespace.
    """
    word_list = []
    with open(filename) as file:
        for line in file:
            word_list.extend([w.lower() for w in line.split()])
    return word_list

def _reconstruct_path(node2, node1, paths):
    """Reconstruct how we got from node1 to node2 in the BFS."""
    path = [node2]
    while node2 != node1:
        node2 = paths[node2]
        path.append(node2)
    return path

def bfs(node1, node2, dictionary):
    """Give a source, a sink, and a graph, breadth-first search from source to sink.

    XXX: This is very implementation specific, because for performance reasons
    we don't generate the entire graph. Instead, we simply pass in the
    dictionary of all words and the BFS knows how to turn that into node
    neighbours. Probably we'd want to pass in a neighbour function instead, if we cared
    that much.
    """

    dictionary_set = set(dictionary)

    if node1 not in dictionary_set:
        raise ValueError("'%s' not found in word list." % node1)
    if node2 not in dictionary_set:
        raise ValueError("'%s' not found in word list." % node2)

    queue = Queue.Queue()
    seen_already = set()
    # Paths will be just next_node->prev_node, instead of maybe a more normal
    # next_node->(path_length, prev_node) for general pathfinding. This is
    # because it's BFS, so the first time we see a node, we know we've gotten
    # there optimally.
    paths = {}

    queue.put_nowait(node1)

    while not queue.empty():
        next_node = queue.get_nowait()
        if next_node == node2:
            return _reconstruct_path(node2, node1, paths)

        for neighbour in [w for w in possible_neighbours_for_word(next_node) if w in dictionary_set and w not in seen_already]:
            seen_already.add(neighbour)
            queue.put_nowait(neighbour)

            paths[neighbour] = next_node

    return []

if __name__ == '__main__':
    dictionary = read_word_list('word_list.txt')
    try:
        path = bfs(sys.argv[1], sys.argv[2], dictionary)
        if not path:
            print "Couldn't find a path"
        pprint.pprint(path)
    except ValueError, e:
        print e
        print "Please try again."

