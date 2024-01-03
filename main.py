#importujemy biblioteki i funkcje, które będą potrzebne
import sys
import numpy as numpy
import pygame
from math import floor
import random

#Inicjalizacja pygame
pygame.init()

#Ekran
screen_width = 740      #szerokośc ekranu
screen_height = 500     #wysokość ekranu
screen = pygame.display.set_mode((screen_width, screen_height))     #wyświetlenie ekranu
pygame.display.set_caption("Nim Game")      #nadanie tytułu okienku gry

#Zdefiniowanie czcionek i kolorów
base_font = pygame.font.Font('./fonts/CarvedRock.ttf', 30)
super_font = pygame.font.Font('./fonts/Lobster.otf', 50)
win_font = pygame.font.Font('./fonts/Zina.otf', 80)
black = (0, 0, 0)
red = (255,0,0)
orange = (255,100,10)

#Załadowanie obrazów
cat = pygame.image.load('./img/lucek.png')
background = pygame.image.load('./img/background.jpeg')
pomoc = pygame.image.load('./img/question.png')
powrot = pygame.image.load('./img/back.png')
instrukcja = pygame.image.load('./img/instrukcja.png')
wygrana = pygame.image.load('./img/wygrana.png')
nr1 = pygame.image.load('./img/numbers/1.png')
nr2 = pygame.image.load('./img/numbers/2.png')
nr3 = pygame.image.load('./img/numbers/3.png')
nr4 = pygame.image.load('./img/numbers/4.png')
nr5 = pygame.image.load('./img/numbers/5.png')
nr6 = pygame.image.load('./img/numbers/6.png')
nr7 = pygame.image.load('./img/numbers/7.png')
nr8 = pygame.image.load('./img/numbers/8.png')
numer = [nr1, nr2, nr3, nr4, nr5, nr6, nr7, nr8]    #stworzenie tablicy, która będzie zawierała obrazy liczb 1-8

#Funkcje matematyczne
def binary(x):      #funkcja obliczająca liczbę dziesiętną x na binarną
    tablica = []

    while x != 0:
        tablica.append(x%2)
        x = floor(x/2)

    return tablica

def decimal(tablica):       #funkcja obliczająca liczbę binarną x na dziesiętną
    x = 0

    for i in range(0,len(tablica)):
        x = x+pow(2,i)*tablica[i]

    return x

def sumColumn(m):       #funkcja obliczająca w macierzy m nim sumę jej kolumn
    return [sum([row[i] for row in m])%2 for i in range(0, len(m[0]))]

def matrix(tab):       #funkcja tworząca macierz z liczb binarnych
    m = []
    for i in range(0, len(tab)):
        m.append(binary(tab[i]))
        if len(m[i]) != len(m[0]):
            for j in range(0, len(m[0])-len(m[i])):
                m[i].append(0)      #jeżeli długośc pierwsza wiersza jest dłuższa od i-tego, to uzupełniamy do końca wiersz zerami

    return m

def nim(tab):
    m = matrix(sorted(tab, reverse=True))   #przekazujemy planszę do zamiany jej na macierz uzupełioną liczbami binarnymi
    suma = sumColumn(m) #obliczamy nim sume stworzonej macierzy

    if sum(suma) != 0:  #jeżeli suma różna od 0, możemy wykonac wygrywający ruch
        for i in range(0, len(tab)):
            if decimal(m[i]) > decimal(sumColumn([m[i], suma])): #szukamy liczby, która nim suma z obliczoną wcześniej nim sumą jest mniejsza od danej liczby
                index = numpy.where(tab == decimal(m[i]))   #szukamy indeksu w tablicy, na którym znajduje się dana liczba
                tab[index[0][0]] = decimal(sumColumn([m[i], suma])) #zmieniamy daną liczbę na sume jej i początkowej nim sumy
                break
    else:   #jeżeli suma równa 0, to jesteśmy w=na przegrnanej pozycji i możemy zrobić jakikolwiek ruch
        while True:
            n = random.randint(0,len(tab)-1)
            if tab[n] != 0:
                tab[n] = tab[n] - random.randint(1, tab[n])
                break

