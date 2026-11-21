import pygame
import random

pygame.init()

# screen
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# player
player_x = 220
player_y = 520
player_size = 40
player_speed = 6

# blocks
blocks = []

for i in range(3):
    blocks.append({
        "x": random.randint(0, WIDTH - 40),
        "y": random.randint(-600, -40),
        "size": 40,
        "speed": 6
    })

# speed boost
speed_boost = 0
speed_boost_timer = 0

# shield
shield = False
shield_timer = 0

# power-ups
speed_powerup = {
    "x": random.randint(0, WIDTH - 30),
    "y": random.randint(-500, -100),
    "size": 30,
    "speed": 4
}

shield_powerup = {
    "x": random.randint(0, WIDTH - 30),
    "y": random.randint(-800, -300),
    "size": 30,
    "speed": 4
}

score = 0
running = True
game_over = False

while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Press R to restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                player_x = 220
                score = 0
                game_over = False

                speed_boost = 0
                speed_boost_timer = 0
                shield = False
                shield_timer = 0

                for block in blocks:
                    block["x"] = random.randint(0, WIDTH - 40)
                    block["y"] = random.randint(-600, -40)
                    block["speed"] = 6

                speed_powerup["x"] = random.randint(0, WIDTH - 30)
                speed_powerup["y"] = random.randint(-500, -100)

                shield_powerup["x"] = random.randint(0, WIDTH - 30)
                shield_powerup["y"] = random.randint(-800, -300)

    # Game over
    if game_over:
        game_over_text = font.render(
            "Game Over! Press R to Restart",
            True,
            (255, 255, 255)
        )

        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2)
        )

        pygame.display.update()
        continue

    # movement
    keys = pygame.key.get_pressed()

    current_speed = player_speed

    # Speed boost
    if speed_boost > 0:
        current_speed = 12
        speed_boost -= 1

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= current_speed

    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += current_speed

    # speed boost timer
    speed_boost_timer += 1

    if speed_boost_timer >= 1000:
        speed_boost_timer = 0
        speed_boost = 300

    # shield timer
    if shield:
        shield_timer -= 1

        if shield_timer <= 0:
            shield = False

    # player rectangle
    player_rect = pygame.Rect(
        player_x,
        player_y,
        player_size,
        player_size
    )

    # blocks falling
    for block in blocks:

        block["y"] += block["speed"]

        if block["y"] > HEIGHT:
            block["y"] = -40
            block["x"] = random.randint(
                0,
                WIDTH - block["size"]
            )

            score += 1
            block["speed"] += 0.2

        block_rect = pygame.Rect(
            block["x"],
            block["y"],
            block["size"],
            block["size"]
        )

        # collision
        if player_rect.colliderect(block_rect):

            if shield:
                # Shield protects from one collision
                shield = False
                shield_timer = 0

                block["y"] = -40
                block["x"] = random.randint(
                    0,
                    WIDTH - block["size"]
                )

            else:
                game_over = True

        # random block color
        block_color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

        pygame.draw.rect(
            screen,
            block_color,
            block_rect
        )

    speed_powerup["y"] += speed_powerup["speed"]

    if speed_powerup["y"] > HEIGHT:
        speed_powerup["y"] = random.randint(-600, -100)
        speed_powerup["x"] = random.randint(
            0,
            WIDTH - speed_powerup["size"]
        )

    speed_rect = pygame.Rect(
        speed_powerup["x"],
        speed_powerup["y"],
        speed_powerup["size"],
        speed_powerup["size"]
    )

    # Green block = speed boost
    pygame.draw.rect(
        screen,
        (0, 255, 0),
        speed_rect
    )

    # Collect speed boost
    if player_rect.colliderect(speed_rect):
        speed_boost = 300

        speed_powerup["y"] = random.randint(-600, -100)
        speed_powerup["x"] = random.randint(
            0,
            WIDTH - speed_powerup["size"]
        )


    shield_powerup["y"] += shield_powerup["speed"]

    if shield_powerup["y"] > HEIGHT:
        shield_powerup["y"] = random.randint(-800, -300)
        shield_powerup["x"] = random.randint(
            0,
            WIDTH - shield_powerup["size"]
        )

    shield_rect = pygame.Rect(
        shield_powerup["x"],
        shield_powerup["y"],
        shield_powerup["size"],
        shield_powerup["size"]
    )

    # Draw shield power-up as a yellow square
    pygame.draw.rect(
        screen,
        (255, 220, 0),
        shield_rect
    )

    # Collect shield
    if player_rect.colliderect(shield_rect):
        shield = True
        shield_timer = 600

        shield_powerup["y"] = random.randint(-800, -300)
        shield_powerup["x"] = random.randint(
            0,
            WIDTH - shield_powerup["size"]
        )


    # Draw shield around player
    if shield:
        pygame.draw.circle(
            screen,
            (255, 220, 0),
            (
                player_x + player_size // 2,
                player_y + player_size // 2
            ),
            player_size // 2 + 8,
            4
        )

    # draw player
    pygame.draw.circle(
        screen,
        (0, 200, 255),
        (
            player_x + player_size // 2,
            player_y + player_size // 2
        ),
        player_size // 2
    )

    # show speed boost
    if speed_boost > 0:
        boost_text = font.render(
            "SPEED BOOST!",
            True,
            (255, 220, 0)
        )

        screen.blit(
            boost_text,
            (
                WIDTH // 2 - boost_text.get_width() // 2,
                50
            )
        )

    # show shield
    if shield:
        shield_text = font.render(
            "SHIELD!",
            True,
            (255, 220, 0)
        )

        screen.blit(
            shield_text,
            (
                WIDTH // 2 - shield_text.get_width() // 2,
                90
            )
        )

    # score
    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()