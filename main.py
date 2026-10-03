# /// script
# dependencies = [
#   "pygame-ce",
# ]
# ///

import os
os.environ["SDL_AUDIODRIVER"] = "dummy"

import asyncio
import sys
import traceback

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player
from shot import Shot


async def main():
    print("--- STARTING GAME LOOP ---")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)
    asteroidfieldobject = AsteroidField()

    dt = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        dt = clock.tick(60) / 1000

        for item in updatable:
            item.update(dt)

        for item in drawable:
            item.draw(screen)

        for item in asteroids:
            if item.collides_with(player):
                print("Game over!")
                return

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()

        pygame.display.flip()
        await asyncio.sleep(0)


# Run directly whether executed as script or loaded by pygbag
asyncio.run(main())