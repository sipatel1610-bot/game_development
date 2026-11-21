import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Jump")
clock = pygame.time.Clock()

GRAY = (60, 60, 60)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEAL_BLUE = (54, 117, 136)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (80, 180, 80)
ROAD = (70, 70, 70)
YELLOW = (255, 220, 0)
RED = (220, 50, 50)

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# -----------------------------
# PLAYER
# -----------------------------
FROG_SIZE = 40
frog_speed = 50

# -----------------------------
# CAR LANES
# -----------------------------
lanes = [120, 220, 320, 420, 520]

# -----------------------------
# CREATE CARS
# -----------------------------
def create_cars():
    cars = []

    for i, y in enumerate(lanes):
        direction = 1 if i % 2 == 0 else -1
        speed = random.choice([3, 4, 5]) * direction

        for j in range(3):
            if direction > 0:
                x = -random.randint(0, 500) - j * 220
            else:
                x = WIDTH + random.randint(0, 500) + j * 220

            car = pygame.Rect(x, y, 70, 40)
            cars.append([car, speed])

    return cars


# -----------------------------
# RESET GAME
# -----------------------------
def reset_game():
    global frog, cars, score, game_over

    frog = pygame.Rect(
        WIDTH // 2 - FROG_SIZE // 2,
        HEIGHT - 60,
        FROG_SIZE,
        FROG_SIZE
    )

    cars = create_cars()
    score = 0
    game_over = False


reset_game()

# -----------------------------
# GAME LOOP
# -----------------------------
running = True

while running:

    clock.tick(60)

    # -------------------------
    # EVENTS
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Restart
            if event.key == pygame.K_r and game_over:
                reset_game()

            # Movement
            if not game_over:

                if event.key == pygame.K_LEFT:
                    frog.x -= frog_speed

                elif event.key == pygame.K_RIGHT:
                    frog.x += frog_speed

                elif event.key == pygame.K_UP:
                    frog.y -= frog_speed

                elif event.key == pygame.K_DOWN:
                    frog.y += frog_speed

    # -------------------------
    # GAME LOGIC
    # -------------------------
    if not game_over:

        # Keep frog inside screen
        frog.x = max(
            0,
            min(WIDTH - frog.width, frog.x)
        )

        frog.y = max(
            60,
            min(HEIGHT - frog.height, frog.y)
        )

        # ---------------------
        # MOVE CARS
        # ---------------------
        for car_data in cars:

            car, speed = car_data

            car.x += speed

            # Move cars around screen
            if speed > 0 and car.x > WIDTH:
                car.x = -car.width

            elif speed < 0 and car.x < -car.width:
                car.x = WIDTH

            # Collision
            if frog.colliderect(car):
                game_over = True

        # ---------------------
        # REACHED GOAL
        # ---------------------
        if frog.y <= 60:

            score += 1

            # Reset frog
            frog.x = WIDTH // 2 - FROG_SIZE // 2
            frog.y = HEIGHT - 60

            # Increase difficulty
            for car_data in cars:

                if car_data[1] > 0:
                    car_data[1] = min(car_data[1] + 0.2, 9)

                else:
                    car_data[1] = max(car_data[1] - 0.2, -9)

    # -----------------------------
    # DRAW BACKGROUND
    # -----------------------------
    screen.fill(LIGHT_GREEN)

    # -----------------------------
    # DRAW ROAD
    # -----------------------------
    for y in lanes:

        pygame.draw.rect(
            screen,
            ROAD,
            (0, y - 20, WIDTH, 80)
        )

        # Road markings
        for x in range(0, WIDTH, 60):

            pygame.draw.rect(
                screen,
                YELLOW,
                (x, y - 2, 30, 4)
            )

    # -----------------------------
    # GOAL AREA
    # -----------------------------
    pygame.draw.rect(
        screen,
        WHITE,
        (0, 0, WIDTH, 60)
    )

    goal_text = font.render(
        "GOAL",
        True,
        DARK_GREEN
    )

    screen.blit(
        goal_text,
        (
            WIDTH // 2 - goal_text.get_width() // 2,
            10
        )
    )

    # -----------------------------
    # DRAW CARS
    # -----------------------------
    for car, speed in cars:

        if speed > 0:
            car_color = DARK_GREEN
        else:
            car_color = TEAL_BLUE

        # Body
        pygame.draw.rect(
            screen,
            car_color,
            car,
            border_radius=8
        )

        # Windows
        pygame.draw.rect(
            screen,
            WHITE,
            (
                car.x + 15,
                car.y + 5,
                40,
                15
            ),
            border_radius=3
        )

        # Wheels
        pygame.draw.circle(
            screen,
            BLACK,
            (car.x + 15, car.y + 38),
            7
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (car.x + 55, car.y + 38),
            7
        )

    # -----------------------------
    # DRAW FROG
    # -----------------------------
    pygame.draw.ellipse(
        screen,
        DARK_GREEN,
        frog
    )

    # Eyes
    pygame.draw.circle(
        screen,
        WHITE,
        (frog.x + 12, frog.y + 10),
        7
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (frog.x + 28, frog.y + 10),
        7
    )

    # Pupils
    pygame.draw.circle(
        screen,
        BLACK,
        (frog.x + 12, frog.y + 10),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (frog.x + 28, frog.y + 10),
        3
    )

    # -----------------------------
    # SCORE
    # -----------------------------
    score_text = font.render(
        f"Score: {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (10, 10)
    )

    # -----------------------------
    # GAME OVER
    # -----------------------------
    if game_over:

        # Dark overlay
        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(170)
        overlay.fill(BLACK)

        screen.blit(
            overlay,
            (0, 0)
        )

        # Game over text
        text1 = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        text2 = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        text3 = font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            text1,
            (
                WIDTH // 2 - text1.get_width() // 2,
                230
            )
        )

        screen.blit(
            text2,
            (
                WIDTH // 2 - text2.get_width() // 2,
                310
            )
        )

        screen.blit(
            text3,
            (
                WIDTH // 2 - text3.get_width() // 2,
                360
            )
        )

    # -----------------------------
    # UPDATE SCREEN
    # -----------------------------
    pygame.display.flip()

pygame.quit()