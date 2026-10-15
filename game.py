import pygame, random
from boss import Boss
from star import Star
from player import Player
from enemy import Enemy, Bomber
from enemy_waves import WaveManager
from bullet import Bullet
from powerup import Powerup
from explosion import Explosion
from bomb import Bomb
class Game():
    def start(self):
        self.setup()
        self.run()

    def setup(self):
        self.width = 1400
        self.height = 800
        self.fps = 60
        
        pygame.init()
        pygame.display.set_caption("space invaders")
        self.screen = pygame.display.set_mode((self.width, self.height),flags = pygame.SCALED, vsync = 1)
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        self.offset = 0
        self.spawn_timer = 0
        self.current_wave = 3
        self.max_stars = 50
        self.spawn_timer_offset = 0
        self.score = 0
        self.score_cooldown = 30
        

        self.state = "start"

        self.wave_manager = WaveManager()
        self.explosion = Explosion()
        self.explosion.start(self.width / 2, self.height / 2)
        self.stars = []
        self.player = Player(48, self.width/2, self.height-50)
        self.enemies = []
        self.player_bullet_pool = []
        self.enemy_bullet_pool = []
        self.enemy_bomb_pool = []
        self.score_pool = []
        self.powerups = []
        powerup = Powerup(64, -self.width, self.height)
        self.powerups.append(powerup)
        

        for i in range(3):
            bullets = []
            for i in range(3):
                bullet = Bullet(32, self.width, self.height, "player")
                bullets.append(bullet)
            self.player_bullet_pool.append(bullets)

        for i in range(10):
            bullet = Bullet(9, self.width, self.height, "enemy")
            self.enemy_bullet_pool.append(bullet)

        for i in range(3):
            bomb = Bomb(64, self.width, self.height)
            self.enemy_bomb_pool.append(bomb)
        
    def run(self):
        running = True
        while running:
            #clock
            self.clock.tick(self.fps)
            pygame.display.set_caption(f"space invaders ({self.clock.get_fps():.0f} fps)")
            
            #events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            #gameplay
            self.update_stars()
            if self.state == "start":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.state = "game"
                    self.spawn_timer_offset = pygame.time.get_ticks()
            elif self.state == "game":
                if len (self.score_pool)>0:
                    self.score_cooldown-=1
                    if self.score_cooldown<=0:
                        self.score_cooldown=30
                        self.score_pool .pop(0)
                    
                self.update_player()
                self.update_enemies()
                for powerup in self.powerups:
                    powerup.move(self.height, self.width)
                    powerup.update()
                    hit_result = powerup.collide(self.player.get_mask(), self.player.position.x, self.player.position.y)
                    if hit_result is not None:
                        powerup.awaken_powerup(self.player)

                for bomb in self.enemy_bomb_pool:
                    bomb.update()
                    bomb.move(self.height)
                    hit_result = bomb.collide(self.player.get_mask(), self.player.position.x, self.player.position.y)
                    if hit_result is not None:
                        self.player.damage(2)
                        bomb.alive = False
                if not self.player.alive:
                    self.state = "end"
            elif self.state == "end":
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    self.reset()
                    self.state = "game"        
            #draw
            self.draw_space()
            

            
            self.draw_stars()
            if self.state == "start":
                self.draw_text("epoc game", 50, centered = True)
            elif self.state == "game":
                for text in self.score_pool:
                    self.draw_text(text[0], 10, x = text[1], y = text[2])
                
                self.player.draw(self.screen)
                self.draw_enemies()
                for powerup in self.powerups:
                    powerup.draw(self.screen)
                for bullets in self.player_bullet_pool:
                    for bullet in bullets:
                        
                        bullet.draw(self.screen)
                for bullet in self.enemy_bullet_pool:
                    bullet.draw(self.screen)
                for bomb in self.enemy_bomb_pool:
                    bomb.draw(self.screen)
                self.explosion.draw(self.screen)
            elif self.state == "end":
                self.draw_text(f"final score: {self.score}", 50, centered = True)
            #render
            pygame.display.update()
        pygame.quit()

    def update_stars(self):
        if random.random()>0.75 and len(self.stars)<self.max_stars:
            star = Star()
            star.start(self.width)
            self.stars.append(star)
        for star in self.stars:
            
            star.move(self.height, self.width)

    def update_player(self):
        keys = pygame.key.get_pressed()
        if not self.player.position.left >0 or not self.player.position.right <self.width:
            self.player.speedx = 0

        if keys[pygame.K_a] and self.player.position.left>0:
            self.player.move_left()
        elif keys[pygame.K_d] and self.player.position.right<self.width: 
            self.player.move_right()
        self.player.move()
        self.player.update()
        self.update_player_bullets()
        if self.player.shield_cooldown <0:
            self.player.godmode = False
        else:
            self.player.godmode = True
        if self.player.speed_cooldown <0:
            self.player.speed_modifier = 1
            self.player.max_speedx = 5
        else:
            self.player.speed_modifier = 2
            self.player.max_speedx = 10

        if self.player.rapid_cooldown <0:
            self.player.fire_rate = 60
        else:
            self.player.fire_rate = 3

    def update_player_bullets(self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_f]:
            if self.player.has_nuke:
                self.explosion.explode()
                for enemy in self.enemies:
                    if enemy.alive:
                        enemy.damage(99999) 
                        self.score+= enemy.value
                self.player.fire_all([])
            if self.player.shoot_cooldown<=0:
                bullets = []
                for l in range(len(self.player_bullet_pool[0])):
                    for i in range(self.player.number_of_bullets):
                    
                    
                        
                        bullet = self.player_bullet_pool[i][l]
                        if not bullet.alive:
                            bullets.append(bullet)
                    if len(bullets)==self.player.number_of_bullets:
                        self.player.fire_all(bullets)
                    
        for bullets in self.player_bullet_pool:
            for bullet in bullets:
                if self.player.buff_cooldown > 0:
                    bullet.damage=2
                else:
                    bullet.damage =1
                bullet.move()
                bullet.update()

                if bullet.position.bottom < 0:
                    bullet.alive = False
                for enemy in self.enemies:
                    if enemy.alive and bullet.alive:
                       if bullet.collide(enemy.get_mask(), enemy.position.x, enemy.position.y) is not None:
                          self.score += enemy.value * bullet.damage 
                          bullet.alive = False


                          self.damage_enemy(enemy, bullet.damage)
                
