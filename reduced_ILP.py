from colour_constrained_dijkstra_algorithm import solve_colour_constrained_dijkstra
from formulation import solve_k_cspp_formulation
from graph_reduction_algorithm import perform_graph_reduction
import time
from utils.result import Result

def perform_reduced_ILP_algorithm(instance):
  start_time = time.time()
  graph, source, destination, k = instance.get_parameters()

  print(f'Solving {instance.to_string()}\n')

  print('Performing Colour Constrained Dijkstra Algorithm...')
  start_time_ccda = time.time()
  initial_solution, is_best_tour = solve_colour_constrained_dijkstra(graph, source, destination, k)
  time_ccda = round(time.time() - start_time_ccda, 2)

  if not initial_solution:
    print(f'No solution found with at most {k} colours\n')
    print(f'Total time: {time_ccda}\n')
    return Result(None, time_ccda, None, None, None, None, None, None, None)

  print(f'Initial solution found in {time_ccda} seconds.\n{initial_solution.to_string()}\n')

  if is_best_tour:
    print('Initial solution is the optimal solution.\n')
    print(f'Total time: {time_ccda} seconds\n')
    return Result(initial_solution, time_ccda, 0, 0, time_ccda, 0, -1, -1, -1) # -1 means graph reduction not performed


  print('Performing Graph Reduction algorithm...')
  start_time_reduction_algorithm = time.time()
  #reduced_graph, more_reduced_graph = perform_graph_reduction(graph, source, destination, initial_solution)
  reduced_graph = perform_graph_reduction(graph, source, destination, initial_solution)
  time_reduction_algorithm = round(time.time() - start_time_reduction_algorithm, 2)
  removed_nodes_percentage = (1 - len(reduced_graph.nodes) / len(graph.nodes)) * 100
  removed_arcs_percentage = (1 - len(reduced_graph.edges) / len(graph.edges)) * 100

  print(f'Reduced Graph: {reduced_graph}:\n  - removed {removed_nodes_percentage}% of nodes\n  - removed {removed_arcs_percentage}% of arcs \n')

  #more_removed_arcs_percentage = (1 - len(more_reduced_graph.edges) / len(reduced_graph.edges)) * 100

  #print(f'Removed {more_removed_arcs_percentage}% of arcs from Reduced Graph\n')

  #print(f'More Reduced Graph: {more_reduced_graph}:\n')


  print('Solving formulation...')
  start_time_formulation = time.time()
  optimal_solution = solve_k_cspp_formulation(reduced_graph, source, destination, k)
  time_solver_formulation = round(time.time() - start_time_formulation, 2)

  total_time = round(time.time() - start_time, 2)

  if not optimal_solution:
    print('No optimal solution found\n')
    return Result(None, total_time, None, None, None, None, None, None, None)

  print(f'Optimal solution found: \n{optimal_solution.to_string()}\n')

  gap = compute_gap(initial_solution, optimal_solution)
  print(f'Gap from initial solution to optimal solution: {gap}\n')

  print(f'Total time: {total_time} seconds\n')

  # return Result(optimal_solution, time_ccda, time_reduction_algorithm, time_solver_formulation, total_time, gap, removed_nodes_percentage, removed_arcs_percentage, more_removed_arcs_percentage)
  return Result(optimal_solution, time_ccda, time_reduction_algorithm, time_solver_formulation, total_time, gap, removed_nodes_percentage, removed_arcs_percentage, None)


def compute_gap(initial_solution, optimal_solution):
  return 100 * (initial_solution.cost - optimal_solution.cost) / optimal_solution.cost
