# Отчёт по практической работе №2: «Развитие игры "Инопланетное вторжение"»

## 1. Цель работы

Дополнить базовую игру «Инопланетное вторжение» функциональностью, которая делает игровой процесс более увлекательным и технологичным. В ходе работы были внедрены: звуковые эффекты, система уровней, сохранение прогресса через сериализацию, интерактивные объекты (бонусы) и подготовлен инструмент для сборки игры в исполняемый файл.

---

## 2. Структура проекта

Проект был расширен и теперь включает следующие модули:

* `settings.py` — конфигурация параметров игры.
* `game_stats.py` — управление состоянием (счет, уровень, жизнь).
* `ship.py` — логика корабля.
* `bullet.py` — логика снарядов.
* `alien.py` — логика пришельцев.
* `bonus.py` — логика интерактивных бонусов.
* `button.py` — графический интерфейс кнопки рестарта.
* `alien_invasion.py` — главный файл и игровой цикл.

---

## 3. Исходные коды реализованных модулей

### `bonus.py` (Новый модуль)

```python
import pygame, random
from pygame.sprite import Sprite

class Bonus(Sprite):
    """Класс для создания интерактивных бонусов."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 255, 0)) # Желтый цвет бонуса
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ai_game.settings.screen_width)
        self.rect.y = 0
        self.speed = 1.0

    def update(self):
        self.rect.y += self.speed

```

### `button.py` (Новый модуль)

```python
import pygame.font

class Button:
    """Класс для создания кнопки интерфейса."""
    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 200, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

```

### `alien_invasion.py` (Главный модуль)

```python
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
    # ... (методы _check_events, _save_game, _load_game, _update_bullets и др.)

```

---

## 4. Описание проделанной работы

### 4.1. Звуковая подсистема

Использован модуль `pygame.mixer`. Ресурсы загружаются из директории `resources/` с помощью `os.path.join`. Звуки выстрела (`shoot.wav`), взрыва (`explosion.wav`) и проигрыша (`game_over.wav`) интегрированы в соответствующие игровые события.

### 4.2. Механика уровней и сохранение

Реализована динамическая сложность: при каждом очищении экрана скорость врагов увеличивается через метод `settings.increase_speed()`. Система сохранения использует модуль `pickle`, сериализуя данные в файл `savefile.pkl`, что позволяет игроку продолжить прогресс после нажатия клавиш 'S' (сохранить) или 'L' (загрузить).

### 4.3. Интерактивные объекты

Создан класс `Bonus`, объекты которого спавнятся с вероятностью 10% при уничтожении врага. Механика подразумевает движение бонуса сверху вниз, что создает элемент риска и поощряет активную игру.

### 4.4. Интерфейс проигрыша и рестарт

Реализован экран «Game Over» и кнопка рестарта. При поражении игровой цикл останавливается, отрисовывается надпись и кнопка, нажатие на которую через `pygame.MOUSEBUTTONDOWN` сбрасывает состояние статистики и объектов.

---

## 5. Сборка приложения

Для кроссплатформенной упаковки игры применен `PyInstaller`.
Команда для сборки:

```bash
pyinstaller --onefile --add-data "resources;resources" alien_invasion.py

```

Использование `--add-data` гарантирует, что папка ресурсов будет включена в итоговый исполняемый файл, обеспечивая портативность игры.

## 6. Выводы

В ходе выполнения практической работы №2 были изучены и применены методы работы с файловой системой, звуком, сериализацией данных и событийным программированием. Проект стал полноценным игровым приложением, готовым к распространению. Архитектура сохраняет гибкость для дальнейшего развития (например, добавления сетевого режима или новых типов бонусов).
