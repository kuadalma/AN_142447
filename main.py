#Projekt AN

import numpy as np
import matplotlib.pyplot as plt

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

def wizualizacja(dane, packet_size = 6):
    if packet_size <= 0:
        return

    y_list = list(dane.keys())
    y_size = len(y_list)

    for i in range(0, y_size, packet_size):
        y_packet = y_list[i: i + packet_size]
        plt.figure(figsize=(10, 6))

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

plik = 'Dane/142447.txt'
dane = wczytaj_dane(plik)

wizualizacja(dane)

# print("Znalezione unikalne linie y:")
# print(len(list(dane.keys())))
#
# x_dla_050 = dane[0.50]['x']
# F_dla_050 = dane[0.50]['fx']
#
# print(f"\nDla y = 0.50 wczytano {len(x_dla_050)} punktów.")
# print(f"Pierwszy x to: {x_dla_050[0]}, a jego F(x,y) to: {F_dla_050[0]}")