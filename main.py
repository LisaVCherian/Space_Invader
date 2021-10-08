import pygame
import random
import math
from pygame import mixer

pygame.init()

# to create screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# player (X and Y are the coordinates)
player_img = pygame.image.load('player.png')
X = 350
Y = 500
X_change = 0

# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# bullet
bullet_img = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 9
bullet_state = "ready"

# background
bg_img = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))


# blit means draw (to draw the image)
def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


over_font = pygame.font.Font('freesansbold.ttf', 60)


def game_over_text():
    over = over_font.render('GAME OVER!!!', True, (255, 255, 255))
    screen.blit(over, (200, 250))


# game loop
running = True
while running:
    # RGB
    screen.fill((0, 100, 200))

    # Background
    screen.blit(bg_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                X_change = -5
            if event.key == pygame.K_RIGHT:
                X_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':  # otherwise we can fire when already fired then X changes
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = X  # current coordinate of spaceship
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                X_change = 0

    X += X_change
    # to restrict the spaceship within the screen
    if X <= 0:
        X = 0
    elif X >= 736:
        X = 736

    # Enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] >= 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # so that enemy disappears below the screen
            game_over_text()

        enemyX[i] += enemyX_change[i]
        # to restrict enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 500
            bullet_state = 'ready'
            score_value += 1
            # for enemy to respawn
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 500
        bullet_state = 'ready'
    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(X, Y)  # to draw (it should be below screen.fill() code, otherwise it will be drawn under the screen)
    show_score(textX, textY)

    pygame.display.update()
