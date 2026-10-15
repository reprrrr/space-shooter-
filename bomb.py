import pygame   
from actor import Actor
from powerup import Powerup
import random
class Bomb(Actor):
    def __init__(self, size, x, y):
        super().__init__(size, x, y)
        self.types = [
            "heal",
            "dbuff",
            #"bfire",
            "sbuff",
            "elife",
            "mfire",
            "shield",
            "nuke"
        ]
        self.size = size
        self.respawn()
    def move(self, screen_height):
        self.position.y+=5
        if self.position.y  > screen_height:# and random.random() > 0.009:
            x = 0
            y = 0
            self.position.center = (x, y)
            self.respawn()
    def draw(self, screen):
        self.image = self.animate(self.sprites)
        super().draw(screen)
    def respawn(self, x = 0, y = 0):
        self.sprite_name = self.randomized_sprite()
        self.spritesheet = pygame.image.load(f"Images/bomb/bomb-{self.sprite_name}-64.png")
        self.sprites = self.split_up_spritesheet(self.spritesheet, self.size)
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.alive = False
    def randomized_sprite(self):
        return random.choice(self.types)