import pygame
import random
import math

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        size=(10,120)
        self.image = pygame.Surface(size)
        self.image.fill((240, 44, 122))
        self.rect = self.image.get_rect(midbottom=(10, 500))
        self.speed = 5

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y = max(120, self.rect.y-self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(670, self.rect.y+self.speed)

class Opponent(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        size=(10,120)
        self.image = pygame.Surface(size)
        self.image.fill((40, 244, 122))
        self.rect = self.image.get_rect(midbottom=(790, 500))
        self.speed = 5
        self.direction = 0

    def move(self, ball):
        preferred_direction = 0
        if ball.rect.centery < self.rect.centery-20:
            preferred_direction = -1
        if ball.rect.centery > self.rect.centery+20:
            preferred_direction = 1

        if random.randint(0, 100) < 8:
            self.direction = preferred_direction
        if self.direction == -1:
            self.rect.y = max(120, self.rect.y-self.speed)
        if self.direction == 1:
            self.rect.y = min(670, self.rect.y+self.speed)


class Ball(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        size=(20,20)
        self.image = pygame.Surface(size)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=(400, 400))
        self.speed = 5
        self.direction = [1/math.sqrt(2), 1/math.sqrt(2)]
        self.position = [400, 400]

    def move(self, player, opponent):
        self.position[0] += self.speed * self.direction[0]
        self.position[1] += self.speed * self.direction[1]

        self.rect.x = int(self.position[0])
        self.rect.y = int(self.position[1])

        if self.rect.top <= 100 or self.rect.bottom >= 800:
            self.direction[1] *= -1
        if self.rect.left <= 15:
            if pygame.sprite.collide_rect(self, player):
                self.direction[0] *= -1
            else:
                return 'opponent'
        if self.rect.right >= 785:
            if pygame.sprite.collide_rect(self, opponent):
                self.direction[0] *= -1
            else:
                return 'player'
        return None


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.opponent = Opponent()
        self.opponent_group = pygame.sprite.GroupSingle(self.opponent)
        self.ball = Ball()
        self.ball_group = pygame.sprite.GroupSingle(self.ball)
        self.player_score = 0
        self.opponent_score = 0

    def reset(self, winner):
        self.ball.rect.center = (400, 400)
        self.ball.position = [400, 400]
        if winner == 'player':
            self.player_score += 1
            self.ball.direction = [1/math.sqrt(2), 1/math.sqrt(2)]
        if winner == 'opponent':
            self.opponent_score += 1
            self.ball.direction = [-1/math.sqrt(2), 1/math.sqrt(2)]

    def run(self):
        self.player.get_input()
        self.opponent.move(self.ball)
        winner = self.ball.move(self.player, self.opponent)
        if winner:
            self.reset(winner)
        self.player_group.draw(self.screen)
        self.opponent_group.draw(self.screen)
        self.ball_group.draw(self.screen)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    game = Game(screen)
    clock = pygame.time.Clock()
    fps = 60
    font = pygame.font.Font(None, 74)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (255, 255, 255), (0, 100, 800, 12))

        img = font.render(f'{game.player_score}:{game.opponent_score}', True, (255, 255, 255))
        screen.blit(img, (380, 30))
        game.run()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    quit()