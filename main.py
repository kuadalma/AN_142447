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

def wizualizacja_wszystkich_y(dane):
    for y, wartosci in dane.items():
        plt.figure(figsize=(8, 4))
        plt.plot(wartosci['x'], wartosci['fx'], "blue", label=f'F(x, y={y})')
        plt.title(f"Przekrój funkcji F(x,y) dla y")
        plt.xlabel("Współrzędna x")
        plt.ylabel("Wartość funkcji F(x,y)")
        plt.grid(True)
        plt.legend()
        plt.show()

plik = 'Dane/142447.txt'
dane = wczytaj_dane(plik)

wizualizacja_wszystkich_y(dane)

# print("Znalezione unikalne linie y:")
# print(len(list(dane.keys())))
#
# x_dla_050 = dane[0.50]['x']
# F_dla_050 = dane[0.50]['fx']
#
# print(f"\nDla y = 0.50 wczytano {len(x_dla_050)} punktów.")
# print(f"Pierwszy x to: {x_dla_050[0]}, a jego F(x,y) to: {F_dla_050[0]}")