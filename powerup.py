import pygame, random

from actor import Actor
#do this
class Powerup(Actor):
    def __init__(self, size, x, y):
        super().__init__(size, x, y)
    
        self.types = {
            "Health":PowerupType("health", 340),
            "Dbuff":PowerupType("dbuff", 40),
            "Bfire":PowerupType("bfire", 40),
            "Sbuff":PowerupType("sbuff", 40),
            "Elife":PowerupType("elife", 35),
            "Mfire":PowerupType("mfire", 30),
            "Shield":PowerupType("shield", 25),
            "Nuke":PowerupType("nuke", 5)
            }
        self.rand_max = 0 
        for powerup in self.types.values():
            self.rand_max += powerup.rarity
        self.type = "Mfire"
        self.sprites = self.get_sprites()
        self.image = self.sprites[0]
        #self.image.fill(self.types[self.type].sprite)
        self.position = self.image.get_rect()
        self.position.center = (x, y)

    def update(self):
        super().update()
        

    def get_sprites(self):
        spritesheet = self.types[self.type].spritesheet
        sprites = self.split_up_spritesheet(spritesheet, self.size)
        return sprites

    def draw(self, screen):
        if self.alive:
            self.image = self.animate(self.sprites)
            screen.blit(self.image, self.position)


    def move(self, screen_height, screen_width):
        self.position.y += 5
        if self.position.y  > screen_height:# and random.random() > 0.009:
            x = random.randint(0, screen_width)
            y = 0
            self.position.center = (x, y)
            
            sum_rarity = 0
            for key in self.types:
                sum_rarity += self.types[key].rarity
            r = random.randint(0, sum_rarity)
            chance = 0
            for key in self.types:
                chance+= self.types[key].rarity
                if chance >= r:
                    self.type = key
                    break
            #self.type = random.choice(list(self.types.keys()))
            self.sprites = self.get_sprites()
            self.image = self.sprites[0]
            self.alive = True


    def awaken_powerup(self, player):
        self.alive = False
        


        match self.type:
            case "Health":
                player.heal()
            case "Dbuff":
                player.buff_cooldown = 10 * 60

            case "Shield":
                player.shield_cooldown = 10 * 60
            
            case "Sbuff":
                player.speed_cooldown = 10 * 60

            case "Elife":
                player.extra_lifes +=1

            case "Mfire":
                player.number_of_bullets += 1
                if player.number_of_bullets > 3:
                    player.number_of_bullets = 3

            case "Bfire":
                player.rapid_cooldown = 10 * 60
            
            case "Nuke":
                player.has_nuke = True

            case _:
                print("not a valid pickup n00b")


class PowerupType:
    def __init__(self, sprite, rarity):
        self.sprite = sprite
        self.rarity = rarity
        self.spritesheet = pygame.image.load(f"Images/powerups/powerup-{self.sprite}-64.png")
