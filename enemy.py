import json
import random
import pygame
from space_ship import SpaceShip

class EnemyLoader:
    def __init__(self, enemy_type):
        self.load_enemy(enemy_type)
        
    def load_enemy(self, enemy_type):
        try:
            with open(f"json/Enemies/{enemy_type}.json", "r") as f:
                enemy_data = json.load(f)
                self.name = enemy_data["name"]
                self.lives = enemy_data["lives"]
                self.score = enemy_data["score"]
                self.sprite = self.setup_sprite(enemy_data["sprite"])
                self.fire_rate = enemy_data["fire_rate"]
        except FileNotFoundError:
            print(f"Enemy {enemy_type} not found.")
            self.name = "Unknown"
            self.lives = 1
            self.score = 10
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 0))

    def setup_sprite(self, path):
        sprite = pygame.image.load(path)
        return pygame.transform.flip(sprite, False, True)
    
class Enemy(SpaceShip):
    def __init__(self, x, y, speedx, speedy, enemy_type, size):
        super().__init__(size, x,y, 1)
        self.enemy_loader = EnemyLoader(enemy_type)
        self.fire_rate = self.enemy_loader.fire_rate
        self.value = self.enemy_loader.score
        self.lives = self.enemy_loader.lives
        self.image = self.enemy_loader.sprite
        self.position = self.image.get_rect()
        self.position.center = (x, y)
        self.speedx = speedx
        self.speedy = speedy
        self.max_speedx = speedx
        self.max_speedy = speedy
        self.type = enemy_type 
        
        
class Bomber(Enemy):
    def fire(self, bullet, bomb, x = 0, y = 0):
        super().fire(bullet, x, y)
        if self.alive and bomb is not None and random.random() > 0.75:
            bomb.position.x = self.position.x + x
            bomb.position.y = self.position.y + y
            bomb.alive = True

