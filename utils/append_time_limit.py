import time
import os
from natsort import natsorted

def append_time_limit_ilp(set_type, instance_type):
  results = f'results/SET_{set_type}/{instance_type}'

  for directory in natsorted(os.listdir(results)):
    os.makedirs(os.path.join(results, directory), exist_ok=True)

    for file in natsorted(os.listdir(os.path.join(results, directory))):
      output_file = os.path.join(results, directory, file)

      with open(output_file, 'r') as f:
        lines = f.readlines()

      if any(l.startswith('Time complete formulation:') for l in lines):
        continue

      with open(output_file, 'a') as f:
        f.write("\n"+"=" * 81 + "\n")
        f.write("Time complete formulation: time limit exceeded (> 10 min)\n")


def main():
  append_time_limit_ilp('A', 'Random')
  append_time_limit_ilp('B', 'Random')

if __name__ == '__main__':
  main()