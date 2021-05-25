from array import typecodes
from warnings import catch_warnings
import pygame
from utils import load_image
from random import randint
from operator import xor

pygame.init()
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()
running = True
import sys


class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, targets)
        all_sprites.add(self)
        self.image = load_image('apple.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH - self.rect.w)
        self.rect.y = randint(0, HEIGHT - self.rect.h)


class Snake():
    def __init__(self):
        # Координаты точек хвоста начиная с головы
        self.tail = []
        self.head = (0, 0)
        # ориентация
        self.orientation = 'x'

        self.size = 1
        
        # скорости
        self.dx = 1
        self.dy = 0

        # размер квадрата
        self.size_of_snake = 40


    def update(self, screen):
        # Переход через границы
        x, y = self.head
        print(x, y)
        if x * self.size_of_snake + self.size_of_snake >= WIDTH and self.dx == 1:
            self.head = (-1, y)
        elif y * self.size_of_snake + self.size_of_snake >= HEIGHT and self.dy == 1:
            self.head = (x, 0)
        elif x * self.size_of_snake <= 0 and self.dx < 0:
            self.head = ((WIDTH + self.size_of_snake) // self.size_of_snake, y)
        elif y * self.size_of_snake <= 0 and self.dy < 0:
            self.head = (x, (HEIGHT + self.size_of_snake) // self.size_of_snake)

        x, y = self.head
        # Проверка поедания еды
        for sprite in targets:
            if sprite.rect.x + sprite.rect.w >= x * self.size_of_snake and\
                sprite.rect.y + sprite.rect.h >= y * self.size_of_snake and\
                x * self.size_of_snake + self.size_of_snake >= sprite.rect.x and\
                y * self.size_of_snake + self.size_of_snake >= sprite.rect.y:
                self.size += 1
                self.add_new_section()
                sprite.kill()
                Target()
                break

        # Механика
        ltx, lty = self.head
        for i, v in enumerate(self.tail):
            _ltx, _lty = self.tail[i]
            self.tail[i] = ltx, lty
            ltx = _ltx
            lty = _lty
        x, y = self.head
        self.head = (x + self.dx, y + self.dy)
        for pos in self.tail:
            if pos == self.head:
                font = pygame.font.SysFont('Times New Roman', 25)
                text = font.render('Game Over', False, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.event.wait(pygame.KEYUP)
                sys.exit()
                        


    def add_new_section(self):
        self.tail = [self.head] + self.tail
        x, y = self.head
        self.head = x + self.dx, y + self.dy
    

    def draw(self, screen):
        x, y = self.head
        pygame.draw.rect(screen, (255, 0, 0), (x * self.size_of_snake, y * self.size_of_snake, self.size_of_snake, self.size_of_snake))
        for x, y in self.tail:
            pygame.draw.rect(screen, (255, 0, 0), (x * self.size_of_snake, y * self.size_of_snake, self.size_of_snake, self.size_of_snake))





class Board:
    def __init__(self, side_of_cube):
        self.side = side_of_cube

    def draw_board(self, screen):
        for row in range((HEIGHT // self.side) + 1):
            for col in range((WIDTH // self.side) + 1):
                row_s = row * self.side
                col_s = col * self.side
                pygame.draw.rect(screen, (255, 255, 255), (col_s, row_s, self.side, self.side), 1)



board = Board(40)
snake = Snake()
# all_sprites.add(snake)
clock = pygame.time.Clock()
FPS = 5
target = Target()
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_d and snake.dx == 0:
                snake.dx = 1
                snake.dy = 0
                snake.orientation = 'x'
            elif ev.key == pygame.K_a and snake.dx == 0:
                snake.dx = -1
                snake.dy = 0
                snake.orientation = 'x'
            elif ev.key == pygame.K_s and snake.dy == 0:
                snake.dy = 1
                snake.dx = 0
                snake.orientation = 'y'
            elif ev.key == pygame.K_w and snake.dy == 0:
                snake.dy = -1
                snake.dx = 0
                snake.orientation = 'y'
    screen.fill((0, 0, 0))
    board.draw_board(screen)
    snake.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    snake.update(screen)
    pygame.display.flip()
    clock.tick(FPS)