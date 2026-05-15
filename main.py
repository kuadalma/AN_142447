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

#interpolacja wielomianowa Lagrange’a
def generuj_krzywa_interpolacyjna(oryginalne_x, oryginalne_y, liczba_punktow=200):
    wspolczynniki = oblicz_wspolczynniki_lagrangea(oryginalne_x, oryginalne_y)

    min_x = min(oryginalne_x)
    max_x = max(oryginalne_x)
    krok = (max_x - min_x) / (liczba_punktow - 1)

    krzywa_x = [min_x + i * krok for i in range(liczba_punktow)]
    krzywa_y = [oblicz_wartosc_wielomianu(oryginalne_x, wspolczynniki, x) for x in krzywa_x]

    return krzywa_x, krzywa_y

def oblicz_wspolczynniki_lagrangea(oryginalne_x, oryginalne_y):
    wspolczynniki = []
    n = len(oryginalne_x)

    for i in range(n):
        mianownik = 1.0
        for j in range(n):
            if i != j:
                mianownik *= (oryginalne_x[i] - oryginalne_x[j])

        a_i = oryginalne_y[i] / mianownik
        wspolczynniki.append(a_i)

    return wspolczynniki

def oblicz_wartosc_wielomianu(oryginalne_x, wspolczynniki, szukany_x):
    wynik = 0.0
    n = len(oryginalne_x)

    for i in range(n):
        skladnik = wspolczynniki[i]
        for j in range(n):
            if i != j:
                skladnik *= (szukany_x - oryginalne_x[j])
        wynik += skladnik

    return wynik

