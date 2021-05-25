import pygame
from utils import load_image
from random import randint

pygame.init()
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
all_sprites = pygame.sprite.Group()
targets = pygame.sprite.Group()


class Snake():
    def __init__(self):
        # Координаты точек хвоста начиная с головы
        self.tail = [(-1, 0), (-2, 0)]
        self.head = (0, 0)
        # ориентация
        self.orientation = 'x'

        self.size = 3
        
        # скорости
        self.dx = 1
        self.dy = 0

        # размер квадрата
        self.size_of_snake = 40


    def update(self):
        # Механика, как ходит червь
        x, y = self.head
        if x >= WIDTH and self.dx > 0:
            self.head = (0, y)
        elif y >= HEIGHT and self.dy > 0:
            self.head = (x, 0)
        elif x + self.size_of_snake <= 0 and self.dx < 0:
            self.head = (WIDTH + self.size_of_snake, y)
        elif y + self.size_of_snake <= 0 and self.dy < 0:
            self.head = (x, HEIGHT + self.size_of_snake)
        buffer = [(x, y)]
        
        for sprite in targets:
            if sprite.rect.x + sprite.rect.w >= x and\
                sprite.rect.y + sprite.rect.h >= y and\
                x + self.size_of_snake >= sprite.rect.x and\
                y + self.size_of_snake >= sprite.rect.y:
                self.size += 1
                sprite.kill()
                print('Съел', sprite.rect.x, sprite.rect.y)
        ltx, lty = self.head
        for i, v in enumerate(self.tail):
            _ltx, _lty = self.tail[i]
            
            self.tail[i] = ltx, lty
            ltx = _ltx
            lty = _lty
        self.head = (x + self.dx, y + self.dy)
        self.tail = buffer

    def draw(self, screen):
        x, y = self.head
        pygame.draw.rect(screen, (255, 0, 0), (x * self.size_of_snake, y * self.size_of_snake, self.size_of_snake, self.size_of_snake))
        for x, y in self.tail:
            pygame.draw.rect(screen, (255, 0, 0), (x * self.size_of_snake, y * self.size_of_snake, self.size_of_snake, self.size_of_snake))


class Target(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('apple.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = randint(0, WIDTH - self.rect.w)
        self.rect.y = randint(0, HEIGHT - self.rect.h)


class Board:
    def __init__(self, side_of_cube):
        self.side = side_of_cube

    def draw_board(self, screen):
        for row in range((HEIGHT // self.side) + 1):
            for col in range((WIDTH // self.side) + 1):
                row_s = row * self.side
                col_s = col * self.side
                pygame.draw.rect(screen, (255, 255, 255), (col_s, row_s, self.side, self.side), 1)


running = True
board = Board(40)
snake = Snake()
# all_sprites.add(snake)
clock = pygame.time.Clock()
FPS = 5
target = Target()
all_sprites.add(target)
targets.add(target)
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_d:
                snake.dx = 1
                snake.dy = 0
                snake.orientation = 'x'
            elif ev.key == pygame.K_a:
                snake.dx = -1
                snake.dy = 0
                snake.orientation = 'x'
            elif ev.key == pygame.K_s:
                snake.dy = 1
                snake.dx = 0
                snake.orientation = 'y'
            elif ev.key == pygame.K_w:
                snake.dy = -1
                snake.dx = 0
                snake.orientation = 'y'
    screen.fill((0, 0, 0))
    board.draw_board(screen)
    snake.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)
    snake.update()
    pygame.display.flip()
    clock.tick(FPS)