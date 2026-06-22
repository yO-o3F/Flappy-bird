import pygame
import random
from setup import setup_game, write_text, spawn_pipe

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# States
running = True
state = "menu"

# Seting up the game
velocity, bird, pipes, score, pipe_timer = setup_game()
record = 0

# Fonts
verySmall_font = pygame.font.Font(None, 20)
small_font = pygame.font.Font(None, 30)
medium_font = pygame.font.Font(None, 35)
# large_font = pygame.font.Font(None, 80)

# Images
# Background
background_image = pygame.image.load("assets/bg5.png")
background_image = pygame.transform.scale(background_image, (800, 600))
# Game Over
game_over_image = pygame.image.load("assets/gameO.jpg")
game_over_image = pygame.transform.scale(game_over_image, (800, 600))
# Bird
bird_image = pygame.image.load("assets/bird.png")
bird_image = pygame.transform.scale(bird_image, (125, 125))
# Pipes
pipe_image = pygame.image.load("assets/pip.png")

while running:
    # Fps is limited to 60
    clock.tick(60)
    

    # menu state
    if state == "menu":
        screen.fill("black")
        screen.blit(
            write_text("Press [Space] to start the Game!", medium_font, "white", "black"),
            (215, 285)
        )

    # playing state
    elif state == "playing":

        # Clear the screen
        screen.fill("black")
        screen.blit(
            background_image,
            (0, 0)
        )

        screen.blit(
            bird_image,
            (bird.x - 25, bird.y - 50)
        )

        # Gravity
        velocity += 0.5
        bird.y += velocity

        # Boundaries
        if bird.top < 0:
            bird.top = 0
        elif bird.bottom > 600:
            bird.bottom = 600
            state = "game_over"

        # Pipe
        # Count time to spawn next pipe
        pipe_timer += 1

        # Remove passed pipes
        pipes = [p for p in pipes if p["top"].right >= 0]
        
        # Spawn
        for pipe in pipes:
            if pipe_timer >= 90:
                spawn_pipe(pipes)
                pipe_timer = 0

        # Movement
            pipe["top"].x -= 5
            pipe["bottom"].x -= 5

        # Pipe image
            screen.blit(
                pipe_image,
                (pipe["bottom"].x - 20, pipe["bottom"].y - 625)
            )

        # Collision
            if bird.colliderect(pipe["bottom"]) or bird.colliderect(pipe["top"]):
                state = "game_over"

        # Score
            if not pipe["counted"] and bird.x > pipe["top"].right:
                score += 1
                pipe["counted"] = True
        
        # Showing live fps and score
        screen.blit(
            write_text(f"Score: {score}", medium_font, "white"),
            (350, 10)
        )
        screen.blit(
            write_text(f"FPS: {int(pygame.time.Clock.get_fps(clock))}", verySmall_font, "white"),
            (10, 10)
        )
        # Record
        if score > record:
            record = score
            
        # Bird and Pipe hit boxes
        # pygame.draw.rect(screen, "yellow", pipe["top"])
        # pygame.draw.rect(screen, "yellow", pipe["bottom"])
        # pygame.draw.rect(screen, "yellow", bird)
      
    # Game Over state
    elif state == "game_over":
        screen.fill("black")
        screen.blit(
            game_over_image,
            (0, 0)
        )

        screen.blit(
            write_text(f"Score: {score}", small_font, "white"),
            (230, 440)
        )
        screen.blit(
            write_text(f"Record: {record}", small_font, "white"),
            (485, 440)
        )
        screen.blit(
            write_text("Press [R]estart or [Q]uit", small_font, "white"),
            (280, 550)
        )

    # Updating the screen to render new things we drew
    pygame.display.update()
    
    # Poll for events
    for event in pygame.event.get():
        # Jump
        if (state == "playing" or state == "menu") and event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            velocity = -9
            state = "playing"

        # Restart
        if state == "game_over" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            screen.fill("black")
            velocity, bird, pipes, score, pipe_timer = setup_game()
            state = "playing"
            
        # Quit game
        if (state == "game_over" or state == "menu") and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
