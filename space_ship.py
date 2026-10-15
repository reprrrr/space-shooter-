import pygame 
from actor import Actor

class SpaceShip(Actor):
    def __init__(self, size, x, y, lives):
        super().__init__(size, x, y)

        self.max_lives = lives
        self.lives = self.max_lives
        self.direction = 0
        self.fire_rate = 80
        self.shoot_cooldown = 0
    def update(self):
        super().update()
        self.shoot_cooldown -=1

    def move_left(self):
        self.direction = -1
        self.speedx = self.max_speedx*self.direction


    def move_right(self):
        self.direction = 1
        self.speedx = self.max_speedx*self.direction

    def damage(self, value):
        self.lives -= value
        if self.lives <1:
            self.alive = False

    def heal(self, value=1):
        if value <0:
            value = 0
        if self.lives + value <= self.max_lives:
            self.lives+=value
    
    def fire(self, bullet, x = 0, y = 0):
        if self.alive:
            bullet.position.x = self.position.x + x
            bullet.position.y = self.position.y + y
            bullet.alive = True
            self.shoot_cooldown = self.fire_rate