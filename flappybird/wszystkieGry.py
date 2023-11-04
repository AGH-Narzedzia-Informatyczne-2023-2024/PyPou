import pygame
from pygame.locals import *
import subprocess

# Inicjalizacja Pygame
pygame.init()

info = pygame.display.Info()  # Pobranie informacji o ekranie

# Ustawienie rozmiaru okna
screen_width = info.current_w  # Szerokość ekranu
screen_height = info.current_h  # Wysokość ekranu
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Obrazki zmodyfikowane')


# Wczytanie obrazków
image1 = pygame.image.load('flappyPou.jpg')  # Wczytaj odpowiedni plik obrazka
image2 = pygame.image.load('pou.png')  # Wczytaj odpowiedni plik obrazka

# Zmiana rozmiaru obrazków
scaled_width_1 = 100  # Nowa szerokość obrazka 1
scaled_height_1 = 100  # Nowa wysokość obrazka 1
image1 = pygame.transform.scale(image1, (scaled_width_1, scaled_height_1))

scaled_width_2 = 100  # Nowa szerokość obrazka 2
scaled_height_2 = 100  # Nowa wysokość obrazka 2
image2 = pygame.transform.scale(image2, (scaled_width_2, scaled_height_2))

# Ustawienie pozycji obrazków
image1_x = 50
image1_y = 50
image2_x = 200
image2_y = 50

# Utworzenie prostokątnych obszarów dla obrazków
image1_rect = image1.get_rect(topleft=(image1_x, image1_y))
image2_rect = image2.get_rect(topleft=(image2_x, image2_y))

running = True
while running:
    window.fill((255, 255, 255))  # Wypełnienie tła na biało

    # Wyświetlenie obrazków
    window.blit(image1, (image1_x, image1_y))
    window.blit(image2, (image2_x, image2_y))

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
       

        if event.type == pygame.KEYDOWN:  # Dodanie obsługi klawisza
            if event.key == pygame.K_ESCAPE:  # Klawisz ESC
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # Sprawdzenie kliknięcia myszą
            mouse_pos = pygame.mouse.get_pos()  # Pobranie pozycji myszy

            # Sprawdzenie, czy kliknięcie nastąpiło w obszarze obrazka
            if image1_rect.collidepoint(mouse_pos):
                pygame.quit()  # Zamknięcie starego okna
                subprocess.Popen(['python', 'flappyPou.py'])  # Uruchomienie pliku flappyPou.py
                running = False  # Zatrzymanie pętli, gdyż okno zostanie zamknięte



    pygame.display.update()

# Zamknięcie okna Pygame
pygame.quit()


