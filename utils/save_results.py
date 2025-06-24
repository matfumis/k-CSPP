import os

from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, MaxNLocator
from natsort import natsorted
import numpy as np

def read_results_rilp(set_type, instance_type):
  results = 'results/SET_' + set_type + '/' + instance_type
  mean_computational_times_ccda = []
  mean_computational_times_reduction_algorithm = []
  mean_computational_times_formulation = []
  mean_computational_total_times = []
  mean_gaps = []
  mean_removed_nodes_percentages = []
  mean_removed_arcs_percentages = []
  mean_more_removed_arcs_percentages = []
  mean_costs = []
  tot_opt_found = []


  for directory in natsorted(os.listdir(results)):
    computational_times_ccda = []
    computational_times_reduction_algorithm = []
    computational_times_formulation = []
    computational_times = []
    gaps = []
    removed_nodes_percentages = []
    removed_arcs_percentages = []
    more_removed_arcs_percentages = []
    costs = []
    opt_found = []

    for file in natsorted(os.listdir(os.path.join(results, directory))):
      file_to_read = os.path.join(results, directory, file)

      with open(file_to_read, 'r') as f:
        lines = f.readlines()

      solution_found = True

      for line in lines:

        if 'Time Colour Constrained Dijkstra Algorithm' in line:
          time_ccda = float(line.split(':')[1].strip())
          computational_times_ccda.append(time_ccda)
        elif 'Time Reduction Algorithm' in line:
          time_reduction_algorithm = float(line.split(':')[1].strip())
          computational_times_reduction_algorithm.append(time_reduction_algorithm)
        elif 'Time Formulation' in line:
          time_formulation = float(line.split(':')[1].strip())
          computational_times_formulation.append(time_formulation)
        elif 'Total time' in line:
          total_time = float(line.split(':')[1].strip())
          computational_times.append(total_time)
        elif 'Gap' in line:
          gap = float(line.split(':')[1].strip())
          gaps.append(gap)
        elif 'Removed nodes percentage' in line:
          removed_nodes_percentage = float(line.split(':')[1].strip())
          if removed_nodes_percentage != -1:
            removed_nodes_percentages.append(removed_nodes_percentage)
        elif 'Removed arcs percentage' in line and 'More' not in line:
          removed_arcs_percentage = float(line.split(':')[1].strip())
          if removed_arcs_percentage != -1:
            removed_arcs_percentages.append(removed_arcs_percentage)
        elif 'More Removed arcs percentage' in line:
          more_removed_arcs_percentage = float(line.split(':')[1].strip())
          if more_removed_arcs_percentage != -1:
            more_removed_arcs_percentages.append(more_removed_arcs_percentage)
        elif '- cost' in line:
          cost = float(line.split(':')[1].strip())
          costs.append(cost)
        elif 'No solution found' in line:
          solution_found = False

      if solution_found:
        opt_found.append(1)


    mean_computational_times_ccda.append(np.mean(computational_times_ccda))
    mean_computational_times_reduction_algorithm.append(np.mean(computational_times_reduction_algorithm))
    mean_computational_times_formulation.append(np.mean(computational_times))
    mean_computational_total_times.append(np.mean(computational_times))
    mean_gaps.append(np.mean(gaps))
    mean_removed_nodes_percentages.append(np.mean(removed_nodes_percentages))
    mean_removed_arcs_percentages.append(np.mean(removed_arcs_percentages))
    mean_more_removed_arcs_percentages.append(np.mean(more_removed_arcs_percentages))
    mean_costs.append(np.mean(costs))
    tot_opt_found.append(np.sum(opt_found))

  return (mean_computational_times_ccda, mean_computational_times_reduction_algorithm,
          mean_computational_times_formulation,
          mean_computational_total_times, mean_gaps, mean_removed_nodes_percentages, mean_removed_arcs_percentages,
          mean_more_removed_arcs_percentages, mean_costs, tot_opt_found)


