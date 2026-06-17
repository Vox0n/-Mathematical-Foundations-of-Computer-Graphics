import pygame, sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while self.stats.game_active:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _create_fleet(self):
        alien = Alien(self)
        number_aliens_x = (self.settings.screen_width - (2 * alien.rect.width)) // (2 * alien.rect.width)
        for alien_number in range(number_aliens_x):
            new_alien = Alien(self)
            new_alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
            new_alien.rect.x = new_alien.x
            self.aliens.add(new_alien)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions: self.stats.score += self.settings.alien_points
        if not self.aliens: self.bullets.empty(); self._create_fleet(); self.settings.increase_speed()

    def _update_aliens(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen.get_rect().right or alien.rect.left <= 0:
                self.settings.fleet_direction *= -1
                for a in self.aliens.sprites(): a.rect.y += self.settings.fleet_drop_speed
                break
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens): self.stats.game_active = False

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: self.ship.moving_right = True
                elif event.key == pygame.K_LEFT: self.ship.moving_left = True
                elif event.key == pygame.K_SPACE: self.bullets.add(Bullet(self))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT: self.ship.moving_right = False
                elif event.key == pygame.K_LEFT: self.ship.moving_left = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()