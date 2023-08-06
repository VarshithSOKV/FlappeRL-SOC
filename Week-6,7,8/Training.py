import numpy as np
import pygame
import random
import time
from classes import Button

def next_pipe(pipes):
    for pipe in pipes:
        # print(pipe.centerx)
        if(pipe.centerx > 400 and pipe.centerx < 800 and pipe.y < 0):
            return pipe
        # else:
        #     return bird_rect

def find_state(bird_rect, pipe_rect, bird_velocity):
    S = np.zeros((25,25,10))
    for j in range(25):
        a = pipe_rect.midbottom[0] - bird_rect.centerx
        b = bird_rect.centery - pipe_rect.midbottom[1]
        if( a >= j*16 and a < (j+1)*16 ):
            for i in range(25):
                if(b >= i*20 - 250 and b < (i+1)*20 - 250):
                    flag = False
                    for k in range(10):
                        if(bird_velocity > 2*k - 10 and bird_velocity < 2*(k+1) - 10):
                            S[i][j][k] = 1
                            flag = True
                    if(flag == False):
                        if(bird_velocity < -10):
                            S[i][j][0] = 1
                        else:
                            S[i][j][9] = 1
    return S

def next_state(pipes, bird_rect, bird_velocity):

    pipe_rect = next_pipe(pipes)

    S = find_state(bird_rect, pipe_rect, bird_velocity)
    n = np.unravel_index(np.argmax(S),S.shape)
    print(n)
    return n

def initialize_Q():
    # Q = np.zeros((50,50,2))
    # return Q
    # open the file in read binary mode
    file = open("Q_function3", "rb")
    #read the file to numpy array
    Q = np.load(file)
    #close the file
    return Q

def save_Q(Q):
    # open a binary file in write mode
    file = open("Q_function3", "wb")
    # save array to the file
    np.save(file, Q)
    # close the file
    file.close
    
def game(Q):
    # Game settings
    WIDTH = 800
    HEIGHT = 500
    FPS = 60
    GRAVITY = 0.7
    JUMP_VELOCITY = -6

    # Colors
    WHITE = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 100)
    font2 = pygame.font.SysFont(None, 30)

    # Load images
    bg_image = pygame.transform.scale(pygame.image.load("./images/background.png"), (800, 500))
    bird_image = pygame.transform.scale(pygame.image.load("./images/plane.png"), (30, 30))
    pipe_image = pygame.transform.scale(pygame.image.load("./images/pipe2.jpeg"), (70, 400))
    pipe_image_inverse = pygame.transform.flip(pygame.transform.scale(pygame.image.load("./images/pipe.jpeg"), (70, 400)), False, True)

    bird_rect = bird_image.get_rect()
    bird_rect.center = (WIDTH // 2, HEIGHT // 2)

    jump_sound = pygame.mixer.Sound('./sounds/jump.wav')
    jump_sound.set_volume(0.3)

    pipes = []

    score = 0

    running = True
    game_over = False
    countdown = 1  # Initial countdown value

    bird_velocity = 0  # Initialize the bird's velocity
    bg_x_1 = 0
    bg_x_2 = 800

    n = 0
    k = 0
    S = [15,22,5]
    S_prime = [15,22,5]
    action = 0
    action_prime = 0
    els = 0
    l = [0, 1]
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
            # time.sleep(1)
            clock.tick(FPS)
        if not game_over:

            k += 1
            if( k == 8 or k > 15):

                k = 2
                S = S_prime
                if( n == 3):
                    S = [15, 22, 5]

                action = action_prime

                S_prime = next_state(pipes, bird_rect, bird_velocity)

                p = np.random.random()
                if p < els:
                    action_prime = np.random.choice(l,1,0)
                else:
                    action_prime = np.argmax(Q[S_prime[0]][S_prime[1]][S_prime[2]])

                Q[S[0]][S[1]][S[2]][action] = Q[S[0]][S[1]][S[2]][action] + 0.9 * (0.5 + (Q[S_prime[0]][S_prime[1]][S_prime[2]][action_prime]) - Q[S[0]][S[1]][S[2]][action])

                if(action == 1):
                    bird_velocity = JUMP_VELOCITY
                    jump_sound.play()
                # print(action)

            if( n > 6 ):
                bird_velocity += GRAVITY
                bird_rect.y += bird_velocity

            # Generate pipes
            # if len(pipes) < 5 and (not pipes or pipes[-1].right < WIDTH // 2):
            #     gap_y = random.randint(200, 450)
            #     pipe_upper = pipe_image_inverse.get_rect(midbottom=(WIDTH - 200,gap_y - 150))
            #     pipe_lower = pipe_image.get_rect(midtop=(WIDTH - 200,gap_y))
            #     pipes.append(pipe_upper)
            #     pipes.append(pipe_lower)

            if len(pipes) < 5 and (not pipes or pipes[-1].right < WIDTH // 2 + 100):
                lower_y = random.randint(300, 400)
                pipe_upper = pipe_image_inverse.get_rect(midbottom=(WIDTH ,lower_y - 170))
                pipe_lower = pipe_image.get_rect(midtop=(WIDTH ,lower_y))
                pipes.append(pipe_upper)
                pipes.append(pipe_lower)

            # Move pipes
            for pipe in pipes:
                pipe.x -= 5

                # Check collision
                if bird_rect.colliderect(pipe):
                    game_over = True
                    Q[S[0]][S[1]][S[2]][action] -= 30

                # Remove pipes that go off-screen
                if pipe.right < 390:
                    pipes.remove(pipe)
                    score += 1
                    Q[S[0]][S[1]][S[2]][action] += 10

            #Move background
            bg_x_1 += -5
            bg_x_2 += -5
            if(bg_x_1 == -800):
                bg_x_1 = bg_x_2
                bg_x_2 = 800

            # Check if the bird hits the ground
            if bird_rect.bottom >= HEIGHT or bird_rect.top <=0:
                game_over = True
                Q[S[0]][S[1]][S[2]][action] -= 400

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
            running = True
            game_over = False
            bird_rect.center = (WIDTH // 2, HEIGHT // 2)
            bird_velocity = 0
            score = 0
            pipes.clear()
            countdown = 1 
            n = 0
            k = 0
            

    # pygame.quit()

if __name__ == "__main__":
    Q = initialize_Q()
    game(Q)
    print(Q)
    # Q = np.zeros((25,25,10,2), float)
    save_Q(Q)