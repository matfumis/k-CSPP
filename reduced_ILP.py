from colour_constrained_dijkstra_algorithm import solve_colour_constrained_dijkstra
from formulation import solve_k_cspp_formulation
from graph_reduction_algorithm import graph_reduction
import time

def reduced_ILP_algorithm(instance):
  start_time = time.time()
  graph, source, destination, k = instance.get_parameters()

  print(f'Solving {instance.to_string()}\n')

  print('Performing Colour Constrained Dijkstra Algorithm...')
  initial_solution, is_best_tour = solve_colour_constrained_dijkstra(graph, source, destination, k)

  time_ccda = round(time.time() - start_time, 2)

  if not initial_solution:
    print(f'No solution found with at most {k} colours\n')
    print(f'Total time: {time_ccda}\n')
    return None, time_ccda, None, None, None, None

  print(f'Initial solution found in {time_ccda} seconds.\n{initial_solution.to_string()}\n')

  if is_best_tour:
    print('Initial solution is the optimal solution.\n')
    print(f'Total time: {time_ccda} seconds\n')
    return initial_solution, time_ccda, time_ccda, 0, -1 , -1 # -1 means graph reduction not performed


  print('Performing Graph Reduction algorithm...')
  reduced_graph = graph_reduction(graph, source, destination, initial_solution.cost)
  removed_nodes_percentage = (1 - len(reduced_graph.nodes) / len(graph.nodes)) * 100
  removed_arcs_percentage = (1 - len(reduced_graph.edges) / len(graph.edges)) * 100


  print(f'Reduced Graph: {reduced_graph}:\n  - removed {removed_nodes_percentage}% of nodes\n  - removed {removed_arcs_percentage}% of arcs \n')


  print('Solving formulation...')
  optimal_solution = solve_k_cspp_formulation(reduced_graph, source, destination, k)

  total_time = round(time.time() - start_time, 2)

  if not optimal_solution:
    print('No optimal solution found\n')
    return None, total_time, None, None, None, None

  print(f'Optimal solution found: \n{optimal_solution.to_string()}\n')

  gap = compute_gap(initial_solution, optimal_solution)
  print(f'Gap from initial solution to optimal solution: {gap}\n')

  print(f'Total time: {total_time} seconds\n')

  return optimal_solution, time_ccda, total_time, gap, removed_nodes_percentage, removed_arcs_percentage


def compute_gap(initial_solution, optimal_solution):
  return 100 * (initial_solution.cost - optimal_solution.cost) / optimal_solution.cost
