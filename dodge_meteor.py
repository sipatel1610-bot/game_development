import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500,700
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dodge the Meteor")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

WHITE = (255,255,255)
RED = (220,50,50)
BLUE = (50,150,255)
BLACK = (20,20,20)

player = pygame.Rect(WIDTH//2-25,HEIGHT - 70,50,50)
player_speed = 7

meteors = []
meteor_speed = 6
score = 0

spawn_timer = 0

running = True

while running:
    clock.tick(60)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False

keys = pygame.key.get_pressed()

if keys[pygame.K_LEFT] and player.left > 0:
    player.x -= player_speed
if keys[pygame.K_RIGHT] and player.right < WIDTH:
    player.x += player_speed

spawn_timer += 1
if spawn_timer >= 20:
    spawn_timer = 0
    x = random.randint(0,WIDTH - 40)
    meteors.append(pygame.RECT(x, -40, 40, 40))

for meteor in meteors[:]:
    meteor.y += meteor_speed

if meteor.colliderect(player):
    running = False

if meteor.top > HEIGHT:
    meteors.remove(meteor)
    score += 1
    
screen.fill(BLACK)

pygame.draw.rect(screen,BLUE,player)

for meteor in meteors:
    pygame.draw.circle(screen,RED,meteor.center,20)

text = font.render(f"Score: {score}", True, WHITE)
screen.blit(text, (10,10))

pygame.display.flip()

pygame.quit()