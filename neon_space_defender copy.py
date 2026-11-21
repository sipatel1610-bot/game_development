import pygame
import random
import math


pygame.init()


# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Space Survival - Power-Ups Edition")


clock = pygame.time.Clock()


# Colors
BLACK = (8, 10, 25)
GOLD = (255, 215, 0)
CYAN = (0, 240, 255)
VIOLET = (238, 130, 238)
WHITE = (255, 255, 255)
RED = (255, 70, 70)
INDIGO = (25, 25, 140)
YELLOW = (255, 230, 50)
GREEN = (50, 255, 120)


font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 80)


# Background stars
stars = []
for i in range(80):
   stars.append([
       random.randint(0, WIDTH),
       random.randint(0, HEIGHT),
       random.randint(1, 3)
   ])


# Game variables
player = pygame.Rect(375, 520, 50, 40)
bullets = []
asteroids = []
particles = []
powerups = []  # Stores active falling power-ups


score = 0
high_score = 0
lives = 3
max_lives = 5
shield_timer = 0  # Counts down from 300 (5 seconds at 60 FPS)
powerup_timer = 0
game_over = False
spawn_timer = 0
shoot_timer = 0


running = True


while running:
   clock.tick(60)


   # Events
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False


       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_r and game_over:
               score = 0
               lives = 3
               shield_timer = 0
               powerup_timer = 0
               game_over = False
               bullets.clear()
               asteroids.clear()
               particles.clear()
               powerups.clear()
               player.x = 375
               player.y = 520
               spawn_timer = 0
               shoot_timer = 0


   keys = pygame.key.get_pressed()
   screen.fill(BLACK)


   # Moving stars
   for star in stars:
       star[1] += star[2]
       if star[1] > HEIGHT:
           star[1] = 0
           star[0] = random.randint(0, WIDTH)


       pygame.draw.circle(screen, GOLD, (star[0], star[1]), star[2])


   if not game_over:
       # 4-way player movement
       if keys[pygame.K_LEFT] or keys[pygame.K_a]:
           player.x -= 8
       if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
           player.x += 8
       if keys[pygame.K_UP] or keys[pygame.K_w]:
           player.y -= 8
       if keys[pygame.K_DOWN] or keys[pygame.K_s]:
           player.y += 8


       player.clamp_ip(screen.get_rect())


       # Count down shield timer
       if shield_timer > 0:
           shield_timer -= 1


       # Shooting (Twin Lasers)
       if shoot_timer > 0:
           shoot_timer -= 1


       if keys[pygame.K_SPACE] and shoot_timer == 0:
           bullets.append(pygame.Rect(player.left + 4, player.top + 10, 5, 18))
           bullets.append(pygame.Rect(player.right - 9, player.top + 10, 5, 18))
           shoot_timer = 10


       # Move bullets
       for bullet in bullets[:]:
           bullet.y -= 14
           if bullet.bottom < 0:
               bullets.remove(bullet)
           else:
               pygame.draw.rect(screen, CYAN, bullet, border_radius=3)


       # Spawn power-ups occasionally (every ~7 seconds)
       powerup_timer += 1
       if powerup_timer >= 420:
           ptype = random.choice(["health", "shield"])
           powerups.append({
               "rect": pygame.Rect(random.randint(30, WIDTH - 60), -30, 30, 30),
               "type": ptype,
               "pulse": 0
           })
           powerup_timer = 0


       # Move & draw power-ups
       for p in powerups[:]:
           rect = p["rect"]
           rect.y += 3
           p["pulse"] += 0.15


           # Pulsing glow radius using math.sin
           glow_radius = int(18 + math.sin(p["pulse"]) * 4)


           if p["type"] == "health":
               # Outer glow ring
               pygame.draw.circle(screen, GREEN, rect.center, glow_radius, 2)
               # Green "+" cross
               pygame.draw.rect(screen, GREEN, (rect.centerx - 3, rect.centery - 9, 6, 18))
               pygame.draw.rect(screen, GREEN, (rect.centerx - 9, rect.centery - 3, 18, 6))
           else:
               # Cyan shield orb
               pygame.draw.circle(screen, CYAN, rect.center, glow_radius, 2)
               pygame.draw.circle(screen, WHITE, rect.center, 8, 2)


           # Player collects power-up
           if rect.colliderect(player):
               if p["type"] == "health" and lives < max_lives:
                   lives += 1
               elif p["type"] == "shield":
                   shield_timer = 300  # 5 seconds of shield


               # Sparkle burst on pickup
               burst_color = GREEN if p["type"] == "health" else CYAN
               for _ in range(15):
                   particles.append([
                       rect.centerx, rect.centery,
                       random.uniform(-4, 4), random.uniform(-4, 4),
                       20, burst_color
                   ])
               powerups.remove(p)
               continue


           if rect.top > HEIGHT:
               powerups.remove(p)


       # Spawn asteroids
       spawn_timer += 1
       spawn_delay = max(15, 45 - score // 50)


       if spawn_timer >= spawn_delay:
           size = random.randint(25, 55)
           asteroids.append({
               "rect": pygame.Rect(random.randint(0, WIDTH - size), -size, size, size),
               "speed": random.randint(3, 6) + score // 100
           })
           spawn_timer = 0


       # Move asteroids
       for asteroid in asteroids[:]:
           rect = asteroid["rect"]
           rect.y += asteroid["speed"]


           pygame.draw.circle(screen, INDIGO, rect.center, rect.width // 2)
           pygame.draw.circle(screen, VIOLET, rect.center, rect.width // 2, 3)


           # Asteroid hits player
           if rect.colliderect(player):
               asteroids.remove(asteroid)


               # If shield is active, smash the asteroid safely!
               if shield_timer > 0:
                   for _ in range(15):
                       particles.append([
                           rect.centerx, rect.centery,
                           random.uniform(-5, 5), random.uniform(-5, 5),
                           20, CYAN
                       ])
               else:
                   lives -= 1
                   if lives <= 0:
                       game_over = True
               continue


           # Asteroid misses player
           if rect.top > HEIGHT:
               asteroids.remove(asteroid)
               continue


           # Bullet collision
           for bullet in bullets[:]:
               if rect.colliderect(bullet):
                   if bullet in bullets:
                       bullets.remove(bullet)
                   if asteroid in asteroids:
                       asteroids.remove(asteroid)


                   score += (65 - rect.width)
                   if score > high_score:
                       high_score = score


                   for _ in range(20):
                       particles.append([
                           rect.centerx, rect.centery,
                           random.uniform(-5, 5), random.uniform(-5, 5),
                           random.randint(15, 30), YELLOW
                       ])
                   break


       # Draw spaceship
       pygame.draw.polygon(
           screen, CYAN,
           [
               (player.centerx, player.top),
               (player.left, player.bottom),
               (player.centerx, player.bottom - 12),
               (player.right, player.bottom)
           ]
       )


       # Cockpit
       pygame.draw.polygon(
           screen, GOLD,
           [
               (player.centerx, player.top + 12),
               (player.centerx - 7, player.bottom - 12),
               (player.centerx + 7, player.bottom - 12)
           ]
       )


       # Flickering engine flame
       flame_length = random.randint(12, 26)
       pygame.draw.polygon(
           screen, WHITE,
           [
               (player.centerx - 8, player.bottom),
               (player.centerx + 8, player.bottom),
               (player.centerx, player.bottom + flame_length)
           ]
       )


       # Draw active energy shield bubble around ship
       if shield_timer > 0:
           # Blink quickly when shield is about to expire (last 1.5 seconds)
           if shield_timer > 90 or (shield_timer // 5) % 2 == 0:
               pygame.draw.circle(screen, CYAN, player.center, 36, 3)


   # Explosion & pickup particle animation
   for particle in particles[:]:
       particle[0] += particle[2]
       particle[1] += particle[3]
       particle[4] -= 1


       if particle[4] <= 0:
           particles.remove(particle)
       else:
           pygame.draw.circle(
               screen, particle[5],
               (int(particle[0]), int(particle[1])), 3
           )


   # Score, High Score & Lives display
   score_text = font.render(f"Score: {score}", True, CYAN)
   high_score_text = font.render(f"Best: {high_score}", True, GOLD)
   lives_text = font.render(f"LIVES: {lives}/{max_lives}", True, VIOLET)


   screen.blit(score_text, (20, 20))
   screen.blit(high_score_text, (20, 55))
   screen.blit(lives_text, (WIDTH - 170, 20))


   # Show shield countdown if active
   if shield_timer > 0 and not game_over:
       shield_sec = math.ceil(shield_timer / 60)
       shield_text = font.render(f"SHIELD: {shield_sec}s", True, CYAN)
       screen.blit(shield_text, (WIDTH - 170, 55))


   # Game Over screen
   if game_over:
       text = big_font.render("GAME OVER", True, RED)
       final_score = font.render(f"Final Score: {score}  |  Best: {high_score}", True, WHITE)
       restart = font.render("Press R to Restart", True, GOLD)


       screen.blit(text, text.get_rect(center=(WIDTH // 2, 230)))
       screen.blit(final_score, final_score.get_rect(center=(WIDTH // 2, 300)))
       screen.blit(restart, restart.get_rect(center=(WIDTH // 2, 360)))


   pygame.display.flip()


pygame.quit()