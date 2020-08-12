import random
import sys
from pygame.locals import *
from os import path
import pygame
import pkg_resources.py2_warn
try:
    import pkg_resources.py2_warn
except ImportError:
    pass


# Image and Sound Directories
img_dir = path.join(path.dirname(__file__), 'sprites')
snd_dir = path.join(path.dirname(__file__), 'audio')


# Global Vars
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'bird.png'
BACKGROUND = 'background.png'
PIPE = 'pipe.png'


def welcomeScreen():
    """Shows welcome screen"""
    
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN: # and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 30 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if playery + GAME_SPRITES['player'].get_height() > pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


def mainGame():
    """Obviously, Logics for the main game"""

    # INITS
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2),'y':newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y':newPipe2[1]['y']}
    ]

    # Accelerations and Velocity Vars
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVely = -8
    playerAccY = 1
    playerFlapAccv = -8     # velocity while flapping
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Blitting all the sprites
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperpipe, lowerpipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        Digits = [int(x) for x in list(str(score))]
        width = 0
        for digits in Digits:
            width += GAME_SPRITES['numbers'][digits].get_width()

        Xoffset = (SCREENWIDTH - width) / 2

        for digits in Digits:
            SCREEN.blit(GAME_SPRITES['numbers'][digits], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digits].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def getRandomPipe():
    """Generates positios of two pipes (straight and inverted) for blitting"""

    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},     # Upper Pipe
        {'x': pipeX, 'y': y2}       # Lower Pipe
    ]
    return pipe


# Running and main game loop
if __name__ == '__main__':
    
    # Initializing pygame
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    # Game graphics / sprites
    GAME_SPRITES['numbers'] = (
        pygame.image.load(path.join(img_dir, '0.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '1.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '2.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '3.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '4.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '5.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '6.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '7.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '8.png')).convert_alpha(),
        pygame.image.load(path.join(img_dir, '9.png')).convert_alpha()
    )
    GAME_SPRITES['numbers'][0].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][1].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][2].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][3].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][4].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][5].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][6].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][7].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][8].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['numbers'][9].fill((255, 255, 255, 100), None, pygame.BLEND_RGBA_MULT)

    
    GAME_SPRITES['message'] = pygame.image.load(path.join(img_dir, "message.png")).convert_alpha()
        
    GAME_SPRITES['base'] = pygame.image.load(path.join(img_dir, 'base.png')).convert_alpha()
    GAME_SPRITES['base'].fill((255, 255, 255, 60), None, pygame.BLEND_RGBA_MULT)
    
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(path.join(img_dir, PIPE)).convert_alpha(), 180),  # Inverted by rotation
        pygame.image.load(path.join(img_dir, PIPE)).convert_alpha()                                 # Original
    )
    GAME_SPRITES['pipe'][0].fill((0, 255, 0, 200), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['pipe'][1].fill((0, 255, 0, 200), None, pygame.BLEND_RGBA_MULT)
    GAME_SPRITES['background'] = pygame.image.load(path.join(img_dir, BACKGROUND)).convert()
    GAME_SPRITES['player'] = pygame.image.load(path.join(img_dir, PLAYER)).convert_alpha()

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound(path.join(snd_dir, 'die.wav'))
    GAME_SOUNDS['hit'] = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
    GAME_SOUNDS['point'] = pygame.mixer.Sound(path.join(snd_dir, 'point.wav'))
    GAME_SOUNDS['whoosh'] = pygame.mixer.Sound(path.join(snd_dir, 'whoosh.wav'))
    GAME_SOUNDS['wing'] = pygame.mixer.Sound(path.join(snd_dir, 'wing.wav'))

    # Main Game Loop
    while True:
        welcomeScreen() # On till user presses a key 
        mainGame()      # Main game function       

