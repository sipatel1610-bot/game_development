import pygame
import random
import sys

pygame.init()

# Settings
WIDTH, HEIGHT = 500, 700
FPS = 60

# Colours
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 180, 0)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
BLACK = (0, 0, 0)
BROWN = (160, 100, 50)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 65)

# Bird settings
bird_x = 120
bird_y = HEIGHT // 2
bird_radius = 18

gravity = 0.5
velocity = 0
jump_strength = -9

# Pipe settings
pipe_width = 80
pipe_gap = 180
pipe_speed = 4

pipes = []

# Create a new pipe
def create_pipe():
    height = random.randint(100, 400)

    return {
        "x": WIDTH,
        "top": height,
        "bottom": height + pipe_gap,
        "passed": False
    }

# Reset the game
def reset_game():
    global bird_y, velocity, pipes, score, game_over, started

    bird_y = HEIGHT // 2
    velocity = 0
    pipes = [create_pipe()]
    score = 0
    game_over = False
    started = False

# Starting values
pipes.append(create_pipe())

score = 0
best_score = 0
game_over = False
started = False

running = True

# Main game loop
while running:

    clock.tick(FPS)

    # Check keyboard and window events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if not game_over:
                    started = True
                    velocity = jump_strength

            if event.key == pygame.K_r and game_over:
                reset_game()

    # Update the game only after it starts
    if started and not game_over:

        # Make the bird fall
        velocity += gravity
        bird_y += velocity

        # Move pipes to the left
        for pipe in pipes:
            pipe["x"] -= pipe_speed

        # Remove pipes that leave the screen
        if pipes[0]["x"] + pipe_width < 0:
            pipes.pop(0)

        # Create new pipes
        if pipes[-1]["x"] < WIDTH - 220:
            pipes.append(create_pipe())

        # Increase score when the bird passes a pipe
        for pipe in pipes:
            if not pipe["passed"] and pipe["x"] + pipe_width < bird_x:
                pipe["passed"] = True
                score += 1
                best_score = max(best_score, score)

        # Bird collision rectangle
        bird_rect = pygame.Rect(
            bird_x - bird_radius,
            bird_y - bird_radius,
            bird_radius * 2,
            bird_radius * 2
        )

        # Check if the bird hits the top or bottom
        if bird_y - bird_radius <= 0 or bird_y + bird_radius >= HEIGHT - 40:
            game_over = True

        # Check if the bird hits a pipe
        for pipe in pipes:

            top_rect = pygame.Rect(
                pipe["x"], 0,
                pipe_width, pipe["top"]
            )

            bottom_rect = pygame.Rect(
                pipe["x"], pipe["bottom"],
                pipe_width, HEIGHT - pipe["bottom"] - 40
            )

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_over = True

    # Draw the sky
    screen.fill(BLUE)

    # Draw simple clouds
    pygame.draw.circle(screen, WHITE, (70, 100), 22)
    pygame.draw.circle(screen, WHITE, (95, 95), 28)
    pygame.draw.circle(screen, WHITE, (120, 105), 20)

    pygame.draw.circle(screen, WHITE, (340, 170), 20)
    pygame.draw.circle(screen, WHITE, (365, 160), 27)
    pygame.draw.circle(screen, WHITE, (390, 170), 20)

    # Draw pipes
    for pipe in pipes:

        pygame.draw.rect(
            screen, GREEN,
            (pipe["x"], 0, pipe_width, pipe["top"])
        )

        pygame.draw.rect(
            screen, GREEN,
            (
                pipe["x"], pipe["bottom"],
                pipe_width, HEIGHT - pipe["bottom"] - 40
            )
        )

    # Draw the ground
    pygame.draw.rect(screen, BROWN, (0, HEIGHT - 40, WIDTH, 40))
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 40, WIDTH, 8))

    # Draw the bird
    pygame.draw.circle(
        screen, YELLOW,
        (bird_x, int(bird_y)), bird_radius
    )

    # Bird eye
    pygame.draw.circle(
        screen, WHITE,
        (bird_x + 6, int(bird_y) - 6), 6
    )
    pygame.draw.circle(
        screen, BLACK,
        (bird_x + 8, int(bird_y) - 6), 3
    )

    # Bird beak
    pygame.draw.polygon(
        screen, ORANGE,
        [
            (bird_x + 14, int(bird_y)),
            (bird_x + 27, int(bird_y) + 4),
            (bird_x + 14, int(bird_y) + 8)
        ]
    )

    # Show the score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    best_text = font.render(f"Best: {best_score}", True, BLACK)
    screen.blit(best_text, (20, 55))

    # Starting screen
    if not started and not game_over:

        title = big_font.render("FLAPPY BIRD", True, BLACK)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 280)
        )

        message = font.render("Press SPACE to Start!", True, BLACK)
        screen.blit(
            message,
            (WIDTH // 2 - message.get_width() // 2, 350)
        )

    # Game over screen
    if game_over:

        title = big_font.render("GAME OVER", True, BLACK)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 280)
        )

        restart = font.render("Press R to Restart", True, BLACK)
        screen.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, 350)
        )

    # Update the screen
    pygame.display.flip()