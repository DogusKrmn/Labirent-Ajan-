import random
from collections import deque

import pygame

pygame.init()

SATIR = 20
SUTUN = 50
HUCRE = 20
PANEL = 90
WIDTH = 1000
HEIGHT = 490

BASLANGIC = (1, 1)
HEDEF = (17, 47)   

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Labirent")
font = pygame.font.SysFont("segoeui,arial", 18)

# Renkler
BG = (24, 26, 33)
DUVAR = (55, 60, 80)
BOSLUK = (236, 239, 244)
GRID_LINE = (214, 218, 226)
BFS_RENGI = (150, 195, 245)        
YOL_RENGI = (250, 215, 40)
BASLANGIC_RENGI = (46, 180, 90)
HEDEF_RENGI = (225, 65, 65)
YAZI = (235, 238, 245)


def build_maze():
    rng = random.Random(7)
    grid = [[1] * SUTUN for _ in range(SATIR)]
    stack = [BASLANGIC]
    grid[BASLANGIC[0]][BASLANGIC[1]] = 0
    while stack:
        r, c = stack[-1]
        options = []
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
            nr, nc = r + dr, c + dc
            if 1 <= nr < SATIR - 1 and 1 <= nc < SUTUN - 1 and grid[nr][nc] == 1:
                options.append((nr, nc, dr, dc))
        if options:
            nr, nc, dr, dc = rng.choice(options)
            grid[r + dr // 2][c + dc // 2] = 0
            grid[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()

    
    removed = 0
    while removed < 60:
        r = rng.randint(1, SATIR - 2)
        c = rng.randint(1, SUTUN - 2)
        if (r % 2) != (c % 2) and grid[r][c] == 1:
            grid[r][c] = 0
            removed += 1

    grid[BASLANGIC[0]][BASLANGIC[1]] = 0
    grid[HEDEF[0]][HEDEF[1]] = 0
    return grid


def komsular(kare):
    r, c = kare
    liste = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < SATIR and 0 <= nc < SUTUN and grid[nr][nc] == 0:
            liste.append((nr, nc))
    return liste


def yol_olustur(ata):
    yol = []
    kare = HEDEF
    while kare is not None:
        yol.append(kare)
        kare = ata[kare]
    return yol[::-1]

def bfs_ara():
    ziyaret = []
    kuyruk = deque([BASLANGIC])
    ata = {BASLANGIC: None}
    while len(kuyruk) > 0:
        kare = kuyruk.popleft()
        ziyaret.append(kare)
        if kare == HEDEF:
            return ziyaret, yol_olustur(ata)
        for k in komsular(kare):
            if k not in ata:
                ata[k] = kare
                kuyruk.append(k)
    return ziyaret, []             


def aramayi_sifirla():
    global ziyaret, yol, asama, sayac, yol_sayac, yazi
    ziyaret = []
    yol = []
    asama = 0
    sayac = 0
    yol_sayac = 0
    yazi = ""


grid = build_maze()

# ANA DÖNGÜ
durum = True

ziyaret = []
yol = []
asama = 0           
sayac = 0           
yol_sayac = 0       
yazi = ""           

while durum:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            durum = False

        if event.type == pygame.KEYDOWN:

            # BOŞLUK: BFS'i başlat
            if event.key == pygame.K_SPACE and (asama == 0 or asama == 3):
                aramayi_sifirla()
                ziyaret, yol = bfs_ara()
                asama = 1
                yazi = "Aranıyor..."

            # R: labirenti ilk haline getir
            if event.key == pygame.K_r and asama != 1:
                grid = build_maze()
                aramayi_sifirla()

    # Fare: sol tuş duvar ekler, sağ tuş siler
    if asama == 0 or asama == 3:
        sol, orta, sag = pygame.mouse.get_pressed()
        if sol or sag:
            x, y = pygame.mouse.get_pos()
            r = y // HUCRE
            c = x // HUCRE
            if 0 <= r < SATIR and 0 <= c < SUTUN and (r, c) != BASLANGIC and (r, c) != HEDEF:
                yeni = 1 if sol else 0
                if grid[r][c] != yeni:
                    grid[r][c] = yeni
                    if asama == 3:
                        aramayi_sifirla()

    # Animasyonu ilerletme
    if asama == 1:
        sayac += 1
        if sayac >= len(ziyaret):
            sayac = len(ziyaret)
            if len(yol) > 0:
                asama = 2
                yazi = "Yol bulundu: " + str(len(yol) - 1) + " adım"
            else:
                asama = 3
                yazi = "Yol bulunamadı! Duvarları sil ve tekrar dene."
    elif asama == 2:
        yol_sayac += 2
        if yol_sayac >= len(yol):
            yol_sayac = len(yol)
            asama = 3

    
    screen.fill(BG)

    taranan = set(ziyaret[:sayac])

    for r in range(SATIR):
        for c in range(SUTUN):
            kutu = (c * HUCRE, r * HUCRE, HUCRE, HUCRE)
            if grid[r][c] == 1:
                pygame.draw.rect(screen, DUVAR, kutu)
            else:
                renk = BFS_RENGI if (r, c) in taranan else BOSLUK
                pygame.draw.rect(screen, renk, kutu)
                pygame.draw.rect(screen, GRID_LINE, kutu, 1)



  
    for i in range(yol_sayac):
        r, c = yol[i]
        pygame.draw.rect(screen, YOL_RENGI, (c * HUCRE + 2, r * HUCRE + 2, HUCRE - 4, HUCRE - 4))


    
    for kare, renk in [(BASLANGIC, BASLANGIC_RENGI), (HEDEF, HEDEF_RENGI)]:
        pygame.draw.rect(screen, renk, (kare[1] * HUCRE + 1, kare[0] * HUCRE + 1, HUCRE - 2, HUCRE - 2))

    # Yazılar
    y0 = SATIR * HUCRE + 12
    screen.blit(font.render("Sol tık: duvar ekle    Sağ tık: duvar sil", True, YAZI), (16, y0))
    screen.blit(font.render("SPACE: BFS'i başlat    R: labirenti sıfırla", True, YAZI), (16, y0 + 24))
    screen.blit(font.render(yazi, True, YOL_RENGI), (16, y0 + 52))

    pygame.display.flip()

pygame.quit()