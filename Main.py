from replit import clear
from haversine import haversine, Unit
import copy
import matplotlib.pyplot as plt
import networkx as nx
import random
import math
import queue

from scipy.stats.morestats import probplot

from Generator import Generator
from NodeStatus import NodeStatus
from NodeType import NodeType

clear()

instance_generated = False

menu_options = {
    1: 'Generate new instance',
    2: 'Import an instance',
    3: 'Export current instance',
    4: 'Show instance data',
    5: 'Create a solution',
    6: 'Improve a solution',
    7: 'Print solutions results',
    0: 'Exit'
}

menu_options_show_instance = {
    1: 'Show distance histogram',
    2: 'Show angle histogram',
    3: 'Show polar coordinates',
    4: 'Show cartesian coordinates',
    5: 'Print total distance',
    6: 'Show graph',
    7: 'Show map',
    0: 'Back'
}

def print_menu():
    print('Menu\n')
    
    for key in menu_options.keys():
        if (key == 3 or key == 4 or key == 5 or key == 6 or key == 7) and instance_generated == False:
            continue
        print(str(key) + ')', menu_options[key])
    print()

def print_menu_show_instance():
    print('Show instance\n')
    
    for key in menu_options_show_instance.keys():
        print(str(key) + ')', menu_options_show_instance[key])
    print()

def print_menu_create_solution(results):
    print('Choose the solution\n')

    random_greedy_string = 'Random Greedy'
    if 'random_greedy' in results:
        random_greedy_string = random_greedy_string + ' (' + str(results['random_greedy']) + 'km)'

    nearest_neighbor_string = 'Nearest Neighbor'
    if 'nearest_neighbor' in results:
        nearest_neighbor_string = nearest_neighbor_string + ' (' + str(results['nearest_neighbor']) + 'km)'
    
    clarke_wright_string = 'Clarke & Wright'
    if 'clarke_wright' in results:
        clarke_wright_string = clarke_wright_string + ' (' + str(results['clarke_wright']) + 'km)'

    genetic_algorithm_string = 'Genetic Algorithm'
    if 'genetic_algorithm' in results:
        genetic_algorithm_string = genetic_algorithm_string + ' (' + str(results['genetic_algorithm']) + 'km)'

    ant_colony_optimization_string = 'Ant Colony Optimization'
    if 'ant_colony_optimization' in results:
        ant_colony_optimization_string = ant_colony_optimization_string + ' (' + str(results['ant_colony_optimization']) + 'km)'

    menu_options_show_solutions = {
        1: random_greedy_string,
        2: nearest_neighbor_string,
        3: clarke_wright_string,
        4: genetic_algorithm_string,
        5: ant_colony_optimization_string,
        0: 'Back',
    }
    
    for key in menu_options_show_solutions.keys():
        print(str(key) + ')', menu_options_show_solutions[key])
    print()

def print_menu_improve_solution(results):
    print('Choose the improvement\n')

    string_exchange_string = 'String Exchange'
    if 'string_exchange' in results:
        string_exchange_string = string_exchange_string + ' (' + str(results['string_exchange']) + 'km)'

    string_relocation_string = 'String Relocation'
    if 'string_relocation' in results:
        string_relocation_string = string_relocation_string + ' (' + str(results['string_relocation']) + 'km)'

    simulated_annealing_string = 'Simulated Annealing'
    if 'simulated_annealing' in results:
        simulated_annealing_string = simulated_annealing_string + ' (' + str(results['simulated_annealing']) + 'km)'

    tabu_search_string = 'Tabu Search'
    if 'tabu_search' in results:
        tabu_search_string = tabu_search_string + ' (' + str(results['tabu_search']) + 'km)'

    menu_options_improve_solution = {
        1: string_exchange_string,
        2: string_relocation_string,
        3: simulated_annealing_string,
        4: tabu_search_string,
        0: 'Back',
    }
    
    for key in menu_options_improve_solution.keys():
        print(str(key) + ')', menu_options_improve_solution[key])
    print()

def generate_instance():
    global instance_generated, generator, drivers_coordinates, passengers_coordinates, ORIGIN, upp
    clear()
    
    print('Insert instance data\n')

    origin_latitude = float(input('Latitude of origin (44.83436): ') or 44.83436)
    origin_longitude = float(input('Longitude of origin (11.59934): ') or 11.59934)

    ORIGIN = (origin_latitude, origin_longitude)

    students_number = int(input('Insert students number (100): ') or 100)
    drivers_percentage = float(input('Insert drivers percentage (25): ') or 25)
    mean = float(input('Insert students distribution mean (1000): ') or 1000)
    sd = float(input('Insert students distribution standard deviation (5000): ') or 5000)
    low = float(input('Insert students truncated distribution lower limit (1000): ') or 1000)
    upp = float(input('Insert students truncated distribution upper limit (10000): ') or 10000)

    generator = Generator(ORIGIN, students_number, drivers_percentage, mean, sd, low, upp)

    students_coordinates = generator.get_students_coordinates()

    drivers_coordinates = generator.get_drivers_coordinates(students_coordinates)
    passengers_coordinates = generator.get_passengers_coordinates(students_coordinates)

    instance_generated = True

def random_greedy(G):

    origin_node = generator.get_origin_node()

    drivers = []
    passengers = []
    
    routes = []

    # Creo le routes per i driver con come elemento iniziale il loro id
    # Riempio la lista dei driver e quella dei passeggeri con come elementi i loro id
    for node in G.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            drivers.append(node[0])
            routes.insert(node[0]-1, [node[0]])
        elif node[1]['t'] == NodeType.PASSENGER.value:
            passengers.append(node[0])

    # Se la lista dei passeggeri non è vuota
    if len(passengers) > 0:

        # Allora ciclo fino alla capienza massima che può raggiungere ogni driver
        for _ in range(4):

            # Ciclo per ogni driver
            for driver in drivers:

                # Se sono ancora disponibili dei passeggeri
                if len(passengers) > 0:

                    # Allora casualmente decido se aggiungerlo o meno alla route del driver corrente
                    new_passenger = random.choice([True, False])

                    # Se ho deciso di aggiungere un passeggero alla route del driver corrente
                    if new_passenger:

                        # Allora seleziono casualmente un passeggero tra quelli ancora disponibili
                        next_passenger = random.choice(passengers)

                        # Aggiungo il passeggero in coda alla route del driver corrente
                        routes[driver-1].append(next_passenger)

                        # Rimuovo il passeggero selezionato dalla lista dei passeggeri ancora disponibili
                        passengers.remove(next_passenger)

                        # Rimuovo dalla soluzione ammissibile iniziale a stella l'arco che collega il passeggero all'università
                        # Questo arco verrà aggiunto forse in seguito solo se questo passeggero sarà l'ultimo prima dell'università
                        G.remove_edge(next_passenger, origin_node[0])

                        # Controllo se il driver è collegato con un arco direttamente all'università
                        if G.has_edge(driver, origin_node[0]):

                            # Se il driver ha un arco collegato diretto verso l'università allora lo cancello
                            G.remove_edge(driver, origin_node[0])
    
    # Ciclo sulle routes dei driver generate
    add_edges = []
    for route in routes:

        # Ad ogni route aggiungo in coda l'id del nodo dell'università
        route.append(origin_node[0])

        # Per ogni arco ne calcolo la lunghezza per salvarla come metadato sul grafo
        for idx, node in enumerate(route):
            try:
                node_i = route[idx]
                node_j = route[idx+1]
                if not G.has_edge(node_i, node_j):
                    add_edges.append((node_i, node_j, { 'distance': int(round(haversine(G.nodes[node_i]['g'], G.nodes[node_j]['g'], unit=Unit.METERS))) }))
            except:
                pass

    G.add_edges_from(add_edges)

    return G

def nearest_neighbor(G):

    origin_node = generator.get_origin_node()
    generator.show_graph(G)
 
    drivers = {}
    for node in G.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            drivers[node[0]] = {}
            drivers[node[0]]['snake'] = [node]
            drivers[node[0]]['distance'] = int(round(haversine(node[1]['g'], origin_node[1]['g'], unit=Unit.METERS)))
    
    drivers_ordered = dict(sorted(drivers.items(), key=lambda item: item[1]['distance'], reverse=True))
    
    partial_distance = []
    G2, partial_distance = get_neighbor(G, origin_node, drivers_ordered, partial_distance)

    return G2, partial_distance

