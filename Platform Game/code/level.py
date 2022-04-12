from re import X
import pygame
from tile import Tile
from player import Player
from settings import TILE_SIZE, SCREEN_WIDTH

class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0
        
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        self.level_setup(level_data)
        
    def level_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
                if cell == 'X':
                    self.tiles.add(Tile((x, y), TILE_SIZE))
                elif cell == 'P':
                    self.player.add(Player((x, y), self.display_surface))
                    
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < SCREEN_WIDTH * 0.25 and direction_x < 0:
            self.world_shift = 6
            player.speed = 0
        elif player_x > SCREEN_WIDTH * 0.75 and direction_x > 0:
            self.world_shift = -6
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 6
    
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right < self.current_x or player.direction.x <= 0):
            player.on_right = False
        

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top       
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and (player.direction.y < 0 or player.direction.y > player.gravity):
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
    
    def run(self):
        
        # level tiles
        self.tiles.draw(self.display_surface)
        self.tiles.update(self.world_shift)
        self.scroll_x()
        
        # player
        self.player.draw(self.display_surface)
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        
