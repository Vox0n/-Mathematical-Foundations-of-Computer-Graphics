import pygame, sys, pickle, os, random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from bonus import Bonus
from button import Button


class AlienInvasion:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bonuses = pygame.sprite.Group()
        self.play_button = Button(self, "Restart")

        self._create_fleet()

        self.shoot_sound = pygame.mixer.Sound(os.path.join('resources', 'shoot.wav'))
        self.explosion_sound = pygame.mixer.Sound(os.path.join('resources', 'explosion.wav'))
        self.game_over_sound = pygame.mixer.Sound(os.path.join('resources', 'game_over.wav'))

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.bonuses.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.stats.game_active and self.play_button.rect.collidepoint(mouse_pos):
                    self._reset_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE and self.stats.game_active:
                    self.bullets.add(Bullet(self));
                    self.shoot_sound.play()
                elif event.key == pygame.K_s:
                    self._save_game()
                elif event.key == pygame.K_l:
                    self._load_game()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _reset_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.aliens.empty();
        self.bullets.empty();
        self.bonuses.empty()
        self._create_fleet();
        self.ship.center_ship()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        if self.stats.game_active:
            self.ship.blitme()
            for bullet in self.bullets.sprites(): bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.bonuses.draw(self.screen)
        else:
            font = pygame.font.SysFont(None, 100)
            go_img = font.render("GAME OVER", True, (255, 0, 0))
            self.screen.blit(go_img, (400, 200))
            self.play_button.draw_button()
        pygame.display.flip()

    # --- Остальные методы (_update_bullets, _update_aliens, _create_fleet, _save_game, _load_game) ---
    # Оставьте их без изменений из предыдущего сообщения
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
        if collisions:
            self.explosion_sound.play()
            self.stats.score += self.settings.alien_points
            if random.random() < 0.1: self.bonuses.add(Bonus(self))
        if not self.aliens:
            self.bullets.empty();
            self._create_fleet();
            self.settings.increase_speed();
            self.stats.level += 1

    def _update_aliens(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen.get_rect().right or alien.rect.left <= 0:
                self.settings.fleet_direction *= -1
                for a in self.aliens.sprites(): a.rect.y += self.settings.fleet_drop_speed
                break
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.stats.game_active = False;
            self.game_over_sound.play()

    def _save_game(self):
        data = {"level": self.stats.level, "score": self.stats.score, "lives": self.stats.ships_left}
        with open("savefile.pkl", "wb") as f: pickle.dump(data, f)

    def _load_game(self):
        if os.path.exists("savefile.pkl"):
            with open("savefile.pkl", "rb") as f:
                data = pickle.load(f)
                self.stats.level, self.stats.score, self.stats.ships_left = data["level"], data["score"], data["lives"]


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()