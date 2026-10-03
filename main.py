import asyncio
import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


async def main():
    # 1. Initialize Pygame display first
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # 2. Setup sprite groups
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
        # Wrap logging so WebAssembly filesystem errors don't crash the loop
        try:
            log_state()
        except Exception:
            pass

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
                try:
                    log_event("player_hit")
                except Exception:
                    pass
                print("Game over!")
                return  # Exit gracefully without sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    try:
                        log_event("asteroid_shot")
                    except Exception:
                        pass
                    asteroid.split()
                    shot.kill()

        pygame.display.flip()

        # Let the browser process input and render frames
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())