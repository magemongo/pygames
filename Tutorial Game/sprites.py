from random import randint
import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk = (
            pg.image.load('graphics\\Player\\player_walk_1.png').convert_alpha(),
            pg.image.load('graphics\\Player\\player_walk_2.png').convert_alpha()
            )
        self.jump = pg.image.load('graphics\\Player\\jump.png').convert_alpha()
        self.index = 0
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom= (80, 300))
        self.gravity = 0
        
        self.jump_sound = pg.mixer.Sound('audio\\jump.mp3')
        self.jump_sound.set_volume(0.1)
        
    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.index += 0.1
            if self.index >= len(self.walk):
                self.index = 0
            self.image = self.walk[int(self.index)]
    
    def update(self):
        self.apply_gravity()
        self.player_input()
        self.animate()
        
class Obstable(pg.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "snail":
            self.frames = (
                pg.image.load('graphics\\snail\\snail1.png').convert_alpha(),
                pg.image.load('graphics\\snail\\snail2.png').convert_alpha()
            )
            y_pos = 300
        elif type == "fly":
            self.frames = (
                pg.image.load('graphics\\fly\\fly1.png').convert_alpha(), 
                pg.image.load('graphics\\fly\\fly2.png').convert_alpha()
            )
            y_pos = 150

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    
    def animate(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        
    def update(self):
        self.animate()
        self.rect.x -= 5
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
