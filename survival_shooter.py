import pygame
import random
import math


pygame.init()


# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Survival Shooter")


clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


# Player
player_pos = [WIDTH//2, HEIGHT//2]
player_speed = 5
player_radius = 15


# Bullets
bullets = []
bullet_speed = 10


# Enemies
enemies = []
enemy_speed = 2
spawn_delay = 60
frame_count = 0


score = 0
running = True


def spawn_enemy():
    side = random.choice(["top","bottom","left","right"])
    if side == "top":
        return [random.randint(0, WIDTH), 0]
    elif side == "bottom":
        return [random.randint(0, WIDTH), HEIGHT]
    elif side == "left":
        return [0, random.randint(0, HEIGHT)]
    else:
        return [WIDTH, random.randint(0, HEIGHT)]


while running:
    clock.tick(60)
    screen.fill((10, 10, 30))


    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx = mx - player_pos[0]
            dy = my - player_pos[1]
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx/dist, dy/dist
                bullets.append([player_pos[0], player_pos[1], dx, dy])


    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos[1] += player_speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed


    # Keep inside screen
    player_pos[0] = max(0, min(WIDTH, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT, player_pos[1]))


    # Spawn enemies
    frame_count += 1
    if frame_count % spawn_delay == 0:
        enemies.append(spawn_enemy())


    # Move bullets
    for b in bullets[:]:
        b[0] += b[2] * bullet_speed
        b[1] += b[3] * bullet_speed
        if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT:
            bullets.remove(b)


    # Move enemies
    for e in enemies:
        dx = player_pos[0] - e[0]
        dy = player_pos[1] - e[1]
        dist = math.hypot(dx, dy)
        if dist != 0:
            e[0] += dx/dist * enemy_speed
            e[1] += dy/dist * enemy_speed


    # Collision: bullet vs enemy
    for e in enemies[:]:
        for b in bullets[:]:
            if math.hypot(e[0]-b[0], e[1]-b[1]) < 15:
                enemies.remove(e)
                bullets.remove(b)
                score += 1
                break


    # Collision: enemy vs player
    for e in enemies:
        if math.hypot(e[0]-player_pos[0], e[1]-player_pos[1]) < 20:
            running = False


    # Increase difficulty
    if score % 10 == 0 and score > 0:
        enemy_speed += 0.005
        spawn_delay = max(20, spawn_delay - 0.01)


    # Draw player
    pygame.draw.circle(screen, (0, 255, 200), player_pos, player_radius)


    # Draw bullets
    for b in bullets:
        pygame.draw.circle(screen, (255, 255, 100), (int(b[0]), int(b[1])), 5)


    # Draw enemies
    for e in enemies:
        pygame.draw.circle(screen, (255, 80, 80), (int(e[0]), int(e[1])), 12)


    # Score
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_text, (10,10))


    pygame.display.update()


# Game Over screen
screen.fill((0,0,0))
text = font.render(f"Game Over! Score: {score}", True, (255,255,255))
screen.blit(text, (WIDTH//2 - 120, HEIGHT//2))
pygame.display.update()
pygame.time.delay(2000)


pygame.quit()