def wizualizacja_interpolacji_lagrangea(oryginalne_x, oryginalne_y, wybrane_y):
    krzywa_x, krzywa_y = generuj_krzywa_interpolacyjna(oryginalne_x, oryginalne_y)

    plt.figure(figsize=(16, 10))
    plt.scatter(oryginalne_x, oryginalne_y,  label='Dane oryginalne', color="red")
    plt.plot(krzywa_x, krzywa_y, '-', label="Wielomian Lagrange'a", color="blue")

    plt.title(f"Interpolacja wielomianowa dla y = {wybrane_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość F(x, y)")
    plt.grid( linestyle='-', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

#interpolacja sklajna B-splajnow
def oblicz_funkcje_bazowe(t):
    b0 = ((1.0 - t) ** 3) / 6.0
    b1 = (3.0 * (t ** 3) - 6.0 * (t ** 2) + 4.0) / 6.0
    b2 = (-3.0 * (t ** 3) + 3.0 * (t ** 2) + 3.0 * t + 1.0) / 6.0
    b3 = (t ** 3) / 6.0

    return b0, b1, b2, b3

def generuj_krzywa_bsplajn(x_nodes, y_nodes, n=20):
    rozszerzone_x = [x_nodes[0]] * 2 + x_nodes + [x_nodes[-1]] * 2
    rozszerzone_y = [y_nodes[0]] * 2 + y_nodes + [y_nodes[-1]] * 2

    krzywa_x = []
    krzywa_y = []
    n = len(rozszerzone_x)

    for i in range(1, n - 2):
        for step in range(n):
            t = step / float(n)

            wartosc_x = oblicz_punkt_bsplajnu(
                rozszerzone_x[i - 1], rozszerzone_x[i], rozszerzone_x[i + 1], rozszerzone_x[i + 2], t
            )
            wartosc_y = oblicz_punkt_bsplajnu(
                rozszerzone_y[i - 1], rozszerzone_y[i], rozszerzone_y[i + 1], rozszerzone_y[i + 2], t
            )

            krzywa_x.append(wartosc_x)
            krzywa_y.append(wartosc_y)

    krzywa_x.append(x_nodes[-1])
    krzywa_y.append(y_nodes[-1])

    return krzywa_x, krzywa_y

def oblicz_punkt_bsplajnu(p0, p1, p2, p3, t):
    b0, b1, b2, b3 = oblicz_funkcje_bazowe(t)
    return p0 * b0 + p1 * b1 + p2 * b2 + p3 * b3

def wizualizacja_spline(original_x, original_y, selected_y):
    curve_x, curve_y = generuj_krzywa_bsplajn(original_x, original_y)

    plt.figure(figsize=(16, 10))
    plt.scatter(original_x, original_y, label='Punkty kontrolne (Dane)', color="red")
    plt.plot(curve_x, curve_y, '-', label='Krzywa B-sklejana (B-splajn)', color="orange")

    plt.title(f"Aproksymacja B-splajnem dla y = {selected_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość F(x, y)")
    plt.grid( linestyle='-', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

#porownanie metod interpolacyjnych
def wizualizacja_porownania_metod(oryginalne_x, oryginalne_y, wybrane_y):
    lagrange_x, lagrange_y = generuj_krzywa_interpolacyjna(oryginalne_x, oryginalne_y)
    bsplajn_x, bsplajn_y = generuj_krzywa_bsplajn(oryginalne_x, oryginalne_y)

    plt.figure(figsize=(16, 10))

    plt.scatter(oryginalne_x, oryginalne_y, label='Dane oryginalne', zorder=3, color="red")
    plt.plot(lagrange_x, lagrange_y, '-', label="Wielomian Lagrange'a", color="blue")
    plt.plot(bsplajn_x, bsplajn_y, '-', label='Krzywa B-sklejana', color="orange")

    plt.title(f"Porównanie metod interpolacji dla y = {wybrane_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość F(x, y)")

    min_y = min(oryginalne_y)
    max_y = max(oryginalne_y)
    margines = (max_y - min_y) * 0.5
    plt.ylim(min_y - margines, max_y + margines)

    plt.grid( linestyle='-', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# aproksymacja metoda najmniejszych kwadratow i liniowa
def rozwiaz_uklad_gaussa(macierz, wektor):
    rozmiar = len(wektor)
    kopia_macierzy = [wiersz[:] for wiersz in macierz]
    kopia_wektora = wektor[:]

    for i in range(rozmiar):
        maksymalny_indeks = i
        for k in range(i + 1, rozmiar):
            if abs(kopia_macierzy[k][i]) > abs(kopia_macierzy[maksymalny_indeks][i]):
                maksymalny_indeks = k

        kopia_macierzy[i], kopia_macierzy[maksymalny_indeks] = kopia_macierzy[maksymalny_indeks], kopia_macierzy[i]
        kopia_wektora[i], kopia_wektora[maksymalny_indeks] = kopia_wektora[maksymalny_indeks], kopia_wektora[i]

        for k in range(i + 1, rozmiar):
            mnoznik = kopia_macierzy[k][i] / kopia_macierzy[i][i]
            for j in range(i, rozmiar):
                kopia_macierzy[k][j] -= mnoznik * kopia_macierzy[i][j]
            kopia_wektora[k] -= mnoznik * kopia_wektora[i]

    wyniki = [0.0] * rozmiar
    for i in range(rozmiar - 1, -1, -1):
        suma_wielomianu = sum(kopia_macierzy[i][j] * wyniki[j] for j in range(i + 1, rozmiar))
        wyniki[i] = (kopia_wektora[i] - suma_wielomianu) / kopia_macierzy[i][i]

    return wyniki

def wyznacz_wspolczynniki_mnk(oryginalne_x, oryginalne_y, stopien):
    rozmiar_ukladu = stopien + 1
    macierz_normalna = [[0.0] * rozmiar_ukladu for _ in range(rozmiar_ukladu)]
    wektor_wyrazow = [0.0] * rozmiar_ukladu

    for i in range(rozmiar_ukladu):
        for j in range(rozmiar_ukladu):
            macierz_normalna[i][j] = sum(x ** (i + j) for x in oryginalne_x)
        wektor_wyrazow[i] = sum(y * (x ** i) for x, y in zip(oryginalne_x, oryginalne_y))

    return rozwiaz_uklad_gaussa(macierz_normalna, wektor_wyrazow)

def oblicz_wartosc_wielomianu_aproksymacyjnego(wspolczynniki, szukany_x):
    return sum(wspolczynnik * (szukany_x ** indeks) for indeks, wspolczynnik in enumerate(wspolczynniki))

def oblicz_miary_bledu(rzeczywiste_y, przewidywane_y):
    liczba_punktow = len(rzeczywiste_y)
    srednia_y = sum(rzeczywiste_y) / liczba_punktow

    suma_kwadratow_resztek = sum((r - p) ** 2 for r, p in zip(rzeczywiste_y, przewidywane_y))
    calkowita_suma_kwadratow = sum((r - srednia_y) ** 2 for r in rzeczywiste_y)

    rmse = (suma_kwadratow_resztek / liczba_punktow) ** 0.5
    r2 = 1.0 - (suma_kwadratow_resztek / calkowita_suma_kwadratow) if calkowita_suma_kwadratow != 0 else 0.0

    return rmse, r2

def generuj_krzywa_aproksymacyjna(wspolczynniki, oryginalne_x, liczba_punktow=200):
    min_x = min(oryginalne_x)
    max_x = max(oryginalne_x)
    krok = (max_x - min_x) / (liczba_punktow - 1)

    krzywa_x = [min_x + i * krok for i in range(liczba_punktow)]
    krzywa_y = [oblicz_wartosc_wielomianu_aproksymacyjnego(wspolczynniki, x) for x in krzywa_x]

    return krzywa_x, krzywa_y

def wizualizacja_aproksymacji(oryginalne_x, oryginalne_y, wybrane_y):
    stopien_nieliniowy = 3

    wspolczynniki_liniowe = wyznacz_wspolczynniki_mnk(oryginalne_x, oryginalne_y, 1)
    wspolczynniki_nieliniowe = wyznacz_wspolczynniki_mnk(oryginalne_x, oryginalne_y, stopien_nieliniowy)

    przewidywane_liniowe = [oblicz_wartosc_wielomianu_aproksymacyjnego(wspolczynniki_liniowe, x) for x in oryginalne_x]
    przewidywane_nieliniowe = [oblicz_wartosc_wielomianu_aproksymacyjnego(wspolczynniki_nieliniowe, x) for x in
                               oryginalne_x]

    rmse_lin, r2_lin = oblicz_miary_bledu(oryginalne_y, przewidywane_liniowe)
    rmse_nielin, r2_nielin = oblicz_miary_bledu(oryginalne_y, przewidywane_nieliniowe)

    print(f"\n--- Błędy Aproksymacji dla y = {wybrane_y} ---")
    print(f"Model liniowy (stopień 1): RMSE = {rmse_lin:.4f}, R^2 = {r2_lin:.4f}")
    print(f"Model nieliniowy (stopień {stopien_nieliniowy}): RMSE = {rmse_nielin:.4f}, R^2 = {r2_nielin:.4f}")

    x_lin, y_lin = generuj_krzywa_aproksymacyjna(wspolczynniki_liniowe, oryginalne_x)
    x_nielin, y_nielin = generuj_krzywa_aproksymacyjna(wspolczynniki_nieliniowe, oryginalne_x)

    plt.figure(figsize=(16, 10))
    plt.scatter(oryginalne_x, oryginalne_y, label='Dane oryginalne', zorder=3, color="red")
    plt.plot(x_lin, y_lin, '-', label=f'Model liniowy', color="blue")
    plt.plot(x_nielin, y_nielin, '-', label=f'Model sześcienny', color="orange")

    plt.title(f"Aproksymacja dla y = {wybrane_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość F(x, y)")
    plt.grid(linestyle='-', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

# całkowanie numeryczne
def oblicz_calke_simpsona(wezly_x, wezly_y):
    liczba_przedzialow = len(wezly_x) - 1

    krok_h = (wezly_x[-1] - wezly_x[0]) / liczba_przedzialow
    calka = wezly_y[0] + wezly_y[-1]

    for i in range(1, liczba_przedzialow):
        if i % 2 == 0:
            calka += 2.0 * wezly_y[i]
        else:
            calka += 4.0 * wezly_y[i]

    return calka * (krok_h / 3.0)

def wizualizacja_wariantow_simpsona(oryginalne_x, oryginalne_y, wybrane_y):
    calka_dokladna = oblicz_calke_simpsona(oryginalne_x, oryginalne_y)

    skok = 4
    szybkie_x = oryginalne_x[::skok]
    szybkie_y = oryginalne_y[::skok]
    calka_szybka = oblicz_calke_simpsona(szybkie_x, szybkie_y)

    print(f"\n--- Całkowanie (Metoda Simpsona) dla y = {wybrane_y} ---")
    print(f"1. Wariant dokładny (przedziały: {len(oryginalne_x) - 1}): Pole = {calka_dokladna:.6f}")
    print(f"2. Wariant szybki (przedziały: {len(szybkie_x) - 1}): Pole = {calka_szybka:.6f}")
    print(f"Różnica w polu powierzchni: {abs(calka_dokladna - calka_szybka):.6f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))

    # Wykres Dokładny (mniejszy krok)
    ax1.plot(oryginalne_x, oryginalne_y, '--', alpha=0.3, label='Kształt rzeczywisty', color="red")
    ax1.fill_between(oryginalne_x, 0, oryginalne_y, color="lightblue", alpha=0.5)
    ax1.plot(oryginalne_x, oryginalne_y, '-', label=f'calka dokladna (Pole = {calka_dokladna:.3f})', color="blue")
    ax1.set_title("Wariant Dokładny (krok=1)")
    ax1.set_xlabel("Współrzędna x")
    ax1.set_ylabel("Wartość F(x, y)")
    ax1.grid(linestyle='-', alpha=0.7)
    ax1.legend()

    # Wykres Szybki (większy krok)
    ax2.plot(oryginalne_x, oryginalne_y, '--', alpha=0.3, label='Kształt rzeczywisty', color="red")
    ax2.fill_between(szybkie_x, 0, szybkie_y, color="lightgreen", alpha=0.5)
    ax2.plot(szybkie_x, szybkie_y, '-', label=f'Duży krok (Pole = {calka_szybka:.3f})', color="green")
    ax2.set_title("Wariant Szybki (krok=4")
    ax2.set_xlabel("Współrzędna x")
    ax2.grid(linestyle='-', alpha=0.7)
    ax2.legend()

    plt.suptitle(f"Porównanie dokładności całkowania numerycznego dla y = {wybrane_y}", fontsize=14)
    plt.tight_layout()
    plt.show()

# różniczkowanie numeryczne
def oblicz_pochodne_roznice_skonczone(wezly_x, wezly_y):
    liczba_punktow = len(wezly_x)
    pochodne = [0.0] * liczba_punktow

    krok_poczatek = wezly_x[1] - wezly_x[0]
    pochodne[0] = (wezly_y[1] - wezly_y[0]) / krok_poczatek

    for i in range(1, liczba_punktow - 1):
        krok_calkowity = wezly_x[i + 1] - wezly_x[i - 1]
        pochodne[i] = (wezly_y[i + 1] - wezly_y[i - 1]) / krok_calkowity

    krok_koniec = wezly_x[-1] - wezly_x[-2]
    pochodne[-1] = (wezly_y[-1] - wezly_y[-2]) / krok_koniec

    return pochodne

def wizualizacja_pochodnych(oryginalne_x, oryginalne_y, wybrane_y):
    pochodne_dokladne = oblicz_pochodne_roznice_skonczone(oryginalne_x, oryginalne_y)

    zgrubne_x = oryginalne_x[::2]
    zgrubne_y = oryginalne_y[::2]
    pochodne_zgrubne = oblicz_pochodne_roznice_skonczone(zgrubne_x, zgrubne_y)

    print(f"\n--- Analiza Różniczkowania na wspólnym wykresie dla y = {wybrane_y} ---")
    print(
        f"Krok dokładny (h={oryginalne_x[1] - oryginalne_x[0]:.2f}): Średnia zmiana pochodnej = {sum(pochodne_dokladne) / len(pochodne_dokladne):.4f}")
    print(
        f"Krok zgrubny  (h={zgrubne_x[1] - zgrubne_x[0]:.2f}): Średnia zmiana pochodnej = {sum(pochodne_zgrubne) / len(pochodne_zgrubne):.4f}")

    plt.figure(figsize=(16, 10))
    plt.plot(oryginalne_x, oryginalne_y, '-', label=f'Funkcja bazowa F(x, y={wybrane_y})')
    plt.plot(oryginalne_x, pochodne_dokladne, '-', label=f"Pochodna F'(x) (krok dokładny)")
    plt.plot(zgrubne_x, pochodne_zgrubne, '--', label=f"Pochodna F'(x) (podwójny krok)", alpha=0.8)

    plt.title(f"Funkcja i jej pochodne kierunkowe na wspólnym wykresie dla y = {wybrane_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość")
    plt.grid(linestyle='-', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()

#okreslanie monotonicznosci funkcji
def wyznacz_przedzialy_monotonicznosci(wezly_x, pochodne, tolerancja=1e-5):
    przedzialy_rosnace = []
    przedzialy_malejace = []

    poczatek_przedzialu = wezly_x[0]
    aktualny_stan = "rosnie" if pochodne[0] > tolerancja else "maleje"

    for i in range(1, len(wezly_x)):
        stan = "rosnie" if pochodne[i] > tolerancja else "maleje"

        if stan != aktualny_stan:
            koniec_przedzialu = wezly_x[i]

            if aktualny_stan == "rosnie":
                przedzialy_rosnace.append((poczatek_przedzialu, koniec_przedzialu))
            elif aktualny_stan == "maleje":
                przedzialy_malejace.append((poczatek_przedzialu, koniec_przedzialu))

            poczatek_przedzialu = koniec_przedzialu
            aktualny_stan = stan

    koniec_przedzialu = wezly_x[-1]
    if poczatek_przedzialu != koniec_przedzialu:
        if aktualny_stan == "rosnie":
            przedzialy_rosnace.append((poczatek_przedzialu, koniec_przedzialu))
        elif aktualny_stan == "maleje":
            przedzialy_malejace.append((poczatek_przedzialu, koniec_przedzialu))

    return przedzialy_rosnace, przedzialy_malejace


def wizualizacja_monotonicznosci(oryginalne_x, oryginalne_y, wybrane_y):
    pochodne = oblicz_pochodne_roznice_skonczone(oryginalne_x, oryginalne_y)
    przedzialy_rosnace, przedzialy_malejace = wyznacz_przedzialy_monotonicznosci(oryginalne_x, pochodne)

    print(f"\n--- Analiza Monotoniczności F(x, y={wybrane_y}) ---")
    print("Funkcja JEST ROSNĄCA w przedziałach:")
    for start, stop in przedzialy_rosnace:
        print(f" x ∈ [{start:.3f}, {stop:.3f}]")

    print("\nFunkcja JEST MALEJĄCA w przedziałach:")
    for start, stop in przedzialy_malejace:
        print(f" x ∈ [{start:.3f}, {stop:.3f}]")

    plt.figure(figsize=(16, 10))
    plt.plot(oryginalne_x, oryginalne_y, '-', label=f'Funkcja F(x, y={wybrane_y})', color="black")

    for start, stop in przedzialy_rosnace:
        plt.axvspan(start, stop, color='green', alpha=0.3,label='Przedział rosnący (F\' > 0)')

    for start, stop in przedzialy_malejace:
        plt.axvspan(start, stop, color='red', alpha=0.3,label='Przedział malejący (F\' < 0)')

    plt.title(f"Przedziały monotoniczności funkcji,  y = {wybrane_y}")
    plt.xlabel("Współrzędna x")
    plt.ylabel("Wartość F(x, y)")
    plt.grid(linestyle='-', alpha=0.5)

    # Redukcja duplikatów
    uchwyty, etykiety = plt.gca().get_legend_handles_labels()
    unikalne_wpisy = dict(zip(etykiety, uchwyty))
    plt.legend(unikalne_wpisy.values(), unikalne_wpisy.keys(), loc='best')
    plt.tight_layout()
    plt.show()

plik = 'Dane/142447.txt'
dane = wczytaj_dane(plik)

wizualizacja(dane) #aby pokazać wszystkie (dane,41)     #dane z pliku
wizualizacja_statystyki(oblicz_statystyki(dane))        #statystyki

#przykładowe dane do interpolacji
wybrane_y = 0.5
original_x = dane[wybrane_y]['x']
original_y = dane[wybrane_y]['fx']

wizualizacja_interpolacji_lagrangea(original_x, original_y, wybrane_y)  #interpolacja Lagrange'a
wizualizacja_spline(original_x, original_y, wybrane_y)                  #interpolacja sklajna B-splajnow
wizualizacja_porownania_metod(original_x, original_y, wybrane_y)        #porownanie danych interpolacyjnych
wizualizacja_aproksymacji(original_x, original_y, wybrane_y)            #aproksymacja MNK i liniowa
wizualizacja_wariantow_simpsona(original_x, original_y, wybrane_y)      #całkowanie numeryczne
wizualizacja_pochodnych(original_x, original_y, wybrane_y)              #różniczkowanie numeryczne
wizualizacja_monotonicznosci(original_x, original_y, wybrane_y)         #okreslanie monotonicznosci funkcji