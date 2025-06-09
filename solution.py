class Solution:
  def __init__(self):
    self.path = []
    self.used_colours = []
    self.cost = 0

  def update_cost(self, cost: int):
    self.cost += cost

  def update_used_colours(self, colors):
    self.used_colours = colors

  def update_path(self, path):
    self.path = path

  def to_string(self) -> str:
    if not self.path:
      start_node = end_node = '?'
    else:
      start_node = self.path[0]
      end_node = self.path[-1]

    solution_string = (
      f'Path\n'
      f'  - source node: {start_node}\n'
      f'  - destination node: {end_node}\n'
      f'  - path: {self.path}\n'
      f'  - number of used nodes: {len(self.path)}\n'
      f'  - cost: {self.cost}\n'
      f'Colours\n'
      f'  - colours: {self.used_colours}\n'
      f'  - number of used colours: {len(self.used_colours)}'
    )

    return solution_string
