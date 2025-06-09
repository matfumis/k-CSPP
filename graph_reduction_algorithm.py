import networkx as nx


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

  return reduced_graph
