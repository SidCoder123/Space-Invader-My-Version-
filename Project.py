import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# writing name for the top white line of application window

pygame.display.set_caption("The Game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

backgroundImg = pygame.image.load('1.png')
'''
mixer.music.load('background.wav')
mixer.music.play(-1)
'''
# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bullet_speed = 0
bulletY_change = 5 + bullet_speed
bullet_state = "at_rest"

playerImg = pygame.image.load('001-jet.png')
playerX = 370
playerY = 500
player_speed = 0
playerX_change = 0

# EnemyArray
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyMax = 1
# THE ENEMY STUFF

for i in range(enemyMax):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 730))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(1)

enemyMax = 1

score = 0
font = pygame.font.Font('freesansbold.ttf', 30)
over_font = pygame.font.Font('freesansbold.ttf', 60)




def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def show_score():
    score_show = font.render("Score :" + str(score), True, (0, 225, 0))
    screen.blit(score_show, (10, 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Function for detecting collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 40:
        return True
    else:
        return False


BLACK = (0, 0, 0)

loop = True

while loop:
    if score % 5 == 0:
        if enemyMax < 5:
            enemyMax += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        change = random.randint(1, 9)



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerX_change += 3.7 + player_speed
            if event.key == pygame.K_LEFT:
                playerX_change -= 3.7 + player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state == "at_rest":
                    shoot_bullet(playerX, bulletY)
                    bulletX = playerX
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    for i in range(enemyMax):
        enemyImg.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0, 600))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(1)
        enemyY_change.append(1)

    screen.blit(backgroundImg, (0, 0))

    pygame.draw.line(screen, BLACK, (0, 480), (800, 480), 5)

    playerX += playerX_change

    if playerX >= 730:
        playerX = 730
    elif playerX <= 0:
        playerX = 0



    for i in range(enemyMax):

        if enemyY[i] > 440:
            for j in range(enemyMax):
                enemyY[j] = 2000
            game_over_text()
            playerX = 10000
            score = 0
            bullet_state = "done"
            break

        if change >= 4:
            if enemyX[i] < 700:
                enemyX_change[i] = 0.5
        else:
            if enemyX[i] > 50:
                enemyX_change[i] = -0.5

        enemyX[i] += enemyX_change[i]
        enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if score % 5 == 0:
            if enemyMax < 2:
                enemyMax += 1

        if collision:
            bulletY = 480
            bullet_state = "at_rest"
            score += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            bullet_speed += 0.1
            player_speed += 0.2
            hit_sound = mixer.Sound('explosion.wav')
            hit_sound.play()

    player(playerX, playerY)
    show_score()

    if bullet_state == "fire":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "at_rest"

    pygame.display.update()
