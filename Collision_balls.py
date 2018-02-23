#!/usr/bin/env python3
#Multi Bonce Ball

import sys, pygame, os
from pygame.locals import *
import random

# set size of the field
size = width, height = 800, 600
black = (0, 0, 0)
speed = [3,3]

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
    def __init__(self, pos, speed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = load_image('ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.speedx = speed[0] * random.choice((-1,1))
        self.speedy = speed[1] * random.choice((-1,1))
        #-print("Ball: ",pos[0], pos[1], self.speedx, self.speedy)

    def update(self, balls):
        #Move ball
        self.rect.move_ip(self.speedx, self.speedy)
        #if hit edge revsere direction
        if self.rect.left < 0 or self.rect.right > width:
            self.speedx = -self.speedx
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speedy = -self.speedy
        #Collided
        ballcol = pygame.sprite.spritecollide(self, balls, 0)
        if len(ballcol) > 1:
            self.speedx = -self.speedx
            self.speedy = -self.speedy
            print(ballcol)

#=====================================================================

def main():
    pygame.init()

    #make a backgroud
    backscreen = pygame.display.set_mode(size)
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    #load_image("ball.png")
    balls = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    Ball.containers = balls, all


    for i in range (0,4):
        #set random location for all of teh instances
        pox = random.randrange(50, width - 100, 25)
        poy = random.randrange(50, height - 100, 25)
        Ball((pox,poy),(speed))

    print("Main Balls container", balls)
    print("All", all)
    print("Ball", balls)

    #keep track of time
    clock = pygame.time.Clock()
    #game loop
    while 1:
        #get input
        for event in pygame.event.get():
            if event.type == pygame.QUIT \
                or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()

        #clear sprites
        backscreen.fill(black)

        #update sprites
        all.update(balls)



        #update display
        dirty = all.draw(backscreen)
        pygame.display.update(dirty)

        pygame.display.flip()

        #timer set for 30 frames
        clock.tick(30)

#This is the main_init
if __name__=='__main__':
    main()
