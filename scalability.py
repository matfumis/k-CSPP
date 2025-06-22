import os
import time
from multiprocessing import Process, Queue

from natsort import natsorted
from formulation import solve_k_cspp_formulation
from k_CSPP_instance import k_CSPP_instance
from reduced_ILP import reduced_ILP_algorithm

total_time_file = 'results/total_execution_time.txt'
os.makedirs(os.path.dirname(total_time_file), exist_ok=True)
with open(total_time_file, 'w') as tf:
    tf.write('')


def save_results_rilp(set_type, instance_type):
  instances = 'instances/SET_' + set_type + '/' + instance_type
  results = 'results/SET_' + set_type + '/' + instance_type

  for directory in natsorted(os.listdir(instances)):
    if not os.path.isdir(os.path.join(results, directory)):
      os.makedirs(os.path.join(results, directory))

    for file in natsorted(os.listdir(os.path.join(instances, directory))):
      input_file = os.path.join(instances, directory, file)
      output_file = os.path.join(results, directory, file)

      instance = k_CSPP_instance(input_file)
      result = reduced_ILP_algorithm(instance)

      with open(output_file, 'w') as f:
        f.write(result.to_string())

      print('\n=================================================================================\n\n')

def _worker(graph, source, dest, k, timelimit, q):
  sol = solve_k_cspp_formulation(graph, source, dest, k)
  q.put(sol)


def save_results_ilp(set_type, instance_type):
  instances = f'instances/SET_{set_type}/{instance_type}'
  results = f'results/SET_{set_type}/{instance_type}'

  for directory in natsorted(os.listdir(instances)):
    os.makedirs(os.path.join(results, directory), exist_ok=True)

    for file in natsorted(os.listdir(os.path.join(instances, directory))):
      input_file = os.path.join(instances, directory, file)
      output_file = os.path.join(results, directory, file)

      print('\n' + '=' * 81)
      print(f'Computing: {input_file}\n')

      with open(output_file, 'r') as f:
        lines = f.readlines()
      if lines[0].startswith('No solution found'):
        continue
      if any(l.startswith('Time complete formulation:') for l in lines):
        continue

      # prepara l'istanza
      graph, source, dest, k = k_CSPP_instance(input_file).get_parameters()
      start = time.time()

      time_limit = 600
      # queue per ricevere la soluzione
      q = Queue()
      p = Process(target=_worker, args=(graph, source, dest, k, time_limit, q))
      p.start()
      p.join(timeout=time_limit)  # aspetta al massimo 600s

      # se ancora vivo dopo 600s, lo uccidiamo
      if p.is_alive():
        p.terminate()
        p.join()
        solution = None
        elapsed = round(time.time() - start, 2)
      else:
        # processo terminato in tempo
        try:
          solution = q.get_nowait()
        except:
          solution = None
        elapsed = round(time.time() - start, 2)

      # append sul file
      with open(output_file, 'a') as f:
        f.write("=" * 81 + "\n")
        if solution is None:
          f.write("Time complete formulation: time limit exceeded (> 10 min)\n")
        else:
          f.write(f"Time complete formulation: {elapsed}\n")
          f.write(solution.to_string())


def main():
  #save_results_rilp('A', 'Grid')
  #save_results_rilp('A', 'Random')
  #save_results_rilp('B', 'Grid')
  #save_results_rilp('B', 'Random')

  save_results_ilp('A', 'Grid')
  save_results_ilp('A', 'Random')
  save_results_ilp('B', 'Grid')
  save_results_ilp('B', 'Random')

if __name__ == '__main__':
  start = time.time()
  main()
  total_elapsed = time.time() - start
  # Write total execution time
  with open(total_time_file, 'w') as tf:
    tf.write(f"Total script execution time: {total_elapsed:.4f} seconds\n")
  print(f"Total script execution time: {total_elapsed:.4f} seconds")
