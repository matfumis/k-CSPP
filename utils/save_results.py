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
  tot_opt_found_formulations = []
  tot_opt_found_ccda = []

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
    opt_found_formulations = []
    opt_found_ccda = []

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
          if gap == 0 or gap == 0.0:
            opt_found_ccda.append(1)
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
        opt_found_formulations.append(1)

    mean_computational_times_ccda.append(np.mean(computational_times_ccda))
    mean_computational_times_reduction_algorithm.append(np.mean(computational_times_reduction_algorithm))
    mean_computational_times_formulation.append(np.mean(computational_times))
    mean_computational_total_times.append(np.mean(computational_times))
    mean_gaps.append(np.mean(gaps))
    mean_removed_nodes_percentages.append(np.mean(removed_nodes_percentages))
    mean_removed_arcs_percentages.append(np.mean(removed_arcs_percentages))
    mean_more_removed_arcs_percentages.append(np.mean(more_removed_arcs_percentages))
    mean_costs.append(np.mean(costs))
    tot_opt_found_formulations.append(np.sum(opt_found_formulations))
    tot_opt_found_ccda.append(np.sum(opt_found_ccda))

  return (mean_computational_times_ccda, mean_computational_times_reduction_algorithm,
          mean_computational_times_formulation,
          mean_computational_total_times, mean_gaps, mean_removed_nodes_percentages, mean_removed_arcs_percentages,
          mean_more_removed_arcs_percentages, mean_costs, tot_opt_found_formulations, tot_opt_found_ccda)


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
  ax.plot(x, list_A, marker='o', linestyle='None', markersize=10, label='Set A')
  ax.plot(x, list_B, marker='o', linestyle='None', markersize=10, label='Set B')

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


def read_new_results(set_type, instance_type):
  results = 'results/SET_' + set_type + '/' + instance_type
  mean_rilp_formulation_no_extra = []

  for directory in natsorted(os.listdir(results)):
    rilp_formulation_no_extra = []

    for file in natsorted(os.listdir(os.path.join(results, directory))):
      file_to_read = os.path.join(results, directory, file)
      with open(file_to_read, 'r') as f:
        lines = f.readlines()

        is_taken = False

        for line in lines:
          if 'Removed nodes percentage:' in line:
            value = float(line.split(':')[1].strip())
            if value >= 0:
              is_taken = True
          if 'RILP Time NO EXTRA REDUCTION' in line:
            if is_taken:
              time = float(line.split(':')[1].strip())
              rilp_formulation_no_extra.append(time)

    mean_rilp_formulation_no_extra.append(np.mean(rilp_formulation_no_extra))
  return mean_rilp_formulation_no_extra




def save_mean_results(set_type, instance_type, times_gra, removed_nodes, removed_arcs, more_removed_arcs, tot_opt_ccda, times_ccda,
                      gaps, tot_opt_formulations, costs, formulation_times_ilp, formulation_times_rilp, filename):
  os.makedirs('results/SET_' + set_type[0], exist_ok=True)

  ilp_path = os.path.join('results/SET_' + set_type[0], filename)
  with open(ilp_path, 'w') as f:
    f.write('Costs:\n')
    for i in range(len(costs)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(costs[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write("\n#Opt formulations:\n")
    for i in range(len(tot_opt_formulations)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(tot_opt_formulations[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write('\n#CCDA:\n')
    f.write('\nComputation times:\n\n')
    for i in range(len(times_ccda)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(times_ccda[i]) + "\n")

    f.write('\nGaps:\n\n')
    for i in range(len(gaps)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(gaps[i]) + "\n")

    f.write('\n#Opt CCDA:\n\n')
    for i in range(len(tot_opt_ccda)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(tot_opt_ccda[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")

    f.write('\nILP:\n')
    f.write('\nILP formulation times:\n\n')
    for i in range(len(formulation_times_ilp)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(formulation_times_ilp[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write("\nRILP:\n\n")
    f.write('\nRILP formulation times:\n\n')
    for i in range(len(formulation_times_rilp)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(formulation_times_rilp[i]) + "\n")

    f.write("\n" + "=" * 81 + "\n")
    f.write("\nGRA:\n\n")
    f.write('Time:\n\n')
    for i in range(len(times_gra)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(times_gra[i]) + "\n")

    f.write('Removed nodes:\n\n')
    for i in range(len(removed_nodes)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(removed_nodes[i]) + "\n")

    f.write("\nRemoved arcs:\n\n")
    for i in range(len(removed_arcs)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(removed_arcs[i]) + "\n")

    f.write("\nMore removed arcs:\n\n")
    for i in range(len(more_removed_arcs)):
      f.write(f"{set_type}-{instance_type[0]}{i + 1}: " + str(more_removed_arcs[i]) + "\n")


def main():
  print(read_new_results('B', 'Grid'))



if __name__ == '__main__':
  main()
