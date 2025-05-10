import pygame
import random
from pygame.locals import *
import time

SIZE = 40  # LENGTH OF SNAKE
BACKGROUND_COLOR = (68, 20, 97)
class Grape:
    def __init__(self, parent_screen):
        self.grape = pygame.image.load("resources/grape.png").convert_alpha()
        self.grape = pygame.transform.smoothscale(self.grape, (SIZE, SIZE))
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.grape, (self.x, self.y))  # (x,y) coordinates
    def move(self):
        self.x = random.randint(1,14) * SIZE
        self.y = random.randint(1,14) * SIZE
class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.head = pygame.image.load("resources/head.jpg").convert_alpha()
        self.head = pygame.transform.smoothscale(self.head, (SIZE, SIZE))
        self.block = pygame.image.load("resources/block.jpg").convert_alpha()
        self.block = pygame.transform.smoothscale(self.block, (SIZE, SIZE))
        self.block_x = [SIZE] * length
        self.block_y = [SIZE] * length
        self.direction = 'down'
        self.length = length
    def increase_length(self):
        self.length += 1
        self.block_x.append(-1) #random value because this is tackled in walk function
        self.block_y.append(-1)
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # Update the positions of the body segments
        for i in range(self.length - 1, 0, -1):
            self.block_x[i] = self.block_x[i - 1]
            self.block_y[i] = self.block_y[i - 1]

        # Update the position of the head based on direction
        if self.direction == 'up':
            self.block_y[0] -= SIZE
        if self.direction == 'down':
            self.block_y[0] += SIZE
        if self.direction == 'left':
            self.block_x[0] -= SIZE
        if self.direction == 'right':
            self.block_x[0] += SIZE

    def draw(self):
            for i in range(self.length):
                if i == 0:
                    self.parent_screen.blit(self.head, (self.block_x[i], self.block_y[i]))
                else:
                    self.parent_screen.blit(self.block, (self.block_x[i], self.block_y[i]))


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((600, 600))
        pygame.mixer.init()
        self.play_background_music()
        pygame.display.set_caption("Snake Game")
        #self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1)
        self.grape = Grape(self.surface)
    def is_collision(self,x1,y1,x2,y2):


        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False
    def play_background_music(self):
        pygame.mixer.music.load("resources/popbeat.mp3")
        pygame.mixer.music.play(loops=-1) #repeats music
    def play_sound(self,sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    def render_background(self):
        bg = pygame.image.load("resources/grid_background.png").convert()
        bg = pygame.transform.scale(bg, (600, 600))
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()  # update snake position
        self.snake.draw()  # draw snake
        self.grape.draw()  # draw grape
        self.display_score()
        pygame.display.flip()
        #snake with grape collision
        if self.is_collision(self.snake.block_x[0],self.snake.block_y[0],self.grape.x,self.grape.y):
            self.play_sound("bubblepop")
            self.snake.increase_length()
            self.grape.move()
        # Snake colliding with itself

        for i in range(3, self.snake.length):
             if self.is_collision(self.snake.block_x[0], self.snake.block_y[0], self.snake.block_x[i],self.snake.block_y[i]):
                 self.play_sound("shortwoosh")
                 raise "Game over"
        # Boundary collision
        if (self.snake.block_x[0] < 0 or self.snake.block_x[0] >= 600 or
                self.snake.block_y[0] < 0 or self.snake.block_y[0] >= 600):
            self.play_sound("shortwoosh")
            pygame.mixer.music.pause()
            raise "Game over"

    def show_game_over(self):
        self.render_background()
        #self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('papyrus', 30)
        line1 = font.render(f"Game Over ! Your Score : {self.snake.length}",True,(54, 17, 79))
        self.surface.blit(line1,(100,250))
        line2 = font.render(f"To play again press Enter !",True,(54, 17, 79))
        self.surface.blit(line2,(100,300))
        line3 = font.render(f"To exit press Escape !", True, (54, 17, 79))
        self.surface.blit(line3, (100, 350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def display_score(self):
        font = pygame.font.SysFont('papyrus',30) #inbuilt font
        score = font.render(f"Scores : {self.snake.length}",True,(54, 17, 79)) #color
        self.surface.blit(score,(450,8))
    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.grape = Grape(self.surface)


    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:

                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()
                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()
                        if event.key == K_LEFT and self.snake.direction != 'right':
                            self.snake.move_left()
                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            self.surface.fill(BACKGROUND_COLOR)  # fill screen once per frame


            # update display
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(0.3)

if __name__ == "__main__":
    game = Game()
    game.run()
