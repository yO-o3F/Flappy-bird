import pygame
import random

gap = 150
pip_starting_x = 850

def setup_game():
    # Pipes
    pipes = []
    spawn_pipe(pipes)
    pipe_timer = 0

    # Score
    score = 0

    return pipes, score, pipe_timer

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
    def __init__(self):
        self.rect = pygame.Rect(200, 300, 80, 30)
        self.velocity = 0
        self.image = pygame.image.load("assets/bird.png")
        self.image = pygame.transform.scale(self.image, (125, 125))

    def gravity(self):
        self.velocity += 0.5
        self.rect.y += self.velocity
    
    def jump(self):
        self.velocity = -9
    
    def draw(self, surface):
        surface.blit(
            self.image,
            (self.rect.x - 25, self.rect.y - 50)
        )
    
    def collides_with(self, top_p, bottom_p):
        return self.rect.colliderect(top_p) or self.rect.colliderect(bottom_p)
