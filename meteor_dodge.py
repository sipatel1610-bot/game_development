import pygame
import random

pygame.init()

W, H = 700,500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Dodge the Meteors!")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def reset():
    global px, score, speed, meteors, game_over
    px = W // 2
    score = 0
    speed = 5
    game_over = False
    meteors = []
    for _ in range(6):
        meteors.append([
            random.randint(20, W - 20),
            random.randint(-500, -20),
            random.randint(20, 40)
        ])

reset()

running = True

while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            reset()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            px -= 7
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            px += 7

        px = max(20, min(W - 20, px))

        player = pygame.Rect(px - 20, H - 50, 40, 40)

        for m in meteors:
            m[1] += speed

            if m[1] - m[2] > H:
                m[0] = random.randint(20, W - 20)
                m[1] = random.randint(-200, -40)
                m[2] = random.randint(20, 40)
                score += 1
                if score % 5  == 0:
                    speed += 0.4

            meteor = pygame.Rect(
                m[0] - m[2], 
                m[1] - m[2],
                m[2] * 2,
                m[2] * 2, 
            )

            if player.colliderect(meteor):
                game_over = True

screen.fill((10, 10, 25))

#stars
for i in range(60):
    pygame.draw.circle(
        screen,
        (180, 180, 220),
        ((i * 73) % W, (i * 41) % H),
        1,
    )

    #player
    pygame.draw.polygon(
        screen,
        (0, 255, 180),
        [
            (px, H - 60),
            (px - 18, H - 20),
            (px + 18, H - 20),
        ]
    )

    #meteors
    for x,y,r in meteors:
        pygame.draw.circle(screen, (255, 120, 60), (int(x), int(y)), r)
        pygame.draw.circle(screen, (255, 120, 60), (int(x - 8), int(y - 6)), r // 3)
    
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (15, 15))

    if game_over:
        t1 = font.render("GAME OVER", True, (255, 70, 70))
        t2 = font.render("Press P to play again", True, (255,255,255))
        screen.blit(t1, (W // 2 - t1.get_width() // 2, 200))
        screen.blit(t2, (W // 2 - t2.get_width() // 2, 240))

    pygame.display.flip()

pygame.quit()