def get_neighbor(G1, origin_node, drivers, partial_distance):

    drivers = dict(sorted(drivers.items(), key=lambda item: item[1]['distance'], reverse=True))

    all_origin = False
    all_full = False
    break_full = False
    break_origin = False
    for idx, snake in drivers.copy().items():
        driver_full = False
        driver_arrived = False
        if len(snake['snake']) == 5:
            if not break_full:
                all_full = True
            driver_full = True
        else:
            all_full = False
            break_full = True
        if snake['snake'][-1][0] == origin_node[0]:
            if not break_origin:
                all_origin = True
            driver_arrived = True
        else:
            all_origin = False
            break_origin = True
        
        if driver_full or driver_arrived:
            drivers.pop(idx)

    if all_full and all_origin or not bool(drivers):
        return G1, partial_distance

    driver = next(iter(drivers.items()))
    driver_node = driver[1]['snake'][-1]
    neighbors = []

    for node in G1.nodes(data=True):
        if driver[1]['snake'][-1][0] != node[0] and node[1]['t'] != NodeType.DRIVER.value and node[1]['s'] != NodeStatus.VISITED.value:
            neighbors.append((node, int(round(haversine(driver[1]['snake'][-1][1]['g'], node[1]['g'], unit=Unit.METERS)))))

    if len(neighbors) == 0:
        return G1, partial_distance

    neighbors_sorted = sorted(neighbors, key=lambda x: x[1])
    next_neighbor = neighbors_sorted[0][0]
    
    driver[1]['snake'].append(next_neighbor)

    new_distance = 0
    old_distance = driver[1]['distance']
    for idx, node in enumerate(driver[1]['snake']):
        node_i = driver[1]['snake'][idx]
        try:
            node_j = driver[1]['snake'][idx+1]
            new_distance = new_distance + int(round(haversine(node_i[1]['g'], node_j[1]['g'], unit=Unit.METERS)))
            distance_recalculated = True
        except:
            pass
    
    if distance_recalculated == True:
        driver[1]['distance'] = new_distance
    else:
        driver[1]['distance'] = old_distance

    if G1.has_edge(driver_node[0], origin_node[0]):
        G1.remove_edge(driver_node[0], origin_node[0])

    add_edges = []

    if not G1.has_edge(driver_node[0], next_neighbor[0]):
        add_edges.append((driver_node[0], next_neighbor[0], { 'distance': generator.get_distance_geographic(driver_node, next_neighbor) }))
        if next_neighbor[0] != origin_node[0]:
            G1.nodes[next_neighbor[0]].update({ 's': NodeStatus.VISITED.value })

    G1.add_edges_from(add_edges)

    # total_distance_G = generator.get_total_distance(G)
    total_distance_G1 = generator.get_total_distance(G1)
    # if total_distance_G1 < total_distance_G:
    #     G_updated = G1
    #     partial_distance.append(total_distance_G1)
    # else:
    #     G_updated = G
    #     partial_distance.append(total_distance_G)

    partial_distance.append(total_distance_G1)

    drivers[driver[0]] = driver[1]

    generator.show_graph(G1, True)

    return get_neighbor(G1, origin_node, drivers, partial_distance)

def clarke_wright(G):

    origin_node = generator.get_origin_node()
    generator.show_graph(G)
 
    drivers = {}
    for node in G.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            drivers[node[0]] = {}
            drivers[node[0]]['snake'] = [node]
            drivers[node[0]]['distance'] = int(round(haversine(node[1]['g'], origin_node[1]['g'], unit=Unit.METERS)))
    
    drivers_ordered = dict(sorted(drivers.items(), key=lambda item: item[1]['distance'], reverse=True))
    
    partial_distance = []
    G2, partial_distance = get_saver(G, origin_node, drivers_ordered, partial_distance)

    return G2, partial_distance

def get_saver(G, origin_node, drivers, partial_distance):

    drivers = dict(sorted(drivers.items(), key=lambda item: item[1]['distance'], reverse=True))

    all_origin = False
    all_full = False
    break_full = False
    break_origin = False
    for idx, snake in drivers.copy().items():
        driver_full = False
        driver_arrived = False
        if len(snake['snake']) == 5:
            if not break_full:
                all_full = True
            driver_full = True
        else:
            all_full = False
            break_full = True
        if snake['snake'][-1][0] == origin_node[0]:
            if not break_origin:
                all_origin = True
            driver_arrived = True
        else:
            all_origin = False
            break_origin = True
        
        if driver_full or driver_arrived:
            drivers.pop(idx)

    if all_full and all_origin or not bool(drivers):
        return G, partial_distance

    driver = next(iter(drivers.items()))
    driver_node = driver[1]['snake'][-1]
    savers = []

    for node in G.nodes(data=True):
        if driver[1]['snake'][-1][0] != node[0] and node[1]['t'] != NodeType.DRIVER.value and node[1]['s'] != NodeStatus.VISITED.value:
            driver_origin_distance = haversine(driver[1]['snake'][-1][1]['g'], origin_node[1]['g'], unit=Unit.METERS)
            driver_passenger_distance = haversine(driver[1]['snake'][-1][1]['g'], node[1]['g'], unit=Unit.METERS)
            distance_formula = driver_origin_distance - driver_passenger_distance
            savers.append((node, distance_formula))

    if len(savers) == 0:
        return G, partial_distance

    savers_sorted = sorted(savers, key=lambda x: x[1], reverse=True)

    if savers_sorted[0][1] >= 0:
        next_saver = savers_sorted[0][0]
    else:
        next_saver = origin_node

    driver[1]['snake'].append(next_saver)

    new_distance = 0
    old_distance = driver[1]['distance']
    for idx, node in enumerate(driver[1]['snake']):
        node_i = driver[1]['snake'][idx]
        try:
            node_j = driver[1]['snake'][idx+1]
            new_distance = new_distance + int(round(haversine(node_i[1]['g'], node_j[1]['g'], unit=Unit.METERS)))
            distance_recalculated = True
        except:
            pass

    if distance_recalculated == True:
        driver[1]['distance'] = new_distance
    else:
        driver[1]['distance'] = old_distance

    if G.has_edge(driver_node[0], origin_node[0]):
        G.remove_edge(driver_node[0], origin_node[0])

    add_edges = []
    if not G.has_edge(driver_node[0], next_saver[0]):
        add_edges.append((driver_node[0], next_saver[0], { 'distance': generator.get_distance_geographic(driver_node, next_saver) }))
        if next_saver[0] != origin_node[0]:
            G.nodes[next_saver[0]].update({ 's': NodeStatus.VISITED.value })
    G.add_edges_from(add_edges)

    total_distance_G = generator.get_total_distance(G)
    partial_distance.append(total_distance_G)

    drivers[driver[0]] = driver[1]

    generator.show_graph(G, update=True)

    return get_saver(G, origin_node, drivers, partial_distance)

