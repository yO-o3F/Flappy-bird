import pygame
from entities import Game

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# Game setup
running = True
game = Game()
draw = game.draw

while running:
    # Fps is limited to 60
    clock.tick(60)

    # menu state
    if game.state == "menu":
        draw.menu_utilities(screen)

    # playing state
    elif game.state == "playing":
        draw.playing_utilities(screen, game.score, clock)
        game.update(screen)
            
    # Game Over state
    elif game.state == "game_over":
        draw.game_over_utilities(screen, game.score, game.record)

    # Update the screen
    pygame.display.update()
    
    # Poll for events
    for event in pygame.event.get():
        # Jump
        if (game.state == "playing" or game.state == "menu") and event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP):
            game.bird.jump()
            game.state = "playing"

        # Restart
        if game.state == "game_over" and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            screen.fill("black")
            game.restart()
            
        # Quit game
        if (game.state == "game_over" or game.state == "menu") and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
