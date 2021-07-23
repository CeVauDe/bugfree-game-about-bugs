import os
import math
import pygame
import sys
import numpy as np


def simulate():
    pos = np.array([center] * beam_nbr, dtype=float)

    pygame.font.init()
    textfont = pygame.font.SysFont('Arial', 30)

    for i in range(0, beam_nbr):
        length = 0

        edge1 = math.sin(math.radians(winkel + beam_degree * i)) * (block_width / 2)
        edge2 = math.cos(math.radians(winkel + beam_degree * i)) * (block_width / 2)

        while not surface.get_at((int(pos[i][0]), int(pos[i][1]))) == BORDER_COLOR and length < 2000:
            length = length + 1
            pos[i][0] = int(center[0] + math.cos(math.radians(winkel + beam_degree * i)) * length)
            pos[i][1] = int(center[1] + math.sin(math.radians(winkel + beam_degree * i)) * length)

        dist[i] = int(math.sqrt(math.pow(pos[i][0] - center[0] - edge2, 2) + math.pow(pos[i][1] - center[1] - edge1, 2)))
        dist_thr1 = 155
        dist_thr2 = int(dist_thr1 / 2)

        if dist[i] > dist_thr1:
            rgb = [0, 0, 255]
        elif dist[i] > dist_thr2:
            rgb = [255 - (dist[i] - dist_thr2) * int(256 / dist_thr2), 0, (dist[i] - dist_thr2) * int(256 / dist_thr2)]
        else:
            rgb = [255, 0, 0]

        pygame.draw.line(surface, rgb, (int(center[0] + edge2), int(center[1] + edge1)), (pos[i][0], pos[i][1]))
        surface.blit(textfont.render(str(dist[i]), False, (0, 0, 0)), (pos[i][0], pos[i][1]))

    surface.blit(textfont.render(f"speed: {speed:.2f}, winkel: {winkel:.2f}", False, (0, 0, 0)), (20, 10))
    rot_Image = pygame.transform.rotate(carImage, 360 - winkel)
    surface.blit(rot_Image, (int(center[0] - rot_Image.get_width() / 2), int(center[1] - rot_Image.get_height() / 2)))


if __name__ == "__main__":

    pygame.init()

    fps = 30  # me no see no difference beyond 30 fps
    fps_clock = pygame.time.Clock()

    displayImage = pygame.image.load(r'../data/green_ring.png')
    screen_width = displayImage.get_width()
    screen_height = displayImage.get_height()

    carImage = pygame.image.load(r'../data/car.png')
    block_width = carImage.get_width()
    block_height = carImage.get_height()

    surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Keyboard_Input Distance Test")

    White = (255, 255, 255)
    BORDER_COLOR = (255, 255, 255, 255)

    mid = np.array ([ int(screen_width / 2),int(screen_height / 2)])

    center = [(1230), (350)]
    delta_xy = [0, 0]

    speed = 0
    acc = [2, 112, -2] #acceleration, air resistance factor, braking]      112 -> vmax = 15
    time_fac = 5

    beam_degree = 45
    beam_nbr = int(360 / beam_degree)

    dist = np.array([])
    for x in range(0, beam_nbr):
        dist = np.append(dist, x)

    winkel = 0

    turn_eff_factor = 1 / 9 * 2
    turn_orth_factor = 10

    joystick_enable = 0
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    axes = joystick.get_numaxes()

    while True:
        surface.fill(White)
        surface.blit(displayImage, (0, 0))
        for eve in pygame.event.get():
            if eve.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if joystick_enable == 0:
            key_input = pygame.key.get_pressed()
            if key_input[pygame.K_LEFT]:
                turn_factor = -1
            if key_input[pygame.K_UP]:
                speed = max(1 / fps * (acc[0] - math.pow(speed , 2) / acc[1]) * time_fac + speed, 0)
            if key_input[pygame.K_RIGHT]:
                turn_factor = 1
            if key_input[pygame.K_DOWN]:
                speed = max(1 / fps * (acc[2] - math.pow(speed , 2) / acc[1]) * time_fac + speed, 0)
            if not (key_input[pygame.K_DOWN] or key_input[pygame.K_UP]):
                speed = max(1 / fps * (0 - math.pow(speed , 2) / acc[1]) * time_fac + speed, 0)
            if not (key_input[pygame.K_LEFT] or key_input[pygame.K_RIGHT]):
                turn_factor = 0

        elif joystick_enable == 1:
            for number in range(axes):
                axis = joystick.get_axis(number)

                if number == 3:
                    if abs(axis) > 0.05:
                        speed = max(1 / fps * (acc * (-axis) - math.pow(speed , 2) / acc[1]) * time_fac + speed, 0)
                    else:
                        speed = max(1 / fps * (0 - math.pow(speed , 2) / acc[1]) * time_fac + speed, 0)
                elif number == 0:
                    if abs(axis) > 0.05:
                        turn_factor = axis
                    else:
                        turn_factor = 0

        if speed > 0:
            delta_w = math.atan(speed * turn_orth_factor * (100 - math.pow(speed, 2) * turn_eff_factor) / 100 * turn_factor / speed)
        else:
            delta_w = 0

        winkel += delta_w
        delta_xy[0] = math.cos(math.radians(winkel)) * speed
        delta_xy[1] = math.sin(math.radians(winkel)) * speed

        if winkel >= 360:
            winkel -= 360

        center[0] += delta_xy[1]
        center[1] -= delta_xy[0]

        simulate()

        pygame.display.update()
        fps_clock.tick(fps)
