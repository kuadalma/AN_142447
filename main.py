#Projekt AN

import numpy as np

def wczytaj_dane(plik):
    dane = {}

    with open(nazwa_pliku, 'r') as plik:
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


plik = 'Dane/142447.txt'
dane = wczytaj_dane(plik)
