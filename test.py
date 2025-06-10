from k_CSPP_instance import k_CSPP_instance
from reduced_ILP import reduced_ILP_algorithm

file_name_grid_instance = 'instances/SET_B/Grid/B-G1/B-G1_8'
grid_instance = k_CSPP_instance(file_name_grid_instance)

print(f'Solving {grid_instance.to_string()}\n')

reduced_ILP_algorithm(grid_instance)

print('\n\n==========================================================\n\n\n')

file_name_random_instance = 'instances/SET_B/Random/B-R1/B-R1_3'
random_instance = k_CSPP_instance(file_name_random_instance)

print(f'Solving {random_instance.to_string()}\n')

reduced_ILP_algorithm(random_instance)

print('\n\n==========================================================\n\n\n')

file_name_random_instance = 'instances/SET_B/Random/B-R1/B-R1_0'
random_instance = k_CSPP_instance(file_name_random_instance)

print(f'Solving {random_instance.to_string()}\n')

reduced_ILP_algorithm(random_instance)