def genetic_algorithm(G):

    I = 0
    Imax = 100
    stall = 0
    stall_max = 10
    population_size = 100
    population = []
    Pc = 0.9
    Pm = 0.5

    # Genero population_size grafi tramite metodo random_greedy() e li aggiungo alla lista population insieme alla loro distanza totale
    for _ in range(population_size):
        G1 = copy.deepcopy(G)
        G2 = random_greedy(G1)
        population.append((G2, generator.get_total_distance(G2)))

    partial_distance = []

    # Ciclo finchè non raggiungo il numero di iterazioni massime oppure uno stallo
    while I < Imax and stall < stall_max:

        # Ordino in ordine decrescente per distanza totale la popolazione dei grafi
        population_ordered = list(sorted(population, key=lambda x: x[1], reverse=True))

        # Assegno a stall_value l'elemento migliore della popolazione
        stall_value = population_ordered[-1][1]
        
        # Seleziono l'elemento migliore della popolazione corrente per poi riinserirlo dopo la fase di mutazione
        elitism = population_ordered[-1]

        # Calcolo la sommatoria dei rank totali
        n = len(population_ordered)
        rank_sum = n*(n+1)/2

        # Per ogni elemento della popolazione associo una probabilità di essere scelto come genitore per la fase di crossover
        fitness_sum_rank = []
        for idx, i in enumerate(population_ordered, 1):
            a = i
            c = idx/rank_sum
            if idx > 1:
                c = c + fitness_sum_rank[-1][2] if idx > 0 else 0
            fitness_sum_rank.append(a + (c,))

        couples = []
        parents = ()
        m = 0
        parent_dict = dict.fromkeys(range(len(fitness_sum_rank)), 0)

        # Ciclo finché non genero m coppie di genitori per la fase di crossover
        while m < len(fitness_sum_rank):
            # Genero una probabilità casuale
            p = random.uniform(0, 1)

            # Per ogni elemento della popolazione cerco quello più aderente alla probabilità generata
            for idx, i in enumerate(fitness_sum_rank):

                # Se la probabilità dell'elemento corrente è inferiore a quella generata continuo
                if i[2] <= p:
                    continue
                else:
                    # Altrimenti se la coppia è formata da almeno 2 genitori
                    if len(parents) % 2 == 0 and len(parents) > 0:
                        # Se la coppia di genitori è già presente allora la svuoto per generarne un'altra
                        # Quindi prima cerco se la coppia generata è un duplicato
                        duplicates = False
                        for p1, p2 in couples:
                            if parents[0] == p1 and parents[1] == p2:
                                duplicates = True
                                break

                        # Se la coppia generata non è un duplicato allora la aggiungo a couples, svuoto la coppia parents per pi inserirci il genitore selezionato al ciclo attuale
                        # incremento m di 2 ed incremento il dizionario dei genitori selezionati per tenere traccia di quante volte i genitori siano stati selezionati
                        if not duplicates:
                            couples.append(parents)
                            parents = ()
                            parents = parents + (idx,)
                            m = m+2
                            parent_dict[idx] += 1
                        else:
                            parents = ()
                            break
                    else:
                        # Se la coppia ha solo un genitore e il suo partner è se stesso fermo il ciclo altrimenti lo aggiungo alla coppia
                        if len(parents) == 1 and idx == parents[0]:
                            break
                        parents = parents + (idx,)
                        parent_dict[idx] += 1
                    break

        next_population = []

        origin_node = generator.get_origin_node()

        # Per ogni coppia generata genero un paio di figli che andranno a formare la popolazione all'iterazione successiva
        first_passenger_id = []
        for idd, (p1, p2) in enumerate(couples):

            # Seleziono i grafi dei genitori della coppia
            gp1 = fitness_sum_rank[p1][0]
            gp2 = fitness_sum_rank[p2][0]

            first_passenger_id.append([])

            # Per ogni grafo dei della coppia selezionata genero le rispettive routes
            routes = []
            for idx, g in enumerate([gp1, gp2]):
                routes.append([])
                first_passenger_found = False

                # Per ogni nodo del grafo del genitore corrente della coppia
                for node in g.nodes(data=True):
                    # Se il nodo selezionato è un driver oppure è un passenger di grado 1 quindi solo collegato direttamente all'origine
                    if node[1]['t'] == NodeType.DRIVER.value or (node[1]['t'] == NodeType.PASSENGER.value and g.degree[node[0]] == 1):

                        # Se il nodo corrente è un passeggero di grado 1 che quindi punta all'origine e non è stato trovato prima un passeggero tale
                        if node[1]['t'] == NodeType.PASSENGER.value and g.degree[node[0]] == 1 and not first_passenger_found:
                            # Allora ne seleziono l'id
                            first_passenger_id[idd].append(node[0])
                            first_passenger_found = True

                        # In paths memorizzo tutti i percorsi che vanno dal nodo corrente al nodo origine del grafo del genitore
                        paths = nx.all_simple_paths(g, node[0], origin_node[0])
                        # Ogni percorso lo memorizzo nella lista routes con indice quello del genitore corrente
                        for path in list(paths):
                            routes[idx].append(path)

            # Probabilità di eseguire il crossover o meno
            crossover_probability = random.uniform(0, 1)
            
            # Se il numero generato casualmente è inferiore a Pc allora eseguo il crossover
            if crossover_probability < Pc:

                # In o1 e o2 memorizzo le routes dei genitori
                o1 = copy.deepcopy(routes[0])
                o2 = copy.deepcopy(routes[1])

                # Seleziono casualmente un path in entrambe le routes
                edges_removed_1 = None
                while edges_removed_1 == None:
                    sub_route_1 = random.choice(routes[0])
                    # Se il primo nodo del path selezionato casualmente è un driver e il path ha almeno un passeggero
                    if gp1.nodes[sub_route_1[0]]['t'] == NodeType.DRIVER.value and len(sub_route_1) > 2:
                        # Rimuovo i passeggeri tra il driver e l'origine
                        edges_removed_1 = o1[o1.index(sub_route_1)][1:-1]
                    # Altrimenti se è un nodo passeggero
                    elif gp1.nodes[sub_route_1[0]]['t'] == NodeType.PASSENGER.value:
                        # Rimuovo dall'altro figlio il passeggero appena selezionato
                        edges_removed_1 = o1[o1.index(sub_route_1)][:-1]

                edges_removed_2 = None
                while edges_removed_2 == None:
                    sub_route_2 = random.choice(routes[1])
                    if gp2.nodes[sub_route_2[0]]['t'] == NodeType.DRIVER.value and len(sub_route_2) > 2:
                        edges_removed_2 = o2[o2.index(sub_route_2)][1:-1]
                    elif gp2.nodes[sub_route_2[0]]['t'] == NodeType.PASSENGER.value:
                        edges_removed_2 = o2[o2.index(sub_route_2)][:-1]

                if edges_removed_1:
                    # Per ogni path in routes di un figlio
                    for i in o2:
                        # Per ogni nodo da rimuovere
                        for x in edges_removed_1:
                            try:
                                # Se le lunghezza del path è maggiore di 2 quindi ha almeno un passeggero provo a rimuoverlo
                                if len(i) > 2:
                                    i.remove(x)
                                else:
                                    # ALtrimenti se il path è composto solo da un passeggero e l'origine e il nodo da rimuovere è presente nel path rimuovo direttamente il path
                                    if x in i:
                                        o2.remove(i)
                                        # break?
                            except:
                                pass

                if edges_removed_2:
                    for i in o1:
                        for x in edges_removed_2:
                            try:
                                if len(i) > 2:
                                    i.remove(x)
                                else:
                                    if x in i:
                                        o1.remove(i)
                                        # break?
                            except:
                                pass

                skip_graph_equals = False
                o2_loop = copy.deepcopy(o2)
                # Per ogni nodo da rimuovere nell'altro fratello
                for i in edges_removed_1:
                    g_cost_array = []
                    insert_possible = False
                    skip_graph_equals = False
                    # Per ogni route del fratello
                    for ido, j in enumerate(o2_loop):
                        if skip_graph_equals:
                            break
                            # Se la route corrente del fratello è di lunghezza inferiore a 6 allora ci sarebbe posto per un altro passeggero
                        if len(j) < 6:
                            if not insert_possible:
                                insert_possible = True
                            # Per ogni nodo della route del fratello vado a provare ad inserire il passeggero corrente i
                            for idx, _ in enumerate(range(len(j))):
                                o2_temp = copy.deepcopy(o2_loop)
                                # Ovviamente andrò a provare ad inserire il passeggero corrente i dopo il driver e prima dell'origine
                                if idx > 0:
                                    # Quindi se l'indice della route è maggiore di 0 proverò al primo ciclo ad inserirlo nella prima posizione dopo il driver

                                    if 0 <= 1 < len(first_passenger_id[idd]) and j[0] < first_passenger_id[idd][1]:
                                        o2_temp[ido].insert(idx, i)
                                    else:
                                        o2_temp.append([i, origin_node[0]])
                                        skip_graph_equals = True
                                    # Pulisco il grafo del fratello da tutti gli archi 
                                    g_temp = nx.create_empty_copy(g)

                                    add_edges = []

                                    # Quindi per ogni possibile configurazione del passeggero nella route corrente del fratello vado a crearci un nuovo grafo
                                    # Qui creo gli archi del grafo e ne calcolo la lunghezza che poi assegno
                                    for route in o2_temp:
                                        for idx, node in enumerate(route):
                                            try:
                                                node_i = route[idx]
                                                node_j = route[idx+1]
                                                if not g_temp.has_edge(node_i, node_j):
                                                    add_edges.append((node_i, node_j, { 'distance': int(round(haversine(g_temp.nodes[node_i]['g'], g_temp.nodes[node_j]['g'], unit=Unit.METERS))) }))
                                            except:
                                                pass

                                    g_temp.add_edges_from(add_edges)
                                    
                                    generator.show_graph(g_temp, True, True, 0.01)
                                    
                                    # Aggiungo alla lista g_cost_array le routes, il grafo e la sua distanza totale per la corrente configurazione
                                    g_cost_array.append((o2_temp, g_temp, generator.get_total_distance(g_temp)))

                    # Se l'inserimento del nodo corrente in almeno una route di un driver non è stato possibile allora ne creo una nuova che puntrà direttamente all'origine
                    # Questo vorrebbe dire che il grafo fratello avrebbe tutte route dei driver di massima capacità
                    if insert_possible == False:
                        o2_temp = copy.deepcopy(o2_loop)
                        o2_temp.append([i, origin_node[0]])

                        g_temp = nx.create_empty_copy(g, with_data=True)

                        add_edges = []
                        for route in o2_temp:
                            for idx, node in enumerate(route):
                                try:
                                    node_i = route[idx]
                                    node_j = route[idx+1]
                                    if not g_temp.has_edge(node_i, node_j):
                                        add_edges.append((node_i, node_j, { 'distance': int(round(haversine(g_temp.nodes[node_i]['g'], g_temp.nodes[node_j]['g'], unit=Unit.METERS))) }))
                                except:
                                    pass

                        g_temp.add_edges_from(add_edges)

                        g_cost_array.append((o2_temp, g_temp, generator.get_total_distance(g_temp)))

                    # Una volta provate tutte le configurazioni dell'inserimento del nodo corrente e memorizzate nella lista g_cost_array le ordino in modo crescente per distanza totale del grafo corrispondente
                    g_cost_array_ordered = sorted(g_cost_array, key=lambda item: item[2])

                    # Una volta trovata la configurazione migliore per il nodo corrente i nel grafo del fratello riassegno il grafo aggiornato per passare al nodo successivo i di indice successivo
                    o2_loop = copy.deepcopy(g_cost_array_ordered[0][0])

                # Una volta inseriti tutti i nodi nelle configurazioni migliori del fratello queso lo aggiungo alla successiva popolazione
                next_population.append((g_cost_array_ordered[0][0], g_cost_array_ordered[0][1], g_cost_array_ordered[0][2]))

                o1_loop = copy.deepcopy(o1)
                for i in edges_removed_2:
                    g_cost_array = []
                    insert_possible = False
                    skip_graph_equals = False
                    for ido, j in enumerate(o1_loop):
                        if skip_graph_equals:
                            break
                        if len(j) < 6:
                            if not insert_possible:
                                insert_possible = True
                            for idx, _ in enumerate(range(len(j))):
                                o1_temp = copy.deepcopy(o1_loop)
                                if idx > 0:
                                    if 0 <= 1 < len(first_passenger_id[idd]) and j[0] < first_passenger_id[idd][0]:
                                        o1_temp[ido].insert(idx, i)
                                    else:
                                        o1_temp.append([i, origin_node[0]])
                                        skip_graph_equals = True

                                    g_temp = nx.create_empty_copy(g)

                                    add_edges = []
                                    for route in o1_temp:
                                        for idx, node in enumerate(route):
                                            try:
                                                node_i = route[idx]
                                                node_j = route[idx+1]
                                                if not g_temp.has_edge(node_i, node_j):
                                                    add_edges.append((node_i, node_j, { 'distance': int(round(haversine(g_temp.nodes[node_i]['g'], g_temp.nodes[node_j]['g'], unit=Unit.METERS))) }))
                                            except:
                                                pass

                                    g_temp.add_edges_from(add_edges)

                                    g_cost_array.append((o1_temp, g_temp, generator.get_total_distance(g_temp)))
                    
                    if insert_possible == False:
                        o1_temp = copy.deepcopy(o1_loop)
                        o1_temp.append([i, origin_node[0]])

                        g_temp = nx.create_empty_copy(g, with_data=True)

                        add_edges = []
                        for route in o1_temp:
                            for idx, node in enumerate(route):
                                try:
                                    node_i = route[idx]
                                    node_j = route[idx+1]
                                    if not g_temp.has_edge(node_i, node_j):
                                        add_edges.append((node_i, node_j, { 'distance': int(round(haversine(g_temp.nodes[node_i]['g'], g_temp.nodes[node_j]['g'], unit=Unit.METERS))) }))
                                except:
                                    pass

                        g_temp.add_edges_from(add_edges)

                        g_cost_array.append((o1_temp, g_temp, generator.get_total_distance(g_temp)))

                    g_cost_array_ordered = sorted(g_cost_array, key=lambda item: item[2])
                    o1_loop = copy.deepcopy(g_cost_array_ordered[0][0])

                next_population.append((g_cost_array_ordered[0][0], g_cost_array_ordered[0][1], g_cost_array_ordered[0][2]))
            else:
                # Se la probabilità del crossover fosse inferiore a Pc allora aggiungerò alla popolazione i genitori stessi
                next_population.append((routes[0], population_ordered[p1][0], population_ordered[p1][1]))
                next_population.append((routes[1], population_ordered[p2][0], population_ordered[p2][1]))

        next_population_mutated = copy.deepcopy(next_population)
        for idx, _ in enumerate(next_population_mutated):
            mutation_probability = random.uniform(0, 1)
            if mutation_probability < Pm:
                route_to_mutate = random.choice(next_population_mutated[idx][0])
                if len(route_to_mutate) > 4:
                    route_mutated = copy.deepcopy(route_to_mutate)

                    node_i = random.choice(route_mutated[1:-1])
                    node_j = node_i
                    while node_i == node_j:
                        node_j = random.choice(route_mutated[1:-1])

                    node_i_index, node_j_index = route_mutated.index(node_i), route_mutated.index(node_j)
                    route_mutated[node_j_index], route_mutated[node_i_index] = route_mutated[node_i_index], route_mutated[node_j_index]

                    next_population_mutated[idx][0].remove(route_to_mutate)
                    next_population_mutated[idx][0].insert(route_mutated[0]-1, route_mutated)

        population = []
        for idx, i in enumerate(next_population_mutated):
            population.append((next_population_mutated[idx][1], next_population_mutated[idx][2]))

        population_ordered = list(sorted(population, key=lambda x: x[1], reverse=True))

        if population_ordered[-1][1] < stall_value:
            stall = 0
        else:
            stall = stall + 1

        population_ordered[0] = copy.deepcopy(elitism)

        I = I + 1

        partial_distance.append(population_ordered[-1][1])

    return population_ordered[-1][0], partial_distance

