import pygame, random
from pygame.sprite import Sprite

class Bonus(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ai_game.settings.screen_width)
        self.rect.y = 0
        self.speed = 1.0

    def update(self):
        self.rect.y += self.speed