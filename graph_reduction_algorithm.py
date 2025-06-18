import copy

import networkx as nx
from networkx.classes import neighbors


def graph_reduction(graph, source, destination, upper_bound) -> nx.Graph:
  """
  Perform the Graph Reduction Algorithm (GRA) on an undirected, weighted graph G.

  Parameters
  ----------
  graph : nx.Graph
      An undirected graph where each edge has a 'weight' attribute (numeric).
  source : int
      The source node ID.
  destination : int
      The destination node ID.
  upper_bound : float
      An upper bound on the length of any feasible source→destination path
      (for example, the cost returned by a heuristic such as CCDA).

  Returns
  -------
  reduced_graph : nx.Graph
      A subgraph of G obtained by removing all nodes node ∉ {source, destination}
      for which dist(source→node) + dist(node→destination) > ub.
      If node is unreachable from source or cannot reach destination, we treat
      its distance as ∞ and thus remove it (unless node is source or destination).
  """
  # 1) Compute single‐source distances from `source` to every other node (weight='weight').
  distances_from_source = nx.single_source_dijkstra_path_length(graph, source, weight='weight')

  # 2) Compute single‐source distances from `destination` to every other node.
  #    Since G is undirected, this is equivalent to distances node→destination.
  distances_to_destination = nx.single_source_dijkstra_path_length(graph, destination, weight='weight')


  # 3) Identify all nodes that must be removed.  We keep source/destination no matter what.
  nodes_to_remove = []
  for node in graph.nodes():

    if node == source or node == destination:
      continue

    distance_from_source = distances_from_source.get(node, float('inf'))
    distance_to_destination = distances_to_destination.get(node, float('inf'))

    # If either is ∞, or if distance_from_source + distance_to_destination > upper bound, we remove node
    if distance_from_source == float('inf') or distance_to_destination == float('inf') or (distance_from_source + distance_to_destination) > upper_bound:
      nodes_to_remove.append(node)

  # 4) Create a copy of G, remove all flagged nodes
  reduced_graph = graph.copy()
  reduced_graph.remove_nodes_from(nodes_to_remove)


  even_more_reduced_graph = reduced_graph.copy()

  #distances_from_source = nx.single_source_dijkstra_path_length(reduced_graph, source, weight='weight')
  #distances_to_destination = nx.single_source_dijkstra_path_length(reduced_graph, destination, weight='weight')

  edges_to_remove = []

  edges_counter = {}
  for node in reduced_graph.nodes():
    node_neighbors = reduced_graph.neighbors(node)
    for neighbor in node_neighbors:

      distance_from_source = distances_from_source.get(node, float('inf'))
      distance_to_neighbor = reduced_graph[node][neighbor].get('weight', float('inf'))
      distance_from_neighbor_to_destination = distances_to_destination.get(neighbor, float('inf'))

      total_distance = distance_from_source + distance_to_neighbor + distance_from_neighbor_to_destination

      edge_direct = (node, neighbor)
      edge_reverse = (neighbor, node)
      if total_distance > upper_bound:
        if edges_counter.get(edge_direct, None) is None:
          edges_counter[edge_direct] = 1
          edges_counter[edge_reverse] = 1
        elif edges_counter.get(edge_reverse, None) is not None:
          edges_counter[edge_direct] += 1
          edges_counter[edge_reverse] += 1
        if edges_counter[edge_direct] is not None and edges_counter[edge_direct] == 2:
          edges_to_remove.append((node, neighbor))

  even_more_reduced_graph.remove_edges_from(edges_to_remove)

  return even_more_reduced_graph
