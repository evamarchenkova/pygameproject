import pygame
import sys
import random
import time


class Game():
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 500

        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(139, 0, 255)

        self.fps = pygame.time.Clock()
        self.score = 0

    def init_and_check_for_errors(self):
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def surface_and_title(self):
        self.game_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('$nake Game')

    def events(self, change_to):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return change_to

    def update_screen(self):
        pygame.display.flip()
        game.fps.tick(15)

    def show_score(self, choice=1):
        s_font = pygame.font.SysFont('arial', 24)
        s_surf = s_font.render(
            'score: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        if choice == 1:
            s_rect.midtop = (80, 10)
        else:
            s_rect.midtop = (245, 250)
        self.game_surface.blit(s_surf, s_rect)

    def game_over(self):
        go_font = pygame.font.SysFont('arial', 72)
        go_surf = go_font.render('good game', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (245, 150)
        self.game_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()
        sys.exit()


class Snake():
    def __init__(self, snake_color):
        self.snake_head_pos = [250, 250]
        self.snake_body = [[250, 250], [240, 250], [230, 250]]
        self.snake_color = snake_color
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self):
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def change_body(
            self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, game_surface, surface_color):
        game_surface.fill(surface_color)
        for pos in self.snake_body:
            pygame.draw.rect(
                game_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def correct_check(self, game_over, screen_width, screen_height):
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()
snake = Snake(game.green)
food = Food(game.brown, game.screen_width, game.screen_height)

game.init_and_check_for_errors()
game.surface_and_title()

while True:
    snake.change_to = game.events(snake.change_to)

    snake.change_direction()
    snake.change_head_position()
    game.score, food.food_pos = snake.change_body(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.game_surface, game.white)

    food.draw_food(game.game_surface)

    snake.correct_check(
        game.game_over, game.screen_width, game.screen_height)
    game.show_score()
    game.update_screen()
