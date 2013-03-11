import Queue
import pprint
import string
import sys

def possible_neighbours_for_word(word):
    possible_neighbours = []
    for i, let in enumerate(word):
        for new_let in string.letters:
            if let == new_let:
                continue
            possible_neighbours.append(str(word[:i] + new_let + word[i+1:]))
    return possible_neighbours

def read_word_list(filename):
    word_list = []
    with open(filename) as file:
        for line in file:
            word_list.extend([w.lower() for w in line.split()])
    return word_list

def reconstruct_path(node2, node1, paths):
    path = [node2]
    while node2 != node1:
        node2 = paths[node2]
        path.append(node2)
    return path

def bfs(node1, node2, dictionary):
    dictionary_set = set(dictionary)
    queue = Queue.Queue()

    seen_already = set()

    queue.put_nowait(node1)

    paths = {}

    while not queue.empty():
        next_node = queue.get_nowait()
        if next_node == node2:
            return reconstruct_path(node2, node1, paths)


        for neighbour in [w for w in possible_neighbours_for_word(next_node) if w in dictionary_set and w not in seen_already]:
            seen_already.add(neighbour)
            queue.put_nowait(neighbour)

            paths[neighbour] = next_node
    return []

if __name__ == '__main__':
    dictionary = read_word_list('word_list.txt')
    path = bfs(sys.argv[1], sys.argv[2], dictionary)
    if not path:
        print "Couldn't find a path"
    pprint.pprint(path)
