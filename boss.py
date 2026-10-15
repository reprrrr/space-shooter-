import pygame 
from enemy import Enemy
from enemy_waves import WaveManager

class Boss(Enemy):
    def __init__(self, x, y, speedx, speedy, enemy_type, size):
        super().__init__(x, y, speedx, speedy, enemy_type, size)
        self.stage = "boss_1"
        self.waves = WaveManager()
        self.wave = self.waves.load_wave(self.stage, 800, 600)
        self.spawn_timer = 0
        self.spawn_timer_offset = 0
        # self.rect = self.image.get_rect()
        # self.rect.x = x
        # self.rect.y = y


    def update(self):
        super().update()

        if self.lives <3:
            self.fire_rate /= 2

    #     if len(self.enemies)< self.wave.number_of_enemies and self.spawn_timer//1000>=self.wave.time_between_enemies*len(self.enemies):
    #         enemy = Enemy(self.position.x, self.position.y, self.wave.speedx, self.wave.speedy, self.wave.enemy_type, 32)
    #         self.enemies.append(enemy)
    #         self.spawn_timer = 0
    #     else:
    #         self.spawn_timer = pygame.time.get_ticks()-self.spawn_timer_offset

    #     for enemy in self.enemies:
    #         enemy.move()
    #         enemy.update()
    # def draw(self, screen):
    #     super().draw(screen)
    #     for enemy in self.enemies:
    #         enemy.draw(screen)