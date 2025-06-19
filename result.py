class result:
  def __init__(self, initial_solution, time_ccda, time_reduction_algorithm, time_formulation, total_time, gap,
               removed_nodes_percentage, removed_arcs_percentage, more_removed_arcs_percentage):
        self.initial_solution = initial_solution
        self.time_ccda = time_ccda
        self.time_reduction_algorithm = time_reduction_algorithm
        self.time_formulation = time_formulation
        self.total_time = total_time
        self.gap = gap
        self.removed_nodes_percentage = removed_nodes_percentage
        self.removed_arcs_percentage = removed_arcs_percentage
        self.more_removed_arcs_percentage = more_removed_arcs_percentage


  def to_string(self):
    if not self.initial_solution:
      return 'No solution found\nTime Colour Constrained Dijkstra Algorithm: ' + str(self.time_ccda)
    else:
      return (
        self.initial_solution.to_string() +
        '\nTime Colour Constrained Dijkstra Algorithm: ' + str(self.time_ccda) +
        '\nTime Reduction Algorithm: ' + str(self.time_reduction_algorithm) +
        '\nTime Formulation: ' + str(self.time_formulation) +
        '\nTotal time: ' + str(self.total_time) +
        '\nGap: ' + str(self.gap) +
        '\nRemoved nodes percentage: ' + str(self.removed_nodes_percentage) +
        '\nRemoved arcs percentage: ' + str(self.removed_arcs_percentage) +
        '\nMore Removed arcs percentage: ' + str(self.more_removed_arcs_percentage)
      )