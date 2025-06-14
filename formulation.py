import gurobipy as gp
from gurobipy import GRB
from solution import Solution


def solve_k_cspp_formulation(graph, source, destination, k):
  """
  Risolve il k-Colour Shortest Path Problem su grafo non orientato graph
  con sorgente `source`, destinazione `destination` e limite di colori `k`.
  """
  # 1) Rappresentiamo ogni arco non orientato come due archi diretti
  arcs = []
  weight = {}  # dict
  colour = {}  # dict

  for u, v, data in graph.edges(data=True):
    for (i, j) in ((u, v), (v, u)):
      arcs.append((i, j))
      weight[i, j] = data['weight']
      colour[i, j] = data['colour']

  # 2) Istanzio il modello
  k_cspp = gp.Model("kCSPP")
  k_cspp.Params.OutputFlag = 0  # no log a video

  # 3) Variabili di decisione
  #   x[i,j] = 1 se arco (i,j) è nel cammino
  x = k_cspp.addVars(arcs, vtype=GRB.BINARY, name="x")
  #   y[h] = 1 se il colore h è usato
  all_colours = set(colour[e] for e in arcs)
  y = k_cspp.addVars(all_colours, vtype=GRB.BINARY, name="y")

  # 4) Funzione obiettivo: minimizzare somma dei pesi degli archi scelti
  k_cspp.setObjective(
    gp.quicksum(weight[i, j] * x[i, j] for i, j in arcs),
    GRB.MINIMIZE
  )

  # 5) Vincoli di flusso (conservazione + sorgente/destinazione)
  for node in graph.nodes():
    inflow = gp.quicksum(x[i, node] for i, _ in arcs if _ == node)
    outflow = gp.quicksum(x[node, j] for _, j in arcs if _ == node)
    if node == source:
      k_cspp.addConstr(inflow - outflow == -1, name=f"flow_src_{node}")
    elif node == destination:
      k_cspp.addConstr(inflow - outflow == 1, name=f"flow_sink_{node}")
    else:
      k_cspp.addConstr(inflow - outflow == 0, name=f"flow_cons_{node}")

  # 6) Vincolo colore–arco: posso usare arco (i,j) solo se seleziono il suo colore
  for i, j in arcs:
    h = colour[i, j]
    k_cspp.addConstr(x[i, j] <= y[h], name=f"col_edge_{i}_{j}")

  # 7) Vincolo sul numero massimo di colori
  k_cspp.addConstr(y.sum() <= k, name="max_colours")

  # 8) Risolvo
  k_cspp.optimize()

  if k_cspp.Status != GRB.OPTIMAL:
    return None


  # 9) Ricostruisco il cammino dal supporto di x[i,j]
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
