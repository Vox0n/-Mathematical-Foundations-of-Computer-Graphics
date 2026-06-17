import pygame
class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.x = float(self.rect.x)
        self.moving_right = self.moving_left = False
    def update(self):
        if self.moving_right and self.rect.right < self.screen.get_rect().right: self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0: self.x -= self.settings.ship_speed
        self.rect.x = self.x
    def blitme(self): self.screen.blit(self.image, self.rect)
    def center_ship(self): self.rect.midbottom = self.screen.get_rect().midbottom; self.x = float(self.rect.x)