def misere(tab):
    rowna_jeden_suma = 0 #zmienna zlicza wieże, gdzie będzie 1 obiekt
    wieksza_od_jeden = 0 #zmienna zlicza wieże, gdzie jest więcej niż 1 obiekt
    tab_wieksza = 0 #oznacza indeks wieży w tablicy, która jako jedyna ma więcej niż 1 obiekt
    for i in range(0, len(tab)):
        if tab[i] == 1:
            rowna_jeden_suma = rowna_jeden_suma + 1
            continue
        if tab[i] > 1:
            wieksza_od_jeden = wieksza_od_jeden + 1
            tab_wieksza = i

    if wieksza_od_jeden == 1:   #jeśli jest tylko 1 wieża z większą liczbą obiektów niż 1 to
        if rowna_jeden_suma %2 == 0:    #jeśli wszystkich innych wież jest parzysta ilość
            tab[tab_wieksza] = 1        #pozostawiamy tylko 1 obiekt w danej więzy
        else:
            tab[tab_wieksza] = 0        #w innym wypadku usuwamy całą
    elif wieksza_od_jeden > 1:  #w innym wypadku możemy grać normalnym nimem
        nim(tab)
    elif wieksza_od_jeden ==0:  #w innym wypadku wybieramy jakikolwiek obiekt z którejkolwiek wieży
        while True:
            n = random.randint(0,len(tab)-1)
            if tab[n] != 0:
                tab[n] = tab[n] - random.randint(1, tab[n])
                break

def generate(fields, type, num):    #generujemy losowo obiekty w wieżach
    game_field = numpy.random.randint(2, fields[1], fields[0])
    game_screen(num, type, game_field)