def get_next_node(cursor, G_complete, id_ant, node_visited, alpha, beta, gamma):

    origin_node = generator.get_origin_node()

    # Costruisco il denominatore della formula quindi per ogni vicino del cursore non ancora visitato da altri driver
    matrix_cost = {}
    matrix_cost[cursor] = {}
    denominator = 0
    for neighbor in G_complete.neighbors(cursor):
        if not node_visited[id_ant][neighbor] and G_complete.nodes[neighbor]['s'] == NodeStatus.FREE.value:
            pheromone = G_complete[cursor][neighbor]['pheromone']
            distance = G_complete[cursor][neighbor]['distance']
            if neighbor != origin_node[0]:
                saving = int(round(haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS) - haversine(G_complete.nodes[cursor]['g'], G_complete.nodes[neighbor]['g'], unit=Unit.METERS)))
                # saving = haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS) / haversine(G_complete.nodes[cursor]['g'], G_complete.nodes[neighbor]['g'], unit=Unit.METERS)
            else:
                saving = int(round(haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS)))
                # saving = 1

            matrix_cost[cursor][neighbor] = (pheromone, distance)
            denominator = denominator + (pow(pheromone, alpha) * pow(1/distance, beta) * pow(saving, gamma))
    
    # Una volta ottenuto il denominatore posso calcolare la formula
    matrix_probability = {}
    for neighbor in G_complete.neighbors(cursor):
        if not node_visited[id_ant][neighbor] and G_complete.nodes[neighbor]['s'] == NodeStatus.FREE.value:
            pheromone = matrix_cost[cursor][neighbor][0]
            distance_inverse = 1/matrix_cost[cursor][neighbor][1]
            if neighbor != origin_node[0]:
                saving = int(round(haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS) - haversine(G_complete.nodes[cursor]['g'], G_complete.nodes[neighbor]['g'], unit=Unit.METERS)))
                # saving = haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS) / haversine(G_complete.nodes[cursor]['g'], G_complete.nodes[neighbor]['g'], unit=Unit.METERS)
            else:
                saving = int(round(haversine(G_complete.nodes[cursor]['g'], origin_node[1]['g'], unit=Unit.METERS)))
                # saving = 1

            matrix_probability[neighbor] = pow(pheromone, alpha) * pow(distance_inverse, beta) * pow(saving, gamma) / denominator

    # Ordino la lista delle tuple (id_nodo, probabilità)
    matrix_probability_sorted = sorted(matrix_probability.items(), key=lambda x: x[1])
    
    n = len(matrix_probability_sorted)
    rank_sum = n*(n+1)/2

    roulette_wheel = []
    for idx, i in enumerate(matrix_probability_sorted, 1):
        a = i
        c = idx/rank_sum
        if idx > 1:
            c = c + roulette_wheel[-1][2]
        roulette_wheel.append(a + (c,))

    probability = random.uniform(0, 1)

    for slice_roulette_wheel in roulette_wheel:
        if slice_roulette_wheel[2] <= probability:
            continue
        else:
            return slice_roulette_wheel[0]

