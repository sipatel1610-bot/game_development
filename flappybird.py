import pygame
import random
import sys

pygame.init()

#settings
WIDTH, HEIGHT = 500,700
FPS = 60

WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (0, 180, 0)
YELLOW = (255, 220, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

#bird
bird_x = 120
bird_y = HEIGHT//2
bird_radius = 18

gravity = 0.5
velocity = 0
jump_strength = -9

#pipes
pipe_width = 80
pipe_gap = 180
pipe_speed = 4

pipes = []

def create_pipe():
    height = random.randint(100,450)
    return{
        "x": WIDTH,
        "top": height,
        "bottom": height + pipe_gap,
        "passed": False
    }

pipes.append(create_pipe())

score = 0
game_over = False

#Reset
def reset_game():
    global bird_y, velocity, pipes, score, game_over

    bird_y = HEIGHT // 2
    velocity = 0
    pipes = [create_pipe()]
    score = 0
    game_over = False

#game loop
running = True

while running:

    clock.tick(FPS)

    #events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if not game_over:
                if event.key == pygame.K_SPACE:
                    velocity = jump_strength

            else:
                if event.key == pygame.K_r:
                    reset_game()
    if not game_over:

        #bird physics 
        velocity += gravity
        bird_y += velocity

        #move pipes
        for pipe in pipes:
            pipe["x"] -= pipe_speed

        #remove old pipes
        if pipes[0]["x"] + pipe_width < 0:
            pipes.pop(0)

        #add new pipes
        if pipes[-1]["x"] < WIDTH - 220:
            pipes.append(create_pipe())

        #score
        for pipe in pipes:
            if not pipe["passed"] and pipe["x"] + pipe_width < bird_x:
                pipe["passed"] = True
                score += 1

        #collsion
        bird_rect = pygame.Rect(
            bird_x - bird_radius,
            bird_y - bird_radius,
            bird_radius * 2,
            bird_radius * 2,
        )

        if bird_y <= 0 or bird_y >= HEIGHT:
            game_over = True

        for pipe in pipes:

            top_rect = pygame.Rect(
                pipe["x"], 0,
                pipe_width,
                pipe["top"]
            )

            bottom_rect = pygame.Rect(
                pipe["x"],
                pipe["bottom"],
                pipe_width,
                HEIGHT - pipe["bottom"],
            )

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_over = True
                
    #draw
    screen.fill(BLUE)

    #Pipes
    for pipe in pipes:

        pygame.draw.rect(
            screen, 
            GREEN,
            (pipe["x"], 0, pipe_width, pipe["top"])
        )

        pygame.draw.rect(
            screen, 
            GREEN,
            (
                pipe["x"],
                pipe["bottom"],
                pipe_width,
                HEIGHT - pipe["bottom"],
            ),
        )

    #Bird
    pygame.draw.circle(
        screen, 
        YELLOW,
        (int(bird_x), int(bird_y)),
        bird_radius,
    )

    #score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20,20))

    if game_over:

        text = big_font.render("GAME OVER", True, BLACK)
        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                HEIGHT // 2,
            ),
        )
        restart = font.render("Press R to Restart", True, BLACK)
        screen.blit(
            restart,
            (
                WIDTH // 2 - restart.get_width() // 2,
                HEIGHT // 2,
            ),
        ) 

    pygame.display.flip()