def winning(num, type, game_field):     #funkcja sprawdzająca wygraną, czy już nadeszła, czy nie
    if sum(game_field)==0: #jeżeli nie można już wykonac ruchu
        while True:
            screen.blit(background, (0, 0))
            if type == 'N': #sprawdzamy którą wersję gry wybraliśmy na samym poczaku i na jej podstawie i
                if num == 3:   #numerów z kim chcieliśmy grać, sprawdzamy, kto wygrał
                    screen.blit(win_font.render('Wygrywa bot!', 1, red), (75, 175))
                elif num ==4:
                    screen.blit(win_font.render('Wygrywa gracz!', 1, red), (50, 175))
                elif num == 2:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 1 !', 1, red), (300, 230))
                else:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 2 !', 1, red), (300, 230))
            else:
                if num == 3:
                    screen.blit(win_font.render('Wygrywa gracz!', 1, red), (50, 175))
                elif num ==4:
                    screen.blit(win_font.render('Wygrywa bot!', 1, red), (75, 175))
                elif num == 2:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 2 !', 1, red), (300, 230))
                else:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 1 !', 1, red), (300, 230))

            screen.blit(wygrana, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    else:   #jak mozna wykonac ruch, to gramy dalej
        game_screen(num, type, game_field)

#Funkcje wyświetlania
#większość działa na tej podstawie, więc podstawy wytłumaczę na podstawie funkcji "menu"
def menu(fields):
    instruction = False #tworzymy zmienne, które będą nam "włączać" kolejną funkcję
    game = False
    gameBorder = pygame.Rect(325, 220,110, 50)  #na ich miejsce stawiamy niewidzialne pole, na które będzie klikać myszka
    instructionBorder = pygame.Rect(270, 300,200,50)    #i będzie to informować program o zmiennej z False na True
    quitBorder = pygame.Rect(310, 380,135, 50)

    while True: #pętla, która cały czas przechodzi dopóki nie klikniemy na zdefiniowane zdarzenie
        screen.blit(background, (0,0))  #ładujemy tło gry

        screen.blit(super_font.render('Witaj w grze Nim!', 1, black), (190, 100))   #ładujemy napis powitalny

        for event in pygame.event.get():    #pętla, która pozwala zamknąć program X
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:    #pętla, któa pozwala reagować na wydarzenia zaczetę przez kliknięcie myszką
                if gameBorder.collidepoint(event.pos):  #warunki jeśli myszka kliknęła w dany region/pole, któe zdefiniowaliśmy na początku funkcji
                    game = True
                else:
                    game = False
                if instructionBorder.collidepoint(event.pos):
                    instruction = True
                else:
                    instruction = False
                if quitBorder.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if game:    #jeżeli zostało kliknięte pole i wartośc przynależącej do niej zmiennej została zmieniona na True, to informacja
            type_game(fields)   #dla programu, aby wejść do nastepnej funkcji
        elif instruction:
            instruction_screen(fields)
        else:   #jeżeli nic nie zostało klikniete, program cały czas pokazuje niezmieniony ekran
            screen.blit(super_font.render('Graj',1, orange), (325,220))
            screen.blit(super_font.render('Instrukcja',1, orange), (270,300))
            screen.blit(super_font.render('Wyjdź', 1, orange), (310, 380))

        pygame.display.update()

def instruction_screen(fields):
    back = False
    backBorder = pygame.Rect(10, 10, 60, 60)

    while True:
        screen.blit(background, (0,0))
        screen.blit(instrukcja, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backBorder.collidepoint(event.pos):
                    back = True
                else:
                    back = False

        if back:
            menu(fields)
        else:
            screen.blit(powrot, (10, 10))

        pygame.display.update()

def type_game(fields):
    misere = False
    nim = False
    misereBorder = pygame.Rect(310, 300,150,50)
    nimBorder = pygame.Rect(270, 220,200, 50)

    while True:
        screen.blit(background, (0,0))

        screen.blit(super_font.render('W którą wersję gry chcesz zagrać?', 1, black), (30, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if misereBorder.collidepoint(event.pos):
                    misere = True
                else:
                    misere = False
                if nimBorder.collidepoint(event.pos):
                    nim = True
                else:
                    nim = False

        if misere:
            with_game(fields, 'M')
        elif nim:
            with_game(fields, 'N')
        else:
            screen.blit(super_font.render('Klasyczna',1, orange), (270,220))
            screen.blit(super_font.render('Misere',1, orange), (310,300))

        pygame.display.update()

def with_game(fields, type):
    bot = False
    user = False
    botBorder = pygame.Rect(340,220,70,50)
    userBorder = pygame.Rect(320,300, 120, 50)

    while True:
        screen.blit(background, (0,0))

        screen.blit(super_font.render('Przeciwko komu chcesz grać?', 1, black), (100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if botBorder.collidepoint(event.pos):
                    bot = True
                else:
                    bot = False
                if userBorder.collidepoint(event.pos):
                    user = True
                else:
                    user = False

        if bot:
            choice_towers(fields, type, 3)
        elif user:
            choice_towers(fields, type, 1)
        else:
            screen.blit(super_font.render('Bot',1, orange), (340,220))
            screen.blit(super_font.render('Gracz',1, orange), (320,300))

        pygame.display.update()

def choice_towers(fields, type, num):
    tower = [False,False,False]
    towerBorder = [0,0,0]
    for i in range(0,3):
        towerBorder[i] = pygame.Rect(230 + i*120, 300, 60, 60)  #kombinacja, aby wyświetlały się w równych odległościach

    while True:
        screen.blit(background, (0,0))

        welcome1 = super_font.render('Wybierz liczbę wież',1, black)
        screen.blit(welcome1, (180, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0,3):    #sprawdzanie każdego po kolei
                    if towerBorder[i].collidepoint(event.pos):
                        tower[i] = True
                    else:
                        tower[i] = False

        for i in range(0,3):
            if tower[i]:
                fields[0] = i+3
                choice_fields(fields, type, num)

        for i in range(0,3):
            screen.blit(numer[i+2], (230 + i*120, 300)) #ponownie kombinacja, aby wyświetlało się równo

        pygame.display.update()

def choice_fields(fields, type, num):
    field = [False, False,False,False,False,False]
    fieldBorder = [0,0,0,0,0,0]
    for i in range(0,6):
        fieldBorder[i] = pygame.Rect(65+i*110, 300, 60, 60)

    while True:
        screen.blit(background, (0,0))

        welcome1 = super_font.render('Wybierz maksymalną liczbę pól',1, black)
        screen.blit(welcome1, (55, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0,6):
                    if fieldBorder[i].collidepoint(event.pos):
                        field[i] = True
                    else:
                        field[i] = False

        for i in range(0,6):
            if field[i]:
                fields[1] = i+3
                generate(fields, type, num)

        for i in range(0, 6):
            screen.blit(numer[i+2], (65+i*110, 300))

        pygame.display.update()

def help(num, type, game_field):
    g_f = game_field.copy() #tworzymy kopię tablicy, aby policzyła dla niej odpowiedni ruch
                            #w innym wypadku zmieniałaby się oryginalna tablica i mielibyśmy problem z powrotem

    m = matrix(sorted(g_f, reverse=True))   #jesteśmy zmuszeni wykonac kawałek funkcji "nim", aby policzyć, czy
    suma = sumColumn(m)                     #mamy do czynienia z sumą nim równą 0

    screen.blit(background, (0, 0))

    if sum(suma) == 0:      #jeśli suma nim jest równa 0, to jesteśmy w przegranej pozycji
        best1 = base_font.render('Możesz wykonać randomowy ruch', 1, red)
        best2 = base_font.render('jesteś w przegranej pozycji.', 1, red)
        screen.blit(best1, (290, 130))
        screen.blit(best2, (340, 180))
    else:                   #w innym wypadku możemy wykonac odpowiedni ruch według algorytmu
        if type == 'N':     #który zależy oczywiście od wybranej wersji gry
            nim(g_f)
        else:
            misere(g_f)

        best1 = base_font.render('Oto Twój najlepszy,', 1, red)
        best2 = base_font.render('możliwy ruch!', 1, red)
        screen.blit(best1, (380, 150))
        screen.blit(best2, (420, 200))

    for i in range(0, len(g_f)):
        for j in range(0, g_f[i]):
            screen.blit(cat, (50 + i * 50, 350 - j * 50))

    if num == 1 or num == 2:
        gracznr = base_font.render(('Gracz nr %d' % num), 1, red)
        screen.blit(gracznr, (600, 5))

    pygame.display.flip()       #wstrzymujemy gry na 2000 mili sekund, aby gracz mógł przypatrzeć się
    pygame.event.pump()         #polecanemu ruchowi; komputer zrobiłby to za szybko, że nie byłoby to zauważone
    pygame.time.wait(2000)

    game_screen(num, type, game_field)
    pygame.display.update()

def game_screen(num, type, game_field):
    fieldsa = []
    fieldsb = []
    fieldsBorder = []

    for j in range(0, 8):
        fieldsb.append(j)
    for i in range(0, 5):
        fieldsa.append(fieldsb.copy())
        fieldsBorder.append(fieldsb.copy())

    for i in range(0, len(game_field)):
        for j in range(0, game_field[i]):
            fieldsa[i][j] = False
            fieldsBorder[i][j] = pygame.Rect(50+i*50,350-j*50,50,50)

    questField = False
    questBorder = pygame.Rect(670,430, 60,60)

    while True:
        screen.blit(background, (0, 0))

        for i in range(0, len(game_field)):
            for j in range(0, game_field[i]):
                screen.blit(cat, (50 + i * 50, 350 - j * 50))

        if num == 1 or num == 2:
            gracznr = base_font.render(('Gracz nr %d' % num), 1, red)
            screen.blit(gracznr, (600,5))

        if num == 1 or num == 3 or num == 2:
            quest1 = base_font.render('Zaznacz na planszy kotka,', 1, black)
            quest2 = base_font.render('którego pragniesz usunąć', 1, black)
            quest3 = base_font.render('włącznie z resztą, która',1,black)
            quest4 = base_font.render('znajduje się nad nim!', 1, black)
            screen.blit(quest1, (335, 100))
            screen.blit(quest2, (340, 150))
            screen.blit(quest3, (350,200))
            screen.blit(quest4, (370, 250))
            screen.blit(pomoc, (670, 430))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(0, len(game_field)):
                        for j in range(0, game_field[i]):
                            if fieldsBorder[i][j].collidepoint(event.pos):
                                fieldsa[i][j] = True
                            elif questBorder.collidepoint(event.pos):
                                questField = True
                            else:
                                fieldsa[i][j] = False
                                questField = False

            if questField:
                help(num, type, game_field)

            for i in range(0, len(game_field)):
                for j in range(0, game_field[i]):
                    if fieldsa[i][j]:
                        game_field[i] = j
                        if num == 1:    #zmieniamy numer gracza na kolejnego
                            num = 2
                        elif num == 2:
                            num = 1
                        else:           #bądź na bota
                            num = 4
                        winning(num, type, game_field)  #po każdym ruchu musi zostać sprawdzone, czy to koniec gry

            pygame.display.update()

        elif num == 4:
            wait = base_font.render('Uwaga, teraz gra bot', 1, red)
            screen.blit(wait, (375, 100))

            pygame.display.flip()       #ponownie wstrzymujemy grę, gdyż komputer zrobiłby to za szybko
            pygame.event.pump()
            pygame.time.wait(2000)

            num = 3
            if type == 'N':
                nim(game_field)
            else:
                misere(game_field)
            winning(num, type, game_field)

            pygame.display.update()

#Petla gry
while True:
    fields = [0, 0]
    menu(fields)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()