##        for bullet in self.player_bullet_pool:
##            if self.player.buff_cooldown >0:
##                bullet.damage = 2
##            else:
##                bullet.damage = 1
##
##                
##                    
##            if keys [pygame.K_f]and self.player.shoot_cooldown<=0:
##                if self.player.has_nuke:
##                    for enemy in self.enemies:
##                        enemy.damage(99999)
##                        self.score+= enemy.value
##                        self.player.fire(bullet)
##                if not bullet.alive:
##                    self.player.fire(bullet)
##            bullet.move()
##            if bullet.position.bottom < 0:
##                bullet.alive = False
##            for enemy in self.enemies:
##                if enemy.alive and bullet.alive:
##                    if bullet.collide(enemy.get_mask(), enemy.position.x, enemy.position.y) is not None:
##                        self.score += enemy.value * bullet.damage 
##                        bullet.alive = False
##                      self.damage_enemy(enemy, bullet.damage)
                       
        

    def damage_enemy(self, enemy, value):
        score = enemy.value * value
        enemy.damage(value)   
        self.score_pool.append((f"{score}", enemy.position.centerx, enemy.position.centery))

    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.direction == 0:
                enemy.move_right()
            elif enemy.position.right>self.width:
                enemy.move_left()
            elif enemy.position.left<0:
                enemy.move_right()

            enemy.move()
            enemy.update()

            if enemy.lives > 3 and enemy.lives < 8:
                self.boss_wave(enemy)

            hit_result = enemy.collide(self.player.get_mask(),self.player.position.x, self.player.position.y)
            if hit_result is not None and self.player.alive:
                self.player.damage(1)
                self.damage_enemy(enemy, enemy.lives)
                self.score += enemy.value
            if enemy.position.top>self.height:
                enemy.alive = False
            

        self.update_enemy_bullets()
        self.update_wave()

        
        
    def update_wave(self):
        wave = self.wave_manager.load_wave(self.current_wave, self.width, self.height)
        next_wave = True
        if len(self.enemies)<wave.number_of_enemies and self.spawn_timer//1000>=wave.time_between_enemies*len(self.enemies):
            match wave.enemy_type:
                case "dreadnought":
                    EnemyType = Boss
                case "bomber":
                    EnemyType = Bomber 
                case _:
                    EnemyType = Enemy
            enemy = EnemyType(wave.startx, wave.starty, wave.speedx, wave.speedy, wave.enemy_type, 32)
            self.enemies.append(enemy)
            self.spawn_timer = 0
        else:
            self.spawn_timer = pygame.time.get_ticks()-self.spawn_timer_offset
        for enemy in self.enemies:
            if enemy.alive:
                next_wave = False
                break
        if next_wave:
            #print("yeah")
            #print("yep")
            #print("awesome")
            #print("oppppppppppppppp")
            self.current_wave = self.current_wave+1 #if self.current_wave+1 < len(self.wave_manager.waves) else 0
            self.enemies = []
            self.spawn_timer_offset+=self.spawn_timer
            self.spawn_timer = 0
    
    def boss_wave(self, boss: Boss):
        print("worked")
        wave = boss.wave
        if len(self.enemies)<=wave.number_of_enemies and boss.spawn_timer//1000>=wave.time_between_enemies*len(self.enemies):
            match wave.enemy_type:
                case "dreadnought":
                    EnemyType = Boss
                case "bomber":
                    EnemyType = Bomber 
                case _:
                    EnemyType = Enemy
            enemy = EnemyType(boss.position.centerx, boss.position.centery, wave.speedx, wave.speedy, wave.enemy_type, 32)
            self.enemies.append(enemy)
            boss.spawn_timer = 0
            boss.spawn_timer_offset = pygame.time.get_ticks()
        else:
            boss.spawn_timer = pygame.time.get_ticks()-boss.spawn_timer_offset
            


    def update_enemy_bullets(self):
        fired = False
        for bullet in self.enemy_bullet_pool:
            if len(self.enemies)> 0 and not fired:
                
                r = random.randint(0, len(self.enemies)-1)
                enemy = self.enemies[r]
                if not bullet.alive and random.random()>0.75 and enemy.shoot_cooldown<=0:
                    fired = True
                    if enemy.type == "bomber":
                        b = None
                        for bomb in self.enemy_bomb_pool:
                            if not bomb.alive:
                                b = bomb
                                break 
                        enemy.fire(bullet, b, x = 28, y = 40)
                    else:

                        enemy.fire(bullet, x = 28, y = 40)
            bullet.move()
            bullet.update()
            if bullet.position.top>self.height:
                bullet.alive = False
            hit_results = bullet.collide(self.player.get_mask(), self.player.position.x, self.player.position.y)
            if hit_results is not None:
                self.player.damage(1)
                bullet.alive = False

            
    def draw_space(self):
        image = pygame.image.load("Images/Space Background (2).png")
        self.screen.blit(image,(0,self.offset))
        self.screen.blit(image,(0,self.offset-image.get_height()))

        if self.offset > image.get_height():
            self.offset = 0
        self.offset += 1


    def draw_stars(self):
        for star in self.stars:
            star.draw(self.screen)
    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
            

    def draw_text(self, message, size, color = "white",x=0,y=0, centered = False):
        font = pygame.font.Font("fonts/pixeled.ttf", size)
        text = font.render(message, 1, color)
        origin_x = 0
        origin_y = 0


        if centered:
            origin_x = (self.width - text.get_width()) /2
            origin_y = (self.height - text.get_height()) /2
        self.screen.blit(text,(origin_x+x, origin_y+y))
game = Game()
game.start()
