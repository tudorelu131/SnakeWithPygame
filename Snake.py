import pygame
import string
import sys
from pygame.locals import *
from pygame.math import Vector2
import random

class Fruit:
    x: int
    y: int
    pos: Vector2
    def __init__(self):
        self.x, self.y = random.randint(0,19), random.randint(0,19)
        self.pos = Vector2(self.x, self.y)
        self.apple = None
        
    def load_image(self):
        self.apple = pygame.image.load('Assets/apple.png').convert_alpha()
        
    def draw_fruit(self, screen: pygame.Surface):
        fruit_rect = pygame.Rect(self.pos.x * 20, self.pos.y * 20, 20, 20)
        screen.blit(self.apple, fruit_rect)
    
    def rand_pos(self, snake_body):
        while True:
            self.x, self.y = random.randint(0,19), random.randint(0,19)
            self.pos = Vector2(self.x, self.y)
            
            if self.pos not in snake_body:
                break

class Snake:
    has_eaten: bool
    dir: Vector2
    body: list
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.dir = Vector2(1,0)
        self.has_eaten = False
        self.head = None
        self.tail = None
        
        self.ur = None
        self.ul = None
        self.dr = None
        self.dl = None
        
        self.hu = None
        self.hr = None
        self.hd = None
        self.hl = None
        
        self.bh = None
        self.bv = None
        
        self.tu = None
        self.tr = None
        self.td = None
        self.tl = None
    
    def draw_snake(self, screen: pygame.Surface):
        self.update_tail_graphics()
        self.update_head_graphics()
        
        for index, block in enumerate(self.body):
            x_pos = block.x * 20
            y_pos = block.y * 20
            block_rect = pygame.Rect(x_pos, y_pos, Game._cell_size, Game._cell_size)
            
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                
                if previous_block.x == next_block.x:
                    screen.blit(self.bv, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.bh, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1  or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.ul, block_rect)
                    if previous_block.x == -1 and next_block.y == 1  or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.dl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1  or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.ur, block_rect)
                    if previous_block.x == 1 and next_block.y == 1  or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.dr, block_rect)
                
            
    def move_snake(self):
        if self.has_eaten == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.dir)
            self.body = body_copy[:]
            self.has_eaten = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.dir)
            self.body = body_copy[:]
            
    def load_images(self):
        self.ur = pygame.image.load('Assets/snake_body_ur.png')
        self.ul = pygame.image.load('Assets/snake_body_ul.png')
        self.dr = pygame.image.load('Assets/snake_body_dr.png')
        self.dl = pygame.image.load('Assets/snake_body_dl.png')
        
        self.hu = pygame.image.load('Assets/snake_head_up.png')
        self.hr = pygame.image.load('Assets/snake_head_right.png')
        self.hd = pygame.image.load('Assets/snake_head_down.png')
        self.hl = pygame.image.load('Assets/snake_head_left.png')
        
        self.bh = pygame.image.load('Assets/snake_body_horizontal.png')
        self.bv = pygame.image.load('Assets/snake_body_vertical.png')
        
        self.tu = pygame.image.load('Assets/snake_tail_up.png')
        self.tr = pygame.image.load('Assets/snake_tail_right.png')
        self.td = pygame.image.load('Assets/snake_tail_down.png')
        self.tl = pygame.image.load('Assets/snake_tail_left.png')
            
    def add_block(self):
        self.has_eaten = True
        
    def is_out_of_bounds(self) -> bool:
        headx = self.body[0].x
        heady = self.body[0].y
        if(headx < 0 or headx > 19 or heady < 0 or heady > 19):
            return True
        return False
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.hl
        elif head_relation == Vector2(-1,0): self.head = self.hr
        elif head_relation == Vector2(0,1): self.head = self.hu
        elif head_relation == Vector2(0,-1): self.head = self.hd
          
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tr
        elif tail_relation == Vector2(-1,0): self.tail = self.tl
        elif tail_relation == Vector2(0,1): self.tail = self.td
        elif tail_relation == Vector2(0,-1): self.tail = self.tu
        
