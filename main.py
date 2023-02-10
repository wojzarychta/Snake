import pygame
import random


class Board:
    spacing = 20

    def __init__(self, width=400, height=400):
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Snake')
        self.width = width
        self.height = height
        pygame.display.update()

    def __del__(self):
        pygame.quit()


class Apple:
    RED = (255, 0, 0)

    def __init__(self):
        self.x = None
        self.y = None
        self.locate()

    def draw(self):
        pygame.draw.circle(board.display, self.RED, (self.x, self.y), Board.spacing//2)

    def locate(self):
        """
        locates new apple randomly on the board
        :return: none
        """
        self.x = random.randrange(Board.spacing//2, board.width - Board.spacing//2, Board.spacing)
        self.y = random.randrange(Board.spacing // 2, board.height - Board.spacing // 2, Board.spacing)


class Snake:
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3
    DARK_GREEN = (0x28, 0x59, 0x2b)
    LIGHT_GREEN = (0x25, 0xe6, 0x31)

    def __init__(self):
        self.snake = []  # list containing tuples with coordinates of snake's body parts
        self.direction = self.RIGHT  # direction of snake's movement
        x = board.width//(2*Board.spacing)*Board.spacing + Board.spacing//2
        y = board.height // (2 * Board.spacing) * Board.spacing + Board.spacing // 2
        self.snake.append((x, y))  # snake's head

    def check_collision(self, head: tuple[int, int]):
        if head[0] < 0 or head[0] > board.width or head[1] < 0 or head[1] > board.height:  # check if head is beyond map
            return True
        for i in self.snake:  # check if head collides with any of snake's body parts
            if i[0] == head[0] and i[1] == head[1]:
                return True
        return False

    @staticmethod
    def check_apple(head: tuple[int, int], apple: Apple):
        return head[0] == apple.x and head[1] == apple.y

    def move(self, apple):
        # move snake's head and store it in 'head'
        if self.direction == self.UP:
            head = (self.snake[0][0], self.snake[0][1] - Board.spacing)
        elif self.direction == self.DOWN:
            head = (self.snake[0][0], self.snake[0][1] + Board.spacing)
        elif self.direction == self.RIGHT:
            head = (self.snake[0][0] + Board.spacing, self.snake[0][1])
        else:
            head = (self.snake[0][0] - Board.spacing, self.snake[0][1])

        if self.check_collision(head):  # game over
            return False

        if self.check_apple(head, apple):
            self.extend(head)  # extend snake by one
            apple.locate()  # generate new apple
        else:
            self.shift(head)  # move whole snake
        return True

    def extend(self, head: tuple[int, int]):
        self.snake.insert(0, head)

    def shift(self, head: tuple[int, int]):
        # (i)th element of snake will change position to position of (i+1)th element
        for i in range(1, len(self.snake)):
            self.snake[-i] = self.snake[-i - 1]
        self.snake[0] = head

    def change_direction(self, key: int):
        if self.direction != self.UP and self.direction != self.DOWN:
            if key == pygame.K_w:
                self.direction = self.UP
            elif key == pygame.K_s:
                self.direction = self.DOWN
        else:
            if key == pygame.K_d:
                self.direction = self.RIGHT
            elif key == pygame.K_a:
                self.direction = self.LEFT

    def draw(self):
        for i in range(len(self.snake)):
            if i == 0:  # snake's head
                color = self.DARK_GREEN
            else:
                color = self.LIGHT_GREEN
            pygame.draw.circle(board.display, color, self.snake[i], Board.spacing // 2)


def game_loop():
    apple = Apple()
    snake = Snake()
    timer = pygame.time.Clock()
    timer_interval = 11
    black = (0, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)
                break  # sometimes KEYDOWN was invoked twice in one loop which caused faulty detection of collision
        if not snake.move(apple):  # game over
            return
        else:
            board.display.fill(black)
            snake.draw()
            apple.draw()
        pygame.display.update()
        timer.tick(timer_interval)


def game_over_message():
    font = pygame.font.SysFont("comicsansms", 35)
    message = font.render('GAME OVER', True, (255, 255, 255))
    board.display.blit(message, (100, 150))
    font = pygame.font.SysFont("comicsansms", 20)
    message = font.render('press any key to play again', True, (255, 255, 255))
    board.display.blit(message, (75, 200))
    pygame.display.update()


def play_again_loop():
    while True:
        game_over_message()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                return


if __name__ == '__main__':
    board = Board()
    while True:
        game_loop()
        play_again_loop()
