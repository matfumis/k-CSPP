import gurobipy as gp
from gurobipy import GRB
from solution import Solution


def solve_k_cspp_formulation(graph, source, destination, k):

  arcs = []
  weight = {}
  colour = {}

  for u, v, data in graph.edges(data=True):
    for (i, j) in ((u, v), (v, u)):
      arcs.append((i, j))
      weight[i, j] = data['weight']
      colour[i, j] = data['colour']

  k_cspp = gp.Model("kCSPP")
  k_cspp.Params.OutputFlag = 0


  x = k_cspp.addVars(arcs, vtype=GRB.BINARY, name="x")

  all_colours = set(colour[e] for e in arcs)
  y = k_cspp.addVars(all_colours, vtype=GRB.BINARY, name="y")

  k_cspp.setObjective(
    gp.quicksum(weight[i, j] * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
  )

  for node in graph.nodes():
    inflow = gp.quicksum(x[i, node] for i, _ in arcs if _ == node)
    outflow = gp.quicksum(x[node, j] for _, j in arcs if _ == node)
    if node == source:
      k_cspp.addConstr(inflow - outflow == -1, name=f"flow_src_{node}")
    elif node == destination:
      k_cspp.addConstr(inflow - outflow == 1, name=f"flow_sink_{node}")
    else:
      k_cspp.addConstr(inflow - outflow == 0, name=f"flow_cons_{node}")

  for i, j in arcs:
    h = colour[i, j]
    k_cspp.addConstr(x[i, j] <= y[h], name=f"col_edge_{i}_{j}")

  k_cspp.addConstr(y.sum() <= k, name="max_colours")

  k_cspp.optimize()

  if k_cspp.Status != GRB.OPTIMAL:
    return None


  successive = {i: j for i, j in arcs if x[i, j].X > 0.5}
  path = [source]
  while path[-1] != destination:
    path.append(successive[path[-1]])

  used_colors = [h for h in all_colours if y[h].X > 0.5]
  total_cost = sum(weight[i, j] for i, j in arcs if x[i, j].X > 0.5)

  solution = Solution()
  solution.update_path(path)
  solution.update_used_colours(used_colors)
  solution.update_cost(total_cost)

  return solution
