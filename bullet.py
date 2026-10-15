import pygame
from actor import Actor

class Bullet(Actor):
    def __init__(self, size, x, y, owner):
        super().__init__(size, x, y)

        self.alive = False
        self.owner = owner

        if owner == "player":
            self.size = 32
            self.speedy = -6
            self.sprites = [self.split_up_spritesheet(pygame.image.load("Images/bullet/player-bullet.png"), self.size),
                            self.split_up_spritesheet(pygame.image.load("Images/bullet/player-bullet-dbuff.png"), self.size)]
        else:
            self.size = 9
            self.speedy = 5
            self.sprites = [self.split_up_spritesheet(pygame.image.load("Images/bullet/enemy-bullet.png"),self.size, flipped_y = True)]

        self.image = self.sprites[0][0]
        self.position = self.image.get_rect()
        self.position.center = (x, y)
        self.sprite_time = 5
        self.damage = 1



    def draw(self, screen):
        if self.alive:
            self.image = self.animate(self.sprites[self.damage-1])
            screen.blit(self.image, self.position)

