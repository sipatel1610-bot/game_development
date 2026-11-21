import pygame 
import random 
import math 
 
pygame.init() 
 
WIDTH, HEIGHT = 800, 600 
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("Zombie survival") 
 
clock = pygame.time.Clock() 
 
WHITE = (255, 255, 255) 
RED = (220, 50, 50) 
GREEN = (50, 220, 50) 
BLUE = (80, 150, 255) 
BLACK = (20, 20, 20) 
YELLOW = (255, 220, 0) 
 
font = pygame.font.SysFont(None, 30) 
bigfont = pygame.font.SysFont(None, 60) 
 
player = pygame.Rect(WIDTH//2, HEIGHT//2, 35, 35) 
speed = 6 
 
health = 100 
score = 0 
 
zombies = [] 
healthpacks = [] 
 
bullets = [] 
bullet_speed = 10 
 
spawn_timer = 0 
health_timer = 0 
 
running = True 
game_over = False 
 
def spawn_zombie(): 
    side = random.randint(0,3) 
 
    if side == 0: 
        x = random.randint(0,WIDTH) 
        y = -40 
    elif side == 1: 
        x = WIDTH + 40 
        y = random.randint(0, HEIGHT) 
    elif side == 2: 
        x = random.randint(0, WIDTH) 
        y = HEIGHT + 40 
    else: 
        x = -40 
        y = random.randint(0, HEIGHT) 
 
    zombies.append({ 
        "rect": pygame.Rect(x,y,30,30), 
        "speed": random.uniform(1.5,3.5) 
    }) 
 
def spawn_health(): 
    x = random.randint(40, WIDTH-40) 
    y = random.randint(40, HEIGHT-40) 
    healthpacks.append(pygame.Rect(x,y,20,20)) 
 
while running: 
 
    clock.tick(60) 
 
    # Events
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
        if event.type == pygame.KEYDOWN: 
            
            # Shoot bullet
            if event.key == pygame.K_SPACE and not game_over: 
                bullet = [
                    player.centerx,
                    player.top,
                    0,
                    -1
                ]
                bullets.append(bullet)

            # Restart game
            if event.key == pygame.K_r and game_over:
                player.x = WIDTH // 2
                player.y = HEIGHT // 2

                health = 100
                score = 0

                zombies.clear()
                bullets.clear()
                healthpacks.clear()

                spawn_timer = 0
                health_timer = 0

                game_over = False
 
    if not game_over: 
 
        keys = pygame.key.get_pressed() 
 
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: 
            player.x -= speed 
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            player.x += speed 
        if keys[pygame.K_UP] or keys[pygame.K_w]: 
            player.y -= speed 
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
            player.y += speed 
 
        player.x = max(0,min(WIDTH - player.width,player.x)) 
        player.y = max(0,min(HEIGHT - player.height,player.y)) 
 
        spawn_timer += 1 
        health_timer += 1 
 
        if spawn_timer > 40: 
            spawn_zombie() 
            spawn_timer = 0 
 
        if health_timer > 500: 
            spawn_health() 
            health_timer = 0 
 
        # Zombies move toward player
        for zombie in zombies: 
 
            dx = player.centerx - zombie["rect"].centerx 
            dy = player.centery - zombie["rect"].centery 
 
            dist = math.hypot(dx,dy) 
 
            if dist != 0: 
                zombie["rect"].x += dx/dist*zombie["speed"] 
                zombie["rect"].y += dy/dist*zombie["speed"] 
 
            if zombie["rect"].colliderect(player): 
                health -= 0.25 
 
        # Move bullets
        for b in bullets[:]: 
            b[0] += b[2] * bullet_speed 
            b[1] += b[3] * bullet_speed 
 
            if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT: 
                bullets.remove(b) 
 
        # Bullet hits ONE zombie
        for b in bullets[:]:
            for z in zombies[:]:

                zombie_x = z["rect"].centerx
                zombie_y = z["rect"].centery

                if math.hypot(zombie_x - b[0], zombie_y - b[1]) < 20:

                    zombies.remove(z)
                    bullets.remove(b)
                    score += 1

                    # This bullet is gone, so it cannot kill another zombie
                    break
 
        # Health packs
        for pack in healthpacks[:]: 
            if player.colliderect(pack): 
                health = min(100,health+25) 
                healthpacks.remove(pack) 
 
        score += 0.03 
 
        if health <= 0: 
            game_over = True 
 
    # Background
    screen.fill((35,35,35)) 
 
    # Grid
    for i in range(0,WIDTH,40): 
        pygame.draw.line(
            screen, 
            (50, 50, 50), 
            (i,0), 
            (i, HEIGHT)
        ) 

    for i in range(0,HEIGHT,40): 
        pygame.draw.line(
            screen, 
            (50, 50, 50), 
            (0,i), 
            (WIDTH, i)
        ) 
 
    # Draw bullets
    for b in bullets: 
        pygame.draw.circle(
            screen, 
            YELLOW, 
            (int(b[0]),int(b[1])), 
            5
        ) 
 
    # Draw player
    pygame.draw.rect(screen,BLUE,player) 
 
    # Draw zombies
    for zombie in zombies: 
        pygame.draw.rect(screen,RED,zombie["rect"]) 
 
        eye1 = (
            zombie["rect"].x+8,
            zombie["rect"].y+10
        ) 

        eye2 = (
            zombie["rect"].x+22,
            zombie["rect"].y+10
        ) 
 
        pygame.draw.circle(screen,BLACK,eye1,2) 
        pygame.draw.circle(screen,BLACK,eye2,2) 
 
    # Draw health packs
    for pack in healthpacks: 
        pygame.draw.rect(screen,GREEN,pack) 
 
        pygame.draw.line(
            screen, 
            WHITE,  
            (pack.centerx,pack.top+3), 
            (pack.centerx,pack.bottom-3),
            2
        ) 
 
        pygame.draw.line(
            screen,
            WHITE, 
            (pack.left+3,pack.centery), 
            (pack.right-3,pack.centery),
            2
        ) 
 
    # Health bar
    pygame.draw.rect(screen,RED,(20,20,200,20)) 
    pygame.draw.rect(screen,GREEN,(20,20,health*2,20)) 
    pygame.draw.rect(screen,WHITE,(20,20,200,20),2) 
 
    # Score
    score_text = font.render(
        f"Score: {int(score)}",
        True,
        WHITE
    ) 
    screen.blit(score_text,(20,55)) 
 
    # Zombie count
    zombie_text = font.render(
        f"zombies: {len(zombies)}",
        True,
        YELLOW
    ) 
    screen.blit(zombie_text,(20,85)) 
 
    # Game over screen
    if game_over: 
        over = bigfont.render(
            "GAME OVER",
            True,
            RED
        ) 

        screen.blit(
            over,
            (WIDTH//2-over.get_width()//2,220)
        ) 
 
        final = font.render(
            f"Final Score: {int(score)}",
            True,
            WHITE
        ) 

        screen.blit(
            final,
            (WIDTH//2-final.get_width()//2,300)
        ) 
 
        again = font.render(
            "Press R to restart",
            True,
            WHITE
        ) 

        screen.blit(
            again,
            (WIDTH//2-again.get_width()//2,340)
        ) 
 
    pygame.display.flip() 
 
pygame.quit()