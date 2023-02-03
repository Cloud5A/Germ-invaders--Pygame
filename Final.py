import math
import random

import pygame
from pygame import mixer



# initialise pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("Sneeze_background.png")

# Background sound
mixer.music.load("background.wav")
mixer.music.play (-1)

# Title and icon
pygame.display.set_caption("Germ Invaders")
icon = pygame.image.load("virus.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('shooter.png')
playerX = 370
playerY = 480
player_changeX = 0

# Virus
virusImg = []
virusX = []
virusY = []
virus_changeX = []
virus_changeY = []
num_of_enemies = 6

for i in range(num_of_enemies):
    virusImg.append(pygame.image.load('germ.png'))
    # virusX.append(3)
    # virusY.append(3)
    virusX.append(random.randint(0, 735))
    virusY.append(0)
    virus_changeX.append(1)
    virus_changeY.append(40)


# bullet
# ready - you can't see the bullet on screen
# fire - the bullet is moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_changeX = 0
bullet_changeY = 3
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 5
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("INFECTED",  True, (0, 255, 0))
    screen.blit(over_text, (200, 250))

def shooter(x, y):
    screen.blit(playerImg, (x, y))


def virus(x, y, i):
    screen.blit(virusImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 37, y + 13))


def isCollision(virusX, virusY, bulletX, bulletY):
    distance = math.sqrt((math.pow(virusX - bulletX, 2)) + (math.pow(virusY - bulletY, 2)))
    # distance = math.sqrt((math.pow(virusX - bulletX, 2)) + (math.pow(virusY - bulletY, 2)))
    if distance < 30:
        return True
    else:
        return False

    # Game loop - ensures program is always running and doesn't close down.


running = True
while running:
    #    RGB
    screen.fill((0, 0, 0))
    #   Background
    screen.blit(background, (0, 0))

    # virusX[i] += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_changeX = - 2
            if event.key == pygame.K_RIGHT:
                player_changeX = + 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_changeX = 0
            if event.key == pygame.K_RIGHT:
                player_changeX = + 0

    # checking for boundaries
    playerX += player_changeX
    if playerX <= 1:
        playerX += 3
    elif playerX >= 730:
        playerX -= 3

    # virus movement
    for i in range(num_of_enemies):

        # Game over
        if virusY[i] > 500:
            for j in range(num_of_enemies):
                virusY[j] = 2000
                game_over_text()
            break

        virusX[i] += virus_changeX[i]
        if virusX[i] >= 736:
            virus_changeX[i] = -1
            virusY[i] += virus_changeY[i]
        elif virusX[i] <= 0:
            virus_changeX[i] = 1
            virusY[i] += virus_changeY[i]
        # if virusY[i] >= 536:
        #     virus_changeY[i] = 536
        #     virusY[i] = virus_changeY[i]

       #Score speed
        if score_value >= 5:
            if virusX[i] >= 736:
                virus_changeX[i] -= 1.5
                virusY[i] += virus_changeX[i]
            elif virusX[i] <= 0:
                virus_changeX[i] += 1.5
                virusY[i] += virus_changeX[i]

                if score_value >= 10:
                    if virusX[i] >= 736:
                        virus_changeX[i] -= 1
                        virusY[i] += virus_changeX[i]
                    elif virusX[i] <= 0:
                        virus_changeX[i] += 1
                        virusY[i] += virus_changeX[i]


            # collision
        collision = isCollision(virusX[i], virusY[i], bulletX, bulletY)
        if collision:
            if bulletY <= 470:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                virusX[i] = random.randint(0, 735)
                virusY[i] = random.randint(0, 100)


        virus(virusX[i], virusY[i], i)

        # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bullet_changeY

    shooter(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
