import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'{current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            screen.blit(snail_surf,obstacle_rect)

            return obstacle_list        
    else: return []

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pixel Run")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/pixeltype.ttf",50)
game_active = False
start_time = 0
score = 0

# Background generation
sky_surf = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()

score_surf = test_font.render("My Game", False,(64,64,64)).convert_alpha()
score_rect = score_surf.get_rect(midtop = (400,50))

# Obstacles
snail_surf = pygame.image.load("graphics/snail/snail1.png")
snail_rect = snail_surf.get_rect(midbottom = (randint(900,1100), 300))

obstacle_rect_list = []

# Player generation
player_surf = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = test_font.render('Pixel Run', False,(111,196,169)).convert_alpha()
title_rect = title_surf.get_rect(midtop = (400,50))
instruction_surf = test_font.render('Press Space to Run',False,(111,196,169)).convert_alpha()
instruction_rect = instruction_surf.get_rect(midbottom = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)
        
        if event.type == obstacle_timer and game_active:
            obstacle_rect_list.append(snail_rect)
    
    if game_active:
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0,300))
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        # Snail
        # snail_rect.right -= 5
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        screen.blit(player_surf,player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        score_message = test_font.render(f'Your Score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(midbottom = (400,350))
        screen.blit(title_surf,title_rect)

        if score == 0:
            screen.blit(instruction_surf,instruction_rect)
        else:
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(60)