def ant_colony_optimization(G):
    origin_node = generator.get_origin_node()

    # Dichiaro valori per i parametri dell'algoritmo
    starting_pheromon = 1
    ants = 100
    iterations = 10
    p = 0.2

    # Dichiaro i pesi dei parametri per la decisione del prossimo nodo: feromone, inverso della distanza e saving
    alpha = 2
    beta = 12
    gamma = 4

    # Creo una copia del grafo originale ma privo di archi 
    G_empty_copy = nx.create_empty_copy(G)

    # Creo un grafo semi-completo ovvero con solo archi del tipo driver-passenger, driver-origin, passenger-passenger, passenger-origin
    # Gli archi del grafo oltre che alla distanza tra i nodi adiacenti, avranno anche il valore iniziale di feromone
    add_edges = []
    for node_i in G_empty_copy.nodes(data=True):
        for increment in G_empty_copy.nodes(data=True):
            if node_i[0] != increment[0] and increment[1]['t'] != NodeType.DRIVER.value:
                if not G_empty_copy.has_edge(node_i[0], increment[0]):
                    add_edges.append((node_i[0], increment[0], {
                        'pheromone': starting_pheromon,
                        'distance': int(round(haversine(node_i[1]['g'], increment[1]['g'], unit=Unit.METERS)))
                    }))
    G_complete = copy.deepcopy(G_empty_copy)
    G_complete.add_edges_from(add_edges)

    # Insieme non ordinato privo di duplicati dei nodi già prenotati
    node_occupied = set()

    # Ordino i drivers per distanza dall'origine in ordine descrescente quindi dal più distante al più vicino
    drivers = {}
    for node in G_complete.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            drivers[node[0]] = {}
            drivers[node[0]]['snake'] = [node[0]]
            drivers[node[0]]['distance'] = int(round(haversine(node[1]['g'], origin_node[1]['g'], unit=Unit.METERS)))
            node_occupied.add(node[0])
    drivers_ordered = dict(sorted(drivers.items(), key=lambda item: item[1]['distance'], reverse=True))

    # Conto i nodi passeggeri non ancora visitati da altri driver TODO: Spostare fuori dai cicli
    last_node_id = 0
    for node in G_complete.nodes(data=True):
        last_node_id = node[0]
    # node_visited = [[True if x in drivers or [True if x in driver['snake'] else False for _, driver in drivers.items() ] else False for x in range(last_node_id+2)] for _ in range(ants)]

    # Continuo a ciclare finché tutti i driver non sono arrivati all'origine
    all_drivers_origin = False
    while not all_drivers_origin:
        # Ciclo per ogni driver ordinati al primo ciclo per distanza dall'origine mentre dal secondo in poi per distanza percorsa
        for driver_id, driver in drivers_ordered.items():

            # Se il driver corrente è arrivato in università continua il ciclo per passare al driver successivo
            if driver['snake'][-1] == origin_node[0]:
                continue

            #
            for _ in range(iterations):
            # for _ in range(1):

                # Matrice a 2 dimensioni dei nodi visitati dalle formiche: una riga per ogni formica, una colonna per ogni nodo
                # Inizialmente questa matrice ha tutti i suoi elementi impostati a False compreso lo 0, eccetto le colonne corrispondenti ai driver impostate a True.
                node_visited = []
                # Per ogni formica
                for y in range(ants):
                    # Crea un array di dimensione pari ai nodi presenti sul grafo
                    node_visited.append([])
                    # Per ogni nodo del grafo + 2
                    for x in range(last_node_id+2):
                        # Se il nodo corrente è presente nei nodi occupati allora imposto l'elemento della matrice a True
                        if x in node_occupied:
                            node_visited[y].insert(x, True)
                        # Altrimenti il nodo corrente è libero quindi lo imposto a False
                        else:
                            node_visited[y].insert(x, False)
                
                # Matrice a 3 dimensioni: per ogni formica, creo una matrice a 2 dimensioni quadrata contenente inizialmente tutti None
                # Questa matrice servirà a tenere traccia degli incrementi di feromone per ogni formica
                tau_tensor = [[[None for _ in range(last_node_id+2)] for _ in range(last_node_id+2)] for _ in range(ants)]

                # Matrice quadrata a 2 dimensioni contenente inizialmente tutti 0
                update_matrix = [[0 for _ in range(last_node_id+2)] for _ in range(last_node_id+2)]
                
                # Lista di routes una per ogni formica contenenti inizialmente il nodo cursore dove si trova attualmente il driver
                ants_list = []
                for i in range(ants):
                    ants_list.append([driver['snake'][-1]])

                # Finchè tutte le formiche non sono arrivate in università
                all_ants_origin = False
                while not all_ants_origin:
                    
                    # Ciclo per ogni formica
                    for id_ant, ant_path in enumerate(ants_list):
                        
                        # Estraggo la posizione attuale del cursore della formica corrente
                        cursor = ant_path[-1]
                        
                        # Se la formica è arrivata in università ripeti il ciclo passando alla formica successiva
                        if cursor == origin_node[0]:
                            continue
                        
                        # Se la formica corrente ha una route composta da meno di 5 nodi (Es: [1,7,8,9, _]) posso inserire un ultimo passeggero
                        if len(ant_path) < 5:
                            # Calcolo prossimo nodo passeggero o università per la formica corrente
                            next_node = get_next_node(cursor, G_complete, id_ant, node_visited, alpha, beta, gamma)
                        
                        # Altrimenti chiudo la route della formica corrente aggiungendoci l'id del nodo università
                        else:
                            next_node = origin_node[0]
                        
                        # Aggiungo il nodo selezionato alla route della formica corrente
                        ants_list[id_ant].append(next_node)

                        # Imposto a True l'elemento nella matrice a 2 dimensioni dei nodi visitati per ogni formica
                        node_visited[id_ant][next_node] = True

                    # Controllo se tutte le formiche sono giunte in università
                    for i in range(len(node_visited)):
                        if node_visited[i][origin_node[0]]:
                            all_ants_origin = True
                            continue
                        else:
                            all_ants_origin = False
                            break
                
                # Aggiornamento dei valori di feromoni per ogni arco
                # Nella matrice a 3 dimensioni tau_tensor imposto il nuovo valore di feromone per la corrente formica
                for ant_id, ant_path in enumerate(ants_list):
                    path_distance = 0
                    path_saving = 0
                    for node_index, _ in enumerate(ant_path):
                        try:
                            path_distance_temp = G_complete[ant_path[node_index]][ant_path[node_index+1]]['distance']
                            path_distance = path_distance + path_distance_temp
                            path_saving_temp = int(round(haversine(G_complete.nodes[ant_path[node_index]]['g'], origin_node[1]['g'], unit=Unit.METERS) - haversine(G_complete.nodes[ant_path[node_index]]['g'], G_complete.nodes[ant_path[node_index+1]]['g'], unit=Unit.METERS)))
                            # path_saving_temp = haversine(G_complete.nodes[ant_path[node_index]]['g'], origin_node[1]['g'], unit=Unit.METERS) / haversine(G_complete.nodes[ant_path[node_index]]['g'], G_complete.nodes[ant_path[node_index+1]]['g'], unit=Unit.METERS)
                            path_saving = path_saving + path_saving_temp
                            tau_tensor[ant_id][ant_path[node_index]].insert(ant_path[node_index+1], path_saving_temp/path_distance_temp)
                        except:
                            pass

                # Per ogni formica, nella matrice update_matrix memorizzo il valore del feromone sommandoci tutti quelli delle altre per lo stesso arco (node_i, node_j)
                for ant_id, _ in enumerate(tau_tensor):
                    for node_i, _ in enumerate(tau_tensor[ant_id]):
                        for node_j, increment in enumerate(tau_tensor[ant_id][node_i]):
                            if increment != None:
                                update_matrix[node_i][node_j] += increment

                # Estraggo dalla matrice update_matrix il minimo e massimo incremento
                min_increment = min([min(x) for x in update_matrix])
                max_increment = max([max(x) for x in update_matrix])

                # Clone della matrice update_matrix con tutti valori 0 iniziali pronta per essere aggiornata con i valori normalizzati degli incrementi
                update_matrix_normalized = [[0 for _ in range(last_node_id+2)] for _ in range(last_node_id+2)]
                
                # Normalizzo i valori di incremento memorizzandoli nella nuova matrice update_matrix_normalized
                for node_i, _ in enumerate(update_matrix):
                    for node_j, _ in enumerate(update_matrix[node_i]):
                        if update_matrix[node_i][node_j] != 0:
                            update_matrix_normalized[node_i][node_j] = (update_matrix[node_i][node_j]-min_increment)/(max_increment-min_increment)
                
                # Aggiorno i valori di feromone degli archi spazzati dalle formiche anche sul grafo, ma solo se maggiori di 0 poiché impossibili valori negativi
                # Attenzione: li aggiorno considerando anche l'evaporazione
                G_update = copy.deepcopy(G_complete)
                for node_i, _ in enumerate(update_matrix_normalized[:-1]):
                    for node_j, _ in enumerate(update_matrix_normalized[node_i][:-1]):
                        if update_matrix_normalized[node_i][node_j] != 0 and node_i != node_j:
                            G_update[node_i][node_j]['pheromone'] = max((1-p)*G_update[node_i][node_j]['pheromone']+update_matrix_normalized[node_i][node_j], 0)
            
            # Cerco l'id del nodo, connesso a quello su cui il driver attualmente è posizionato, con arco con feromone massimo
            max_pheromone = 0
            max_edge_id = None
            for node_i in G_update.nodes(data=True):
                if node_i[0] == driver['snake'][-1]:
                    for node_j in G_update.nodes(data=True):
                        if node_j[1]['s'] == NodeStatus.FREE.value:
                            if node_i[0] != node_j[0] and node_j[1]['t'] != NodeType.DRIVER.value and G_update[node_i[0]][node_j[0]]['pheromone'] > max_pheromone:
                                max_pheromone = G_update[node_i[0]][node_j[0]]['pheromone']
                                max_edge_id = node_j[0]

            # Aggiungo alla route del driver corrente il nodo collegato con l'arco con feromone più alto
            drivers_ordered[driver_id]['snake'].append(max_edge_id)

            # Se il nodo selezionato è diverso da quello dell'università allora lo occupo poiché prenotato dal driver corrente e ne cambio lo status a visitato
            if max_edge_id != origin_node[0]:
                node_occupied.add(max_edge_id)
            if max_edge_id != origin_node[0]:
                G_update.nodes[max_edge_id]['s'] = NodeStatus.VISITED.value

            G_complete = copy.deepcopy(G_update)

        # Finché tutti i driver non sono giunti in università continuo il ciclo
        for _, driver in drivers_ordered.items():
            if driver['snake'][-1] == origin_node[0]:
                all_drivers_origin = True
                continue
            else:
                all_drivers_origin = False
                break

        # Sovrascrivo il grafo con la sua versione aggiornata con un nodo in più per ogni route di ogni driver
        G_complete = copy.deepcopy(G_complete)

        # Ordino i driver per distanza percorsa
        for _, driver in drivers_ordered.items():
            total_distance = 0
            for node_id, node in enumerate(driver['snake']):

                if node != origin_node[0]:
                    G_update.nodes[node]['s'] = NodeStatus.VISITED.value

                try:
                    node_i = driver['snake'][node_id]
                    node_j = driver['snake'][node_id+1]
                    total_distance = total_distance + haversine(G_update.nodes[node_i]['g'], G_update.nodes[node_j]['g'], unit=Unit.METERS)
                except:
                    pass
            driver['distance'] = total_distance

        drivers_ordered = dict(sorted(drivers_ordered.items(), key=lambda driver: driver[1]['distance']))

    # Creo il grafo finale partendo da uno senza archi
    G_final = nx.create_empty_copy(G)

    # Aggiungo al grafo finale gli archi dalle liste delle routes di ogni driver
    add_edges = []
    for _, value in drivers_ordered.items():
        for id_node, _ in enumerate(value['snake']):
            try:
                node_i = value['snake'][id_node]
                node_j = value['snake'][id_node+1]
                distance = haversine(G_final.nodes[node_i]['g'], G_final.nodes[node_j]['g'], unit=Unit.METERS)
                add_edges.append((node_i, node_j, { 'distance': int(round(distance)) }))
            except:
                pass
    G_final.add_edges_from(add_edges)

    return G_final, []

