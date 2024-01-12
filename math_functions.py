from math import floor
import numpy


# mathematical functions

def binary(x):  # funkcja obliczająca liczbę dziesiętną x na binarną
    tablica = []

    while x != 0:
        tablica.append(x % 2)
        x = floor(x / 2)

    return tablica


def decimal(tablica):  # funkcja obliczająca liczbę binarną x na dziesiętną
    x = 0

    for i in range(0, len(tablica)):
        x = x + pow(2, i) * tablica[i]

    return x


def sumColumn(m):  # funkcja obliczająca w macierzy m nim sumę jej kolumn
    return [sum([row[i] for row in m]) % 2 for i in range(0, len(m[0]))]


def matrix(tab):  # funkcja tworząca macierz z liczb binarnych
    m = []
    for i in range(0, len(tab)):
        m.append(binary(tab[i]))
        if len(m[i]) != len(m[0]):
            for j in range(0, len(m[0]) - len(m[i])):
                m[i].append(
                    0)  # jeżeli długośc pierwsza wiersza jest dłuższa od i-tego, to uzupełniamy do końca wiersz zerami

    return m

