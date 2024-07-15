import csv
import math
from collections import defaultdict
import matplotlib.pyplot as plt
from tkinter import *


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = math.radians(lat2 - lat1) 
    dlon = math.radians(lon2 - lon1) 
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def load_stations(filename):
    stations = {} 
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile) 
        next(reader)  
        for row in reader:
            station_id, latitude, longitude, name, _, _, _, _ = row 
            stations[int(station_id)] = {
                'latitude': float(latitude),
                'longitude': float(longitude),
                'name': name
            }
    return stations

def load_connections(filename, stations):
    graph = defaultdict(dict) 
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile) 
        next(reader) 
        for row in reader: 
            station1, station2, line = map(int, row) 
            weight = haversine(stations[station1]['latitude'], stations[station1]['longitude'], stations[station2]['latitude'], stations[station2]['longitude']) 
            graph[station1][station2] = (weight, line) 
            graph[station2][station1] = (weight, line)

    return graph

def dijkstra(graph, start, end):
    unvisited = set(graph.keys()) 
    distances = {node: float('infinity') for node in graph} 
    distances[start] = 0 
    previous_nodes = {node: None for node in graph} 

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])  
        unvisited.remove(current_node)

        if current_node == end: 
            break 

        for neighbor, (weight, line) in graph[current_node].items():
            if neighbor not in unvisited:
                continue 
            new_distance = distances[current_node] + weight 
            if new_distance < distances[neighbor]: 
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

    path = [] 
    while end is not None: 
        path.append(end)
        end = previous_nodes[end]
    path = path[::-1]

    return path, distances[path[-1]] 
def update_graph(entry_start, entry_end, label_result):
    start_station = int(entry_start.get()) 
    end_station = int(entry_end.get()) 

    num_stations = len(stations)
    if start_station > num_stations or end_station > num_stations:
        label_result.config(text=f"Erro: Você digitou um número maior do que o número de estações disponíveis ({num_stations}).")
        return 
    
    path, total_weight = dijkstra(graph, start_station, end_station)

    result_text = f"O menor caminho entre as estações {stations[start_station]['name']} e {stations[end_station]['name']} é:\n"
    for i, station_id in enumerate(path):
        if i > 0:
            result_text += ", "
        result_text += f"{station_id} ({stations[station_id]['name']})"
    result_text += f"\nO peso total do caminho é: {total_weight:.2f}"
    label_result.config(text=result_text)

    plt.clf() 

    
    for station1 in graph:
        for station2, (weight, line) in graph[station1].items():
            if (station1, station2) in zip(path, path[1:]) or (station2, station1) in zip(path, path[1:]):
                plt.plot([stations[station1]['latitude'], stations[station2]['latitude']], [stations[station1]['longitude'], stations[station2]['longitude']], color='red', linestyle='-', linewidth=1.5)
                plt.text((stations[station1]['latitude'] + stations[station2]['latitude']) / 2, (stations[station1]['longitude'] + stations[station2]['longitude']) / 2, str(line), fontsize=8, ha='center', va='center', color='red')
            else:
                plt.plot([stations[station1]['latitude'], stations[station2]['latitude']], [stations[station1]['longitude'], stations[station2]['longitude']], color='grey', linestyle='-', linewidth=0.5)

    
    plt.scatter(stations[start_station]['latitude'], stations[start_station]['longitude'], color='green', label='Estação de partida', zorder=5)
    plt.scatter(stations[end_station]['latitude'], stations[end_station]['longitude'], color='red', label='Estação de chegada', zorder=5)

    
    plt.legend()
    plt.title("Conexões entre as estações de metrô")
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.show() 

def create_gui():
    root = Tk()
    root.title("Encontrar Rota de Metrô")

    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    label_start = Label(frame, text="Estação de Partida:")
    label_start.grid(row=0, column=0, padx=5, pady=5, sticky=W)

    entry_start = Entry(frame)
    entry_start.grid(row=0, column=1, padx=5, pady=5)

    label_end = Label(frame, text="Estação de Chegada:")
    label_end.grid(row=1, column=0, padx=5, pady=5, sticky=W)

    entry_end = Entry(frame)
    entry_end.grid(row=1, column=1, padx=5, pady=5)

    button_submit = Button(frame, text="Encontrar Rota", command=lambda: update_graph(entry_start, entry_end, label_result))
    button_submit.grid(row=2, columnspan=2, padx=5, pady=5)

    label_result = Label(frame, text="", wraplength=400) 
    label_result.grid(row=3, columnspan=2, padx=5, pady=5)

    root.mainloop()

stations = load_stations("Stations.csv")
graph = load_connections("Line_definitions.csv", stations)

create_gui()