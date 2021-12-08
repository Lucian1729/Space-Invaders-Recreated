import pygame
import random
import time
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

backgroundImg = pygame.image.load('background.png')

mixer.music.load('game_music.wav')
mixer.music.play(-1)

game_state = True

playerImg = pygame.image.load('spaceship2.png')
playerX = 368
playerY = 480
playerX_change = 0
playerRect = pygame.Rect(playerX, playerY, 64, 64)

enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemyRect = []
enemyImg1 = pygame.image.load('enemy1.png')
enemyImg2 = pygame.image.load('enemy2.png')
enemy_number = 10
enemy_state = 1
for i in range(enemy_number):
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(8)
    enemyY_change.append(40)
    enemyRect.append(pygame.Rect(enemyX[i], enemyY[i], 64, 64))
movement_state = True
movement_count = 1

bulletImg = pygame.image.load('missile.png')
bulletX = []
bulletY = []
bulletRect = []
bulletY_change = 20
bullet_state = []
fire_delay = 0
last_fire_delay = -20

explosionImg = pygame.image.load('explosion1.png')
explosionX = 0
explosionY = 0
explosion_frames = 12
explosion_count = 13

score_value = 0
score_font = pygame.font.Font('game_over.ttf', 48)
score_font_over = pygame.font.Font('game_over.ttf', 100)

over_font = pygame.font.Font('game_over.ttf', 200)
exit_font = pygame.font.Font('game_over.ttf', 48)


def game_over():
    over_object = over_font.render("GAME OVER", True, (128, 0, 0))
    screen.blit(over_object, (160, 200))
    exit_object = exit_font.render("Press ESCAPE key to exit.", True, (255, 255, 255))
    screen.blit(exit_object, (290, 550))


def score():
    if game_state:
        score_object = score_font.render("Score : " + str(score_value), True, (128, 0, 0))
        screen.blit(score_object, (10, 10))
    else:
        score_object = score_font_over.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score_object, (320, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, z):
    if z:
        screen.blit(enemyImg1, (x, y))
    else:
        screen.blit(enemyImg2, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state.append("fire")
    bulletX.append(x + 24)
    bulletY.append(y - 20)
    bulletRect.append(pygame.Rect(x + 24, y - 20, 16, 16))


def bullet(x, y):
    screen.blit(bulletImg, (x, y))


def explosion(x, y):
    screen.blit(explosionImg, (x, y))


start_time = time.time()

running = True
while running:
    screen.blit(backgroundImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if fire_delay > (last_fire_delay + 20):
                    fire_bullet(playerX, playerY)
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    last_fire_delay = fire_delay
            if event.key == pygame.K_ESCAPE:
                if not game_state:
                    running = False
        if event.type == pygame.KEYUP:
            playerX_change = 0
    if game_state:
        fire_delay += 1
        end_time = time.time()

    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    if playerX > 736:
        playerX = 736

    for i in range(enemy_number):
        if playerRect.colliderect(enemyRect[i]):
            game_over()

            game_state = False
            for ene in range(enemy_number):
                if enemyY[0] < 1000:
                    mixer.music.pause()
                    game_over_sound = mixer.Sound('game_over_sound.wav')
                    game_over_sound.play()
                enemyY[ene] = 2000
        if enemyY[i] > 1000:
            game_over()

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        if enemyX[i] > 736:
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += enemyY_change[i]
        enemyRect[i] = pygame.Rect(enemyX[i], enemyY[i], 64, 64)

        enemy(enemyX[i], enemyY[i], movement_state)

    if movement_count % 16 == 0:
        movement_state = not movement_state
        movement_count = 1
    movement_count += 1

    s = False
    l = len(bulletY)
    i = 0
    while i < l:
        bulletY1 = bulletY
        bulletX1 = bulletX
        bullet_state1 = bullet_state
        if bullet_state[i] == "fire":
            bullet(bulletX[i], bulletY[i])
            bulletY[i] -= bulletY_change
            bulletRect[i] = pygame.Rect(bulletX[i], bulletY[i], 16, 16)
            for en in range(enemy_number):
                if enemyRect[en].colliderect(bulletRect[i]):
                    explosionX = enemyX[en]
                    explosionY = enemyY[en]
                    explosion_count = 0

                    enemyX[en] = random.randint(0, 736)
                    enemyY[en] = random.randint(50, 150)

                    bulletY1.pop(i)
                    bulletX1.pop(i)
                    bullet_state1.pop(i)

                    score_value += 1

                    collision_sound = mixer.Sound('explosion.wav')
                    collision_sound.play()

                    s = True
                    l -= 1
                    i -= 1
                    # If bullet collides with 2 enemies in same frame, will be popped twice and may cause index error.
                    # Hence must use break.
                    break
        i += 1
    if s:
        bulletY = bulletY1
        bulletX = bulletX1
        bullet_state = bullet_state1

    bulletY = [i for i in bulletY if i > -32]
    if len(bulletY) < len(bulletX):
        bulletX.pop(0)
        bullet_state.pop(0)
        bulletRect.pop(0)

    if explosion_frames > explosion_count:
        explosion(explosionX, explosionY)
    explosion_count += 1

    player(playerX, playerY)
    playerRect = pygame.Rect(playerX, playerY, 64, 64)

    score()

    pygame.display.update()

    clock.tick(60)

game_time = end_time - start_time
print(game_time)
print(score_value)
