import pygame
import sys

# constants for the game
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 7

    def move(self, up_key, down_key, keys):
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down_key] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self, direction):
        # centers the ball after a score
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 5 * direction
        self.speed_y = 5

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()

        self.paddle1 = Paddle(30, HEIGHT // 2 - 50, 15, 100)
        self.paddle2 = Paddle(WIDTH - 45, HEIGHT // 2 - 50, 15, 100)
        self.ball = Ball(WIDTH // 2 - 7, HEIGHT // 2 - 7, 15)

        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 74)

    def handle_collision(self):
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= HEIGHT:
            self.ball.speed_y *= -1

        # Ball collision with paddles
        if self.ball.rect.colliderect(self.paddle1.rect) or self.ball.rect.colliderect(self.paddle2.rect):
            self.ball.speed_x *= -1

        if self.ball.rect.left <= 0:
            self.score2 += 1
            self.ball.reset(direction=1)
        elif self.ball.rect.right >= WIDTH:
            self.score1 += 1
            self.ball.reset(direction=-1)

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.paddle1.move(pygame.K_w, pygame.K_s, keys)
            self.paddle2.move(pygame.K_UP, pygame.K_DOWN, keys)

            self.ball.move()
            self.handle_collision()

            # Drawing everything
            self.screen.fill(BLACK)
            self.paddle1.draw(self.screen)
            self.paddle2.draw(self.screen)
            self.ball.draw(self.screen)

            pygame.draw.aaline(self.screen, WHITE,
                               (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

            score_text = f"{self.score1} : {self.score2}"
            text_surface = self.font.render(score_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, 50))
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
