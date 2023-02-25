import glob
import xml.etree.ElementTree as ET
from collections import deque

def read_files(node_threshold = 11, base_path = "../rome/"):
    # print(glob.glob(base_path + "/*.graphml"))
    # print(base_path + "/*.graphml")
    for filename in glob.glob(base_path + "/*.graphml"):
    # Open the file and read its contents
        with open(filename, "r") as f:
            content = f.read()

            # Parse the GraphML file using ElementTree
            root = ET.fromstring(content)

            # Find the <graph> element using the tag name only
            graph = root.findall("graph")[0]

            # Extract the list of nodes
            nodes = graph.findall("node")

            # Filter for graphs with less than 10 nodes
            
            if len(nodes) <= node_threshold:
                # count = count+1
                # Extract the list of edges
                edges = graph.findall("edge")
                node_dict = {node.attrib["id"]: i for i, node in enumerate(nodes)}
                edge_list = [(node_dict[edge.attrib["source"]], node_dict[edge.attrib["target"]]) for edge in edges]

                yield {'filename': filename, 'graph': graph, 'edge_list': edge_list}

def count_edge_crossings(graph, node_order):
    crossings = 0
    # print("node order", node_order)
    
    for i in range(len(node_order)):
        for j in range(i + 1, len(node_order)):
            a, b = node_order[i], node_order[j]

            for u, v in graph:
                if u in a and v in b:
                    for u2, v2 in graph:
                        if u2 in a and v2 in b:
                            if u == u2 and v == v2:
                                continue
                            if a.index(u) < a.index(u2) and b.index(v) > b.index(v2):
                                # print(u, v, u2, v2)
                                crossings += 1
                            elif a.index(u) > a.index(u2) and b.index(v) < b.index(v2):
                                # print(u, v, u2, v2)
                                crossings += 1
                        elif u2 in b and v2 in a:
                            if u == u2 and v == v2:
                                continue
                            if a.index(u) > a.index(v2) and b.index(v) < b.index(u2):
                                # print(u, v, u2, v2)
                                crossings += 1
                            elif a.index(u) < a.index(v2) and b.index(v) > b.index(u2):
                                # print(u, v, u2, v2)
                                crossings += 1
                elif u in b and v in a:
                    for u2, v2 in graph:
                        if u2 in a and v2 in b:
                            if u == u2 and v == v2:
                                continue
                            if a.index(v) < a.index(u2) and b.index(u) > b.index(v2):
                                # print(u, v, u2, v2)
                                crossings += 1
                            elif a.index(v) > a.index(u2) and b.index(u) < b.index(v2):
                                # print(u, v, u2, v2)
                                crossings += 1
                        elif u2 in b and v2 in a:
                            if u == u2 and v == v2:
                                continue
                            if a.index(v) > a.index(v2) and b.index(u) < b.index(u2):
                                # print(u, v, u2, v2)
                                crossings += 1
                            elif a.index(v) < a.index(v2) and b.index(u) > b.index(u2):
                                # print(u, v, u2, v2)
                                crossings += 1
    
    return crossings/2
    
def bfs(graph, start_node):
    visited = {start_node}
    queue = deque([(start_node, 0)])
    node_ranks = {}

    while queue:
        current_node, depth = queue.popleft()

        if depth not in node_ranks:
            node_ranks[depth] = [current_node]
        else:
            node_ranks[depth].append(current_node)

        for edge in graph:
            source, target = edge
            if source == current_node and target not in visited:
                visited.add(target)
                queue.append((target, depth + 1))
            elif target == current_node and source not in visited:
                visited.add(source)
                queue.append((source, depth + 1))

    return node_ranks

def cleanup_edges(edge_list, node_ranks):
    new_edge_list = []

    for u, v in edge_list:
        # print(u, v)

        # find key based on item
        u_key = [k for k, v in node_ranks.items() if u in v][0]
        v_key = [k for k, val in node_ranks.items() if v in val][0]

        if u_key == v_key:
            continue

        if u_key < v_key:
            new_edge_list.append((u, v))
        else:
            new_edge_list.append((v, u))
        
    return new_edge_list

def count_edge_length(edge_list, node_ranks):
    total = 0
    for u, v in edge_list:
        # find key based on dictionary item
        rank_u = [k for k, val in node_ranks.items() if u in val][0]
        rank_v = [k for k, val in node_ranks.items() if v in val][0]
        # print(u, ":", rank_u, ",", v, ":", rank_v)
        total += abs(rank_u - rank_v)

    return total
