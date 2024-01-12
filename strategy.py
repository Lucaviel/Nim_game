import random

from display import *
from math_functions import *

pygame.init()


def nim(tab):
    m = matrix(
        sorted(tab, reverse=True))  # przekazujemy planszę do zamiany jej na macierz uzupełioną liczbami binarnymi
    suma = sumColumn(m)  # obliczamy nim sume stworzonej macierzy

    if sum(suma) != 0:  # jeżeli suma różna od 0, możemy wykonac wygrywający ruch
        for i in range(0, len(tab)):
            if decimal(m[i]) > decimal(sumColumn([m[i],
                                                  suma])):  # szukamy liczby, która nim suma z obliczoną wcześniej nim sumą jest mniejsza od danej liczby
                index = numpy.where(
                    tab == decimal(m[i]))  # szukamy indeksu w tablicy, na którym znajduje się dana liczba
                tab[index[0][0]] = decimal(
                    sumColumn([m[i], suma]))  # zmieniamy daną liczbę na sume jej i początkowej nim sumy
                break
    else:  # jeżeli suma równa 0, to jesteśmy w=na przegrnanej pozycji i możemy zrobić jakikolwiek ruch
        while True:
            n = random.randint(0, len(tab) - 1)
            if tab[n] != 0:
                tab[n] = tab[n] - random.randint(1, tab[n])
                break


def misere(tab):
    rowna_jeden_suma = 0  # zmienna zlicza wieże, gdzie będzie 1 obiekt
    wieksza_od_jeden = 0  # zmienna zlicza wieże, gdzie jest więcej niż 1 obiekt
    tab_wieksza = 0  # oznacza indeks wieży w tablicy, która jako jedyna ma więcej niż 1 obiekt
    for i in range(0, len(tab)):
        if tab[i] == 1:
            rowna_jeden_suma = rowna_jeden_suma + 1
            continue
        if tab[i] > 1:
            wieksza_od_jeden = wieksza_od_jeden + 1
            tab_wieksza = i

    if wieksza_od_jeden == 1:  # jeśli jest tylko 1 wieża z większą liczbą obiektów niż 1 to
        if rowna_jeden_suma % 2 == 0:  # jeśli wszystkich innych wież jest parzysta ilość
            tab[tab_wieksza] = 1  # pozostawiamy tylko 1 obiekt w danej więzy
        else:
            tab[tab_wieksza] = 0  # w innym wypadku usuwamy całą
    elif wieksza_od_jeden > 1:  # w innym wypadku możemy grać normalnym nimem
        nim(tab)
    elif wieksza_od_jeden == 0:  # w innym wypadku wybieramy jakikolwiek obiekt z którejkolwiek wieży
        while True:
            n = random.randint(0, len(tab) - 1)
            if tab[n] != 0:
                tab[n] = tab[n] - random.randint(1, tab[n])
                break

