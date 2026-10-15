import pygame

class Explosion:
    def start(self, x, y):
        self.size = 480
        self.spritesheet = pygame.image.load("images/explosion.png")
        self.spritesheet = pygame.transform.scale_by(self.spritesheet, 10)
        self.sprites = self.split_up_spritesheet(self.spritesheet, self.size)
        self.sprite = self.sprites[0]
        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.active = False
        self.timer = 0
        self.sprite_time = 5
        self.index = 0

    def split_up_spritesheet(self, spritesheet, size, flipped = False):
        sprite_list = []
        number_of_sprites = spritesheet.get_width()//size
        for x in range(number_of_sprites):
            sprite = spritesheet.subsurface(x*size, 0, size, size)
            flipped_sprite = pygame.transform.flip(sprite, flipped, False)
            sprite_list.append(flipped_sprite)
        return sprite_list


    def draw(self, screen):
        if self.active:
            self.animate()
            screen.blit(self.sprite, self.rect)


    def animate(self):
        self.index = self.timer//self.sprite_time
        if self.index >= len(self.sprites):
            self.active = False
        else:
            self.sprite = self.sprites[self.index]
            self.timer+=1

    def explode(self):
        self.timer = 0
        self.active = True
        