def read_results_ilp(set_type, instance_type):
  results = 'results/SET_' + set_type + '/' + instance_type
  mean_computational_times_complete_formulation = []

  for directory in natsorted(os.listdir(results)):
    computational_times_complete_formulation = []

    for file in natsorted(os.listdir(os.path.join(results, directory))):
      file_to_read = os.path.join(results, directory, file)

      with open(file_to_read, 'r') as f:
        lines = f.readlines()

      for line in lines:
        if 'Time complete formulation' in line:
          if 'time limit exceeded' in line:
            computational_times_complete_formulation.append(600)
          else:
            time_complete_formulation = float(line.split(':')[1].strip())
            computational_times_complete_formulation.append(time_complete_formulation)

    mean_computational_times_complete_formulation.append(np.mean(computational_times_complete_formulation))

  return mean_computational_times_complete_formulation

def save_image(list_A, list_B, instance_type, image_name):
  images_base = 'images'
  dir_path = os.path.join(images_base, instance_type)
  os.makedirs(dir_path, exist_ok=True)

  n = len(list_A)
  x = list(range(n))
  labels = [f"{instance_type}{i + 1}" for i in range(n)]

  fig, ax = plt.subplots(figsize=(8, 5))
  ax.plot(x, list_A, marker='o', linestyle='-', label='Set A')
  ax.plot(x, list_B, marker='o', linestyle='-', label='Set B')

  ax.xaxis.set_major_locator(MultipleLocator(1))
  ax.set_xticks(x)
  ax.set_xticklabels(labels, rotation=45, ha='right')

  ax.yaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
  ax.set_xlabel('Instance')
  ax.set_ylabel(image_name)
  ax.set_title(f"{image_name} ({'Grid' if instance_type == 'G' else 'Random'})")
  ax.legend()
  fig.tight_layout()

  # Save and close
  filename = os.path.join(dir_path, f"{image_name}_{instance_type}.png")
  fig.savefig(filename)
  plt.close(fig)


