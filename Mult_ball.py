#!/usr/bin/env python3
#Multi Bonce Ball

import sys, pygame, os
from pygame.locals import *

size = width, height = 800, 600
black = 0, 0, 0
speed = [3,3]
speed2 = [-2,4]


main_dir = os.path.split(os.path.abspath(__file__))[0]
#data_dir = os.path.join(main_dir, 'data')


def load_image(file):
    try:
        image = pygame.image.load(os.path.join(main_dir, file))
    except pygame.error:
        raise SystemExit('could not load ball image.')
    return image


class Ball(pygame.sprite.Sprite):
    image = None
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self, mov):
        self.rect.move_ip(mov)

        #super(Ball, self).__init__()

    #def move(self.direction):
        #ballrect = ballrect.move(speed)
        #if ballrect.left < 0 or ballrect.right > width:
            #speed[0] = -speed[0]
        #if ballrect.top < 0 or ballrect.bottom > height:
            #speed[1] = -speed[1]


def main():
    pygame.init()

    #make a backgroud
    backscreen = pygame.display.set_mode(size)
    backscreen.fill(black)
    backscreen.blit(backscreen, (0,0))

    #keep track of Sprites
    #load_image("ball.png")

    ball1 = Ball((150, 300))
    ball2 = Ball((300, 150))
    all = pygame.sprite.RenderPlain(ball1, ball2)


    #ballrect = ball.get_rect()

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
        #all.clear(screen, backgroud)
        #update sprites

        backscreen.fill(black)
        ball1.move(speed)
        ball2.move(speed2)
        if ball1.rect.left < 0 or ball1.rect.right > width:
            speed[0] = -speed[0]
        if ball1.rect.top < 0 or ball1.rect.bottom > height:
            speed[1] = -speed[1]

        if ball2.rect.left < 0 or ball2.rect.right > width:
            speed2[0] = -speed2[0]
        if ball2.rect.top < 0 or ball2.rect.bottom > height:
            speed2[1] = -speed2[1]


        dirty = all.draw(backscreen)
        pygame.display.update(dirty)

        pygame.display.flip()

        #redraw sprites
        #screen.blit(ball, ballrect)
        #dirty = all.draw(backscreen)
        #pygame.display(dirty)
        clock.tick(30)

#This is the main_init
if __name__=='__main__':
    main()
