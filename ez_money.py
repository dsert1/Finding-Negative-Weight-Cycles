import math
import pprint


def ez_money(D):
    """Find a sequence of commodities to exchange to get more of that
    commodity.

    Args:
        D: A list of deals, each deal is of the form (A, x, B, y)
           which means someone will give you y of B for x of A.

    Returns:
        None if no such opputunity is found, otherwise a List of
        commodities to exchange.
    """
    adj, all_nodes = create_adjacency_list(D)
    # arbitrary as long as we get more

    infinity = float('inf')
    d = {v: infinity for v in all_nodes}
    parent = {v: 'S' for v in all_nodes}

    # init Supernode
    adj['S'] = {node:0 for node in all_nodes}
    parent['S'] = 'S'
    d['S'] = 0
    all_nodes.add('S')
    # print(adj)

    # construct shortest path in rounds
    # adj (dict) --> {node_A (string): {node_B: weight}}
    V = len(adj)
    for _ in range(V - 1):  # iterations of Bellman Ford
        for commodity in all_nodes:  # think about the new adj, and nodes
            for child_node in adj[commodity]:
                if d[commodity] + adj[commodity][child_node] < d[child_node]:  # relax
                    d[child_node] = d[commodity] + adj[commodity][child_node]
                    parent[child_node] = commodity

    print('parent: ', parent)

    # check for negative weight cycle accessible from s
    # only 1 more iteration needed
    for commodity in all_nodes:
        for child_node in adj[commodity]:
            if d[commodity] + adj[commodity][child_node] < d[child_node]:  # relax
                print('\n\n**\n\n: ', parent)
                cyc = find_cycle(parent, child_node) # not sure
                # print('cyc: ', cyc)
                if cyc:
                    return cyc
    return None


def find_cycle(parent_dict, node):
    '''returns a negative weight cycle'''
    seen = set()
    while node not in seen and node != None:
        seen.add(node)  # no cycle found
        node = parent_dict[node]  # changing current node


    # backtracking from node
    # looks similar, but use list
    start_node = node
    cycle = [node]

    node = parent_dict[start_node]
    seen = set()
    while node != start_node and node not in seen:
        seen.add(node)
        cycle.append(node)
        node = parent_dict[node]
        print(node)
        if node == None:
            break

    return cycle[::-1]
# reversed() is an iterator

# collections defaultdict could make 75-80 a one-liner
def create_adjacency_list(input_list):
    '''parses a list of input items'''
    adj = {}
    nodes = set()

    # print('input: ', input_list)
    for tup in input_list:
        A, x, B, y = tup
        weight = -math.log2(y/x)

        if A in adj:
            adj[A][B] = weight
        else:
            adj[A] = {}
        if B not in adj:
            adj[B] = {}

        adj[A][B] = weight

        nodes.add(A)
        nodes.add(B)

    return adj, nodes


if __name__ == '__main__':
    pp = pprint.PrettyPrinter()
    inp = [('laptop', 1, 'shirt', 5), ('alarm clock', 2, 'fishbowl', 5), ('alarm clock', 15, 'laptop', 1), ('frisbee', 1, 'textbook', 2), ('textbook', 1, 'alarm clock', 2), ('alarm clock', 2, 'textbook', 1), ('laptop', 1, 'shoe', 5), ('textbook', 1, 'laptop', 5)]
#     inp = [("laptop", 5, "TV", 3), ("TV", 1, "shirt", 10), ("shirt", 3, "laptop", 5)]
#     pp.pprint(create_adjacency_list(inp))
# print('***\n\n***')
#     pp.pprint(create_adjacency_list(inp))
# print(u)

    print(ez_money(inp))

