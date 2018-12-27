import math
import pygame
import random
import time
import numpy

# Constants
BAT_HEIGHT = 50
BAT_WIDTH = 10
BAT_SPEED = 5
BALL_WIDTH = 3
BALL_HEIGHT = 3
BALL_SPEED = 5
FRAMERATE = 60

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Bat:
    def __init__(self, *args, **kwargs):
        self.height = kwargs["height"]
        self.width = kwargs["width"]
        self.xposition = kwargs["xposition"]
        self.yposition = kwargs["yposition"]

    # Draw a bat
    def render(self):
        pygame.draw.rect(game.display_surface, WHITE,
                         (self.xposition, self.yposition, BAT_WIDTH, BAT_HEIGHT))

    def moveup(self):
        self.yposition -= BAT_SPEED
        if self.yposition < 0:
            self.yposition = 0

    def movedown(self):
        self.yposition += BAT_SPEED
        if self.yposition > game.surface_height - BAT_HEIGHT:
            self.yposition = game.surface_height - BAT_HEIGHT


class Ball:
    def __init__(self, *args, **kwargs):
        self.xposition = self.newball_xposition = kwargs["newball_xposition"]
        self.yposition = self.newball_yposition = kwargs["newball_yposition"]
        self.angle = 0
        self.speed = BALL_SPEED

    def newball(self):
        self.xposition = self.newball_xposition
        self.yposition = self.newball_yposition
        self.angle = random.uniform(0, math.pi * 2)

    def render(self):
        pygame.draw.rect(game.display_surface, RED,
                         (self.xposition - BALL_WIDTH / 2,
                          self.yposition - BALL_HEIGHT / 2,
                          BALL_WIDTH,
                          BALL_HEIGHT)
                         )

    def move_random(self):
        self.xposition += random.randint(-5, 5)
        self.yposition += random.randint(-5, 5)

    def move(self, leftbat, rightbat):
        # Calculate and move the ball
        self.xposition += math.cos(self.angle) * self.speed
        self.yposition += math.sin(self.angle) * self.speed

        # Check if the ball has left the screen at the top (and so needs to bounce)
        if self.yposition >= game.surface_height:
            self.yposition = game.surface_height
            self.angle = -self.angle

        # Check if the ball has left the screen at the bottom (and so needs to bounce)
        if self.yposition <= 0:
            self.yposition = 0
            self.angle = -self.angle

        ### These next two things are COPY + PASTE and thus bad. This should be functionified.
        # Check if the ball has reached the left side of the screen
        if self.xposition <= BAT_WIDTH:
            # The ball bounces off the left bat.
            if leftbat.yposition < self.yposition < (leftbat.yposition + BAT_HEIGHT):
                print(leftbat.yposition, self.yposition, leftbat.yposition + BAT_HEIGHT)
                myrange = numpy.linspace(0, math.pi / 4, num=BAT_HEIGHT)
                print(f"LEFTBAT {int(self.yposition - leftbat.yposition)}")
                self.angle = (myrange[int(self.yposition - leftbat.yposition)])

                # DIRTY HACK. Move the ball to the right so we don't get "double hits"
                self.xposition = BAT_WIDTH + 5 + BALL_SPEED

            # The left player has missed the ball.
            else:
                # Make a newball and pause for a second.
                self.newball()
                time.sleep(1)


        if self.xposition >= (game.surface_width - BAT_WIDTH):
            # The ball bounces off the right bat.
            if rightbat.yposition < self.yposition < (rightbat.yposition + BAT_HEIGHT):
                print(rightbat.yposition, self.yposition, rightbat.yposition + BAT_HEIGHT)
                myrange = numpy.linspace((math.pi / 2), ((3 * math.pi) / 2), num=BAT_HEIGHT)
                print(f"RIGHTBAT {int(self.yposition - rightbat.yposition)}")
                self.angle = -(myrange[int(self.yposition - rightbat.yposition)])
                self.xposition = game.surface_width - BAT_WIDTH - 1

                # DIRTY HACK. Move the ball speed to the left so we don't get "double hits"
                self.xposition = game.surface_width - 5 - BAT_WIDTH - BALL_SPEED


            # The right player has missed the ball
            else:
                # Make a newball and pause for a second.
                self.newball()
                time.sleep(1)


class Game:
    def __init__(self):

        self._running = True
        self.display_surface = None
        self.size = self.surface_width, self.surface_height = 640, 480

        # Make bats
        self.leftbat = Bat(height=BAT_HEIGHT,
                           width=BAT_WIDTH,
                           xposition=0,
                           yposition=self.surface_height / 2)
        self.rightbat = Bat(height=BAT_HEIGHT,
                            width=BAT_WIDTH,
                            xposition=self.surface_width - BAT_WIDTH,
                            yposition=self.surface_height / 2)

        # And a ball
        self.ball = Ball(newball_xposition=self.surface_width / 2,
                         newball_yposition=self.surface_width / 2
                         )

    # This setups the game at the start, making a window and calling it that we are running.
    def setup(self):
        # Start pygame internals
        pygame.init()

        # Make our screen we will draw the game on
        self.display_surface = pygame.display.set_mode(self.size, pygame.HWSURFACE)

        # We are running now
        self.running = True

    # Here we handle events (like key presses).
    def event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # Here we handle the main game loop
    def loop(self):
        # Q (player 1)
        if pygame.key.get_pressed()[pygame.K_q]:
            self.leftbat.moveup()

        # A (player 2)
        if pygame.key.get_pressed()[pygame.K_a]:
            self.leftbat.movedown()

        # Up Arrow (player 2)
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rightbat.moveup()

        # Down Arrow (player 2)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rightbat.movedown()

        # B (to reset the ball for debugging)
        if pygame.key.get_pressed()[pygame.K_b]:
            self.ball.newball()

        # Move the ball
        self.ball.move(self.leftbat, self.rightbat)

    def render(self):
        # Clear the old screen, make the screen totally black.
        # This is NOT the optimal way to do it, but it works for pong.
        self.display_surface.fill(BLACK)

        # Draw the two bats
        game.leftbat.render()
        game.rightbat.render()
        game.ball.render()

        # Render the naw frame to the screen. "Page Flip" style.
        pygame.display.update()

    # When the game ends
    def cleanup(self):
        pygame.quit()

    # The main thing
    def run(self):
        while self._running:
            for event in pygame.event.get():
                self.event(event)
            self.loop()
            self.render()
            time.sleep(1 / FRAMERATE)
        self.cleanup()

# range() for floats.
def frange(x, y, jump):
  while x < y:
    yield x
    x += jump

# If we just run this program, do this.
if __name__ == '__main__':
    game = Game()
    game.setup()
    game.run()