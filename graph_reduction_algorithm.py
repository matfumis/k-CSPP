import networkx as nx


def perform_graph_reduction(graph, source, destination, initial_solution):

  reduced_graph = perform_first_reduction(graph, source, destination, initial_solution)
  # even_more_reduced_graph = perform_extra_edges_reduction(reduced_graph, source, destination, initial_solution)

  #return reduced_graph, even_more_reduced_graph
  return reduced_graph


def perform_first_reduction(graph, source, destination, initial_solution):
  distances_from_source = nx.single_source_dijkstra_path_length(graph, source, weight='weight')
  distances_to_destination = nx.single_source_dijkstra_path_length(graph, destination, weight='weight')

  nodes_to_remove = []
  for node in graph.nodes():

    if node in initial_solution.path:
      continue

    distance_from_source_to_node = distances_from_source.get(node, float('inf'))
    distance_to_destination = distances_to_destination.get(node, float('inf'))

    if (distance_from_source_to_node == float('inf') or distance_to_destination == float('inf') or
        (distance_from_source_to_node + distance_to_destination) >= initial_solution.cost):
      nodes_to_remove.append(node)

  reduced_graph = graph.copy()
  reduced_graph.remove_nodes_from(nodes_to_remove)

  return reduced_graph



def perform_extra_edges_reduction(reduced_graph, source, destination, initial_solution):
  even_more_reduced_graph = reduced_graph.copy()

  distances_from_source = nx.single_source_dijkstra_path_length(reduced_graph, source, weight='weight')
  distances_to_destination = nx.single_source_dijkstra_path_length(reduced_graph, destination, weight='weight')

  edges_to_remove = []
  edges_counter = {}

  for node in reduced_graph.nodes():
    node_neighbors = reduced_graph.neighbors(node)
    for neighbor in node_neighbors:

      distance_from_source_to_node = distances_from_source.get(node, float('inf'))
      distance_from_node_to_neighbor = reduced_graph[node][neighbor].get('weight', float('inf'))
      distance_from_neighbor_to_destination = distances_to_destination.get(neighbor, float('inf'))

      total_distance = distance_from_source_to_node + distance_from_node_to_neighbor + distance_from_neighbor_to_destination

      edge_direct = (node, neighbor)
      edge_reverse = (neighbor, node)

      if total_distance >= initial_solution.cost:
        edges_counter[edge_direct] = edges_counter.get(edge_direct, 0) + 1
        edges_counter[edge_reverse] = edges_counter.get(edge_reverse, 0) + 1

        if edges_counter[edge_direct] == 2:
          edges_to_remove.append((node, neighbor))

  even_more_reduced_graph.remove_edges_from(edges_to_remove)

  return even_more_reduced_graph