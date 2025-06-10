import heapq
from solution import Solution


def solve_colour_constrained_dijkstra(graph, source, destination, k):
  """
  Itera su una lista di penalità e cerca un percorso con ≤ k colori.
  Restituisce (path, used_colours, cost) o (None, None, None).
  """

  '''
  un elemento di graph.edge() ha 3 elementi:
    1) nodo di partenza
    2) nodo di arrivo
    3) dizionario attributi dell'arco data = {'weight': int, 'colour': int}
  '''
  weights = [data['weight'] for _, _, data in graph.edges(data=True)]

  min_edge_cost, max_edge_cost = min(weights), max(weights)
  mean_edge_cost = sum(weights) / len(weights)

  penalties_list = [
    0,
    min_edge_cost / 8, # aggiunto
    min_edge_cost / 6, # aggiunto
    min_edge_cost / 4,
    min_edge_cost / 2,
    min_edge_cost * 3 / 4,  # aggiunto
    min_edge_cost,
    min_edge_cost * 2,
    mean_edge_cost / 4,
    mean_edge_cost / 2,
    mean_edge_cost,
    max_edge_cost
  ]


  for penalty in penalties_list:
    solution = penalised_dijkstra(graph, source, destination, penalty)
    if solution and len(solution.used_colours) <= k:
      return solution, True if penalty == 0 else False

  return None, None