def string_exchange(G, k=1000):
    origin_node = generator.get_origin_node()
    generator.show_graph(G)

    routes = []
    for node in G.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            paths = nx.all_simple_paths(G, node[0], origin_node[0])
            for path in list(paths):
                routes.append(path)

    if len(routes) > 1:
        partial_distance = []

        for _ in range(k):
            path1, path2 = random.sample(range(0, len(routes)), 2)

            if len(routes[path1]) < 3 or len(routes[path2]) < 3:
                continue

            node1 = random.randint(1, len(routes[path1]) - 2)
            node2 = random.randint(1, len(routes[path2]) - 2)

            G1 = copy.deepcopy(G)
            
            G1.remove_edge(routes[path1][node1-1], routes[path1][node1])
            G1.remove_edge(routes[path1][node1], routes[path1][node1+1])
            G1.remove_edge(routes[path2][node2-1], routes[path2][node2])
            G1.remove_edge(routes[path2][node2], routes[path2][node2+1])

            add_edges = []
            if not G1.has_edge(routes[path1][node1-1], routes[path2][node2]):
                add_edges.append((routes[path1][node1-1], routes[path2][node2], { 'distance': int(round(haversine(G1.nodes[routes[path1][node1-1]]['g'], G1.nodes[routes[path2][node2]]['g'], unit=Unit.METERS))) }))
            if not G1.has_edge(routes[path2][node2], routes[path1][node1+1]):
                add_edges.append((routes[path2][node2], routes[path1][node1+1], { 'distance': int(round(haversine(G1.nodes[routes[path2][node2]]['g'], G1.nodes[routes[path1][node1+1]]['g'], unit=Unit.METERS))) }))
            if not G1.has_edge(routes[path2][node2-1], routes[path1][node1]):
                add_edges.append((routes[path2][node2-1], routes[path1][node1], { 'distance': int(round(haversine(G1.nodes[routes[path2][node2-1]]['g'], G1.nodes[routes[path1][node1]]['g'], unit=Unit.METERS))) }))
            if not G1.has_edge(routes[path1][node1], routes[path2][node2+1]):
                add_edges.append((routes[path1][node1], routes[path2][node2+1], { 'distance': int(round(haversine(G1.nodes[routes[path1][node1]]['g'], G1.nodes[routes[path2][node2+1]]['g'], unit=Unit.METERS))) }))
            G1.add_edges_from(add_edges)

            total_distance_G = generator.get_total_distance(G)
            total_distance_G1 = generator.get_total_distance(G1)
            if total_distance_G1 < total_distance_G:
                routes[path1][node1], routes[path2][node2] = routes[path2][node2], routes[path1][node1]
                generator.show_graph(G1, True, True)
                G = G1
                partial_distance.append(total_distance_G1)
            else:
                partial_distance.append(total_distance_G)
        
    return G, partial_distance

def string_relocation(G, k=1000):
    origin_node = generator.get_origin_node()
    generator.show_graph(G)

    routes = []
    for node in G.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            paths = nx.all_simple_paths(G, node[0], origin_node[0])
            for path in list(paths):
                routes.append(path)

    if len(routes) > 1:
        partial_distance = []

        for _ in range(k):
            path1, path2 = random.sample(range(0, len(routes)), 2)

            if len(routes[path1]) < 3 or len(routes[path2]) > 4:
                continue

            node1 = random.randint(1, len(routes[path1]) - 2)
            node2 = random.randint(0, len(routes[path2]) - 2)

            G1 = copy.deepcopy(G)
            
            G1.remove_edge(routes[path1][node1-1], routes[path1][node1])
            G1.remove_edge(routes[path1][node1], routes[path1][node1+1])
            
            G1.remove_edge(routes[path2][node2], routes[path2][node2+1])

            add_edges = []
            if not G1.has_edge(routes[path1][node1-1], routes[path1][node1+1]):
                add_edges.append((routes[path1][node1-1], routes[path1][node1+1], { 'distance': int(round(haversine(G1.nodes[routes[path1][node1-1]]['g'], G1.nodes[routes[path1][node1+1]]['g'], unit=Unit.METERS))) }))
            if not G1.has_edge(routes[path2][node2], routes[path1][node1]):
                add_edges.append((routes[path2][node2], routes[path1][node1], { 'distance': int(round(haversine(G1.nodes[routes[path2][node2]]['g'], G1.nodes[routes[path1][node1]]['g'], unit=Unit.METERS))) }))
            if not G1.has_edge(routes[path1][node1], routes[path2][node2+1]):
                add_edges.append((routes[path1][node1], routes[path2][node2+1], { 'distance': int(round(haversine(G1.nodes[routes[path1][node1]]['g'], G1.nodes[routes[path2][node2+1]]['g'], unit=Unit.METERS))) }))
            G1.add_edges_from(add_edges)

            total_distance_G = generator.get_total_distance(G)
            total_distance_G1 = generator.get_total_distance(G1)
            if total_distance_G1 < total_distance_G:
                routes[path2].insert(node2+1, routes[path1][node1])
                del routes[path1][node1]
                generator.show_graph(G1, True, True)
                G = G1
                partial_distance.append(total_distance_G1)
            else:
                partial_distance.append(total_distance_G)
        
    return G, partial_distance

def simulated_annealing(X):
    
    # Temperatura di partenza, finale e tasso di raffreddamento
    T0 = 900
    Tf = 0.1
    alpha = 0.92
    
    I = 0
    Iter = 400
    N = 0
    NIter = 100

    # L'algoritmo inizialmente parte da una temperatura alta
    T = T0

    # All'inizio come soluzione migliore salvo quella iniziale
    XBest = copy.deepcopy(X)
    FBest = generator.get_total_distance(X)

    origin_node = generator.get_origin_node()
    generator.show_graph(X)

    # Ottengo le routes del grafo passato come input
    routes = []
    for node in X.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            paths = nx.all_simple_paths(X, node[0], origin_node[0])
            for path in list(paths):
                routes.append(path)
    
    # Se c'è almeno una route
    if len(routes) > 1:
        partial_distance = []

        # Finchè la temperatura corrente è maggiore di quella finale
        while T > Tf:

            # Finché non si raggiunge il numero massimo di iterazioni
            I = 0
            while I < Iter:

                # Seleziono casualmente due route
                path1, path2 = random.sample(range(0, len(routes)), 2)

                # Se almeno una delle route selezionate non ha passeggeri riprovo al successivo ciclo
                if len(routes[path1]) < 3 or len(routes[path2]) < 3:
                    continue

                # Seleziono casualmente due passeggeri delle due rispettive route
                node1 = random.randint(1, len(routes[path1]) - 2)
                node2 = random.randint(1, len(routes[path2]) - 2)

                Y = copy.deepcopy(X)
                
                # Rimuovo gli archi connessi ai passeggeri selezionati
                Y.remove_edge(routes[path1][node1-1], routes[path1][node1])
                Y.remove_edge(routes[path1][node1], routes[path1][node1+1])
                Y.remove_edge(routes[path2][node2-1], routes[path2][node2])
                Y.remove_edge(routes[path2][node2], routes[path2][node2+1])

                # Aggiungo gli archi per riconnettere i nodi
                add_edges = []
                if not Y.has_edge(routes[path1][node1-1], routes[path2][node2]):
                    add_edges.append((routes[path1][node1-1], routes[path2][node2], { 'distance': int(round(haversine(Y.nodes[routes[path1][node1-1]]['g'], Y.nodes[routes[path2][node2]]['g'], unit=Unit.METERS))) }))
                if not Y.has_edge(routes[path2][node2], routes[path1][node1+1]):
                    add_edges.append((routes[path2][node2], routes[path1][node1+1], { 'distance': int(round(haversine(Y.nodes[routes[path2][node2]]['g'], Y.nodes[routes[path1][node1+1]]['g'], unit=Unit.METERS))) }))
                if not Y.has_edge(routes[path2][node2-1], routes[path1][node1]):
                    add_edges.append((routes[path2][node2-1], routes[path1][node1], { 'distance': int(round(haversine(Y.nodes[routes[path2][node2-1]]['g'], Y.nodes[routes[path1][node1]]['g'], unit=Unit.METERS))) }))
                if not Y.has_edge(routes[path1][node1], routes[path2][node2+1]):
                    add_edges.append((routes[path1][node1], routes[path2][node2+1], { 'distance': int(round(haversine(Y.nodes[routes[path1][node1]]['g'], Y.nodes[routes[path2][node2+1]]['g'], unit=Unit.METERS))) }))
                Y.add_edges_from(add_edges)

                # Ottengo la lunghezza totale del grafo
                total_distance_Y = generator.get_total_distance(Y)
                total_distance_X = generator.get_total_distance(X)

                # Se la differenza tra la lunghezza totale del nuovo grafo è minore del migliore
                delta = total_distance_Y - total_distance_X
                if delta < 0:

                    # Sostituisco il grafo con quello corrente migliore
                    X = copy.deepcopy(Y)

                    # Eseguo una operazione di swap delle route
                    routes[path1][node1], routes[path2][node2] = routes[path2][node2], routes[path1][node1]

                    # Mostro il grafo corrente migliore
                    # generator.show_graph(Y, True, True)

                    # Salvo la lunghezza totale del grafo
                    partial_distance.append(total_distance_Y)

                    # Se la lunghezza totale è inferiore di quella migliore
                    if total_distance_Y < FBest:
                        # Salvo la lunghezza totale e il grafo corrente
                        FBest = total_distance_Y
                        XBest = copy.deepcopy(Y)

                    # Resetto lo stallo
                    N = 0
                
                # Altrimenti c'è la possibilità di accettare un peggioramento
                else:
                    # Genero casualmente un numero compreso tra 0 e 1
                    r = random.uniform(0, 1)

                    # Se il numero generato è inferiore alla formula e^(-delta/T) allora accetto il peggioramento
                    if r < math.exp(-delta/T):
                        # Sostituisco il grafo con quello corrente peggiore
                        X = copy.deepcopy(Y)

                        # Eseguo una operazione di swap delle route
                        routes[path1][node1], routes[path2][node2] = routes[path2][node2], routes[path1][node1]

                        # Mostro il grafo corrente peggiore
                        # generator.show_graph(Y, True, True)
                        
                        # Salvo la lunghezza totale del grafo corrente
                        partial_distance.append(total_distance_Y)

                        # Resetto lo stallo
                        N = 0
                    
                    # Altrimenti se non accetto il peggioramento incremento lo stallo e se superato il massimo di iterazioni peggiorative esco dal ciclo delle iterazioni per cambiare la temperatura
                    else:
                        N = N + 1
                        if N > NIter:
                            break
                
                # Incremento il numero di iterazioni
                I = I + 1
            else:
                # Diminuisco la temperatura se nel ciclo più interno ho accettato un miglioramento o un peggioramento
                T = T*alpha
            break

    return XBest, partial_distance

