import sys

# init section
import pygame
import pygame.event as GAME_EVENTS
import pygame.locals as GAME_GLOBALS

pygame.init()

# vars
windowWidth = 700
windowHeight = 700
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Pygame Keyboard!')

playerSize = 20
playerX = ((windowWidth / 4) * 3) - (playerSize / 2)
playerX2 = (windowWidth / 4) - (playerSize / 2)
playerY = (windowHeight - playerSize - 20)
playerY2 = (windowHeight - playerSize - 20)
playerVX = 1.0
playerVX2 = 1.0
playerVY = 0.0
playerVY2 = 0.0
jumpHeight = 2.1
moveSpeed = 1.0
gravity = 0.01

leftDown = False
aDown = False
rightDown = False
dDown = False
haveJumped = False
haveJumped2 = False

running = True
ready = False

redWins = 0
greenWins = 0

fps = 180

font_name = pygame.font.match_font('times')


# call this when players need to be reset
def reset():
    global playerX, playerX2, playerY, playerY2, playerVX, playerVX2, playerVY, playerVY2, gravity, leftDown, aDown, rightDown, dDown, haveJumped, haveJumped2, running, ready

    playerX = ((windowWidth / 4) * 3) - (playerSize / 2)
    playerX2 = (windowWidth / 4) - (playerSize / 2)
    playerY = (windowHeight - playerSize - 20)
    playerY2 = (windowHeight - playerSize - 20)
    playerVX = 1.0
    playerVX2 = 1.0
    playerVY = 0.0
    playerVY2 = 0.0
    gravity = 0.01

    leftDown = False
    aDown = False
    rightDown = False
    dDown = False
    haveJumped = False
    haveJumped2 = False

    running = True
    ready = False


