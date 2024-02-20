import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (0, 106, 0)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("Resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(0, 15) * SIZE
        self.y = random.randint(0, 10) * SIZE

class Snake:
    def __init__(self, parent_screen, length, game):
        self.parent_screen = parent_screen
        self.game = game
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_left(self):
       self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        screen_width, screen_height = pygame.display.get_surface().get_size()

        if self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        elif self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE

        if (self.x[0] < 0 or self.x[0] > screen_width or self.y[0] < 0 or self.y[0] > screen_height):
            self.game.play_sound("violin-lose")
            raise Exception("Snake hit the wall!")

        self.draw()
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snakes and Apples")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((800, 500))
        self.surface.fill(BACKGROUND_COLOR)
        self.snake = Snake(self.surface, 1, self)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("Resources/thinking-time.mp3")
        pygame.mixer.music.play(-1, 0)
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"Resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("Resources/grass_background.jpeg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.update()

        # Snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("Apple-crunch")
            self.snake.increase_length()
            self.apple.move()

        # Snake colliding with self
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("violin-lose")
                raise Exception("Collision Occurred")

    def display_score(self):
        font = pygame.font.SysFont('arial', 15)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (720, 5))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 20)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 200))
        line2 = font.render("Press Enter to play again or Escape to Quit", True, (255, 255, 255))
        self.surface.blit(line2, (200, 250))
        pygame.display.flip()
        pygame.mixer.music.stop()

    def reset(self):
        self.snake = Snake(self.surface, 1, self)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.play(-1, 0)
                        pause = False
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

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
