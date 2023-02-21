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
    for r in node_ranks:
        if r == len(node_ranks) - 1:
            break
        for u, v in edge_list:
            if u in node_ranks[r] and v in node_ranks[r]:
                continue
            if u in node_ranks[r] and v in node_ranks[r+1]:
                new_edge_list.append((u, v))
            if u in node_ranks[r+1] and v in node_ranks[r]:
                new_edge_list.append((v, u))
                # new_edge_list.append((u, v))
        
    return new_edge_list

def count_edge_length(graph):
    return len(graph)
