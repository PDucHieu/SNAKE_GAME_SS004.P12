import pygame
import time
import sys   
import random
from pygame.math import Vector2

pygame.init()

title_font = pygame.font.Font(None, 60)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

OFFSET = 50

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
    
    def draw(self):
        food_rect = pygame.Rect( OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, DARK_GREEN, food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position   

class Snake:
    def __init__(self):
        self.body = [Vector2(3, 1), Vector2(2,1), Vector2(1,1)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        
    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7 )  
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:    
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(3, 1), Vector2(2, 1), Vector2(1, 1)]
        self.direction = Vector2(1, 0)
        
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
    
    def draw(self):
        self.snake.draw()
        self.food.draw()
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_the_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
    
    def check_collision_with_the_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
    
    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
    
    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        
    def check_collision_with_tail(self):
        headless_body = self.snake.body [1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
    
screen = pygame.display.set_mode ((2*OFFSET + cell_size*number_of_cells, 2*OFFSET + cell_size*number_of_cells))

pygame.display.set_caption("SNAKE GAME")

clock = pygame.time.Clock()

game = Game()

SNAKE_UPDATE = pygame.USEREVENT 
pygame.time.set_timer(SNAKE_UPDATE, 200)

while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            else:
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)
    
            
    screen.fill(GREEN)        
    pygame.draw.rect(screen, DARK_GREEN, 
                     (OFFSET - 5, OFFSET - 5, cell_size * number_of_cells + 10, cell_size * number_of_cells +10), 5)
    game.draw()
    title_surface = title_font.render("SNAKE GAME", True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET - 5, 20))
    
    pygame.display.update()
    clock.tick(60)