def tabu_search(S):

    origin_node = generator.get_origin_node()
    generator.show_graph(S)

    SBest = copy.deepcopy(S)
    FSBest = generator.get_total_distance(SBest)
    FSCurrent = FSBest
    search_max = 100
    search = 0
    Niter = 1000
    N = 0
    stall = 0
    stall_max = 50
    tabu_list = queue.Queue(5)

    # Creo le routes dei driver
    routes = []
    for node in S.nodes(data=True):
        if node[1]['t'] == NodeType.DRIVER.value:
            paths = nx.all_simple_paths(S, node[0], origin_node[0])
            for path in list(paths):
                routes.append(path)

    routes_alias = copy.deepcopy(routes)
    
    partial_distance = []
    
    # Se c'è almeno una route di un driver
    if len(routes_alias) > 1:
        S1 = copy.deepcopy(S)
        
        # Ciclo finché non raggiungo il numero massimo di iterazioni oppure lo stallo massimo
        while N < Niter and stall < stall_max:
            moves = []
            search = 0

            # Ciclo finché non raggiungo il numero di mosse di ricerche locali massime
            while search < search_max:
                S2 = copy.deepcopy(S1)
                routes_temp = copy.deepcopy(routes_alias)

                # Estraggo a caso 2 indici corrispondenti alle routes dei driver
                path1, path2 = random.sample(range(0, len(routes_temp)), 2)

                # Se almeno una delle routes selezionate è senza passeggeri allora riprova al prossimo ciclo senza incrementare variabile search
                if len(routes_temp[path1]) < 3 or len(routes_temp[path2]) < 3:
                    continue

                # Seleziono casualmente 2 indici corrispondenti ai passeggeri delle routes selezionate
                node1 = random.randint(1, len(routes_temp[path1]) - 2)
                node2 = random.randint(1, len(routes_temp[path2]) - 2)
                
                # Applico come mossa una string exchange (swap): il nodo1 verrà collegato con la route2 e viceversa
                S2.remove_edge(routes_temp[path1][node1-1], routes_temp[path1][node1])
                S2.remove_edge(routes_temp[path1][node1], routes_temp[path1][node1+1])
                S2.remove_edge(routes_temp[path2][node2-1], routes_temp[path2][node2])
                S2.remove_edge(routes_temp[path2][node2], routes_temp[path2][node2+1])

                add_edges = []
                if not S2.has_edge(routes_temp[path1][node1-1], routes_temp[path2][node2]):
                    add_edges.append((routes_temp[path1][node1-1], routes_temp[path2][node2], { 'distance': int(round(haversine(S2.nodes[routes_temp[path1][node1-1]]['g'], S2.nodes[routes_temp[path2][node2]]['g'], unit=Unit.METERS))) }))
                if not S2.has_edge(routes_temp[path2][node2], routes_temp[path1][node1+1]):
                    add_edges.append((routes_temp[path2][node2], routes_temp[path1][node1+1], { 'distance': int(round(haversine(S2.nodes[routes_temp[path2][node2]]['g'], S2.nodes[routes_temp[path1][node1+1]]['g'], unit=Unit.METERS))) }))
                if not S2.has_edge(routes_temp[path2][node2-1], routes_temp[path1][node1]):
                    add_edges.append((routes_temp[path2][node2-1], routes_temp[path1][node1], { 'distance': int(round(haversine(S2.nodes[routes_temp[path2][node2-1]]['g'], S2.nodes[routes_temp[path1][node1]]['g'], unit=Unit.METERS))) }))
                if not S2.has_edge(routes_temp[path1][node1], routes_temp[path2][node2+1]):
                    add_edges.append((routes_temp[path1][node1], routes_temp[path2][node2+1], { 'distance': int(round(haversine(S2.nodes[routes_temp[path1][node1]]['g'], S2.nodes[routes_temp[path2][node2+1]]['g'], unit=Unit.METERS))) }))
                S2.add_edges_from(add_edges)

                # Calcolo distanze totali del grafo originale e del nuovo grafo con la mossa applicata
                total_distance_S1 = generator.get_total_distance(S1)
                total_distance_S2 = generator.get_total_distance(S2)

                # Se il nuovo grafo ha distanza totale inferiore a quello originale
                if total_distance_S2 < total_distance_S1:
                    # Allora aggiungo la mossa migliorativa nella lista tabù
                    moves.append((((path1, node1), (path2, node2)), S2, total_distance_S2))
                
                # Che sia peggiorativa o migliroativa la mossa incremento il numero di iterazioni di ricerca locale
                search = search + 1
            
            # Se delle mosse applicate nessuna è di miglioramento oppure non se ne sono trovate di possibili semplicemente, allora fermo e riavvio il ciclo di ricerca locale
            if len(moves) < 1:
                break
            
            # Altrimenti ordino le mosse dalla migliore alla peggiore in base alle distanze totali dei grafi ottenuti
            moves_ordered = sorted(moves, key=lambda item: item[2])
            
            # Estraggo la migliore mossa accoppiata con il suo grafo soluzione dalla lista delle mosse ordinate
            next_move = moves_ordered[0]

            # Estraggo la mossa sottoforma di ((path1, node1), path2, node2)
            next_exchange = next_move[0]

            # Estraggo il grafo aggiornato con la migliore mossa tra quelle provate precedentemente
            next_G = copy.deepcopy(next_move[1])

            # Estraggo la distanza totale del grafo aggiornato con la migliore mossa applicata
            next_FSBest = next_move[2]

            # Estraggo dalla tupla ((path1, node1), path2, node2) della migliore mossa trovata i singoli valori
            next_path1 = next_exchange[0][0]
            next_node1 = next_exchange[0][1]

            next_path2 = next_exchange[1][0]
            next_node2 = next_exchange[1][1]

            # Se la distanza totale del grafo aggiornato con la migliore mossa trovata è minore di quella trovata al ciclo precedente
            # Oppure se la mossa trovata non è presente nella lista tabù (Notare il doppio controllo necessario per via degli archi non ordientati)
            if next_FSBest < FSCurrent or (((next_path1, next_node1), (next_path2, next_node2)) not in tabu_list.queue and ((next_path2, next_node2), (next_path1, next_node1)) not in tabu_list.queue):
                
                # Allora prima di tutto applico la mossa sulle liste delle due route selezionate 
                routes_alias[next_path1][next_node1], routes_alias[next_path2][next_node2] = routes_alias[next_path2][next_node2], routes_alias[next_path1][next_node1]
                S1 = copy.deepcopy(next_G)
                
                # Se la mossa trova una soluzione migliore di quella trovata fino ad ora
                if next_FSBest < FSBest:
                    # Allora salvo il suo grafo e sovrascrivo la distanza totale minima fino ad ora trovata resettando infine lo stallo
                    SBest = copy.deepcopy(next_G)
                    FSBest = next_FSBest
                    stall = 0
                else:
                    # Altrimenti se la mossa non è migliore di quella fino ad ora trovata allora incremento lo stallo
                    stall = stall + 1
     
                # Se la lista tabu è piena e non vuota, allora rimuovo il più vecchio elemento della coda FIFO
                if tabu_list.full() and not tabu_list.empty():
                    tabu_list.get()
                
                # Aggiungo la mossa alla lista tabù
                tabu_list.put(next_exchange)
     
                # Mostro il grafo con la mossa applicata
                # generator.show_graph(S1, True, True)
            
            partial_distance.append(next_FSBest)
            
            # Sovrascrivo il costo della funzione obiettivo con quello corrente trovato
            FSCurrent = next_FSBest

            # Incremento il numero di iterazioni
            N = N + 1

    # Ritorno il grafo con le migliori mosse trovate e applicate
    return SBest, partial_distance

clear()

#print('Operative Research - University of Ferrara, Italy - A.A. 2020/21')
#print('Andrea Bazerla - 151792')
#print()

