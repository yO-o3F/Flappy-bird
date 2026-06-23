import pygame
import random

def setup_game():
    # Score
    score = 0

    return score

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
        self.velocity = -7
    
    def draw(self, surface):
        surface.blit(
            self.image,
            (self.rect.x - 25, self.rect.y - 50)
        )
    
    def collides_with(self, top_p, bottom_p):
        return self.rect.colliderect(top_p) or self.rect.colliderect(bottom_p)

    def passed_by(self, pipe):
        return not pipe["counted"] and self.rect.x > pipe["top"].right


class Pipes:
    def __init__(self, starting_x, gap):
        self.Pipes = []
        self.pip_starting_x = starting_x
        self.gap = gap
        self.pipe_timer = 0
        self.image = pygame.image.load("assets/pip.png")

    def spawn(self):
        self.top_height = random.randrange(50, 400, 30)
        self.bottom_top = self.top_height + self.gap

        self.Pipes.append({
            "top": pygame.Rect(
                self.pip_starting_x,
                0,
                100,
                self.top_height
            ),
            "bottom": pygame.Rect(
                self.pip_starting_x,
                self.bottom_top,
                100,
                600 - self.bottom_top
            ),
            "counted" : False
        })
    
    def remove_passed_pipes(self):
        self.Pipes = [p for p in self.Pipes if p["top"].right >= 0]

    def move(self, pipe):
        pipe["top"].x -= 5
        pipe["bottom"].x -= 5

    def draw(self, surface, x, y):
        surface.blit(
            self.image,
            (x - 20, y - 625)
        )
    def time_elapsed(self):
        self.pipe_timer += 1
        if self.pipe_timer >= 90:
            self.pipe_timer = 0
            return True
        return False
