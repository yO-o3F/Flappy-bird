import pygame
import random
from setup import setup_game, write_text, Bird, Pipes

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# States
running = True
state = "menu"

# Seting up the game
bird = Bird()
score = setup_game()
pipes = Pipes(850, 150)
pipes.spawn()
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

        bird.draw(screen)

        # Gravity
        bird.gravity()

        # Boundaries
        if bird.rect.top < 0:
            bird.rect.top = 0
        elif bird.rect.bottom > 600:
            bird.rect.bottom = 600
            state = "game_over"

        # Pipe
        # Spawn next pipe
        if pipes.time_elapsed():
            pipes.spawn()

        # Remove passed pipes
        pipes.remove_passed_pipes()
        
        # For each pipe
        for pipe in pipes.Pipes:
        # Movement
            pipes.move(pipe)

        # Pipe image
            pipes.draw(screen, pipe["bottom"].x, pipe["bottom"].y)
        
        # Collision
            if bird.collides_with(pipe["top"], pipe["bottom"]):
                state = "game_over"

        # Score
            if bird.passed_by(pipe):
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
            bird.jump()
            state = "playing"

        # Restart
        if state == "game_over" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            screen.fill("black")
            score = setup_game()
            state = "playing"
            
        # Quit game
        if (state == "game_over" or state == "menu") and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
