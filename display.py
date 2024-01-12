import pygame
import sys
import numpy
from strategy import nim, misere
from math_functions import sumColumn, matrix

pygame.init()

# screen settings
screen_width = 740
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))  # display screen
pygame.display.set_caption("Nim Game")  # game's window's title

# define colors and fonts
base_font = pygame.font.Font('./fonts/CarvedRock.ttf', 30)
super_font = pygame.font.Font('./fonts/Lobster.otf', 50)
win_font = pygame.font.Font('./fonts/Zina.otf', 80)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 100, 10)

# load images
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
numer = [nr1, nr2, nr3, nr4, nr5, nr6, nr7, nr8]  # table of images (numbers 1-8)


# functions of displaying
# the majority works on the same rules, so I explain only basing on function "menu"

def menu():
    instruction = False  # the variable which rule is to turn on another function
    game = False
    gameBorder = pygame.Rect(325, 220, 110, 50)  # field which can be clicked
    instructionBorder = pygame.Rect(270, 300, 200, 50)  # i będzie to informować program o zmiennej z False na True
    quitBorder = pygame.Rect(310, 380, 135, 50)

    while True:  # pętla, która cały czas przechodzi dopóki nie klikniemy na zdefiniowane zdarzenie
        screen.blit(background, (0, 0))  # load background of the game

        screen.blit(super_font.render('Witaj w grze Nim!', 1, black), (190, 100))  # load the welcome text

        for event in pygame.event.get():  # loop which close the program by 'X'
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # pętla, która pozwala reagować na wydarzenia
                if gameBorder.collidepoint(         # zaczęte przez kliknięcie myszką
                        event.pos):  # warunki jeśli myszka kliknęła w dany region/pole,
                    game = True      # które zdefiniowaliśmy na początku funkcji
                else:
                    game = False
                if instructionBorder.collidepoint(event.pos):
                    instruction = True
                else:
                    instruction = False
                if quitBorder.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        if game:  # if a field was clicked, that's the information for the program to enter the next function
            type_game()
        elif instruction:
            instruction_screen()
        else:  # if nothing has been clicked, the program still shows the unchanged screen
            screen.blit(super_font.render('Graj', 1, orange), (325, 220))
            screen.blit(super_font.render('Instrukcja', 1, orange), (270, 300))
            screen.blit(super_font.render('Wyjdź', 1, orange), (310, 380))

        pygame.display.update()


def instruction_screen():
    back = False
    backBorder = pygame.Rect(10, 10, 60, 60)

    while True:
        screen.blit(background, (0, 0))
        screen.blit(instrukcja, (0, 0))

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
            menu()
        else:
            screen.blit(powrot, (10, 10))

        pygame.display.update()


def type_game():
    misere = False
    nim = False
    misereBorder = pygame.Rect(310, 300, 150, 50)
    nimBorder = pygame.Rect(270, 220, 200, 50)

    while True:
        screen.blit(background, (0, 0))

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
            with_game('M')
        elif nim:
            with_game('N')
        else:
            screen.blit(super_font.render('Klasyczna', 1, orange), (270, 220))
            screen.blit(super_font.render('Misere', 1, orange), (310, 300))

        pygame.display.update()


def with_game(type):
    bot = False
    user = False
    botBorder = pygame.Rect(340, 220, 70, 50)
    userBorder = pygame.Rect(320, 300, 120, 50)

    while True:
        screen.blit(background, (0, 0))

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
            choice_towers(type, 3)
        elif user:
            choice_towers(type, 1)
        else:
            screen.blit(super_font.render('Bot', 1, orange), (340, 220))
            screen.blit(super_font.render('Gracz', 1, orange), (320, 300))

        pygame.display.update()


