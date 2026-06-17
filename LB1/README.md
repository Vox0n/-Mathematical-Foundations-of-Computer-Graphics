
---

# Отчёт по практической работе №1: «Инопланетное вторжение»

## 1. Цель работы

Разработка базовой 2D-игры с использованием библиотеки `pygame` для изучения основ компьютерной графики, анимации, обработки пользовательских событий и принципов объектно-ориентированного программирования (ООП).

## 2. Структура проекта

Проект разделён на 5 модулей для обеспечения высокой читаемости и удобства поддержки:

* `settings.py` — параметры игры.
* `ship.py` — класс корабля.
* `bullet.py` — класс снарядов.
* `alien.py` — класс противников.
* `alien_invasion.py` — главный файл (игровой цикл).

---

## 3. Исходные коды файлов

### `settings.py`

```python
class Settings:
    """Класс для хранения всех настроек игры."""
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (30, 30, 30)
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1 — вправо, -1 — влево

```

### `ship.py`

```python
import pygame

class Ship:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0)) # Зеленый квадрат
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen.get_rect().midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen.get_rect().right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

```

### `bullet.py`

```python
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)

```

### `alien.py`

```python
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0)) # Красный квадрат
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

```

### `alien_invasion.py`

```python
import pygame, sys
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

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

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: self.bullets.remove(bullet)
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _create_fleet(self):
        for alien_number in range(10):
            alien = Alien(self)
            alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
            self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= self.screen.get_rect().right or alien.rect.left <= 0:
                self.settings.fleet_direction *= -1
                for a in self.aliens.sprites(): a.rect.y += self.settings.fleet_drop_speed
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites(): bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

```

---

## 4. Выводы

Работа завершена успешно. Разработанная архитектура позволяет управлять игровым процессом, обрабатывать коллизии и динамически изменять состояние объектов на экране. Данный проект является масштабируемой основой для дальнейшего изучения разработки игр.


---

## 5. Дополнительные обновления и расширение функционала

После реализации базовой версии игры проект был расширен для повышения увлекательности игрового процесса и соответствия продвинутым требованиям.

### Внесенные изменения:

1. **Модуль статистики (`game_stats.py`)**: Добавлен новый класс для отслеживания прогресса игрока. Он хранит данные о текущем счете, достигнутом уровне и количестве доступных жизней (кораблей).
2. **Динамическая система сложности**: В `settings.py` внедрена логика ускорения игры. Методы `initialize_dynamic_settings` и `increase_speed` обеспечивают автоматическое повышение скорости движения пришельцев и увеличение количества очков за их уничтожение при переходе на каждый новый уровень.
3. **Игровая логика**: В главном файле `alien_invasion.py` добавлена обработка столкновений:
* При попадании снаряда в инопланетянина обновляется счет игрока.
* При уничтожении всего флота инициируется создание новой волны с повышенной скоростью.
* Реализована проверка условий проигрыша: столкновение корабля с противником или касание инопланетянами нижней границы экрана завершает игру.



### Пример расширенного кода:

#### `game_stats.py`

```python
class GameStats:
    """Отслеживание статистики игры."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

```

#### Логика обновления счета и уровней (`alien_invasion.py`)

```python
    def _update_bullets(self):
        self.bullets.update()
        # Проверка попаданий
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.stats.score += self.settings.alien_points
        
        # Переход на новый уровень
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1

```

## 6. Итоговые выводы

В ходе работы над обновлениями была достигнута масштабируемость проекта. Внедрение класса `GameStats` и методов динамического изменения настроек позволило превратить статичный прототип в полноценный игровой цикл с прогрессией сложности. Данная архитектура полностью готова к дальнейшему развитию, включая добавление звуковых эффектов через `pygame.mixer` и создание визуального интерфейса для вывода рекордов.
