import pygame, random

class Star():
    def start(self, screen_width):
        size = random.randint(1,4)
        self.image = pygame.Surface((size, size))
        self.position = self.image.get_rect()
        self.respawn(screen_width)

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def move(self, screen_height, screen_width):
        self.position.y+=self.speed
        if self.position.y >screen_height:
            self.respawn(screen_width)

            
    def respawn(self, screen_width):
        r = random.randint(0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        x = random.randint(0,screen_width)

        self.speed = random.randint(1,5)
        self.image.fill((r,g,b))
        self.position.center = (x, -100)
