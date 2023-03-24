import pygame
import random

pygame.init()

pygame.mixer.music.load("gamemusic.ogg")
crash_sound = pygame.mixer.Sound("gameover.wav")

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Race Car')

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
bright_red = (255, 0, 0)
green = (0, 200, 0)
bright_green = (0, 245, 0)

clock = pygame.time.Clock()
carimg = pygame.image.load("car icon.png")
car_width = 30


def button(msg, x, y, w, h, ic, ac, action=None):
    # msg for message, w for width, h for height, ic for inactive color, ac for active color
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < w + x and y < mouse[1] < y + h:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            if action == "play":
                game_loop()
            elif action == "exit":
                pygame.quit()
                quit()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Let's Play Game", largeText)
        TextRect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Play!", 150, 450, 100, 50, green, bright_green, "play")
        button("Exit", 550, 450, 100, 50, red, bright_red, "exit")
        pygame.display.update()


def score(count):
    font = pygame.font.SysFont('None', 25)
    text = font.render("score : " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))


def stuff(stuffx, stuffy, stuffw, stuffh, color):
    pygame.draw.rect(gameDisplay, color, [stuffx, stuffy, stuffw, stuffh])


def car(x, y):
    gameDisplay.blit(carimg, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.Font('freesansbold.ttf', 90)
    TextSurf, TextRect = text_objects("YOU CRASHED", largeText)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Again!", 150, 450, 100, 50, green, bright_green, "play")
        button("Exit", 550, 450, 100, 50, red, bright_red, "exit")
        pygame.display.update()


def game_loop():
    pygame.mixer.music.play(-1)
    x = display_width * 0.45
    y = display_height * 0.8

    x_change = 0

    stuff_startx = random.randrange(0, display_width)
    stuff_starty = -600
    stuff_speed = 7
    stuff_width = 100
    stuff_height = 100
    counter = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        x += x_change

        gameDisplay.fill(white)
        stuff(stuff_startx, stuff_starty, stuff_width, stuff_height, red)
        stuff_starty += stuff_speed
        score(counter)
        car(x, y)

        if x > (display_width - car_width) or x < 0:
            crash()
        if stuff_starty > display_height:
            stuff_starty = 0 - stuff_height
            stuff_startx = random.randrange(0, (display_width - stuff_width))
            counter += 1
            if counter % 5 == 0:
                stuff_speed += 3
        if y < stuff_starty + stuff_height:
            if stuff_startx < x < stuff_startx + stuff_width or stuff_startx < x + car_width < stuff_startx + stuff_width:
                crash()

        pygame.display.update()
        clock.tick(60)


game_intro()


game_loop()
