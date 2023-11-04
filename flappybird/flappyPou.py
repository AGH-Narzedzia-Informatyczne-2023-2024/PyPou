import pygame
from pygame.locals import *
import random
import subprocess

pygame.init()

clock = pygame.time.Clock()
fps = 60

info = pygame.display.Info()  # Pobranie informacji o ekranie

screen_width = info.current_w  # Szerokość ekranu
screen_height = info.current_h  # Wysokość ekranu

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy PyPou')

#czcionka i kolor
font=pygame.font.SysFont('Bauhaus 93', 60)
white=(255,255,255)

#define game variables
ground_scroll = 0
scroll_speed = 4
flying=False
game_over = False
pipe_gap=150
pipe_frequency = 1500 #milisekundy
last_pipe = pygame.time.get_ticks() - pipe_frequency
score=0
pass_pipe=False

#load images
bg = pygame.image.load('tlo2.jpg')
bg = pygame.transform.scale(bg, (screen_width, screen_height))  # Skaluj obraz tła
ground_img = pygame.image.load('ground2.png')
ground_img = pygame.transform.scale(ground_img, (screen_width, screen_height))
button_img = pygame.image.load('restart.png')
button2_img = pygame.image.load('back.png')

def draw_text(text, font, text_col, x, y):
    img=font.render(text, True, text_col)
    screen.blit(img, (x,y))

def reset_game():
    pipe_group.empty()
    
    flappy.rect.x=100
    flappy.rect.y=int(screen_height/2)
    flappy.vel=0
    flying=False
    score=0
    return score

class Pou(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('pou.png')
        # Przeskalowanie obrazu do rozmiaru ekranu
        self.original_image = pygame.transform.scale(self.original_image, (0.04*screen_width, 0.04*screen_height))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel = 0
        self.kat = 0
        self.clicked = False

    def update(self):
       
        if flying ==True:
           #grawitacja
           self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        if self.rect.bottom < 675:
            self.rect.y += int(self.vel)
    
            if game_over==False:
                #skok
                if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                    self.clicked = True
                    self.vel = -10
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

                #rotacja
                # Sprawdź, czy postać spada w dół
                if self.vel > 0:
                    # Obracaj postać o 30 stopni w dół
                    if self.kat < 30:
                        self.kat = 30  # Ustaw obrót na 30 stopni w dół

                    # Zastosuj obrót
                    self.image = pygame.transform.rotate(self.original_image, self.kat*-1)
                else:
                    # W innych przypadkach (np. skok lub ruch w górę), zachowaj standardową rotację
                    self.image = pygame.transform.rotate(self.original_image, self.kat)
            else:
                  self.image = pygame.transform.rotate(self.original_image, 180)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.image = pygame.transform.scale(self.image, (0.09*screen_width, 0.6*screen_height))
        self.rect = self.image.get_rect()
        #pozycja 1 z góry, -1 z dołu
        
        if position == 1:
            self.image = pygame.transform.flip(self.image, False ,True)
            self.rect.bottomleft = [x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap/2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right<100:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)

    def draw(self):

        action=False
        #myszka pozycja
        pos=pygame.mouse.get_pos()
        #nad przyciskiem?
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                action=True
                


        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))    
        return action
    
    #przycisk restaru
button_restart =Button(screen_width//2-50, screen_height//2-100, button_img)
#przycisk back
button_back =Button(screen_width//2-50, screen_height//2+100, button2_img)
   
        

pou_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Pou(100, int(screen_height / 2))
pou_group.add(flappy)




run = True
while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

        if event.type == pygame.KEYDOWN:  # Dodanie obsługi klawisza
            if event.key == pygame.K_ESCAPE:  # Klawisz ESC
                run = False

    # tło
    screen.blit(bg, (0, 0))
    pou_group.draw(screen)
    pou_group.update()

    pipe_group.draw(screen)
    

    #ziemia
    screen.blit(ground_img, (ground_scroll, 650))

    #wynik
    
    if len(pipe_group) > 0 and len(pou_group) > 0:
            if pou_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
              and pou_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
               and pass_pipe==False:
                pass_pipe=True
            if pass_pipe==True:
                if pou_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe=False
                 
    draw_text(str(score), font, white, int(screen_width/2), 20)      

    #kolizja
    if pygame.sprite.groupcollide(pou_group, pipe_group, False, False) or flappy.rect.top<0:
       game_over=True
       

    #uderzenie w ziemie
    if flappy.rect.bottom>=649:
        game_over=True
        flying=False
        ground_scroll = 0
        flappy.image = pygame.transform.rotate(flappy.original_image, 180)

    if game_over== False and flying == True:
    
    #rysowanie rur
       time_now=pygame.time.get_ticks()
       if time_now - last_pipe > pipe_frequency:
           pipe_height = random.randint(-200,200)
           btm_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, -1)
           top_pipe = Pipe(screen_width, int(screen_height / 2)+pipe_height, 1)
           pipe_group.add(btm_pipe)
           pipe_group.add(top_pipe)
           last_pipe = time_now

    # rysuj i przewiń ziemię
  
       ground_scroll -= scroll_speed
       if abs(ground_scroll) > 10:
          ground_scroll = 0

       pipe_group.update()

    #koniec gry i reset
    if game_over == True:
       if button_restart.draw() == True:
           game_over=False
           score=reset_game()
           flying=False
       if button_back.draw() == True:
           if event.type == pygame.MOUSEBUTTONDOWN:  # Sprawdzenie kliknięcia myszą
            mouse_pos = pygame.mouse.get_pos()  # Pobranie pozycji myszy

             #przycisk przenoszacy do pliku wszystkieGry
            # Sprawdzenie, czy kliknięcie nastąpiło w obszarze obrazka
            if button_back.rect.collidepoint(mouse_pos):
                pygame.quit()  # Zamknięcie starego okna
                subprocess.Popen(['python', 'wszystkieGry.py'])  # Uruchomienie pliku wszystkieGry.py
                running = False  # Zatrzymanie pętli, gdyż okno zostanie zamknięte

    pygame.display.update()

pygame.quit()

