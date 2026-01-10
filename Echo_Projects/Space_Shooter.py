import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Space Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_width = 50
player_height = 40
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 70
player_speed = 6

# Bullet
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy
enemy_width = 40
enemy_height = 40
enemy_speed = 3
enemies = []

# Score
score = 0
font = pygame.font.SysFont("arial", 30)

def draw_text(text, x, y):
    render = font.render(text, True, WHITE)
    screen.blit(render, (x, y))

def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-100, -40)
    enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

# Main loop
running = True
enemy_timer = 0

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:
            bullets.append(pygame.Rect(player_x + 22, player_y, bullet_width, bullet_height))

    # Player
    player = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, WHITE, player)

    # Bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        pygame.draw.rect(screen, WHITE, bullet)
        if bullet.y < 0:
            bullets.remove(bullet)

    # Enemies
    enemy_timer += 1
    if enemy_timer > 30:
        spawn_enemy()
        enemy_timer = 0

    for enemy in enemies[:]:
        enemy.y += enemy_speed
        pygame.draw.rect(screen, RED, enemy)

        # Collision with player
        if enemy.colliderect(player):
            running = False

        # Collision with bullet
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    # Score
    draw_text(f"Score: {score}", 10, 10)

    pygame.display.update()

# Game Over
screen.fill(BLACK)
draw_text("GAME OVER", WIDTH // 2 - 90, HEIGHT // 2 - 20)
draw_text(f"Final Score: {score}", WIDTH // 2 - 110, HEIGHT // 2 + 20)
pygame.display.update()
pygame.time.delay(3000)

pygame.quit()
sys.exit(format)
