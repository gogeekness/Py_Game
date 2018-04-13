#!/usr/bin/env python3
#Multi Bonce Ball

import sys, pygame, os
from pygame.locals import *
import random, math

# set size of the field
size = width, height = 800, 600
black = (0, 0, 0)
speed = 4
pi = math.pi

random.seed(124)

#define where data directory is located
main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(file):
    try:
        image = pygame.image.load(os.path.join(main_dir, file))
    except pygame.error:
        raise SystemExit('could not load ball image.')
    return image

#========================================================================

class Ball(pygame.sprite.Sprite):
    image = None

    #Construct the ball instance
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
        #-print("Ball: ",pos[0], pos[1], self.speedx, self.speedy)

    #Move the ball and check boundries
    def update(self):
        #Move ball
        self.rect.move_ip(self.speedx, self.speedy)
        #if hit edge revsere direction
        if self.rect.left < 0 or self.rect.right > width:
            self.speedx = -self.speedx
            self.rect.x += self.speedx
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speedy = -self.speedy
            self.rect.y += self.speedy

    #Does it hit another ball
    def collide(self, B2: object) -> object:
        B1mag = math.hypot(self.speedx, self.speedy)
        Mdiff = 1.00 #self.mass / B2.mass
        Xdiff = self.speedx - B2.speedx
        Ydiff = self.speedy - B2.speedy
        if Xdiff > 0:
            if Ydiff > 0:
                angle = math.atan(Ydiff/Xdiff)
            else:
                angle = (2 * pi) - math.atan(Ydiff/Xdiff)
        elif Xdiff < 0:
            if Ydiff > 0:
                angle = pi + math.atan(Ydiff/Xdiff)
            else:
                angle = pi - math.atan(Ydiff/Xdiff)
        elif Xdiff == 0:
            if Ydiff > 0:
                Angle = (pi / 2)
            else:
                Angle = -(pi / 2)
        elif Ydiff == 0:
            if Xdiff < 0:
                Angle = 0
            else:
                Angle = pi
        angledeg = math.degrees(angle)
        print("Angle for ball", angledeg, "Xdiff/Ydiff",Xdiff, Ydiff, "Pos of X,Y of ball:", self.rect.x, self.rect.y)
        self.speedx = - B1mag * math.cos(angle) * Mdiff
        self.speedy = - B1mag * math.sin(angle) * Mdiff
        # to make sure they don't hug
        self.rect.x += self.speedx
        self.rect.y += self.speedy

#=====================================================================

def main():
    pygame.init()
    ballset = []

    #make a backgroud
    backscreen = pygame.display.set_mode(size)
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    #load_image("ball.png")
    balls = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    Ball.containers = balls, all

    # create the balls for the field
    for i in range (0,3):
        #set random location for all of teh instances
        pox = random.randrange(50, width - 100, 120)
        poy = random.randrange(50, height - 100, 120)
        ballset.append(Ball((pox,poy)))

    #keep track of time
    clock = pygame.time.Clock()
    #game loop
    while 1:
        #get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == KEYDOWN and event.key == K_ESCAPE) \
                or (event.type == KEYDOWN and event.key == K_q):
                    sys.exit()

        #clear sprites
        backscreen.fill(black)

        #Check if Collided
        for ball1 in ballset:
            for ball2 in ballset:
                if ball1 != ball2:
                    if pygame.sprite.collide_circle(ball1, ball2):
                        ball1.collide(ball2)


        #update sprites
        all.update()

        #update display
        dirty = all.draw(backscreen)
        pygame.display.update(dirty)

        pygame.display.flip()

        #timer set for 30 frames
        clock.tick(30)

#This is the main_init
if __name__=='__main__':
    main()
