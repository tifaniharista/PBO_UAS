import math
import random
import pygame
from pygame import mixer

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

pygame.display.set_caption("Space War Game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Base class for game objects
class GameObject:
    def __init__(self, image_path, x, y):
        self.image = pygame.image.load(image_path)
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

# Player class
class Player(GameObject):
    def __init__(self):
        super().__init__('player.png', 350, 500)
        self.x_change = 0

    def move(self):
        self.x += self.x_change
        # Boundary check
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736

# Enemy class
class Enemy(GameObject):
    def __init__(self):
        super().__init__('enemy.png', random.randint(0, 550), random.randint(50, 550))
        self.x_change = 0.5
        self.y_change = 5

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 1
            self.y += self.y_change
        elif self.x >= 736:
            self.x_change = -1
            self.y += self.y_change

# Bullet class
class Bullet(GameObject):
    def __init__(self):
        super().__init__('bullet.png', 0, 480)
        self.state = "ready"

    def fire(self, x):
        self.state = "fire"
        self.x = x

    def move(self):
        if self.state == "fire":
            self.y -= 10
            if self.y <= 0:
                self.state = "ready"
                self.y = 480

# Function to check collision
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

# Score setup
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over font
over_font = pygame.font.Font('freesansbold.ttf', 64)
retry_font = pygame.font.Font('freesansbold.ttf', 40)
retry_button_rect = pygame.Rect(300, 350, 200, 50)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def retry_button():
    pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)  # Green button
    retry_text = retry_font.render("Retry", True, (255, 255, 255))
    screen.blit(retry_text, (retry_button_rect.x + 50, retry_button_rect.y + 10))

def reset_game(player, enemies):
    global score_value
    score_value = 0
    player.x = 350
    player.y = 500
    player.x_change = 0
    for enemy in enemies:
        enemy.x = random.randint(0, 736)
        enemy.y = random.randint(50, 150)

# Main game loop
running = True
game_over = False

player = Player()
bullets = Bullet()
enemies = [Enemy() for _ in range(3)]

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -2
            if event.key == pygame.K_RIGHT:
                player.x_change = 2
            if event.key == pygame.K_SPACE and bullets.state == "ready":
                bulletSound = mixer.Sound("laser.wav")
                bulletSound.play()
                bullets.fire(player.x)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_over and retry_button_rect.collidepoint(event.pos):
            reset_game(player, enemies)
            game_over = False

    if not game_over:
        player.move()

        for enemy in enemies:
            if enemy.y > 440:
                game_over_text()
                game_over = True
                break

            enemy.move()
            collision = is_collision(enemy.x, enemy.y, bullets.x, bullets.y)
            if collision:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()
                bullets.y = 480
                bullets.state = "ready"
                score_value += 1
                enemy.x = random.randint(0, 736)
                enemy.y = random.randint(50, 150)

            enemy.draw()

        bullets.move()
        bullets.draw()
        player.draw()
        show_score(10, 10)

    if game_over:
        retry_button()
        game_over_text()

    pygame.display.update()
