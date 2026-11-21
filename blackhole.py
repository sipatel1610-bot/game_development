import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Simulator")

clock = pygame.time.Clock()

# Colors
WHITE = (240, 240, 255)
BLACK = (5, 5, 15)
PURPLE = (130, 50, 255)
BLUE = (50, 150, 255)
RED = (255, 80, 80)

# Stars
stars = []

for i in range(250):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(1, 3)
    ])


# Black hole
hole = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
gravity_power = 0.8
event_horizon = 25


class Particle:

    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.life = random.randint(20, 50)
        self.size = random.randint(1, 3)

    def update(self):
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(
                screen,
                PURPLE,
                self.pos,
                self.size
            )


particles = []


class Asteroid:

    def __init__(self, x, y):

        self.pos = pygame.Vector2(x, y)

        angle = random.random() * math.pi * 2
        speed = random.uniform(1, 4)

        self.vel = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )

        self.radius = random.randint(4, 10)

        self.color = (
            random.randint(120, 220),
            random.randint(120, 220),
            random.randint(120, 220)
        )

        self.dead = False

    def update(self):

        direction = hole - self.pos
        distance = direction.length()

        if distance > 1:

            force = gravity_power / (distance / 50)

            self.vel += direction.normalize() * force

            self.pos += self.vel

            # Create particle trail
            particles.append(
                Particle(
                    self.pos.x,
                    self.pos.y
                )
            )

            # Swallowed by black hole
            if distance < event_horizon:
                self.dead = True

            # Screen wrapping
            if self.pos.x < 0:
                self.pos.x = WIDTH

            if self.pos.x > WIDTH:
                self.pos.x = 0

            if self.pos.y < 0:
                self.pos.y = HEIGHT

            if self.pos.y > HEIGHT:
                self.pos.y = 0

    def draw(self):

        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.radius
        )


asteroids = []


# Starting asteroid field
for i in range(80):

    asteroids.append(
        Asteroid(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        )
    )


running = True

while running:

    clock.tick(60)

    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Add asteroids with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:

            for i in range(5):

                asteroids.append(
                    Asteroid(
                        event.pos[0],
                        event.pos[1]
                    )
                )

        # Increase gravity with SPACE
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                gravity_power += 0.3

    # Black hole follows mouse
    hole.x, hole.y = pygame.mouse.get_pos()

    # Stars
    for s in stars:

        pygame.draw.circle(
            screen,
            WHITE,
            (s[0], s[1]),
            s[2]
        )

    # Update particles
    for p in particles[:]:

        p.update()
        p.draw()

        if p.life <= 0:
            particles.remove(p)

    # Update asteroids
    for a in asteroids[:]:

        a.update()
        a.draw()

        # Remove asteroid if swallowed
        if a.dead:
            asteroids.remove(a)

    # Black hole glow
    pygame.draw.circle(
        screen,
        (50, 0, 100),
        hole,
        45
    )

    pygame.draw.circle(
        screen,
        PURPLE,
        hole,
        30
    )

    pygame.draw.circle(
        screen,
        BLACK,
        hole,
        18
    )

    # UI
    font = pygame.font.SysFont(
        "Arial",
        24
    )

    text = font.render(
        f"Asteroids: {len(asteroids)}  Gravity: {gravity_power:.2f}",
        True,
        WHITE
    )

    screen.blit(
        text,
        (20, 20)
    )

    pygame.display.flip()


pygame.quit()