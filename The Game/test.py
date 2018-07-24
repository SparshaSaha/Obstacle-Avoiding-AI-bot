import pygame
pygame.init()
background_colour = (255,255,255)
(width, height) = (1370, 750)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('T-Rex')
screen.fill(background_colour)
pygame.display.flip()

x = 30
y = 650

direction = -1

running = True
jump = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    keys = pygame.key.get_pressed()

    if not jump:
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        y += 1 * direction
        if y < 600 :
            direction = 1;
        elif y == 650:
            direction = -1;
            jump = False

    screen.fill(background_colour)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 10, 10))
    pygame.display.update()
