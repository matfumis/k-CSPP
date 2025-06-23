import heapq
from solution import Solution


def solve_colour_constrained_dijkstra(graph, source, destination, k):
  weights = [data['weight'] for _, _, data in graph.edges(data=True)]

  min_edge_cost, max_edge_cost = min(weights), max(weights)
  mean_edge_cost = sum(weights) / len(weights)

  penalties_list = [
    0,
    min_edge_cost / 4,
    min_edge_cost / 2,
    min_edge_cost,
    min_edge_cost * 2,
    mean_edge_cost / 4,
    mean_edge_cost / 2,
    mean_edge_cost,
    max_edge_cost
  ]


  for penalty in penalties_list:
    solution = penalised_dijkstra(graph, source, destination, penalty)
    if solution and len(solution.used_colours) <= k:
      return solution, True if penalty == 0 else False

  return None, None


def penalised_dijkstra(graph, source, destination, penalty):
  penalised_distances = {n: float('inf') for n in graph.nodes()}

  used_colours = {n: set() for n in graph.nodes()}

  real_distances = {n: 0 for n in graph.nodes()}

  predecessors = {}

  penalised_distances[source] = 0

  real_distances[source] = 0

  priority_queue = [(0, source)]

  while priority_queue:
    current_distance, current_node = heapq.heappop(priority_queue)

    if current_distance > penalised_distances[current_node]:
      continue

    if current_node == destination:
      break

    for neighbor_node, data in graph[current_node].items():
      weight = data['weight']

      colour = data['colour']

      neighbor_node_penalty = 0 if colour in used_colours[current_node] else penalty

      actual_distance = current_distance + weight + neighbor_node_penalty

      if actual_distance < penalised_distances[neighbor_node]:
        penalised_distances[neighbor_node] = actual_distance

        predecessors[neighbor_node] = current_node

        real_distances[neighbor_node] = real_distances[current_node] + weight

        used_colours[neighbor_node] = used_colours[current_node].copy()

        used_colours[neighbor_node].add(colour)

        heapq.heappush(priority_queue, (actual_distance, neighbor_node))

  if penalised_distances[destination] == float('inf'):
    return None, None, None

  solution = Solution()
  destination_node = destination
  path = []

  while destination_node != source:
    path.append(destination_node)
    destination_node = predecessors[destination_node]

  path.append(source)
  path.reverse()

  solution.update_path(path)
  solution.update_used_colours(used_colours[destination])
  solution.update_cost(real_distances[destination])

  return solution