def save_mean_results(set_type, instance_type, tot_opt, costs, formulation_times_ilp, formulation_times_rilp, filename):

  os.makedirs('results/SET_' + set_type[0], exist_ok=True)

  ilp_path = os.path.join('results/SET_' + set_type[0], filename)
  with open(ilp_path, 'w') as f:
    f.write('Costs:\n')
    for i in range(len(costs)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(costs[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write("#Opt:\n")
    for i in range(len(tot_opt)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(tot_opt[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")

    f.write('\nILP:\n')
    f.write('\nFormulation times:\n\n')
    for i in range(len(formulation_times_ilp)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(formulation_times_ilp[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write("\nRILP:\n\n")
    f.write('Formulation times:\n\n')
    for i in range(len(formulation_times_rilp)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(formulation_times_rilp[i]) + "\n")


def main():
  (mean_computational_times_ccda_A_Grid, mean_computational_times_reduction_algorithm_A_Grid,
   mean_computational_times_formulation_A_Grid,
   mean_computational_times_A_Grid, mean_gaps_A_Grid, mean_removed_nodes_percentages_A_Grid,
   mean_removed_arcs_percentages_A_Grid, mean_more_removed_arcs_percentages_A_Grid,
   mean_costs_A_Grid, tot_opt_found_A_Grid) = read_results_rilp('A', 'Grid')

  (mean_computational_times_ccda_B_Grid, mean_computational_times_reduction_algorithm_B_Grid,
   mean_computational_times_formulation_B_Grid,
   mean_computational_times_B_Grid, mean_gaps_B_Grid, mean_removed_nodes_percentages_B_Grid,
   mean_removed_arcs_percentages_B_Grid, mean_more_removed_arcs_percentages_B_Grid,
   mean_costs_B_Grid, tot_opt_found_B_Grid) = read_results_rilp('B', 'Grid')

  (mean_computational_times_ccda_A_Random, mean_computational_times_reduction_algorithm_A_Random,
   mean_computational_times_formulation_A_Random, mean_computational_times_A_Random, mean_gaps_A_Random,
   mean_removed_nodes_percentages_A_Random, mean_removed_arcs_percentages_A_Random,
   mean_more_removed_arcs_percentages_A_Random, mean_costs_A_Random, tot_opt_found_A_Random) = read_results_rilp('A', 'Random')

  (mean_computational_times_ccda_B_Random, mean_computational_times_reduction_algorithm_B_Random,
   mean_computational_times_formulation_B_Random, mean_computational_times_B_Random, mean_gaps_B_Random,
   mean_removed_nodes_percentages_B_Random, mean_removed_arcs_percentages_B_Random,
   mean_more_removed_arcs_percentages_B_Random, mean_costs_B_Random, tot_opt_found_B_Random) = read_results_rilp('B', 'Random')

  mean_computational_times_complete_formulation_A_Grid = read_results_ilp('A', 'Grid')
  mean_computational_times_complete_formulation_A_Random = read_results_ilp('A', 'Random')
  mean_computational_times_complete_formulation_B_Grid = read_results_ilp('B', 'Grid')
  mean_computational_times_complete_formulation_B_Random = read_results_ilp('B', 'Random')

  # save_image(mean_computational_times_ccda_A_Grid, mean_computational_times_ccda_B_Grid, 'G', 'mean_computational_times_ccda')
  # save_image(mean_computational_times_reduction_algorithm_A_Grid, mean_computational_times_reduction_algorithm_B_Grid, 'G', 'mean_computational_times_reduction_algorithm')
  # save_image(mean_computational_times_formulation_A_Grid, mean_computational_times_formulation_B_Grid, 'G', 'mean_computational_times_formulation_reduced')
  # save_image(mean_computational_times_A_Grid, mean_computational_times_B_Grid, 'G', 'mean_computational_total_times_')
  # save_image(mean_gaps_A_Grid, mean_gaps_B_Grid, 'G', 'mean_gaps')
  # save_image(mean_removed_nodes_percentages_A_Grid, mean_removed_nodes_percentages_B_Grid, 'G', 'mean_removed_nodes_percentage')
  # save_image(mean_removed_arcs_percentages_A_Grid, mean_removed_arcs_percentages_B_Grid, 'G', 'mean_removed_arcs_percentage')
  # save_image(mean_more_removed_arcs_percentages_A_Grid, mean_more_removed_arcs_percentages_B_Grid, 'G', 'mean_more_removed_arcs_percentage')
  #
  # save_image(mean_computational_times_ccda_A_Random, mean_computational_times_ccda_B_Random, 'R', 'mean_computational_times_ccda')
  # save_image(mean_computational_times_reduction_algorithm_A_Random, mean_computational_times_reduction_algorithm_B_Random,'R', 'mean_computational_times_reduction_algorithm')
  # save_image(mean_computational_times_formulation_A_Random, mean_computational_times_formulation_B_Random, 'R','mean_computational_times_formulation_reduced')
  # save_image(mean_computational_times_A_Random, mean_computational_times_B_Random, 'R', 'mean_computational_times')
  # save_image(mean_gaps_A_Random, mean_gaps_B_Random, 'R', 'mean_gaps')
  # save_image(mean_removed_nodes_percentages_A_Random, mean_removed_nodes_percentages_B_Random, 'R', 'mean_removed_nodes_percentage')
  # save_image(mean_removed_arcs_percentages_A_Random, mean_removed_nodes_percentages_B_Random, 'R', 'mean_removed_arcs_percentage')
  # save_image(mean_more_removed_arcs_percentages_A_Random, mean_more_removed_arcs_percentages_B_Random, 'R', 'mean_more_removed_arcs_percentage')

  save_mean_results('A', 'Grid', tot_opt_found_A_Grid, mean_costs_A_Grid, mean_computational_times_complete_formulation_A_Grid, mean_computational_times_formulation_A_Grid, 'mean_results_A_Grid.txt')
  save_mean_results('A', 'Random', tot_opt_found_A_Random, mean_costs_A_Random, mean_computational_times_complete_formulation_A_Random, mean_computational_times_formulation_A_Random, 'mean_results_A_Random.txt')
  save_mean_results('B', 'Grid', tot_opt_found_B_Grid, mean_costs_B_Grid, mean_computational_times_complete_formulation_B_Grid, mean_computational_times_formulation_B_Grid, 'mean_results_B_Grid.txt')
  save_mean_results('B', 'Random', tot_opt_found_B_Random, mean_costs_B_Random, mean_computational_times_complete_formulation_B_Random, mean_computational_times_formulation_B_Random, 'mean_results_B_Random.txt')

if __name__ == '__main__':
  main()