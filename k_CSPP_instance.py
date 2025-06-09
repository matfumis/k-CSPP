from parser import parse_file

class k_CSPP_instance:
  def __init__(self, file_path):
    self.file_path = file_path
    self.graph, self.source, self.destination, self.k = parse_file(file_path)

  def get_parameters(self):
    return self.graph, self.source, self.destination, self.k

  def to_string(self):
    name_instance = self.file_path.split('/')[-1]
    instance_string = (
      f'k-CSPP instance {name_instance}:\n'
      f'  {self.graph}\n'
      f'  Source node: {self.source}\n'
      f'  Destination node: {self.destination}\n'
      f'  k: {self.k}'
    )
    return instance_string