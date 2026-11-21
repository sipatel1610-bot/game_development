
import pygame
import random

pygame.init()

# screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Stars")

# colors
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
YELLOW = (255, 250, 50)
RED = (230, 60, 60)
BLUE = (80, 150, 255)
GOLD = (255, 180, 0)
PINK = (255, 80, 130)

# clock
clock = pygame.time.Clock()

# fonts
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 70)

# basket
basket = pygame.Rect(WIDTH // 2 - 60, HEIGHT - 70, 120, 35)
basket_speed = 8

# falling objects
objects = []

for i in range(6):
    x = random.randint(20, WIDTH - 40)
    y = random.randint(-500, -50)

    # Choose the type of object
    object_type = random.choice(
        ["star", "star", "star", "bomb", "gold", "heart"]
    )

    objects.append({
        "rect": pygame.Rect(x, y, 30, 30),
        "speed": random.randint(3, 7),
        "type": object_type
    })

score = 0
lives = 20
game_over = False
running = True

while running:

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # restart if game over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                score = 0
                lives = 20
                game_over = False

                basket.x = WIDTH // 2 - 60

                # reset objects
                for obj in objects:
                    obj["rect"].x = random.randint(20, WIDTH - 40)
                    obj["rect"].y = random.randint(-500, -50)
                    obj["speed"] = random.randint(3, 7)

    keys = pygame.key.get_pressed()

    if not game_over:

        # move basket
        if keys[pygame.K_LEFT]:
            basket.x -= basket_speed

        if keys[pygame.K_RIGHT]:
            basket.x += basket_speed

        # keep basket inside screen
        if basket.left < 0:
            basket.left = 0

        if basket.right > WIDTH:
            basket.right = WIDTH

        # move falling objects
        for obj in objects:

            obj["rect"].y += obj["speed"]

            # collision with basket
            if obj["rect"].colliderect(basket):

                # normal star gives 10 points
                if obj["type"] == "star":
                    score += 10

                # golden star gives 50 points
                elif obj["type"] == "gold":
                    score += 50

                # bomb removes one life
                elif obj["type"] == "bomb":
                    lives -= 1

                # heart gives one extra life
                elif obj["type"] == "heart":
                    lives += 1

                # reset object
                obj["rect"].x = random.randint(20, WIDTH - 40)
                obj["rect"].y = random.randint(-200, -50)
                obj["speed"] = random.randint(3, 7)

                # choose a new object type
                obj["type"] = random.choice(
                    ["star", "star", "star", "bomb", "gold", "heart"]
                )

            # object reaches bottom
            if obj["rect"].top > HEIGHT:

                # missing a normal or golden star costs a life
                if obj["type"] in ["star", "gold"]:
                    lives -= 1

                # reset object
                obj["rect"].x = random.randint(20, WIDTH - 40)
                obj["rect"].y = random.randint(-200, -50)
                obj["speed"] = random.randint(3, 7)

                obj["type"] = random.choice(
                    ["star", "star", "star", "bomb", "gold", "heart"]
                )

        # game over
        if lives <= 0:
            game_over = True

    # DRAW
    screen.fill(BLACK)

    # draw falling objects
    for obj in objects:

        # normal star
        if obj["type"] == "star":
            x = obj["rect"].centerx
            y = obj["rect"].centery

            points = [
                (x, y - 15),
                (x + 7, y - 5),
                (x + 15, y),
                (x + 7, y + 7),
                (x, y + 15),
                (x - 7, y + 7),
                (x - 15, y),
                (x - 7, y - 5)
            ]

            pygame.draw.polygon(screen, YELLOW, points)

        # golden star
        elif obj["type"] == "gold":
            x = obj["rect"].centerx
            y = obj["rect"].centery

            points = [
                (x, y - 15),
                (x + 7, y - 5),
                (x + 15, y),
                (x + 7, y + 7),
                (x, y + 15),
                (x - 7, y + 7),
                (x - 15, y),
                (x - 7, y - 5)
            ]

            pygame.draw.polygon(screen, GOLD, points)

        # bomb
        elif obj["type"] == "bomb":
            pygame.draw.circle(
                screen, RED, obj["rect"].center, 15
            )

            pygame.draw.line(
                screen,
                WHITE,
                (obj["rect"].centerx + 8, obj["rect"].centery - 10),
                (obj["rect"].centerx + 15, obj["rect"].centery - 18),
                3
            )

        # heart power-up
        elif obj["type"] == "heart":
            x = obj["rect"].centerx
            y = obj["rect"].centery

            pygame.draw.circle(screen, PINK, (x - 7, y - 4), 9)
            pygame.draw.circle(screen, PINK, (x + 7, y - 4), 9)
            pygame.draw.polygon(
                screen,
                PINK,
                [(x - 16, y), (x + 16, y), (x, y + 17)]
            )

    # draw basket
    pygame.draw.rect(screen, BLUE, basket)

    # basket handle
    pygame.draw.arc(
        screen,
        WHITE,
        (basket.x + 20, basket.y - 25, 80, 50),
        0,
        3.14,
        4
    )

    # score
    score_text = font.render(
        f"Score: {score}", True, WHITE
    )
    screen.blit(score_text, (20, 20))

    # lives
    lives_text = font.render(
        f"Lives: {lives}", True, WHITE
    )
    screen.blit(lives_text, (650, 20))

    # game over screen
    if game_over:

        game_over_text = big_font.render(
            "GAME OVER!", True, RED
        )

        final_score = font.render(
            f"Final Score: {score}", True, WHITE
        )

        restart_text = font.render(
            "Press R to Restart", True, YELLOW
        )

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, 220)
        )

        screen.blit(
            final_score,
            (WIDTH // 2 - final_score.get_width() // 2, 300)
        )

        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 360)
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()