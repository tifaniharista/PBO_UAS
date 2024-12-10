import math
import random
import pygame
from pygame import mixer
from abc import ABC, abstractmethod

pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')

pygame.display.set_caption("Space War Game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Abstract class for game objects
class GameObject(ABC):
    def __init__(self, image_path, x, y):
        self._image = pygame.image.load(image_path)
        self._x = x
        self._y = y

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, screen):
        screen.blit(self._image, (self._x, self._y))

# Player class inheriting from GameObject
class Player(GameObject):
    def __init__(self):
        super().__init__('player.png', 350, 500)
        self._x_change = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 0 <= value <= 736:
            self._x = value

    def move(self):
        self._x += self._x_change
        self.x = self._x  # Ensure it stays within bounds

    def draw(self, screen):
        super().draw(screen)

    def change_direction(self, direction):
        self._x_change = direction

# Enemy class inheriting from GameObject
class Enemy(GameObject):
    def __init__(self):
        super().__init__('enemy.png', random.randint(0, 736), random.randint(50, 150))
        self._x_change = 2
        self._y_change = 10

    def move(self):
        self._x += self._x_change
        if self._x <= 0:
            self._x_change = 2
            self._y += self._y_change
        elif self._x >= 736:
            self._x_change = -2
            self._y += self._y_change

    def draw(self, screen):
        super().draw(screen)

# Bullet class inheriting from GameObject
class Bullet(GameObject):
    def __init__(self):
        super().__init__('bullet.png', 0, 480)
        self.state = "ready"

    def fire(self, x):
        if self.state == "ready":
            self.state = "fire"
            self._x = x
            self._y = 480

    def move(self):
        if self.state == "fire":
            self._y -= 10
            if self._y <= 0:
                self.state = "ready"

    def draw(self, screen):
        if self.state == "fire":
            super().draw(screen)

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

# Retry button setup
retry_font = pygame.font.Font('freesansbold.ttf', 40)
retry_button_rect = pygame.Rect(300, 350, 200, 50)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def retry_button():
    pygame.draw.rect(screen, (0, 255, 0), retry_button_rect)
    retry_text = retry_font.render("Retry", True, (255, 255, 255))
    screen.blit(retry_text, (retry_button_rect.x + 50, retry_button_rect.y + 10))

def reset_game(player, enemies):
    global score_value
    score_value = 0
    player.x = 350
    for enemy in enemies:
        enemy._x = random.randint(0, 736)
        enemy._y = random.randint(50, 150)

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
                player.change_direction(-2)
            if event.key == pygame.K_RIGHT:
                player.change_direction(2)
            if event.key == pygame.K_SPACE:
                mixer.Sound("laser.wav").play()
                bullets.fire(player.x)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.change_direction(0)

        if event.type == pygame.MOUSEBUTTONDOWN and game_over and retry_button_rect.collidepoint(event.pos):
            reset_game(player, enemies)
            game_over = False

    if not game_over:
        player.move()

        for enemy in enemies:
            if enemy._y > 440:
                game_over_text()
                game_over = True
                break

            enemy.move()
            collision = is_collision(enemy._x, enemy._y, bullets._x, bullets._y)
            if collision:
                mixer.Sound("explosion.wav").play()
                bullets.state = "ready"
                score_value += 1
                enemy._x = random.randint(0, 736)
                enemy._y = random.randint(50, 150)

            enemy.draw(screen)

        bullets.move()
        bullets.draw(screen)
        player.draw(screen)
        show_score(10, 10)

    if game_over:
        retry_button()
        game_over_text()

    pygame.display.update()
