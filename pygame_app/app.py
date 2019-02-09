#!/usr/bin/env python

import pygame
import sys
import time
import numpy as np
import atexit
import math

from pygame.locals import *

FPS = 200
pygame.init()
pygame.font.init()
fpsClock = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = 1400, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255, 255, 255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

screen.blit(surface, (0, 0))

rect_width = 150
rect_height = 150
start = time.time()
HEIGHT_OFFSET = 20
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Rect:
    def __init__(self, surface, x, y, width, height, hz, start_time):
        self.sprite = pygame.Rect((x - width / 2, y - height), (width, height))
        self.text = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = self.text.render(str(hz/2) + ' hz', False, (0, 0, 0))
        self.period = 1 / hz
        self.hz = hz
        self.state = 0
        self.last_flick = start_time
        self.surface = surface
        self.surface.blit(self.text_surface, (x, y + 1))
        self.statistic = {
            'error': [],
            'check_frequency': []
        }

    def check_for_flick(self, current_time):
        time_passed = current_time - self.last_flick
        # record how frequent we check for flick
        self.statistic['check_frequency'].append(time_passed)

        if time_passed > self.period:
            self.statistic['error'].append(math.fabs((time_passed - self.period) / self.period))
            self.last_flick = current_time
            self.flick()

    def flick(self):
        if self.state == 1:
            pygame.draw.rect(self.surface, GREEN, self.sprite)
            self.state = 0
        else:
            pygame.draw.rect(self.surface, BLUE, self.sprite)
            self.state = 1


def report_statistic(tiles):
    print('On Exit Report')
    for tile in tiles:
        print('Tile with %.2f hz:' % (tile.hz/2))
        print('Average Error: %.2f%%' % (np.mean(tile.statistic['error']) * 100))
        print('Average Checking Freqency: %.2f ms' % np.mean(tile.statistic['check_frequency']))


if __name__ == '__main__':
    i = True
    rects = [
        Rect(surface, SCREEN_WIDTH / 2, rect_height + HEIGHT_OFFSET, rect_width, rect_height, 6 * 2, time.time()),
        Rect(surface, rect_height, SCREEN_HEIGHT / 2 + HEIGHT_OFFSET, rect_width, rect_height, 6.57 * 2, time.time()),
        Rect(surface, SCREEN_WIDTH / 2, SCREEN_HEIGHT - HEIGHT_OFFSET, rect_width, rect_height, 7.5 * 2, time.time()),
        Rect(surface, SCREEN_WIDTH - rect_width, SCREEN_HEIGHT / 2 + HEIGHT_OFFSET, rect_width, rect_height, 8.57 * 2, time.time()),
    ]
    atexit.register(lambda: report_statistic(rects))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for r in rects:
            r.check_for_flick(time.time())
        pygame.display.flip()
        screen.blit(surface, (0, 0))
