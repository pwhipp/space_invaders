import random
import pygame
from actors import Player, Enemy, Bullet
import settings

player_move_step = {pygame.K_LEFT: -0.5, pygame.K_RIGHT: 0.5}


class Game:
    def __init__(self, num_enemies=6):
        pygame.init()
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.num_enemies = num_enemies
        self.enemy_dx = 0.6
        self.enemy_x_offset = 64
        self.enemies = []

        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        self.screen_width, self.screen_height = self.screen.get_size()
        pygame.display.set_caption("TD PCG")

        self.background = pygame.image.load('assets/background.jpg')

        self.player = Player(self)
        self.bullet = Bullet(self)
        self.actors = [self.player, self.bullet]
        self.reset_enemies()

        self.score = 0

    def reset_enemies(self):
        first_x = 200
        y = 50

        self.enemies = [Enemy(self,
                              x=first_x + (i * self.enemy_x_offset),
                              y=y,
                              dx=self.enemy_dx)
                        for i in range(self.num_enemies)]
        self.actors = [*self.enemies, *self.actors]
        self.enemy_dx *= 1.1  # 10% faster each reset

    def enemy_destroyed(self, enemy):
        self.score += 1
        self.actors.remove(enemy)
        self.enemies.remove(enemy)
        if not self.enemies:
            self.reset_enemies()

    def run(self):
        keys_down = set()
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            keys_down, running = process_events(keys_down, running)

            if pygame.K_SPACE in keys_down:
                self.bullet.fire(self.player)

            self.player.move(sum([player_move_step[k] for k in keys_down if k in player_move_step]), 0)
            game_over = any(enemy.update() for enemy in self.enemies)
            self.bullet.update()

            for actor in self.actors:
                actor()

            if game_over:
                print(f'game over: You scored {self.score}')
                running = False

            self.show_score()
            pygame.display.update()

    def show_score(self):
        score = self.font.render(f'{self.score}', True, (255, 255, 255))
        self.screen.blit(score, (10, 10))


def process_events(keys_down, running) -> tuple:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            keys_down.add(event.key)
        if event.type == pygame.KEYUP:
            keys_down.remove(event.key)

    return keys_down, running


if __name__ == "__main__":
    Game().run()
