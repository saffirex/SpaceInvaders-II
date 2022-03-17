
import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))

#Title and icon and background
pygame.display.set_caption("Space Invaders-II")
icon = pygame.image.load('player.png')
background = pygame.image.load('bg.jpg')
pygame.display.set_icon(icon)

# background sound
mixer.music.load('music.wav')
mixer.music.play()

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 20
textY = 20


def showScore():
    scoreX = font.render("Score = "+str(score), True, (255, 255, 255))
    screen.blit(scoreX, (textX, textY))


# Player
playerImg = pygame.image.load('battleship.png')
playerX = 370
playerY = 480
playerXchange = 0
playerYchange = 0
movementSpeed = 0.9

# Aliens
alienImg = []
alienX = []
alienY = []
alienXchange = []
alienYchange = []
alienCount = 6
def createAliens():
    global alienCount
    for i in range(alienCount):
        alienImg.append(pygame.image.load('opponent.png'))
        alienX.append(random.randint(0, 736))
        alienY.append(random.randint(50, 150))
        alienXchange.append(0.5)
        alienYchange.append(50)
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX
bulletY = playerY
bulletYchange = 0.3
bulletState = "Ready"

def player():
    screen.blit(playerImg, (playerX, playerY))
    bullet()


def alien(i):
    screen.blit(alienImg[i], (alienX[i], alienY[i]))


def bullet():
    if bulletState == "fire":
        screen.blit(bulletImg, (bulletX+16, bulletY-40))


def checkPlayerBoundary():
    global playerX
    global playerY
    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0
    if playerY >= 536:
        playerY = 536
    if playerY <= 100:
        playerY = 100


def checkAlien(i):
    global alienX
    global alienY
    global alienXchange
    if alienX[i] >= 736:
        alienXchange[i] = -0.5
        alienY[i] += alienYchange[i]
    if alienX[i] <= 0:
        alienXchange[i] = 0.5
        alienY[i] += alienYchange[i]
    if alienY[i] >= 536:
        alienX[i] = random.randint(0, 736)
        alienY[i] = random.randint(50, 150)


def checkBullet():
    global bulletYchange
    global bulletState
    global bulletX
    global bulletY
    if bulletY <= 0:
        bulletState = "Ready"
        print("Missed")
    if bulletState == "Ready":
        bulletX = playerX
        bulletY = playerY


def checkCollision(i):
    global bulletX
    global bulletY
    global bulletState
    global score
    global alienX
    global alienY
    global alienCount
    distance = math.sqrt(math.pow(alienX[i]-bulletX, 2) +
                         math.pow((alienY[i]-bulletY), 2))
    if distance < 40:
        bulletState = "Ready"
        bulletX = playerX
        bulletY = playerY
        print("Wasted")
        score += 1
        print(score)
        alienX[i] = random.randint(0, 735)
        alienY[i] = random.randint(50, 150)
        # Aliens count increases
        if score % 15 == 0:
            alienCount += 6
            createAliens()


gameOverCheck = 0


def checkGameOver(i):
    global alienX
    global alienY
    global gameOverCheck
    distance = math.sqrt(math.pow(alienX[i]-playerX, 2) +
                         math.pow((alienY[i]-playerY), 2))
    if distance < 40:
        for j in range(alienCount):
            print("Game Ends Here")
            alienY[j] = 2000
            gameOverCheck = 1
        return 1
    else:
        return 0


over = pygame.font.SysFont("Segoe UI", 50)


# Game loop
running = False
loadingScreen = True
screen.blit(background, (0, 0))
startText = font.render("Press Enter To Play", True, (255, 255, 255))
screen.blit(startText, (300, 280))
while loadingScreen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard events handlers
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                createAliens()
                loadingScreen = False
                running = True

    pygame.display.update()

while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard events handlers
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -movementSpeed
            elif event.key == pygame.K_RIGHT:
                playerXchange = movementSpeed
            elif event.key == pygame.K_DOWN:
                playerYchange = movementSpeed
            elif event.key == pygame.K_UP:
                playerYchange = -movementSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerXchange = 0
            elif event.key == pygame.K_RIGHT:
                playerXchange = 0
            elif event.key == pygame.K_DOWN:
                playerYchange = 0
            elif event.key == pygame.K_UP:
                playerYchange = 0
            elif event.key == pygame.K_b:
                bulletState = "fire"

    # Player movements
    playerX += playerXchange
    playerY += playerYchange
    checkPlayerBoundary()
    player()
    # Alien movements
    for i in range(alienCount):
        alienX[i] += alienXchange[i]
        checkAlien(i)

        # Bullet firing
        if bulletState == "fire":
            bulletY -= bulletYchange
            checkCollision(i)
        checkBullet()

        alien(i)
        if checkGameOver(i):
            break

    showScore()
    if gameOverCheck == 1:
        running = False
    pygame.display.update()
# Game loop end
gameSakyo = True
while gameSakyo:
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))

    overText = over.render("Game Over", True, (255, 0, 0))
    screen.blit(overText, (270, 250))

    showScore()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameSakyo = False

        # keyboard event handlers
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pass

    pygame.display.update()
