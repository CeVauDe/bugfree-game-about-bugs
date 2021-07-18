import os
import math
import pygame
import sys


def simulate():

    surface.fill(White)
    surface.blit(displayImage, (0, 0))
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    key_input = pygame.key.get_pressed()
    if key_input[pygame.K_LEFT]:
        center[0] -= step
    if key_input[pygame.K_UP]:
        center[1] -= step
    if key_input[pygame.K_RIGHT]:
        center[0] += step
    if key_input[pygame.K_DOWN]:
        center[1] += step

    update()
    fps_clock.tick(fps)


def update():
    pos = [[center[0], center[1]], [center[0], center[1]], [center[0], center[1]], [center[0], center[1]],
           [center[0], center[1]], [center[0], center[1]], [center[0], center[1]], [center[0], center[1]]]

    pygame.font.init()
    textfont = pygame.font.SysFont('Arial', 30)

    for i in range(0, 8):
        length = 0
        while not surface.get_at((pos[i][0], pos[i][1])) == BORDER_COLOR and length < 2000:
            length = length + 1
            pos[i][0] = int(center[0] + math.cos(math.radians(360 - degree)) * length * pos_fak[i][0])
            pos[i][1] = int(center[1] + math.sin(math.radians(360 - degree)) * length * pos_fak[i][1])

        pygame.draw.line(surface, (0, 0, 255), (center[0], center[1]), (pos[i][0], pos[i][1]))

        dist[i] = int(math.sqrt(math.pow(pos[i][0] - center[0], 2) + math.pow(pos[i][1] - center[1], 2)))
        surface.blit(textfont.render(str(dist[i]), False, (0, 0, 0)), (pos[i][0] + offset[i][0], pos[i][1] + offset[i][1]))

    surface.blit(blockImage, (center[0] - 25, center[1] - 25))

    pygame.display.update()


if __name__ == "__main__":

    pygame.init()

    fps = 30
    fps_clock = pygame.time.Clock()

    displayImage = pygame.image.load(r'../data/green.png')
    screen_width = displayImage.get_width()
    screen_height = displayImage.get_height()

    blockImage = pygame.image.load(r'../data/block.png')
    block_width = blockImage.get_width()
    block_height = blockImage.get_height()

    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Keyboard_Input Distance Test")

    White = (255, 255, 255)

    p1 = int(screen_width / 2)
    p2 = int(screen_height / 2)

    center = [int(p1 + block_width / 2), int(p2 + block_height / 2)]

    step = 5
    BORDER_COLOR = (255, 255, 255, 255)

    degree = 45
    pos_fak = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    dist = [0, 0, 0, 0, 0, 0, 0, 0]
    offset = [[-20, -25], [-20, -25], [10, -25], [-20, 0], [-20, 0], [-20, 0], [-40, -25], [-20, -25]]

    while True:
        simulate()
