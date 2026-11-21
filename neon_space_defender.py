import pygame
import random
import math

pygame.init()

#screen
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Space Survival")

clock = pygame.time.Clock()

#colors
BLACK = (8, 10, 25)
WHITE = (255, 255, 255)
CYAN = (0, 240, 255)
PINK = (255, 60, 150)
YELLOW = (255, 230, 50)
RED = (255, 70, 70)
PURPLE = (160, 90, 255)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 80)

#background stars
stars = []
for i in range(80):
    stars.append([
        random.randint(0, WIDTH),
        random.randint(0, WIDTH),
        random.randint(1, 3)
    ])

#game variables
player = pygame.Rect(375, 520, 50, 40)
bullets = []
asteroids = []
particles = []

score = 0
lives = 3
game_over = False
spawn_timer = 0
shoot_timer = 0

running = True

while running:
    clock.tick(60)

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                score = 0
                lives = 3
                game_over = False
                bullets.clear()
                asteroids.clear()
                particles.clear()
                player.x = 375
                spawn_timer = 0
                shoot_timer = 0

    keys = pygame.key.get_pressed()

    screen.fill(BLACK)

    #moving stars
    for star in stars:
        star[1] += star[2]

        if star[1] > HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, WIDTH)

        pygame.draw.circle(
            screen, WHITE, 
            (star[0], star[1]), star[2]
        )

    if not game_over:

        #player movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 7

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 7

        player.clamp_ip(screen.get_rect())

        #shooting
        if shoot_timer > 0:
            shoot_timer -= 1

        if keys[pygame.K_SPACE] and shoot_timer == 0:
            bullets.append(
                pygame.Rect(player.centerx - 3,
                            player.top, 6, 18)
            )
            shoot_timer = 12

        #move bullets
        for bullet in bullets[:]:
            bullet.y -= 12

            if bullet.bottom < 0:
                bullets.remove(bullet)
            else:
                pygame.draw.rect(
                    screen, CYAN, bullet, 
                    border_radius = 3
                )

        #spawn asteroids
        spawn_timer += 1
        spawn_delay = max(15, 45 - score // 50)
        
        if spawn_timer >= spawn_delay:
            size = random.randint(25, 55)

            asteroids.append({
                "rect": pygame.Rect(
                    random.randint(0, WIDTH - size),
                    -size, size, size
                ),
                "speed": random.randint(3, 6)
                            + score // 100                    
            })

            spawn_timer = 0

        #move asteroids
        for asteroid in asteroids[:]:
            rect = asteroid["rect"]
            rect.y += asteroid["speed"]

            pygame.draw.circle(
                screen, PURPLE, 
                rect.center, rect.width // 2
            )
            pygame.draw.circle(
                screen, PINK, 
                rect.center, rect.width // 2, 3
            )

            #asteroid hits player
            if rect.colliderect(player):
                asteroids.remove(asteroid)
                lives -= 1

                if lives <= 0:
                        game_over = True
                continue

            #asteroid misses player
            if rect.top > HEIGHT:
                asteroids.remove(asteroid)
                continue

            #bullet collision
            for bullet in bullets[:]:
                if rect.colliderect(bullet):
                    if bullet in bullets:
                        bullets.remove(bullet)

                    if asteroid in asteroids:
                        asteroids.remove(asteroid)

                    score += 10

                    #explosion particles
                    for i in range(12):
                        particles.append([
                            rect.centerx,
                            rect.centery,
                            random.uniform(-4, 4),
                            random.uniform(-4, 4),
                            20
                        ])
                    break

        #draw spaceship
        pygame.draw.polygon(
            screen, CYAN,
            [
                (player.centerx, player.top),
                (player.left, player.bottom),
                (player.centerx, player.bottom - 12),
                (player.right, player.bottom)
            ]
       )

        pygame.draw.polygon(
            screen, WHITE,
            [
                (player.centerx, player.top + 12),
                (player.centerx - 7, player.bottom - 12),
                (player.centerx + 7, player.bottom - 12)
            ]
        )

        #engine flame
        pygame.draw.polygon(
            screen, YELLOW, 
            [
                (player.centerx - 8, player.bottom),
                (player.centerx + 8, player.bottom),
                (player.centerx, player.bottom + 15)
            ]
        )

    #explosion animation
    for particle in particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 1

        if particle[4] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(
                screen, YELLOW,
                (int(particle[0]), int(particle[1])), 3

            )

    #score display
    score_text = font.render(
        f"Score: {score}", True, CYAN
    )
    lives_text = font.render(
        f"LIVES: {lives}", True, PINK
    )

    screen.blit(score_text, (20, 20))
    screen.blit(lives_text, (WIDTH - 150,20))

    #game over screen
    if game_over:
        text = font.render(
            "GAME OVER", True, RED
        )
        restart = font.render(
            "Press R to Restart", True, WHITE
        )

        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, 260))
        )
        screen.blit(
            restart, 
            restart.get_rect(center=(WIDTH // 2, 340))
        )

    pygame.display.flip()

pygame.quit()