from django.shortcuts import render
from django.http import HttpResponse
import joblib
from math import radians,tan
from pyproj import Proj
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.path as mpath
import networkx as nx
# Create your views here.
def pathplanning(request):
    import json
    if request.method=='POST':
        cordinates = request.POST
        cordinates1 = dict(cordinates)
        cr=[]
        for key,value in cordinates1.items():
            if key.startswith('cordinates'):
                cr.append(value)
        cor = []
        for i in cr:
            lat = float(i[0])
            lan = float(i[1])
            d = [lat,lan]
            cor.append(d)
        # print(cor)
        lng=[]
        lat=[]
        for i in range(len(cor)):
            lng.append(cor[i][0])
            lat.append(cor[i][1])
        pp = Proj(proj='utm',zone=42,ellps='WGS84', preserve_units=False)
        x,y = pp(lng,lat)
        aspect_ratio = 16/9
        al = radians(90)
        cell_y_o = (2*50*tan(al/2))/(1+aspect_ratio**2)**0.5
        cell_x_o = aspect_ratio*((2*50*tan(al/2))/(1+aspect_ratio**2)**0.5)
        cell_y = (1-.80)*cell_y_o
        cell_x = (1-.80)*cell_x_o
        xmin=np.min(x)
        ymin=np.min(y)
        xmax=np.max(x)
        ymax=np.max(y)
        polygon = np.column_stack((x, y))
        num_x = int(np.ceil((xmax-xmin)/cell_x))
        num_y = int(np.ceil((ymax-ymin)/cell_y))
        cells = np.zeros((num_x,num_y), dtype=bool)
        poly_path = mpath.Path(polygon)
        x_centers = np.zeros(num_x)
        y_centers = np.zeros(num_y)
        for i in range(num_x):
            for j in range(num_y):
                cell_xmin = xmin + i * cell_x
                cell_ymin = ymin + j * cell_y
                cell_xmax = cell_xmin + cell_x
                cell_ymax = cell_ymin + cell_y
                cell_poly = np.array([[cell_xmin, cell_ymin],
                              [cell_xmin, cell_ymax],
                              [cell_xmax, cell_ymax],
                              [cell_xmax, cell_ymin]])
                cell_path = mpath.Path(cell_poly)
                cells[i, j] = poly_path.intersects_path(cell_path)
                x_centers[i] = cell_xmin + cell_x/2
                y_centers[j] = cell_ymin + cell_y/2
        G2 = nx.Graph()
        for i in range(num_x):
            for j in range(num_y):
                if cells[i][j]:
                    node_id = f"{i},{j}"
                    if i > 0 and cells[i-1][j]:
                        neighbor_id = f"{i-1},{j}"
                        G2.add_edge(node_id, neighbor_id)
                    if i < num_x-1 and cells[i+1][j]:
                        neighbor_id = f"{i+1},{j}"
                        G2.add_edge(node_id, neighbor_id)
                    if j > 0 and cells[i][j-1]:
                        neighbor_id = f"{i},{j-1}"
                        G2.add_edge(node_id, neighbor_id)
                    if j < num_y-1 and cells[i][j+1]:
                        neighbor_id = f"{i},{j+1}"
                        G2.add_edge(node_id, neighbor_id)
                    if cells[i, j]:
                        node_id = f"{i},{j}"
                        G2.add_node(node_id, pos=(x_centers[i], y_centers[j]))
        pos = nx.get_node_attributes(G2, 'pos')
        g2 = nx.to_dict_of_lists(G2)
        visited = set()
        path = []
        def dfs(visited, graph, node):  
            if node not in visited:
                path.append(node)
                visited.add(node)
                for neighbour in graph[node]:
                    dfs(visited, graph, neighbour)
        s=list(g2.keys())
        dfs(visited, g2, s[0])
        path2=[]
        for i in path:
            cord = pos[i]
            path2.append(cord)
        lng = []
        lat = []
        final_path_with_lat_lng = []
        for i in range(len(path2)):
            x,y = path2[i]
            lat_lng = pp(x,y,inverse=True)
            final_path_with_lat_lng.append(lat_lng)
    print(final_path_with_lat_lng)
    return HttpResponse(final_path_with_lat_lng)