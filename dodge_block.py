import pygame
import random

pygame.init()

# screen
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

font = pygame.font.SysFont(None, 30) 
bigfont = pygame.font.SysFont(None, 60) 

# player
player_x = 220
player_y = 520
player_size = 40
player_speed = 6

# block
block_x = random.randint(0, WIDTH - 40)
block_y = -40
block_size = 40
block_speed = 6

score = 0
running = True

while running:
    clock.tick(60)
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # block falling
    block_y += block_speed
    if block_y > HEIGHT:
        block_y = -40
        block_x = random.randint(0, WIDTH - block_size)
        score += 1
        block_speed += 0.2  # increase difficulty

    # rectangles
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    block_rect = pygame.Rect(block_x, block_y, block_size, block_size)

    # collision
    if player_rect.colliderect(block_rect):
        running = False

    # draw
    pygame.draw.rect(screen, (0, 200, 255), player_rect)
    pygame.draw.rect(screen, (255, 80, 80), block_rect)

    # score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()