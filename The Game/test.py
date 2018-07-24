import pygame
import random
from Sprites.Player import Player
from Sprites.CactusSingle import CactusSingle
from Sprites.CactusDouble import CactusDouble
from Sprites.CactusTriple import CactusTriple
from Sprites.Bird import Bird
from Logger import Logger

# Game Variables
obstacleProbability = 0.01
obstaclesOnScreen = []
speed = 3.0
lastQuotient = 0
score = 0
tRexIndex = 0
direction = -1
running = True
jump = False
gameOver = False
jumpSpeed = 3.2
fontName = pygame.font.match_font('arial')
clock = pygame.time.Clock()
background_colour = (255,255,255)
(width, height) = (900, 600)

# Display Score on Screen
def drawText(surf, text, size, x, y):
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, (0, 0, 0))
    textRect = textSurface.get_rect()
    textRect.midtop = (x, y)
    surf.blit(textSurface, textRect)

# Draw the game background
def drawGameBackground():
    screen.fill(background_colour)

# Draw TRex and all obstacles on Screen
def drawCharacter():
    tRex.drawCharacter(screen, tRexIndex)
    for obstacles in obstaclesOnScreen:
        obstacles.drawCharacter(screen)

# Randomly generate game obstacles depending on obstacle probability
def generateGameObstacles():
    if len(obstaclesOnScreen) == 0 or obstaclesOnScreen[len(obstaclesOnScreen) - 1].x < 650:
        if random.uniform(0,1) < obstacleProbability:
            #obstacleNumber = random.randint(0,11)
            #if obstacleNumber <= 4:
            obstaclesOnScreen.append(CactusSingle(900, 515))
            #elif obstacleNumber <= 6:
            #    obstaclesOnScreen.append(CactusDouble(900, 515))
            #elif obstacleNumber <= 8:
            #    obstaclesOnScreen.append(CactusTriple(900, 515))
            #elif obstacleNumber <= 9 and score >= 25:
            #    obstaclesOnScreen.append(Bird(900, 490))
            #elif score >= 30:
            #    obstaclesOnScreen.append(Bird(900, 515))

# Remove dead obstacles from obstacle array
def cleanDeadObstaclesAndPropagate(obstacles, score):
    index = 0
    for obstacle in obstacles:
        if obstacle.x > 100:
            lastDistance = 900
            break
        else:
            score += 1
        index+=1

    obstacles = obstacles[index : ]
    for obstacle in obstacles:
        obstacle.propagate(speed)
    return obstacles, score


# 0 - jump
# 1 - duck
# 2 - nothing

pygame.init()
logger = Logger(1)
action = 0;
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('T-Rex Runner')
drawGameBackground()
pygame.display.flip()

lastpos = 900

tRex = Player(90, 500)
while running:
    action = 2
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        gameOver = False
        score = 0
        obstaclesOnScreen = []

    if keys[pygame.K_DOWN] and not jump:
        tRexIndex = 1
        action = 1
    else:
        tRexIndex = 0

    if not jump:
        if keys[pygame.K_UP]:
            jump = True
            action = 0
    else:
        jump, direction = tRex.jump(jump, direction, jumpSpeed)
        action = -1

    if not gameOver:
        drawGameBackground()
        generateGameObstacles()
        obstaclesOnScreen, score = cleanDeadObstaclesAndPropagate(obstaclesOnScreen, score)
        drawCharacter()
        drawText(screen, 'score: ' + str(score), 20, 700, 50)
        pygame.display.update()

    if len(obstaclesOnScreen) > 0 and tRex.detectCollision(obstaclesOnScreen[0]):
        gameOver = True
        speed = 1.5
        break

    if score // 10 > lastQuotient:
        lastQuotient += 1
        speed += 0.5
        jumpSpeed += 0.1

    # Logging
    if len(obstaclesOnScreen) != 0:
        if (lastpos - obstaclesOnScreen[0].x) > speed * 15.0  or action != 2:
            if obstaclesOnScreen[0].x - 120 > 0 and action != -1:
                logger.logData(1, speed, action, obstaclesOnScreen[0].x - 115)
            lastpos = obstaclesOnScreen[0].x
