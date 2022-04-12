from matplotlib import animation
import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        
        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        
        # player movement
        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.gravity = 0.8
        self.jump_speed = -16
        
        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {
            'idle': [], 'run': [],
            'jump': [], 'fall': []
            }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    def import_dust_run_particles(self):
        character_path = '../graphics/character/dust_particles/run'
        self.dust_run_particles = import_folder(character_path)
    
    def character_animation(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        if self.facing_right:
            self.image = animation[int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(
                animation[int(self.frame_index)], True, False
                )
              
        # set the rect
        if self.on_ground:
            if self.on_left:
                self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
            elif self.on_right:
                self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
            else:
                self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling:
            if self.on_left:
                self.rect = self.image.get_rect(topleft = self.rect.topleft)
            elif self.on_right:
                self.rect = self.image.get_rect(topright = self.rect.topright)
            else:
                self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)
    
    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]
    
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # movement input
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0
        
        # jump input
        if keys[pygame.K_SPACE] and self.on_ground:
            self.direction.y = self.jump_speed
    
    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    def update(self):
        self.get_input()
        self.get_status()
        self.character_animation()
        
         