# call this when you need to print text to your surface
def draw_text(surf, text, size, x=0, y=0, color=(255, 255, 255)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# pause function
def pause():
    ready = False
    draw_text(window, "PAUSED", 85, windowWidth//2, 300)
    draw_text(window, "Press Space To Continue", 40, windowWidth//2, 400)
    pygame.display.update()
    while not ready:
        for event in GAME_EVENTS.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    ready = True
                if event.key == pygame.K_ESCAPE:
                    quit_game()
            if event.type == GAME_GLOBALS.QUIT:
                quit_game()
        pygame.time.delay(1)


# call this when someone wins
def win(color):
    global ready, greenWins, redWins
    if color == "RED":
        redWins += 1
    if color == "GREEN":
        greenWins += 1
    draw_text(window, "YOU WIN " + color, 85, windowWidth // 2, 300)
    draw_text(window, "Press Space To Play Again", 40, windowWidth // 2, 400)
    draw_text(window, str(greenWins) + "-" + str(redWins), 40, windowWidth // 2, 450)
    pygame.display.update()
    while not ready:
        for event in GAME_EVENTS.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    ready = True
                if event.key == pygame.K_ESCAPE:
                    quit_game()
            if event.type == GAME_GLOBALS.QUIT:
                quit_game()
        pygame.time.delay(1)
    reset()


def gravity_green():
    global playerY2, playerVY2, playerY, playerVY, haveJumped2, haveJumped, playerX, playerX2, playerSize
    if playerY2 > 0:
        playerY2 -= playerVY2
    else:
        playerY2 += 1
    if playerY2 + 20 > playerY and not (
            playerX2 + playerSize < playerX or playerX2 > playerX + playerSize) and not haveJumped and haveJumped2 and playerY2 < playerY:
        win("GREEN")
    elif window.get_at((int(playerX2), int(playerY2 + 21))) == (255, 255, 255):
        playerY2 = round(playerY2, 0)
        playerVY2 = 0.0
        haveJumped2 = False
    else:
        playerVY2 -= gravity


def gravity_red():
    global playerY2, playerVY2, playerY, playerVY, haveJumped2, haveJumped, playerX, playerX2, playerSize
    if playerY > 0:
        playerY -= playerVY
    else:
        playerY += 1
    if playerY + 20 > playerY2 and not (
            playerX + playerSize < playerX2 or playerX > playerX2 + playerSize) and not haveJumped2 and haveJumped and playerY < playerY2:
        win("RED")
    elif window.get_at((int(playerX + 10), int(playerY + 21))) == (255, 255, 255):
        playerY = round(playerY, 0)
        playerVY = 0.0
        haveJumped = False
    else:
        playerVY -= gravity


# calculates movement(needs to be called often)
def move():
    global playerX, playerX2, playerY, playerY2, playerVX, playerVX2, playerVY, playerVY2, haveJumped, haveJumped2, gravity
    if leftDown:
        playerVX = -moveSpeed
        if playerX > 0 and (playerX > playerX2 + playerSize or playerX + playerSize < playerX2):
            playerX += playerVX
        elif playerX > 0 and playerY + playerSize < playerY2:
            playerX += playerVX

    if aDown:
        playerVX2 = -moveSpeed
        if playerX2 > 0 and (playerX2 > playerX + playerSize or playerX2 + playerSize < playerX):
            playerX2 += playerVX2
        elif playerX2 > 0 and playerY2 + playerSize < playerY:
            playerX2 += playerVX2

    if rightDown:
        playerVX = moveSpeed
        if playerX + playerSize < windowWidth and (playerX + playerSize < playerX2 or playerX > playerX2 + playerSize):
            playerX += playerVX
        elif playerX + playerSize < windowWidth and playerY + playerSize < playerY2:
            playerX += playerVX

    if dDown:
        playerVX2 = moveSpeed
        if playerX2 + playerSize < windowWidth and (playerX2 + playerSize < playerX or playerX2 > playerX + playerSize):
            playerX2 += playerVX2
        elif playerX2 + playerSize < windowWidth and playerY2 + playerSize < playerY:
            playerX2 += playerVX2

    gravity_red()
    gravity_green()


# call whenever you are closing the pygame window
def quit_game():
    pygame.quit()
    sys.exit()


# event loop(calls other functions)
clock = pygame.time.Clock()
while running:
    window.fill((0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0),
                     (playerX, playerY, playerSize, playerSize))

    pygame.draw.rect(window, (0, 255, 0),
                     (playerX2, playerY2, playerSize, playerSize))

    pygame.draw.line(window, (255, 255, 255), (0, 500), (200, 500), 5)
    pygame.draw.line(window, (255, 255, 255), (0, 700), (windowWidth, 700), 15)
    pygame.draw.line(window, (255, 255, 255), (windowWidth, 500), (windowWidth - 200, 500), 5)
    pygame.draw.line(window, (255, 255, 255), (windowWidth / 4, 350), (windowWidth / 4 * 3, 350), 5)
    pygame.draw.line(window, (255, 255, 255), (0, 200), (200, 200), 5)
    pygame.draw.line(window, (255, 255, 255), (windowWidth, 200), (windowWidth - 200, 200), 5)
    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                leftDown = True
            if event.key == pygame.K_RIGHT:
                rightDown = True
            if event.key == pygame.K_UP:
                if not haveJumped:
                    haveJumped = True
                    playerVY += jumpHeight

            if event.key == pygame.K_a:
                aDown = True
            if event.key == pygame.K_d:
                dDown = True
            if event.key == pygame.K_w:
                if not haveJumped2:
                    haveJumped2 = True
                    playerVY2 += jumpHeight

            if event.key == pygame.K_ESCAPE:
                quit_game()
            if event.key == pygame.K_f:
                gravity -= 0.001
                gravity = round(gravity, 3)
                print(gravity)
            if event.key == pygame.K_h:
                gravity += 0.001
                gravity = round(gravity, 3)
                print(gravity)

            if event.key == pygame.K_q:
                fps -= 5
                print(fps)
            if event.key == pygame.K_e:
                fps += 5
                print(fps)
            if event.key == pygame.K_r:
                reset()
                greenWins = 0
                redWins = 0
            if event.key == pygame.K_k:
                jumpHeight -= 0.1
            if event.key == pygame.K_l:
                jumpHeight += 0.1
            if event.key == pygame.K_p:
                pause()

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                leftDown = False
                playerVX = moveSpeed
            if event.key == pygame.K_RIGHT:
                rightDown = False
                playerVX = moveSpeed

            if event.key == pygame.K_a:
                aDown = False
                playerVX2 = moveSpeed
            if event.key == pygame.K_d:
                dDown = False
                playerVX2 = moveSpeed

        if event.type == GAME_GLOBALS.QUIT:
            quit_game()

    move()

    if pygame.mouse.get_pressed()[2]:
        playerX = pygame.mouse.get_pos()[0]
        playerY = pygame.mouse.get_pos()[1]
    if pygame.mouse.get_pressed()[0]:
        playerX2 = pygame.mouse.get_pos()[0]
        playerY2 = pygame.mouse.get_pos()[1]

    pygame.display.update()

    clock.tick(fps)
