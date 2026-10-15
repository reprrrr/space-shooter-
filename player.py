import pygame
from space_ship import SpaceShip
class Player(SpaceShip):
    def __init__(self, size, x,y):
        super().__init__(size, x,y, 3)
        self.godmode = False
        self.extra_lifes = 0
        self.main_sprites = [pygame.image.load("Images/player/player-health-0.png"),
                             pygame.image.load("Images/player/player-health-1.png"),
                             pygame.image.load("Images/player/player-health-2.png"),
                             pygame.image.load("Images/player/player-health-3.png")]
        self.engine_sprite = pygame.image.load("Images/player/engine.png")
        self.flame_sprites = self.split_up_spritesheet(pygame.image.load("Images/player/engine-flames.png"), self.size)
        self.boost_sprites = self.split_up_spritesheet(pygame.image.load("Images/player/engine-flames-boost.png"), self.size)
        self.shield_sprites = self.split_up_spritesheet(pygame.image.load("Images/player/player-shield.png"), self.size)
        self.elife_sprite = pygame.image.load("Images/player/player-health-plus-sheet.png")
        self.image = self.main_sprites[self.lives]
        self.flame_sprite = self.flame_sprites[0]
        self.position = self.image.get_rect()
        self.position.center = (self.x, self.y)
        self.max_speedx = 5
        self.speed_modifier = 1
        self.sprite_time = 5
        self.buff_cooldown = 0
        self.shield_cooldown = 0
        self.speed_cooldown = 0
        self.rapid_cooldown = 0
        self.fire_rate = 60
        self.has_nuke = False
        self.number_of_bullets = 1

    def update(self):
        super().update()
        self.shoot_cooldown -= 1
        self.buff_cooldown -= 1
        self.shield_cooldown -= 1
        self.speed_cooldown -= 1
        self.rapid_cooldown -= 1

    def draw(self, screen):
        if self.alive:
            screen.blit(self.engine_sprite, self.position)

            if self.extra_lifes > 0:
                screen.blit(self.elife_sprite, self.position)
            else:
                self.image = self.main_sprites[self.lives]
                screen.blit(self.image, self.position) 
                
            if self.speed_cooldown >0:
                self.flame_sprite = self.animate(self.boost_sprites)
                screen.blit(self.flame_sprite, self.position)
            else:
                self.flame_sprite = self.animate(self.flame_sprites)
                screen.blit(self.flame_sprite, self.position)

            if self.shield_cooldown > 0:
                self.shield_sprite = self.animate(self.shield_sprites)
                screen.blit(self.shield_sprite, self.position)
    
    def move(self):
        if self.alive:

            if self.speedx >0.01:
                self.speedx -= 0.2 * self.speed_modifier
            elif self.speedx < 0.01:
                self.speedx += 0.2 * self.speed_modifier
            else:
                self.direction = 0
                self.speedx = 0
            self.position.x+= self.speedx

    def damage(self, value):
        if self.godmode:

            return
        if self.number_of_bullets > 1:
            self.number_of_bullets -= 1
        if self.extra_lifes >0:
            self.extra_lifes -= value
        else:
            self.lives -= value
            if self.lives <0:
                self.alive = False
    def fire_all(self, bullets):
        if self.alive:
            if self.has_nuke:
                self.has_nuke = False
            elif self.number_of_bullets ==3:
                self.fire(bullets[0], x = 8)
                self.fire(bullets[1], x = 0)
                self.fire(bullets[2], x = 16)
            elif self.number_of_bullets ==2:
                self.fire(bullets[0], x = 0)
                self.fire(bullets[1], x = 16)
            else:
                self.fire(bullets[0], x = 8)
