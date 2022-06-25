import geopandas as gpd
import networkx as nx
# import geopy
import matplotlib.pyplot as plt
import numpy as np
import networkx.algorithms.approximation as nx_app
# import math
from itertools import permutations
import folium

%matplotlib inline
from shapely.geometry import Polygon
import warnings
warnings.filterwarnings(action = "ignore")

def get_coordinates(cities):
  coordinates = []
  import http.client, urllib.parse
  import json
  conn = http.client.HTTPConnection('api.positionstack.com')
  for city in cities:
    params = urllib.parse.urlencode({
        'access_key': '3327d83d1f4f3dcbd5b50579808e69e4',
        'query': city,
        'limit': 1,
        })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    data = data.decode('utf-8')
    coordinate = (json.loads(data)['data'][0]['longitude'],json.loads(data)['data'][0]['latitude'])
    coordinates.append(coordinate)
  return coordinates

def createGraph(capitals,coordinates):
  G = nx.Graph()
  #Create a graph object with number of nodes same as number of cities
  nodes = np.arange(0, len(capitals))
  G.add_nodes_from(nodes)

  #Create a dictionary of node and coordinate of each state for positions
  positions = {node:coordinate for node, coordinate in zip(nodes, coordinates)}

  #Create a dictionary of node and capital for labels
  labels = {node:capital for node, capital in zip(nodes, capitals)}

  fig, ax = plt.subplots(figsize = (10, 7))
  country.plot(color = "whitesmoke", edgecolor = "black", ax = ax)
  for i in nodes:
      for j in nodes:
          if i!=j:
              G.add_edge(i, j)
  # return [G,positions,labels]

# # def drawGraph(G,positions,labels):
#   nx.draw_networkx(G, pos = positions,
#                   labels = labels, ax = ax,
#                   bbox = dict(facecolor = "skyblue", boxstyle = "round",
#                               ec = "black", pad = 0.3),)

#   plt.title(f"Map of {country_name} with capital cities of {len(capitals)} federal states")
#   plt.axis("off")
#   # plt.show()
  return G

def christofides(G, weight="weight", tree=None):
    # Remove selfloops if necessary
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)
    # Check that G is a complete graph
    N = len(G) - 1
    # This check ignores selfloops which is what we want here.
    if any(len(nbrdict) != N for n, nbrdict in G.adj.items()):
        raise nx.NetworkXError("G must be a complete graph.")

    if tree is None:
        tree = nx.minimum_spanning_tree(G, weight=weight)
    L = G.copy()
    L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])
    MG = nx.MultiGraph()
    MG.add_edges_from(tree.edges)
    edges = nx.min_weight_matching(L, maxcardinality=True, weight=weight)
    MG.add_edges_from(edges)
    # nodes =_shortcutting(nx.eulerian_circuit(MG))
    nodes = []
    for u, v in nx.eulerian_circuit(MG):
        if v in nodes:
            continue
        if not nodes:
            nodes.append(u)
        nodes.append(v)
    nodes.append(nodes[0])
    return nodes

def routeCycle(G, coordinates):
  nodes = christofides(G, weight="weight", tree=None)
  pos = {node:list(coordinate) for node, coordinate in zip(nodes, coordinates)}
  # Calculating the distances between the nodes as edge's weight.
  for i in range(len(pos)):
      for j in range(i + 1, len(pos)):
          dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
          dist = dist
          G.add_edge(i, j, weight=dist)

  for i in range(len(pos)): 
    for j in range(i + 1, len(pos)):

      #Multidimensional Euclidean distance from the origin to a point.
      #euclidean distance between (x1, y1) and (x2, y2) is ((x2-x1)**2 + (y2-y1)**2)**0.5
      dist = math.hypot(pos[i][0] - pos[j][0], pos[i][1] - pos[j][1])
      dist = dist
      G.add_edge(i, j, weight=dist)

  cycle = nx_app.christofides(G, weight="weight")
  return cycle

def drawMap(capitals,coordinates,cycle,start):
  # coordinates=[]
  folium_coordinates = []
  for x,y in coordinates:
      folium_coordinates.append([y,x])
      
  route = []
  for stop in cycle:
      route.append(folium_coordinates[stop])
      
  m1 = folium.Map(location = start, #[51, 10],   #latitude (N), longitude (E)
                  tiles = "OpenStreetMap", 
                  zoom_start= 10
                  )

  for coordinate, capital in zip(folium_coordinates, capitals):
      folium.Marker(location = coordinate,icon=folium.Icon(icon_color='green'),
                  popup = capital).add_to(m1)
      
  folium.PolyLine(route).add_to(m1)
  return m1
