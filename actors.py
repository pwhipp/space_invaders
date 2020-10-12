import random
import pygame


class Actor:
    image_file = None

    def __init__(self, game):
        self.image = pygame.image.load(self.image_file)
        self.game = game
        self.screen_width, self.screen_height = self.screen.get_size()
        self.width, self.height = self.image.get_size()
        self.position = (0, 0)

    def __call__(self):
        x, y = self.position
        self.screen.blit(self.image, (int(round(x)), int(round(y))))

    def move(self, dx, dy):
        x, y = self.position
        self.position = (min(self.screen_width - self.width, max(0, x + dx)),
                         min(self.screen_height, max(0, y + dy)))

    @property
    def screen(self):
        return self.game.screen

    @property
    def rect(self):
        x, y = self.position
        return pygame.Rect(x, y, self.width, self.height)


class Player(Actor):
    image_file = 'assets/player.png'

    def __init__(self, screen):
        super().__init__(screen)
        self.position = (int(round(self.screen_width/2 - self.width/2)),
                         self.screen_height - (self.height + 10))


class Enemy(Actor):
    image_file = 'assets/alien.png'

    def __init__(self, game, x, y, dx=0.6, dy=50, direction=+1):
        super().__init__(game)
        self.dx = dx
        self.dy = dy
        self.direction = direction
        self.position = (x, y)

    def update(self) -> bool:  # True if game is over
        x, y = self.position
        x = x + (self.direction * self.dx)
        if x < 0:
            self.direction *= -1
            x = 0
            y = y + self.dy
        if x > (self.screen_width - self.width):
            x = self.screen_width - self.width
            self.direction *= -1
            y = y + self.dy
        if y >= (self.screen_height - self.height):
            return True
        self.position = (x, y)
        return False

    # noinspection PyUnusedLocal
    def hit_by(self, actor):
        self.game.enemy_destroyed(self)


class Bullet(Actor):
    image_file = 'assets/bullet.png'

    def __init__(self, game, dy=-1.5):
        super().__init__(game)
        self.dy = dy
        self.state = 'ready'

    def __call__(self):
        if self.state == 'fired':
            super().__call__()

    def fire(self, player):
        if self.state == 'ready':
            self.state = 'fired'
            player_x, player_y = player.position
            self.position = player_x + 27, player_y - 10

    def update(self):
        if self.state == 'fired':
            x, y = self.position
            self.position = x, y + self.dy

            for enemy in self.game.enemies:
                if self.is_hitting(enemy):
                    enemy.hit_by(self)
                    self.state = 'ready'

            if y < 0:
                self.state = 'ready'

    def is_hitting(self, actor):
        if self.state == 'fired':
            return self.rect.colliderect(actor.rect)
        return False
