import networkx as nx

def parse_file(path):
  with open(path) as f:
    number_of_nodes, k, source, destination = map(int, f.readline().split())
    degrees = [int(f.readline()) for _ in range(number_of_nodes)]
    graph = nx.Graph()
    for i in range(1, number_of_nodes + 1):
      for _ in range(degrees[i-1]):
        node, weight, colour = map(int, f.readline().split())
        graph.add_edge(i, node, weight=weight, colour=colour)

  return graph, source, destination, k