import random
import math

# Функция для расчета длины маршрута
def get_route_length(route, edges):
    length = 0
    #route.append(route[0])
    for i in range(len(route)-1):
        id1 = route[i]
        id2 = route[i+1]
        for j in edges:
            if id1 in j and id2 in j:
                length += j[2]
    return length


# Функция для генерации начального маршрута
def generate_initial_route(n):
    route = list(range(n))
    random.shuffle(route)
    return route


# Функция для генерации нового маршрута
def generate_new_route(route):
    i = random.randint(0, len(route) - 1)
    j = random.randint(0, len(route) - 1)
    new_route = route.copy()
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


# Функция для вычисления вероятности принятия нового маршрута
def get_acceptance_probability(current_length, new_length, temperature):
    if new_length < current_length:
        return 1.0
    else:
        return math.exp((current_length - new_length) / temperature)


# Функция решения задачи коммивояжера методом отжига
def solve_tsp_with_simulated_annealing(mass):
    k = 0
    canvas = mass[0]
    stemperature = int(mass[1].get())
    ftemperature = float(mass[2].get())
    cooling_rate = float(mass[3].get())
    canvas.best_edges_delete()
    canvas.edges_mass = canvas.table.check_data(canvas.edges_mass)
    vertices, edges = canvas.circle_mass, canvas.edges_mass

    current_route = generate_initial_route(len(vertices))
    best_route = current_route.copy()
    current_length = get_route_length(current_route, edges)
    best_length = current_length

    while stemperature > ftemperature:
        k+=1
        new_route = generate_new_route(current_route)
        new_length = get_route_length(new_route, edges)
        acceptance_probability = get_acceptance_probability(current_length, new_length, stemperature)

        if acceptance_probability > random.random():
            current_route = new_route.copy()
            current_length = new_length

        if current_length < best_length:
            best_route = current_route.copy()
            best_length = current_length

        stemperature *= 1 - cooling_rate
    best_route.append(best_route[0])
    canvas.best_way = best_route
    canvas.best_weight = best_length
    canvas.all_edges_hidden(True)
    canvas.counter = k
    canvas.draw_best_way()

    return canvas
