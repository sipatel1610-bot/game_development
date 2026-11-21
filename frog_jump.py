import pygame
import random

pygame.init()

# window
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Jump")
clock = pygame.time.Clock()

# colors
GREEN = (50, 200, 50)
DARK_GREEN = (20, 120, 20)
GRAY = (60, 60, 60)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 220, 50)
BLACK = (0, 0, 0)

font = pygame.font.SysFont(None, 40)

# player
frog = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 60, 40, 40)
frog_speed = 50

# car lanes
lanes = [120, 220, 320, 420, 520]
cars = []

for i, y in enumerate(lanes):
    for j in range(3):
        x = random.randint(0, WIDTH)
        speed = random.choice([3, 4, 5]) * (1 if i % 2 == 0 else -1)
        cars.append([pygame.Rect(x + j * 220, y, 70, 40), speed])

score = 0
running = True
game_over = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                frog.x -= frog_speed
            elif event.key == pygame.K_RIGHT:
                frog.x += frog_speed
            elif event.key == pygame.K_UP:
                frog.y -= frog_speed
            elif event.key == pygame.K_DOWN:
                frog.y += frog_speed

    if not game_over:
        # keep frog inside screen
        frog.x = max(0, min(WIDTH - frog.width, frog.x))
        frog.y = max(0, min(HEIGHT - frog.height, frog.y))

        # move cars
        for car, speed in cars:
            car.x += speed

            if speed > 0 and car.x > WIDTH:
                car.x = -80
            elif speed < 0 and car.x < -80:
                car.x = WIDTH + 20

            # collision
            if frog.colliderect(car):
                game_over = True

        # reached top
        if frog.y < 40:
            score += 1
            frog.x = WIDTH // 2 - 20
            frog.y = HEIGHT - 60

            # increase difficulty
            for car_data in cars:
                if car_data[1] > 0:
                    car_data[1] += 0.2
                else:
                    car_data[1] -= 0.2

    # draw background
    screen.fill(GREEN)

    # draw road lines
    for y in lanes:
        pygame.draw.rect(screen, GRAY, (0, y - 20, WIDTH, 80))
        for x in range(0, WIDTH, 60):
            pygame.draw.circle(screen, WHITE, (x, y), 6)

    # draw goal area
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))

    # draw cars
    for car, speed in cars:
        color = RED if speed > 0 else YELLOW
        pygame.draw.rect(screen, color, car, border_radius=8)
        pygame.draw.circle(screen, BLACK, (car.x + 15, car.y + 35), 6)
        pygame.draw.circle(screen, BLACK, (car.x + 55, car.y + 35), 6)

    # draw frog
    pygame.draw.ellipse(screen, DARK_GREEN, frog)
    pygame.draw.circle(screen, WHITE, (frog.x + 12, frog.y + 12), 4)
    pygame.draw.circle(screen, WHITE, (frog.x + 28, frog.y + 12), 4)

    # score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over = font.render("GAME OVER!", True, WHITE)
        retry = font.render("Close window to exit", True, WHITE)

        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(retry, (WIDTH // 2 - retry.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

pygame.quit()