results = {}

if __name__=='__main__':
    while(True):

        sub_menu = False
        output = False
        menu_option = ''

        print_menu()

        try:
            menu_option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a valid number...')

        if menu_option == 1:
            generate_instance()
            clear()

            print('Instance created :)\n')
            continue

        elif menu_option == 2:
            clear()
            file_name = ''

            try:
                file_name = input('Insert file name: ')
            except:
                print('Wrong input. Please enter a valid number...')

            G = Generator.read_graph(file_name)
            
            instance_generated = True

            clear()
            print('Graph imported :)\n')

        elif menu_option == 3:
            clear()
            file_name = ''

            try:
                file_name = input('Insert file name: ')
            except:
                print('Wrong input. Please enter a valid number...')

            origin_coordinates = generator.get_origin_coordinates()
            G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
            generator.write_graph(G, file_name)
            clear()
            print('Graph exported :)\n')

        elif menu_option == 4:
            if instance_generated == True:
                while(True):
                    if output == False:
                        clear()
                    output = False
                    
                    print_menu_show_instance()
                
                    menu_option_create_solution = ''
                    
                    try:
                        menu_option_create_solution = int(input('Enter the solution: '))
                    except:
                        print('Wrong input. Please enter a valid number...')

                    if menu_option_create_solution == 1:
                        generator.show_distances_distribution()
                    elif menu_option_create_solution == 2:
                        generator.show_angles_distribution()
                    elif menu_option_create_solution == 3:
                        generator.show_polar_coordinates()
                    elif menu_option_create_solution == 4:
                        generator.show_cartesian_coordinates()
                    elif menu_option_create_solution == 5:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        clear()
                        print('Total distance:', str(generator.get_total_distance(G)/1000) + 'km\n')
                        output = True
                    elif menu_option_create_solution == 6:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        generator.show_graph(G)
                    elif menu_option_create_solution == 7:
                        generator.show_map(ORIGIN, upp, drivers_coordinates, passengers_coordinates)
                    elif menu_option_create_solution == 0:
                        clear()
                        sub_menu = True
                        break
                    else:
                        clear()
                        print('Invalid option. Please enter a valid number...(1)\n')
            else:
                clear()
                print('Invalid option. Please enter a valid number...(2)\n')
                continue

        elif menu_option == 5:
            if instance_generated == True:
                while(True):
                    if output == False:
                        clear()
                    output = False

                    print_menu_create_solution(results)

                    menu_option_create_solution = ''

                    try:
                        menu_option_create_solution = int(input('Choose new solution: '))
                    except:
                        print('Wrong input. Please enter a valid number...')
                    
                    if menu_option_create_solution == 1:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        generator.show_graph(G)
                        random_greedy_returns = random_greedy(G)
                        G1_random_greedy = random_greedy_returns
                        generator.show_graph(G1_random_greedy)
                        clear()
                        random_greedy_result = generator.get_total_distance(G1_random_greedy)/1000
                        results['random_greedy'] = random_greedy_result
                        output = True
                    elif menu_option_create_solution == 2:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        nearest_neighbor_returns = nearest_neighbor(G)
                        G1_nearest_neighbor = nearest_neighbor_returns[0]
                        generator.show_graph(G1_nearest_neighbor)
                        plt.plot(nearest_neighbor_returns[1])
                        plt.ylim([0, nearest_neighbor_returns[1][0]])
                        plt.show()
                        clear()
                        nearest_neighbor_result = generator.get_total_distance(G1_nearest_neighbor)/1000
                        results['nearest_neighbor'] = nearest_neighbor_result
                        output = True
                    elif menu_option_create_solution == 3:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        clarke_wright_returns = clarke_wright(G)
                        G1_clarke_wright = clarke_wright_returns[0]
                        generator.show_graph(G1_clarke_wright)
                        plt.plot(clarke_wright_returns[1])
                        plt.ylim([0, clarke_wright_returns[1][0]])
                        plt.show()
                        clear()
                        clarke_wright_result = generator.get_total_distance(G1_clarke_wright)/1000
                        results['clarke_wright'] = clarke_wright_result
                        output = True
                    elif menu_option_create_solution == 4:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        generator.show_graph(G)
                        genetic_algorithm_returns = genetic_algorithm(G)
                        G1_genetic_algorithm = genetic_algorithm_returns[0]
                        generator.show_graph(G1_genetic_algorithm)
                        plt.plot(genetic_algorithm_returns[1])
                        plt.ylim([0, genetic_algorithm_returns[1][0]])
                        plt.show()
                        clear()
                        genetic_algorithm_result = generator.get_total_distance(G1_genetic_algorithm)/1000
                        results['genetic_algorithm'] = genetic_algorithm_result
                        output = True
                    elif menu_option_create_solution == 5:
                        origin_coordinates = generator.get_origin_coordinates()
                        G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                        generator.show_graph(G)
                        ant_colony_optimization_returns = ant_colony_optimization(G)
                        G1_ant_colony_optimization = ant_colony_optimization_returns[0]
                        generator.show_graph(G1_ant_colony_optimization)
                        # plt.plot(ant_colony_optimization_returns[1])
                        # plt.ylim([0, ant_colony_optimization_returns[1][0]])
                        # plt.show()
                        clear()
                        ant_colony_optimization_result = generator.get_total_distance(G1_ant_colony_optimization)/1000
                        results['ant_colony_optimization'] = ant_colony_optimization_result
                        output = True
                    elif menu_option_create_solution == 0:
                        clear()
                        sub_menu = True
                        break
                    else:
                        clear()
                        print('Invalid option. Please enter a valid number...(4)\n')

            else:
                clear()
                print('Invalid option. Please enter a valid number...(2)\n')
                continue

        elif menu_option == 6:
            while(True):
                if output == False:
                    clear()
                output = False

                print_menu_improve_solution(results)

                try:
                    menu_option_improve_solution = int(input('Enter the improvement: '))
                except:
                    print('Wrong input. Please enter a valid number...')
                
                if menu_option_improve_solution == 1:
                    string_exchange_returns = string_exchange(G)
                    G1_string_exchange = string_exchange_returns[0]
                    generator.show_graph(G1_string_exchange)
                    plt.plot(string_exchange_returns[1])
                    plt.ylim([0, max(string_exchange_returns[1])])
                    plt.show()
                    clear()
                    string_exchange_result = generator.get_total_distance(G1_string_exchange)/1000
                    results['string_exchange'] = string_exchange_result
                    output = True
                elif menu_option_improve_solution == 2:
                    string_relocation_returns = string_relocation(G)
                    G1_string_relocation = string_relocation_returns[0]
                    generator.show_graph(G1_string_relocation)
                    plt.plot(string_relocation_returns[1])
                    if len(string_relocation_returns[1]) > 0:
                        plt.ylim([0, max(string_relocation_returns[1])])
                    plt.show()
                    clear()
                    string_relocation_result = generator.get_total_distance(G1_string_relocation)/1000
                    results['string_relocation'] = string_relocation_result
                    output = True
                elif menu_option_improve_solution == 3:
                    simulated_annealing_returns = simulated_annealing(G)
                    G1_simulated_annealing = simulated_annealing_returns[0]
                    generator.show_graph(G1_simulated_annealing)
                    plt.plot(simulated_annealing_returns[1])
                    if len(simulated_annealing_returns[1]) > 0:
                        plt.ylim([0, max(simulated_annealing_returns[1])])
                    plt.show()
                    clear()
                    simulated_annealing_result = generator.get_total_distance(G1_simulated_annealing)/1000
                    results['simulated_annealing'] = simulated_annealing_result
                    output = True
                elif menu_option_improve_solution == 4:
                    tabu_search_returns = tabu_search(G)
                    G1_tabu_search = tabu_search_returns[0]
                    generator.show_graph(G1_tabu_search)
                    plt.plot(tabu_search_returns[1])
                    if len(tabu_search_returns[1]) > 0:
                        plt.ylim([0, max(tabu_search_returns[1])])
                    plt.show()
                    clear()
                    tabu_search_result = generator.get_total_distance(G1_tabu_search)/1000
                    results['tabu_search'] = tabu_search_result
                    output = True
                elif menu_option_improve_solution == 0:
                    clear()
                    sub_menu = True
                    break
                else:
                    clear()
                    print('Invalid option. Please enter a valid number...(4)\n')

        elif menu_option == 7:
            if instance_generated == True:
                origin_coordinates = generator.get_origin_coordinates()
                G = generator.build_graph(origin_coordinates, drivers_coordinates, passengers_coordinates)
                clear()
                total_distance = generator.get_total_distance(G)/1000
                print('Total initial distance:', str(total_distance) + 'km')
                if 'nearest_neighbor' in results:
                    print('Nearest Neighbor:', str(results['nearest_neighbor']) + 'km', '(-' + str(round(100 - results['nearest_neighbor']*100/total_distance, 1)) + '%)')
                if 'string_exchange' in results:
                    print('String Exchange:', str(results['string_exchange']) + 'km', '(-' + str(round(100 - results['string_exchange']*100/total_distance, 1)) + '%)')
                print()
                output = True
            else:
                clear()
                print('Invalid option. Please enter a valid number...(2)\n')
                continue
        
        elif menu_option == 0:
            clear()
            exit()
        
        else:
            if sub_menu == True:
                sub_menu = False
            else:
                clear()
                print('Invalid option. Please enter a valid number...(3)\n')