#!/usr/bin/env python3
# Multi Bonce Ball

import sys, pygame, os
from pygame.locals import *
import random, math

# set size of the field
size = width, height = 800, 600
black = (0, 0, 0)
speed = 6
pi = math.pi

random.seed(870)

# define where data directory is located
main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    try:
        image = pygame.image.load(os.path.join(main_dir, file))
    except pygame.error:
        raise SystemExit('could not load ball image.')
    return image

# ========================================================================

class Ball(pygame.sprite.Sprite):
    image = None

    # Construct the ball instance
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('ball.png')
        self.radius = 54
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        angle = (random.random() * 2 * math.pi)
        self.speedx = (math.cos(angle) * speed)
        self.speedy = (math.sin(angle) * speed)
        self.mass = random.randint(20, 41)
        # print("Ball: ",pos[0], pos[1], self.speedx, self.speedy)

    # Move the ball and check boundries
    def update(self):
        # Move ball
        self.rect.move_ip(self.speedx, self.speedy)
        # if hit edge reverse direction
        if self.rect.left < 0 or self.rect.right > width:
            self.speedx = -self.speedx
            self.rect.x += self.speedx
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speedy = -self.speedy
            self.rect.y += self.speedy

    # Does it hit another ball
    def collide(self, B2):
        b1mag = math.hypot(self.speedx, self.speedy)
        b2mag = math.hypot(B2.speedx, B2.speedy)
        Mdiff = 1.00   #self.mass / B2.mass

        # will use the negative diffs for B2's computations
        xdiff = self.speedx - B2.speedx
        ydiff = self.speedy - B2.speedy
        xposd = self.rect.x - B2.rect.x
        yposd = self.rect.y - B2.rect.y

        angleB1 = math.atan2(ydiff, xdiff)
        angleB2 = math.atan2(-ydiff, -xdiff)
        tangB1 = math.atan2(yposd, xposd)
        tangB2 = math.atan2(-yposd, -xposd)

        angleB1 = 2 * tangB1 - angleB1
        angleB2 = 2 * tangB2 - angleB2

        angledeg1 = math.degrees(angleB1)
        print("Angle for ball", angledeg1, "Xdiff/Ydiff",xdiff, ydiff, "Pos of X,Y of ball:", self.rect.x, self.rect.y)
        angledeg2 = math.degrees(angleB2)
        print("Angle for ball", angledeg2, "Xdiff/Ydiff",-xdiff, -ydiff, "Pos of X,Y of ball:", B2.rect.x, B2.rect.y)

        # Ball 1
        self.speedx = - b1mag * math.cos(angleB1) * Mdiff
        self.speedy = - b1mag * math.sin(angleB1) * Mdiff
        # Ball 2
        B2.speedx = - b2mag * math.cos(angleB2) * Mdiff
        B2.speedy = - b2mag * math.sin(angleB2) * Mdiff

        # to make sure they don't hug
        # need both balls to react at the same time
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        B2.rect.x += B2.speedx
        B2.rect.y += B2.speedy

# =====================================================================

def main():
    pygame.init()
    ballset = []

    # make a backgroud
    backscreen = pygame.display.set_mode(size)
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    # load_image("ball.png")
    balls = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    Ball.containers = balls, all

    # create the balls for the field
    for i in range (0,6):
        # set random location for all of teh instances
        pox = random.randrange(50, width - 100, 120)
        poy = random.randrange(50, height - 100, 120)
        ballset.append(Ball((pox,poy)))

    # keep track of time
    clock = pygame.time.Clock()
    # game loop
    while 1:
        # get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == KEYDOWN \
                and event.key == K_q):
                    sys.exit()

        # clear sprites
        backscreen.fill(black)

        # Check if Collided
        for ball1 in ballset:
            for ball2 in ballset:
                if ball1 != ball2:
                    if pygame.sprite.collide_circle(ball1, ball2):
                        ball1.collide(ball2)

        # update sprites
        all.update()

        # update display
        dirty = all.draw(backscreen)
        pygame.display.update(dirty)

        pygame.display.flip()

        # timer set for 30 frames
        clock.tick(30)


# This is the main_init
if __name__=='__main__':
    main()
