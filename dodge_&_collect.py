import pygame
import random
import math


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Survival")


clock = pygame.time.Clock()


font = pygame.font.SysFont(None, 40)


player = pygame.Rect(400, 300, 40, 40)


coins = []
enemies = []


score = 0
enemy_speed = 2


for _ in range(5):
    coins.append(
        pygame.Rect(
            random.randint(0, WIDTH-20),
            random.randint(0, HEIGHT-20),
            20,
            20
        )
    )


for _ in range(3):
    enemies.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    ])


game_over = False


running = True


while running:


    clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player.x = 400
                    player.y = 300
                    score = 0
                    enemy_speed = 2
                    game_over = False


                    enemies.clear()


                    for _ in range(3):
                        enemies.append([
                            random.randint(0, WIDTH),
                            random.randint(0, HEIGHT)
                        ])


    keys = pygame.key.get_pressed()


    if not game_over:


        speed = 5


        if keys[pygame.K_w]:
            player.y -= speed


        if keys[pygame.K_s]:
            player.y += speed


        if keys[pygame.K_a]:
            player.x -= speed


        if keys[pygame.K_d]:
            player.x += speed


        player.clamp_ip(screen.get_rect())


        for coin in coins[:]:
            if player.colliderect(coin):


                score += 1


                coins.remove(coin)


                coins.append(
                    pygame.Rect(
                        random.randint(0, WIDTH-20),
                        random.randint(0, HEIGHT-20),
                        20,
                        20
                    )
                )


                if score % 10 == 0:
                    enemy_speed += 0.5


                    enemies.append([
                        random.randint(0, WIDTH),
                        random.randint(0, HEIGHT)
                    ])


        for enemy in enemies:


            dx = player.centerx - enemy[0]
            dy = player.centery - enemy[1]


            distance = math.hypot(dx, dy)


            if distance != 0:
                enemy[0] += dx / distance * enemy_speed
                enemy[1] += dy / distance * enemy_speed


            enemy_rect = pygame.Rect(enemy[0], enemy[1], 30, 30)


            if player.colliderect(enemy_rect):
                game_over = True


    screen.fill((30, 30, 40))


    for coin in coins:
        pygame.draw.circle(
            screen,
            (255, 215, 0),
            coin.center,
            10
        )


    for enemy in enemies:
        pygame.draw.rect(
            screen,
            (220, 50, 50),
            (enemy[0], enemy[1], 30, 30)
        )


    pygame.draw.rect(screen, (50, 200, 255), player)


    score_text = font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )


    screen.blit(score_text, (10, 10))


    if game_over:
        text1 = font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )


        text2 = font.render(
            "Press R to Restart",
            True,
            (255, 255, 255)
        )


        screen.blit(
            text1,
            (WIDTH//2 - text1.get_width()//2, 250)
        )


        screen.blit(
            text2,
            (WIDTH//2 - text2.get_width()//2, 300)
        )


    pygame.display.flip()


pygame.quit()