import pygame
import random

class UI:
    def __init__(self):
        # Fonts
        self.verySmall_font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 30)
        self.medium_font = pygame.font.Font(None, 35)

        # Images
        # Background
        self.background_image = pygame.image.load("assets/bg5.png")
        self.background_image = pygame.transform.scale(self.background_image, (800, 600))
        # Gameover
        self.game_over_image = pygame.image.load("assets/gameO.jpg")
        self.game_over_image = pygame.transform.scale(self.game_over_image, (800, 600))

    def write_text(self, text, f, background=None, color="white"):
        return f.render(
            text,
            True,
            color,
            background
        )

    def menu_utilities(self, surface):
        surface.fill("black")
        surface.blit(
            self.write_text("Press [Space] to start the Game!", self.medium_font, "black"),
            (215, 285)
        )

    def game_over_utilities(self, surface, score, record):
        surface.fill("black")
        surface.blit(
            self.game_over_image,
            (0, 0)
        )

        surface.blit(
            self.write_text(f"Score: {score}", self.small_font),
            (230, 440)
        )
        
        surface.blit(
            self.write_text(f"Record: {record}", self.small_font),
            (485, 440)
        )
        
        surface.blit(
            self.write_text("Press [R]estart or [Q]uit", self.small_font),
            (280, 550)
        )

    def playing_utilities(self, surface, score, clock):
        surface.fill("black")
        surface.blit(
            self.background_image,
            (0, 0)
        )

        surface.blit(
            self.write_text(f"Score: {score}", self.medium_font),
            (350, 10)
        )

        surface.blit(
            self.write_text(f"FPS: {int(clock.get_fps())}", self.verySmall_font),
            (10, 10)
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

    def passed(self, pipe):
        return self.rect.x > pipe.top.right
    
    def draw_hit_box(self, surface):
        pygame.draw.rect(surface, "yellow", self.rect)

class Pipes:
    image = pygame.image.load("assets/pip.png")

    def __init__(self, x):
        gap = 150
        top_height = random.randrange(50, 400, 30)
        
        
        self.top = pygame.Rect(x, 0, 100, top_height)
        self.bottom = pygame.Rect(
            x,
            top_height + gap,
            100,
            600 - (top_height + gap)
        )
        self.counted = False
    
    def off_screen(self):
        # What is this?
        return self.top.right < 0

    def move(self):
        self.top.x -= 5
        self.bottom.x -= 5

    def draw(self, surface):
        surface.blit(
            self.image,
            (self.bottom.x - 20, self.bottom.y - 625)
        )

    def collides_with(self, bird):
        return self.top.colliderect(bird) or self.bottom.colliderect(bird)

    def draw_hit_box(self, surface):
        pygame.draw.rect(surface, "yellow", self.top)
        pygame.draw.rect(surface, "yellow", self.bottom)

class Game():
    record = 0

    def __init__(self):
        self.state = "menu"
        self.pipes = []
        self.pipe_timer = 89
        self.score = 0
        self.bird = Bird()
        self.draw = UI()

    def spawn_pipe(self):
        self.pipes.append(Pipes(850))
        # print(len(self.pipes))

    def restart(self):
        self.__init__()
        self.state = "playing"

    def show_hit_boxes(self, surface):
        for p in self.pipes:
            p.draw_hit_box(surface)
        self.bird.draw_hit_box(surface)
    
    def update(self, surface):
        if not self.state == "playing":
            return

        # draw bird
        self.bird.draw(surface)

        # bird.gravity
        self.bird.gravity()

        # bird boundaries?
        if self.bird.rect.top < 0:
            self.bird.rect.top = 0
        elif self.bird.rect.bottom > 600:
            self.bird.rect.bottom = 600
            self.state = "game_over"

        # pipe timer and spawn
        self.pipe_timer += 1
        if self.pipe_timer >= 90:
            self.spawn_pipe()
            self.pipe_timer = 0

        self.pipes = [p for p in self.pipes if not p.off_screen()]

        # pipes draw
        for pipe in self.pipes:
            # draw pipes
            pipe.draw(surface)
            
            # pipes move
            pipe.move()
            
            # collision
            if pipe.collides_with(self.bird.rect):
                self.state = "game_over"

            # score
            if not pipe.counted and self.bird.passed(pipe):
                self.score += 1
                pipe.counted = True

            # record
            if self.score > self.record:
                self.record = self.score
