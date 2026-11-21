
import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

FPS = 60
VEL = 5
BOOST_VEL = 9
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Draw everything
def draw_window(red, yellow, red_bullets, yellow_bullets,
                red_health, yellow_health, red_score,
                yellow_score, power_up):

    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, BORDER)

    red_text = HEALTH_FONT.render(
        "RED: " + str(red_health) + "  Score: " + str(red_score), 1, WHITE)
    yellow_text = HEALTH_FONT.render(
        "YELLOW: " + str(yellow_health) + "  Score: " + str(yellow_score), 1, WHITE)

    WIN.blit(red_text, (WIDTH - red_text.get_width() - 10, 10))
    WIN.blit(yellow_text, (10, 10))

    pygame.draw.rect(WIN, RED, red)
    pygame.draw.rect(WIN, YELLOW, yellow)

    # Draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Draw speed boost power-up
    pygame.draw.rect(WIN, GREEN, power_up)

    pygame.display.update()


# Yellow movement
def yellow_handle_movement(keys_pressed, yellow, speed):
    if keys_pressed[pygame.K_a] and yellow.x - speed > 0:
        yellow.x -= speed
    if keys_pressed[pygame.K_d] and yellow.x + speed + yellow.width < BORDER.x:
        yellow.x += speed
    if keys_pressed[pygame.K_w] and yellow.y - speed > 0:
        yellow.y -= speed
    if keys_pressed[pygame.K_s] and yellow.y + speed + yellow.height < HEIGHT:
        yellow.y += speed


# Red movement
def red_handle_movement(keys_pressed, red, speed):
    if keys_pressed[pygame.K_LEFT] and red.x - speed > BORDER.x + BORDER.width:
        red.x -= speed
    if keys_pressed[pygame.K_RIGHT] and red.x + speed + red.width < WIDTH:
        red.x += speed
    if keys_pressed[pygame.K_UP] and red.y - speed > 0:
        red.y -= speed
    if keys_pressed[pygame.K_DOWN] and red.y + speed + red.height < HEIGHT:
        red.y += speed


# Move bullets and check hits
def handle_bullets(yellow_bullets, red_bullets, yellow, red,
                   red_score, yellow_score):

    for bullet in yellow_bullets[:]:
        bullet.x += BULLET_VEL

        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            yellow_score += 1

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets[:]:
        bullet.x -= BULLET_VEL

        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            red_score += 1

        elif bullet.x < 0:
            red_bullets.remove(bullet)

    return red_score, yellow_score


# Winner screen
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (
        WIDTH / 2 - draw_text.get_width() / 2,
        HEIGHT / 2 - draw_text.get_height() / 2
    ))
    restart_text = HEALTH_FONT.render("Press R to restart", 1, WHITE)
    WIN.blit(restart_text, (
        WIDTH / 2 - restart_text.get_width() / 2, 400
    ))
    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    red_score = 0
    yellow_score = 0

    # Speed boost settings
    power_up = pygame.Rect(
        random.randint(200, 650), random.randint(100, 400), 25, 25
    )

    red_speed = VEL
    yellow_speed = VEL

    red_boost_timer = 0
    yellow_boost_timer = 0

    clock = pygame.time.Clock()
    run = True
    game_over = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN and not game_over:

                if event.key == pygame.K_SPACE and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10, 5
                    )
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height // 2 - 2,
                        10, 5
                    )
                    red_bullets.append(bullet)

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

            # Restart game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if game_over:
                    main()
                    return

        if red_health <= 0:
            game_over = True
            winner_text = "Yellow wins!"

        elif yellow_health <= 0:
            game_over = True
            winner_text = "Red wins!"

        if game_over:
            draw_winner(winner_text)
            continue

        keys_pressed = pygame.key.get_pressed()

        # Speed boost movement
        yellow_handle_movement(keys_pressed, yellow, yellow_speed)
        red_handle_movement(keys_pressed, red, red_speed)

        # Collect power-up
        if yellow.colliderect(power_up):
            yellow_speed = BOOST_VEL
            yellow_boost_timer = pygame.time.get_ticks()
            power_up.x = random.randint(200, 650)
            power_up.y = random.randint(100, 400)

        if red.colliderect(power_up):
            red_speed = BOOST_VEL
            red_boost_timer = pygame.time.get_ticks()
            power_up.x = random.randint(200, 650)
            power_up.y = random.randint(100, 400)

        # Boost lasts 5 seconds
        current_time = pygame.time.get_ticks()

        if current_time - yellow_boost_timer > 5000:
            yellow_speed = VEL

        if current_time - red_boost_timer > 5000:
            red_speed = VEL

        # Move bullets
        red_score, yellow_score = handle_bullets(
            yellow_bullets, red_bullets, yellow, red,
            red_score, yellow_score
        )

        draw_window(
            red, yellow, red_bullets, yellow_bullets,
            red_health, yellow_health, red_score,
            yellow_score, power_up
        )

    pygame.quit()


if __name__ == "__main__":
    main()

print("End of game. Congratulations, you made it!")