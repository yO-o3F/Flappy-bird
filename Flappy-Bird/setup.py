import pygame
import random

gap = 150
pip_starting_x = 850

def setup_game():
    # Bird
    velocity = 1
    bird = pygame.Rect(200, 300, 80, 30)

    # Pipes
    pipes = []
    spawn_pipe(pipes)
    pipe_timer = 0

    # Score
    score = 0

    return velocity, bird, pipes, score, pipe_timer

def spawn_pipe(pipes):
    top_height = random.randrange(50, 400, 30)
    bottom_top = top_height + gap

    pipes.append({
        "top": pygame.Rect(
            pip_starting_x,
            0,
            100,
            top_height
        ),
        "bottom": pygame.Rect(
            pip_starting_x,
            bottom_top,
            100,
            600 - bottom_top
        ),
        "counted" : False
    })
    return pipes

def write_text(text, f, color, background=None):
    return f.render(
        text,
        True,
        color,
        background
    )

class Bird:
    def __init__():
        pass