def choice_towers(type, num):
    fields = [0, 0]
    tower = [False, False, False]
    towerBorder = [0, 0, 0]
    for i in range(0, 3):
        towerBorder[i] = pygame.Rect(230 + i * 120, 300, 60,
                                     60)  # kombinacja, aby wyświetlały się w równych odległościach

    while True:
        screen.blit(background, (0, 0))

        welcome1 = super_font.render('Wybierz liczbę wież', 1, black)
        screen.blit(welcome1, (180, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, 3):  # sprawdzanie każdego po kolei
                    if towerBorder[i].collidepoint(event.pos):
                        tower[i] = True
                    else:
                        tower[i] = False

        for i in range(0, 3):
            if tower[i]:
                fields[0] = i + 3
                choice_fields(fields, type, num)

        for i in range(0, 3):
            screen.blit(numer[i + 2], (230 + i * 120, 300))  # ponownie kombinacja, aby wyświetlało się równo

        pygame.display.update()


def choice_fields(fields, type, num):
    field = [False, False, False, False, False, False]
    fieldBorder = [0, 0, 0, 0, 0, 0]
    for i in range(0, 6):
        fieldBorder[i] = pygame.Rect(65 + i * 110, 300, 60, 60)

    while True:
        screen.blit(background, (0, 0))

        welcome1 = super_font.render('Wybierz maksymalną liczbę pól', 1, black)
        screen.blit(welcome1, (55, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(0, 6):
                    if fieldBorder[i].collidepoint(event.pos):
                        field[i] = True
                    else:
                        field[i] = False

        for i in range(0, 6):
            if field[i]:
                fields[1] = i + 3
                game_field = numpy.random.randint(2, fields[1], fields[0])
                game_screen(num, type, game_field)

        for i in range(0, 6):
            screen.blit(numer[i + 2], (65 + i * 110, 300))

        pygame.display.update()


def winning(num, type, game_field):  # funkcja sprawdzająca wygraną, czy już nadeszła, czy nie
    if sum(game_field) == 0:  # jeżeli nie można już wykonac ruchu
        while True:
            screen.blit(background, (0, 0))
            if type == 'N':  # sprawdzamy którą wersję gry wybraliśmy na samym poczaku i na jej podstawie i
                if num == 3:  # numerów z kim chcieliśmy grać, sprawdzamy, kto wygrał
                    screen.blit(win_font.render('Wygrywa bot!', 1, red), (75, 175))
                elif num == 4:
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
                elif num == 4:
                    screen.blit(win_font.render('Wygrywa bot!', 1, red), (75, 175))
                elif num == 2:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 2 !', 1, red), (300, 230))
                else:
                    screen.blit(win_font.render('Wygrywa gracz', 1, red), (50, 150))
                    screen.blit(win_font.render('nr 1 !', 1, red), (300, 230))

            screen.blit(wygrana, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    else:  # jak mozna wykonac ruch, to gramy dalej
        game_screen(num, type, game_field)


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
            fieldsBorder[i][j] = pygame.Rect(50 + i * 50, 350 - j * 50, 50, 50)

    questField = False
    questBorder = pygame.Rect(670, 430, 60, 60)

    while True:
        screen.blit(background, (0, 0))

        for i in range(0, len(game_field)):
            for j in range(0, game_field[i]):
                screen.blit(cat, (50 + i * 50, 350 - j * 50))

        if num == 1 or num == 2:
            gracznr = base_font.render(('Gracz nr %d' % num), 1, red)
            screen.blit(gracznr, (600, 5))

        if num == 1 or num == 3 or num == 2:
            quest1 = base_font.render('Zaznacz na planszy kotka,', 1, black)
            quest2 = base_font.render('którego pragniesz usunąć', 1, black)
            quest3 = base_font.render('włącznie z resztą, która', 1, black)
            quest4 = base_font.render('znajduje się nad nim!', 1, black)
            screen.blit(quest1, (335, 100))
            screen.blit(quest2, (340, 150))
            screen.blit(quest3, (350, 200))
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
                hint(num, type, game_field)

            for i in range(0, len(game_field)):
                for j in range(0, game_field[i]):
                    if fieldsa[i][j]:
                        game_field[i] = j
                        if num == 1:  # zmieniamy numer gracza na kolejnego
                            num = 2
                        elif num == 2:
                            num = 1
                        else:  # bądź na bota
                            num = 4
                        winning(num, type, game_field)  # po każdym ruchu musi zostać sprawdzone, czy to koniec gry

            pygame.display.update()

        elif num == 4:
            wait = base_font.render('Uwaga, teraz gra bot', 1, red)
            screen.blit(wait, (375, 100))

            pygame.display.flip()  # ponownie wstrzymujemy grę, gdyż komputer zrobiłby to za szybko
            pygame.event.pump()
            pygame.time.wait(2000)

            num = 3
            if type == 'N':
                nim(game_field)
            else:
                misere(game_field)
            winning(num, type, game_field)

            pygame.display.update()


def hint(num, type, game_field):
    g_f = game_field.copy()  # tworzymy kopię tablicy, aby policzyła dla niej odpowiedni ruch
    # w innym wypadku zmieniałaby się oryginalna tablica i mielibyśmy problem z powrotem

    m = matrix(sorted(g_f, reverse=True))  # jesteśmy zmuszeni wykonac kawałek funkcji "nim", aby policzyć, czy
    suma = sumColumn(m)  # mamy do czynienia z sumą nim równą 0

    screen.blit(background, (0, 0))

    if sum(suma) == 0:  # jeśli suma nim jest równa 0, to jesteśmy w przegranej pozycji
        best1 = base_font.render('Możesz wykonać randomowy ruch', 1, red)
        best2 = base_font.render('jesteś w przegranej pozycji.', 1, red)
        screen.blit(best1, (290, 130))
        screen.blit(best2, (340, 180))
    else:  # w innym wypadku możemy wykonac odpowiedni ruch według algorytmu
        if type == 'N':  # który zależy oczywiście od wybranej wersji gry
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

    pygame.display.flip()  # wstrzymujemy gry na 2000 mili sekund, aby gracz mógł przypatrzeć się
    pygame.event.pump()  # polecanemu ruchowi; komputer zrobiłby to za szybko, że nie byłoby to zauważone
    pygame.time.wait(2000)

    game_screen(num, type, game_field)
    pygame.display.update()