#Projekt AN 142447

import matplotlib.pyplot as plt

#wczytywanie danych
def wczytaj_dane(plik):
    dane = {}

    with open(plik, 'r') as plik:
        for linia in plik:
            elementy = linia.strip().split(',')

            x = float(elementy[0])
            y = float(elementy[1])
            fxy = float(elementy[2])

            if y not in dane:
                dane[y] = {'x': [], 'fx': []}

            dane[y]['x'].append(x)
            dane[y]['fx'].append(fxy)

    return dane

#wizualizacja danych
def wizualizacja(dane, packet_size = 6):
    if packet_size <= 0:
        return

    y_list = list(dane.keys())
    y_size = len(y_list)

    for i in range(0, y_size, packet_size):
        y_packet = y_list[i: i + packet_size]
        plt.figure(figsize=(16, 10))

        for y in y_packet:
            plt.plot(dane[y]['x'], dane[y]['fx'], label=f'y={y}')

        if packet_size == 1:
            plt.title(f"Wykresy F(x,y) dla y = {y_packet[0]}")
        else:
            plt.title(f"Wykresy F(x,y) dla y od {y_packet[0]} do {y_packet[-1]}")
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.xlabel("x")
        plt.ylabel("F(x,y)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

#obliczanie statystyk z podzialem na wspolrzedne y
def oblicz_statystyki(data):
    stats = {'y': [], 'srednia': [], 'mediana': [], 'odchylenie': []}

    for y in sorted(data.keys()):
        f_values = data[y]['fx']

        stats['y'].append(y)
        stats['srednia'].append(oblicz_srednia(f_values))
        stats['mediana'].append(oblicz_mediana(f_values))
        stats['odchylenie'].append(oblicz_odchylenie_standardowe(f_values))

    return stats

def oblicz_srednia(values):
    if not values:
        return 0.0
    return sum(values) / len(values)

def oblicz_mediana(values):
    if not values:
        return 0.0

    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2

    if n % 2 != 0:
        return sorted_values[mid]

    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0

def oblicz_odchylenie_standardowe(values):
    if not values:
        return 0.0

    n = len(values)
    mean = sum(values) / n

    variance = sum((x - mean) ** 2 for x in values) / n

    return variance ** 0.5

def wizualizacja_statystyki(stats):
    y_labels = stats['y']
    srednia = stats['srednia']
    mediana = stats['mediana']
    odchylenie = stats['odchylenie']

    n_groups = len(y_labels)
    x_indices = list(range(n_groups))

    bar_width = 0.25
    x_srednia = [x - bar_width for x in x_indices]
    x_mediana = x_indices
    x_odchylenie = [x + bar_width for x in x_indices]

    plt.figure(figsize=(16, 10))

    plt.bar(x_srednia, srednia, width=bar_width, label='Średnia: F(y)', color='blue', alpha=0.75)
    plt.bar(x_mediana, mediana, width=bar_width, label='Mediana: F(x,y)', color='green', alpha=0.75)
    plt.bar(x_odchylenie, odchylenie, width=bar_width, label='Odchylenie standowe: σ(F(x,y))', color='red', alpha=0.75)

    plt.xlabel('Wartości Y')
    plt.ylabel('Wyliczona wartość')
    plt.title('Zestawienie statystyk F(x,y)')

    plt.xticks(x_indices, y_labels, rotation=45)
    plt.legend()
    plt.grid(axis='y', linestyle='-', alpha=0.7)
    plt.tight_layout()
    plt.show()

plik = 'Dane/142447.txt'
dane = wczytaj_dane(plik)

wizualizacja(dane)
wizualizacja_statystyki(oblicz_statystyki(dane))