import pygame as pg
from sprites import Player, Obstable
from sys import exit
from random import choice

def display_score():
    curr_time = (pg.time.get_ticks() // 1000) - start_time
    score_surf = pixel_font.render(f'Score: {curr_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time

def sprite_collision():
    if pg.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    return True

    
# Constants
pg.init()
screen = pg.display.set_mode((800, 400))
pg.display.set_caption("Tutorial Game")
clock = pg.time.Clock()
pixel_font = pg.font.Font('font\\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pg.mixer.Sound('audio\\music.wav')
bg_music.set_volume(0.01)
bg_music.play(loops = -1)

player = pg.sprite.GroupSingle()
player.add(Player())

obstacles = pg.sprite.Group()

# Background
sky_surf = pg.image.load('graphics\\sky.png').convert()
ground_surf = pg.image.load('graphics\\ground.png').convert()

# Intro screen
title_surf = pixel_font.render('Tutorial Game', False, (111, 196, 169))
title_rect = title_surf.get_rect(center = (400, 50))
player_stand = pg.transform.rotozoom(
    pg.image.load('graphics\\Player\\player_stand.png').convert_alpha(),
    angle=0, scale=2
    )
player_stand_rect = player_stand.get_rect(center = (400, 200))
intro_surf = pixel_font.render('Press SPACE to start!', False, (111, 196, 169))
intro_rect = intro_surf.get_rect(center = (400, 350))

# Timer
obstacle_timer = pg.USEREVENT + 1 # importante adicionar 1 para custom events
pg.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pg.USEREVENT + 2 
pg.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pg.USEREVENT + 3 
pg.time.set_timer(fly_animation_timer, 200)


while True:
    # Event Loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstable(choice(['fly', "snail", "snail", "snail"])))
                
        else:
            if (event.type == pg.KEYDOWN) and (event.key == pg.K_SPACE):
                game_active = True
                start_time = pg.time.get_ticks() // 1000      
    
    if game_active:
        bg_music.set_volume(0.1)
        # Background
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        score = display_score()
        
        # Player
        player.draw(screen)
        player.update()
        
        # Obstacles
        obstacles.draw(screen)
        obstacles.update()
        
        # Collisions
        game_active = sprite_collision()
     
    else:
        # Intro/Replay Screen
        bg_music.set_volume(0.01)
        screen.fill((94, 129, 162))
        screen.blit(title_surf, title_rect)
        screen.blit(player_stand, player_stand_rect)
        score_message = pixel_font.render(f"Your last score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 350))
        if score:
            screen.blit(score_message, score_message_rect)
        else:
            screen.blit(intro_surf, intro_rect)

   
    pg.display.update()
    clock.tick(60)