def penalised_dijkstra(graph, source, destination, penalty):
  """
  Variante di Dijkstra che penalizza l'uso di nuovi colori.
  Restituisce (path, used_colours, real_distances) oppure (None, None, None) se dest non è raggiungibile.
  real_distances è la somma dei soli pesi weight degli archi lungo il percorso scelto.
  """
  # Crea un dizionario 'penalised_distances' in cui, per ogni nodo 'destination_node' del grafo, inizializziamo
  # la distanza stimata (peso + eventuale penalità) a infinito (float('inf')).
  penalised_distances = {n: float('inf') for n in graph.nodes()}

  # Crea un dizionario 'used_colours' in cui, per ogni nodo 'destination_node', abbiamo un insieme vuoto.
  # Questo insieme conterrà, per ciascun nodo, i colori degli archi usati lungo il cammino migliore trovato finora.
  used_colours = {n: set() for n in graph.nodes()}

  # Crea un dizionario 'real_distances' in cui, per ogni nodo 'destination_node', inizializziamo il costo reale (somma dei soli pesi weight)
  # a zero. Inizialmente non abbiamo percorso verso nessun nodo, quindi costo reale = 0.
  real_distances = {n: 0 for n in graph.nodes()}

  # Crea un dizionario 'predecessors' (predecessori), vuoto per ora, che
  # verrà popolato con predecessors[neighbor_node] = current_node ogni volta che troviamo un cammino migliore a neighbor_node passando per current_node.
  predecessors = {}

  # Inizializziamo la distanza del nodo sorgente 'source' a 0 (nessun costo per partire da sé stesso).
  penalised_distances[source] = 0

  # Inizializziamo anche il costo reale del nodo sorgente a 0 (nessun peso speso finora).
  real_distances[source] = 0

  # Creiamo la coda con priorità (min-heap) come lista di tuple.
  # Ogni tupla è (distanza_stimata, nodo). Qui inseriamo inizialmente solo (0, source),
  # perché il punto di partenza ha distanza stimata = 0.
  priority_queue = [(0, source)]

  # Finché nella coda di priorità ci sono elementi, continuiamo a estrarre il nodo più vicino (distanza stimata minore).
  while priority_queue:
    # Estrai la tupla (current_distance, current_node) con distanza current_distance minima e nodo current_node associato.
    current_distance, current_node = heapq.heappop(priority_queue)

    # Se la distanza estratta 'current_distance' è maggiore di quella già memorizzata in penalised_distances[current_node],
    # significa che abbiamo già trovato un percorso migliore in passato, quindi scartiamo questa entry.
    if current_distance > penalised_distances[current_node]:
      continue

    # Se il nodo estratto 'current_node' è la destinazione, possiamo interrompere il ciclo,
    # perché abbiamo già trovato il cammino ottimo verso 'destination'.
    if current_node == destination:
      break

    # Altrimenti, esploriamo tutti i vicini 'neighbor_node' di 'current_node'.
    # In NetworkX, graph[current_node].items() restituisce per ciascun arco current_node->neighbor_node il dizionario degli attributi.
    for neighbor_node, data in graph[current_node].items():
      # Estraiamo il peso 'weight' dell'arco current_node->neighbor_node
      weight = data['weight']

      # Estraiamo il colore 'colour' dell'arco current_node->neighbor_node
      colour = data['colour']

      # Se il colore 'colour' è già presente in used_colours[current_node], non paghiamo penalità,
      # altrimenti applichiamo la penalità 'penalty' per usare un nuovo colore.
      neighbor_node_penalty = 0 if colour in used_colours[current_node] else penalty

      # Calcoliamo la nuova distanza stimata 'actual_distance' per arrivare a 'neighbor_node' passando per 'current_node':
      # distanza estratta 'current_distance' fino a 'current_node' + peso 'weight' + eventuale penalità 'neighbor_node_penalty' per il colore.
      actual_distance = current_distance + weight + neighbor_node_penalty

      # Se questa nuova distanza stimata 'actual_distance' è migliore (minore) di quella già memorizzata in penalised_distances[neighbor_node],
      # allora aggiorniamo penalised_distances[neighbor_node], predecessors[neighbor_node], real_distances[neighbor_node], used_colours[neighbor_node] e inseriamo (actual_distance, neighbor_node) nella coda.
      if actual_distance < penalised_distances[neighbor_node]:
        # Aggiorniamo la distanza stimata più piccola per 'neighbor_node'
        penalised_distances[neighbor_node] = actual_distance

        # Impostiamo il predecessore di 'neighbor_node' come 'current_node'
        predecessors[neighbor_node] = current_node

        # Aggiorniamo il costo reale (somma dei soli pesi weight) per arrivare a 'neighbor_node':
        # è il costo reale fino a 'current_node' più il peso 'weight' di (current_node->neighbor_node).
        real_distances[neighbor_node] = real_distances[current_node] + weight

        # Copiamo l'insieme di colori già usati fino a 'current_node' in used_colours[neighbor_node]
        used_colours[neighbor_node] = used_colours[current_node].copy()

        # Aggiungiamo il colore 'colour' dell'arco (current_node->neighbor_node) all'insieme di colori di 'neighbor_node'
        used_colours[neighbor_node].add(colour)

        # Inseriamo nella coda (actual_distance, neighbor_node) per esplorare in seguito il nodo 'neighbor_node' con priorità 'actual_distance'
        heapq.heappush(priority_queue, (actual_distance, neighbor_node))

  # Dopo il ciclo, se penalised_distances[destination] è ancora infinito significa che la destinazione non è raggiungibile.
  if penalised_distances[destination] == float('inf'):
    return None, None, None

  # Ricostruisco il percorso dal nodo destinazione alla sorgente utilizzando il dizionario 'predecessors'
  solution = Solution()
  destination_node = destination  # Parto dal nodo di destinazione
  path = []
  # Continuo finché non arrivo al nodo sorgente
  while destination_node != source:
    path.append(destination_node)
    destination_node = predecessors[destination_node]  # Mi sposto al predecessore di 'destination_node' (il nodo da cui sono arrivato a 'destination_node')

  path.append(source)
  path.reverse()

  solution.update_path(path)
  solution.update_used_colours(used_colours[destination])
  solution.update_cost(real_distances[destination])

  # Ritorno una solution contenente:
  # - path: la lista dei nodi dal source al destination
  # - used_colours[destination]: l’insieme dei colori usati per arrivare a 'destination'
  # - real_distances[destination]: il costo reale (somma dei soli pesi weight) del percorso fino a 'destination'
  return solution
