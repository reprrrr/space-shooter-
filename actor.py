import pygame

class Actor:
    def __init__(self, size, x,y):
        self.alive = True
        self.size = size
        self.x = x
        self.y = y
        self.speedx = 0
        self.speedy = 0
        self.max_speedx = 0
        self.max_speedy = 0
        self.sprite_time = 10
        self.timer = 0

        self.image = pygame.Surface((size, size))
        self.position = self.image.get_rect()

    def update(self):
        self.timer +=1

    def split_up_spritesheet(self, spritesheet, size, flipped_x = False, flipped_y = False):
        sprite_list = []
        number_of_sprites = spritesheet.get_width()//size
        for x in range(number_of_sprites):
            sprite = spritesheet.subsurface(x*size, 0, size, size)
            flipped_sprite = pygame.transform.flip(sprite, flipped_x, flipped_y)
            sprite_list.append(flipped_sprite)
        return sprite_list


    def get_mask(self):
        return pygame.mask.from_surface(self.image)


    def collide(self, mask, x=0, y=0):
        if self.alive:
            actor_mask = self.get_mask()
            offset = (self.position.x - x, self.position.y - y)
            return mask.overlap(actor_mask, offset)
        else:
            return None

    def move(self):
        if self.alive:
            self.position.x += self.speedx
            self.position.y += self.speedy
        

    def draw(self, screen:pygame.Surface):
        if self.alive:
             screen.blit(self.image, self.position)


    def animate(self, sprites):
        index = self.timer // self.sprite_time % len (sprites)
        return sprites [index]