class GameOverOverlay:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.font_large = None
        self.font_medium = None
        self.retry_button = None
        self.exit_button = None
        
    def load_fonts(self):
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 48)
        
    def create_buttons(self):
        bw = 120
        bh = 40
        center_x = self.sw // 2
        
        self.retry_button = pygame.Rect(center_x - bw - 10, 350, bw, bh)
        self.exit_button = pygame.Rect(center_x + 10, 350, bw, bh)
        
    def draw(self, screen: pygame.Surface, score):
        
        overlay = pygame.Surface((self.sw, self.sh))
        overlay.set_alpha(128)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0, 0))
        
        bw = 300
        bh = 200
        bx = (self.sw - bw) // 2
        by = (self.sh - bh) // 2
        
        pygame.draw.rect(screen, (50, 50, 50), (bx, by, bw, bh))
        pygame.draw.rect(screen, (255, 255, 255), (bx, by, bw, bh), 3)
        
        score_text = self.font_medium.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.sw // 2, by + 80))
        screen.blit(score_text, score_rect)
        
        pygame.draw.rect(screen, (0, 150, 0), self.retry_button)
        pygame.draw.rect(screen, (255, 255, 255), self.retry_button, 2)
        retry_text = self.font_medium.render("RETRY", True, (255, 255, 255))
        retry_text_rect = retry_text.get_rect(center=self.retry_button.center)
        screen.blit(retry_text, retry_text_rect)
        
        pygame.draw.rect(screen, (150, 0, 0), self.exit_button)
        pygame.draw.rect(screen, (255, 255, 255), self.exit_button, 2)
        exit_text = self.font_medium.render("EXIT", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=self.exit_button.center)
        screen.blit(exit_text, exit_text_rect)
        
    def handle_click(self, mouse_pos) -> string:
        if self.retry_button.collidepoint(mouse_pos):
            return "retry"
        elif self.exit_button.collidepoint(mouse_pos):
            return "exit"
        return None

class Game:
    _screen_update = pygame.USEREVENT
    _cell_number = 20
    _cell_size = 20
    _clock = pygame.time.Clock()
    _test_surface = pygame.Surface((_cell_number * _cell_size,_cell_number * _cell_size))
    _test_rect = pygame.Rect(20,100,400,400)
    size = ()
    
    def __init__(self):
        self._score = 0
        self._running = True
        self._screen = None
        self.size = self.width, self.height = 440, 520
        self._fruit = None
        self._snake = None
        self._font = None
        self._game_over_state = False
        self._overlay = None  
        
    def reset_game(self):
        self._fruit = Fruit()
        self._snake = Snake()
        self._fruit.load_image()
        self._snake.load_images()
        self._fruit.rand_pos(self._snake.body)
        self._game_over_state = False 
        self._score = 0  
        self._font_render = self._font.render(f"Score: {self._score}", True, pygame.Color('BLACK'), None)
        
    def on_init(self):
        pygame.init()
        pygame.time.set_timer(self._screen_update, 150)
        self._screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.mixer.init()
        pygame.mixer.music.load('Assets/nom.mp3')
        pygame.mixer.music.set_volume(0.4)
        self._running = True
        
        self._overlay = GameOverOverlay(self.width, self.height)
        self._overlay.load_fonts()
        self._overlay.create_buttons()
        
        self._fruit = Fruit()
        self._snake = Snake()
        self._fruit.load_image()
        self._snake.load_images()
        self._fruit.rand_pos(self._snake.body)
        
        self._font = pygame.font.SysFont('impact', 40)
        pygame.display.set_caption('Snake Game')
        self._font_render = self._font.render(f"Score: {self._score}", True, pygame.Color('BLACK'), None)
        self._font_rect = (20, 50)
        
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
            
        if self._game_over_state:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    action = self._overlay.handle_click(event.pos)
                    if action == 'retry':
                        self.reset_game()
                    elif action == 'exit':
                        self._running = False
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self._snake.dir != Vector2(-1,0):
                self._snake.dir = Vector2(1,0)
            if event.key == pygame.K_DOWN and self._snake.dir != Vector2(0,-1):
                self._snake.dir = Vector2(0,1)
            if event.key == pygame.K_LEFT and self._snake.dir != Vector2(1,0):
                self._snake.dir = Vector2(-1,0)
            if event.key == pygame.K_UP and self._snake.dir != Vector2(0,1):
                self._snake.dir = Vector2(0,-1)
                
        if event.type == self._screen_update:
            self._snake.move_snake()
            self.check_collision()

    def on_render(self):
        self._fruit.draw_fruit(self._test_surface)
        self._snake.draw_snake(self._test_surface)
        
        if self._game_over_state:
            self._overlay.draw(self._screen, self._score)
        
    def on_cleanup(self):
        pygame.quit()
        
    def check_collision(self):
        if self._game_over_state:
            return
            
        if self._snake.body[0] == self._fruit.pos:
            self._snake.add_block()
            self._fruit.rand_pos(self._snake.body)
            self._score += 10
            self._font_render = self._font.render(f"Score: {self._score}", True, pygame.Color('BLACK'), None)
            pygame.mixer.music.play()
            
        for i in range(1, len(self._snake.body)):
            if self._snake.body[0] == self._snake.body[i] or self._snake.is_out_of_bounds():
                self.game_over()
                break
                
    def game_over(self):
        self._game_over_state = True  
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            self._screen.fill(pygame.Color(120, 200, 50))
            
            for event in pygame.event.get():
                self.on_event(event)

            if not self._game_over_state:
                self._test_surface.fill((60, 150, 80))
                self.on_render()
                self._screen.blit(self._test_surface, self._test_rect)
            else:
                self.on_render()

            self._screen.blit(self._font_render, self._font_rect)
            pygame.display.update()
            self._clock.tick(60)

        self.on_cleanup()

if __name__ == "__main__":
    SnakeGame = Game()
    SnakeGame.on_execute()