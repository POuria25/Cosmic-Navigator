import math
import pygame
import sys
import random

# Constantes
NOIR = (0, 26, 51)
BLEU = (51, 153, 255)
ORANGE = (255, 153, 0)
JAUNE = (255, 255, 77)
ROUGE = (230, 0, 0)
BLANC = (255, 255, 255)

KEY_RIGHT = pygame.K_RIGHT
KEY_LEFT = pygame.K_LEFT
KEY_UP = pygame.K_UP
KEY_DOWN = pygame.K_DOWN

 # Parametre
dimension_fenetre = (800, 600) #en pixels
images_par_seconde = 25
position_vaisseau = [100,200]
orientation_vaisseau = 0
VAISSEAU_RAYON = 15
pi = math.pi
r = 23
a = orientation_vaisseau+pi
b = pi / 7
p = position_vaisseau

compteur_propulseur = 0
compteur_touche = 0
masse = 1


position_planete = [400, 300]
present_planete = False
planete_color =  (0, 179, 89)
PLANETE_RAYON = 40
PLANETE_WEIGHT = 1600
G = 0.001



def deplacer_pol(point, distance, orientation):
    x, y = point

    x = math.cos(orientation)*distance + x
    y = math.sin(orientation)*distance + y

    return (x, y)

def dessiner_triangle(couleur, p, r, a, b):

    global position_vaisseau
    p = position_vaisseau
    p1 = deplacer_pol (p, r, (a+b))
    p2 = deplacer_pol (p, r, (a-b))
    polygone = [p, p1, p2]
    pygame.draw.polygon(fenetre, couleur, polygone)

    return

def afficher_vaisseau():

    if compteur_propulseur != 0 and pygame.time.get_ticks() % 2 == 0:
        dessiner_triangle(JAUNE, position_vaisseau, 38, orientation_vaisseau+ 21 *pi/20, pi/30)
        dessiner_triangle(JAUNE, position_vaisseau, 38, orientation_vaisseau+ 19 *pi/20, pi/30)

    dessiner_triangle(ORANGE, position_vaisseau, r, orientation_vaisseau+ pi, pi/7)
    pygame.draw.circle(fenetre, BLEU, (int (position_vaisseau[0]), int(position_vaisseau[1])), VAISSEAU_RAYON)
 #Initialisation

def gerer_touche(key):

    global orientation_vaisseau, compteur_propulseur, compteur_touche
    if key == KEY_RIGHT :
            orientation_vaisseau += pi/20
    elif key == KEY_LEFT :
            orientation_vaisseau -= pi/20
    elif key == KEY_UP :
            compteur_propulseur = 3
    elif key == KEY_DOWN and compteur_touche == 0 :
            compteur_touche = 10

            orientation_vaisseau += pi

def gerer_button(ev):
    global present_planete, position_planete
    if ev.button == 1:
        present_planete = True
        position_planete = ev.pos
    if ev.button == 3:
        present_planete = False

def afficher_planete():

    if present_planete:
        pygame.draw.circle(fenetre,planete_color, position_planete, PLANETE_RAYON)

def initialiser_calculs():

    global xprecedent
    global tprecedent
    global vprecedent

    xprecedent = 0
    tprecedent = 0
    vprecedent = (0, 0)

    return

def update_position(tnow, position_vaisseau, masse, force, orientation_vaisseau, PLANETE_WEIGHT, G):

    global  xprecedent, tprecedent, vprecedent

    dt = tnow - tprecedent

    forcex = force * math.cos(orientation_vaisseau)
    forcey = force * math.sin(orientation_vaisseau)

    dx = position_vaisseau[0] - position_planete[0]
    dy = position_vaisseau[1] - position_planete[1]

    delta_x = dx*dx
    delta_y = dy*dy

    distance = math.sqrt((delta_x + delta_y))

    if present_planete == False :
        forcegx = 0
        forcegy = 0
    else:
        forcegx = - G * ((PLANETE_WEIGHT* masse) / (distance**3)) * dx

        forcegy = - G * ((PLANETE_WEIGHT* masse) / (distance**3)) * dy

    ax = (forcex + forcegx) / masse
    ay = (forcey + forcegy) / masse
    vx = vprecedent[0] + dt * ax
    vy = vprecedent[1] + dt * ay
    vprecedent = [vx , vy]

    position_vaisseau[0] += vx * dt
    position_vaisseau[1] += vy * dt

    tprecedent = tnow

def check_collision():

    dx = position_vaisseau[0] - position_planete[0]
    dy = position_vaisseau[1] - position_planete[1]

    delta_x = dx*dx
    delta_y = dy*dy

    distance = math.sqrt((delta_x + delta_y))
    if (present_planete == True) and ((PLANETE_RAYON + VAISSEAU_RAYON) > distance) :
        titre = police_game_over.render("Game over", True, ROUGE)
        fenetre.blit(titre, (230, 300))
        pygame.display.flip()
        pygame.time.wait(1000)
        sys.exit()

def afficher_etoiles():

        for i in range (40):

            x = random.random()*dimension_fenetre[0]
            y = random.random()*dimension_fenetre[1]
            if int(random.random() * 7) == 0 :
                fenetre.blit(etoile,(x, y))

def border():

	global position_vaisseau
	if position_vaisseau[0] > 800 :
		position_vaisseau[0] = 1

	if position_vaisseau[0] < 0:
		position_vaisseau[0] = 800

	if position_vaisseau[1] > 600:
		position_vaisseau[1] = 1

	if position_vaisseau[1] < 0:
		position_vaisseau[1] = 600


pygame.init()
pygame.font.init()

police_game_over = pygame.font.SysFont('impact, fantasy', 80, True, True)

fenetre = pygame.display.set_mode(dimension_fenetre)
pygame.display.set_caption("Programme 7")
horloge = pygame.time.Clock()
couleur_fond = NOIR

pygame.key.set_repeat(10, 10)
initialiser_calculs()

police_etoile = pygame.font.SysFont('impact, fantasy', 12, True, True)
etoile = police_etoile.render("*", True, BLANC)

while True :

    tnow = pygame.time.get_ticks()
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
             finish = True
             sys.exit()
        elif evenement.type == pygame.KEYDOWN:
            gerer_touche(evenement.key)
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_button(evenement)
    fenetre.fill(couleur_fond)
    tnow = pygame.time.get_ticks()

    if compteur_propulseur > 0:
        force = 0.0003
    else :
        force = 0
    update_position(tnow, position_vaisseau, masse, force, orientation_vaisseau, PLANETE_WEIGHT, G)
    afficher_etoiles()
    afficher_vaisseau()
    afficher_planete()
    check_collision()
    border()
    pygame.display.flip()
    horloge.tick(images_par_seconde)
    if compteur_propulseur > 0:
        compteur_propulseur -=1
    if compteur_touche > 0 :
        compteur_touche -=1
