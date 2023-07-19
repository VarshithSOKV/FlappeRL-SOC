import pygame
import random
import time
import sys
from classes import Button

# Game settings
WIDTH = 800
HEIGHT = 500
FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 100)
font2 = pygame.font.SysFont(None, 30)

# Load images
bg_image = pygame.transform.scale(pygame.image.load("./images/background.png"), (800, 500))
bird_image = pygame.transform.scale(pygame.image.load("./images/plane.png"), (40, 40))
pipe_image = pygame.transform.scale(pygame.image.load("./images/pipe2.jpeg"), (70, 400))
pipe_image_inverse = pygame.transform.flip(pygame.transform.scale(pygame.image.load("./images/pipe.jpeg"), (70, 400)), False, True)
game_over_image = pygame.image.load("./images/gameover.png")
game_over_rect = game_over_image.get_rect()
game_over_rect.center = (400,250)

bird_rect = bird_image.get_rect()
bird_rect.center = (WIDTH // 2, HEIGHT // 2)

play_again_image = pygame.image.load('./images/play_again.png').convert_alpha()
exit_image = pygame.image.load('./images/exit.png').convert_alpha()

play_again_button = Button(170,380,play_again_image,0.3)
exit_button = Button(630,380,exit_image,0.3)

jump_sound = pygame.mixer.Sound('./sounds/jump.wav')
jump_sound.set_volume(0.3)

pipes = []

score = 0

running = True
game_over = False
countdown = 3  # Initial countdown value

bird_velocity = 0  # Initialize the bird's velocity
bg_x_1 = 0
bg_x_2 = 800

n = 0
while running:
    n += 1
    if countdown > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(bg_image, (0, 0))
        countdown_text = font.render(str(countdown), True, WHITE)
        countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(countdown_text, countdown_rect)

        if pygame.time.get_ticks() >= 1000:
            countdown -= 1
            pygame.time.set_timer(pygame.USEREVENT, 1000)

        pygame.display.update()
        time.sleep(1)
        clock.tick(FPS)
    elif not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = JUMP_VELOCITY
                    jump_sound.play()
        if( n > 6 ):
            bird_velocity += GRAVITY
            bird_rect.y += bird_velocity

        # Generate pipes
        if len(pipes) < 5 and (not pipes or pipes[-1].right < WIDTH // 2):
            gap_y = random.randint(200, 450)
            pipe_upper = pipe_image_inverse.get_rect(midbottom=(WIDTH + 100,gap_y - 150))
            pipe_lower = pipe_image.get_rect(midtop=(WIDTH + 100,gap_y))
            pipes.append(pipe_upper)
            pipes.append(pipe_lower)

        # Move pipes
        for pipe in pipes:
            pipe.x -= 5

            # Check collision
            if bird_rect.colliderect(pipe):
                game_over = True

            # Remove pipes that go off-screen
            if pipe.right < 0:
                pipes.remove(pipe)
                score += 1

        #Move background
        bg_x_1 += -5
        bg_x_2 += -5
        if(bg_x_1 == -800):
            bg_x_1 = bg_x_2
            bg_x_2 = 800

        # Check if the bird hits the ground
        if bird_rect.bottom >= HEIGHT:
            game_over = True

        screen.blit(bg_image, (bg_x_1,0))
        screen.blit(bg_image, (bg_x_2, 0))
        screen.blit(bird_image, bird_rect)

        for pipe in pipes:
            if pipe.top < 0:
                screen.blit(pipe_image_inverse, pipe)
            else:
                screen.blit(pipe_image, pipe)

        score_text = font2.render("Score: " + str(score), True, WHITE)
        score_rect = score_text.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(FPS)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         game_over = False
            #         bird_rect.center = (WIDTH // 2, HEIGHT // 2)
            #         pipes.clear()
            #         score = 0

        screen.blit(bg_image, (bg_x_1, 0))
        screen.blit(bg_image,(bg_x_2,0))
        screen.blit(game_over_image, game_over_rect)
        final_score_text = font.render("Score: " + str(score), True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))
        screen.blit(final_score_text, final_score_rect)

        if play_again_button.draw(screen):
            running = True
            game_over = False
            bird_rect.center = (WIDTH // 2, HEIGHT // 2)
            score = 0
            pipes.clear()
            countdown = 3
            n = 0
        elif exit_button.draw(screen):
            pygame.quit()
            sys.exit()
        pygame.display.update()

        

pygame.quit()
