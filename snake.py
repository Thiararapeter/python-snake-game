import pygame
import random
import time

# Initializing pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Coders Home")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)  # Reduced font size

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, gameWindow):
        pygame.draw.rect(gameWindow, red, [self.x, self.y, self.width, self.height])

# Function to display text on the screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Function to draw the snake on the screen
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Function to check collision with obstacles
def check_collision_with_obstacles(snake_x, snake_y, snake_size, obstacles):
    for obstacle in obstacles:
        if (
            snake_x < obstacle.x + obstacle.width
            and snake_x + snake_size > obstacle.x
            and snake_y < obstacle.y + obstacle.height
            and snake_y + snake_size > obstacle.y
        ):
            return True
    return False

# Function to generate obstacles
def generate_obstacles():
    obstacles = []
    for _ in range(2):  # Adjust the number of obstacles as needed
        obstacle = Obstacle(random.randint(0, screen_width - 20), random.randint(50, screen_height - 20), 20, 20)
        obstacles.append(obstacle)
    return obstacles

# Main game loop
def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, screen_width - 30)
    food_y = random.randint(60, screen_height - 30)
    score = 0
    init_velocity = 4
    snake_size = 20
    fps = 60
    lives = 3
    obstacles = []

    highest_score = 0
    start_time = time.time()
    time_limit = 30

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and game_over:
                    snake_x = 45
                    snake_y = 55
                    velocity_x = 0
                    velocity_y = 0
                    snk_list = []
                    snk_length = 1
                    food_x = random.randint(20, screen_width - 30)
                    food_y = random.randint(60, screen_height - 30)
                    score = 0
                    lives = 3
                    start_time = time.time()
                    game_over = False
                    obstacles = []

                if not game_over:
                    if event.key == pygame.K_RIGHT and velocity_x != -init_velocity:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT and velocity_x != init_velocity:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP and velocity_y != init_velocity:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN and velocity_y != -init_velocity:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_p:
                        pause_game()

        if not game_over:
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 1
                food_x = random.randint(20, screen_width - 30)
                food_y = random.randint(60, screen_height - 30)
                snk_length += 5
                start_time = time.time()

                # Generate obstacles at random positions
                obstacles.extend(generate_obstacles())

            elapsed_time = time_limit - (time.time() - start_time)
            if elapsed_time <= 0:
                game_over = True
                lives -= 1
                if lives == 0:
                    exit_game = True

            if score > highest_score:
                highest_score = score

            # Check for collision with obstacles
            if check_collision_with_obstacles(snake_x, snake_y, snake_size, obstacles):
                lives -= 1
                obstacles = []  # Reset obstacles after a collision
                if lives == 0:
                    game_over = True

        gameWindow.fill(white)

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw(gameWindow)

        text_screen(
            f"Score: {score * 10}        Lives Remaining: {lives}        Time to eat remaining : {max(0, int(elapsed_time))}s       High Score To Beat: {highest_score * 10}",
            black,
            5,
            5,
        )

        pygame.draw.rect(gameWindow, green, [food_x, food_y, snake_size, snake_size])
        pygame.draw.line(gameWindow, red, (0, 40), (900, 40), 5)

        head = []
        head.append(snake_x)
        head.append(snake_y)
        snk_list.append(head)

        if len(snk_list) > snk_length:
            del snk_list[0]

        if head in snk_list[:-1]:
            game_over = True

        if snake_x < 0 or snake_x > screen_width - 20 or snake_y < 50 or snake_y > screen_height - 20:
            game_over = True

        plot_snake(gameWindow, black, snk_list, snake_size)

        if game_over:
            text_screen("Trial Limit Exceeded! Try Again! Press Enter To Continue", red, 100, 250)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

        text_screen("Paused. Press P to Continue", red, 250, 250)
        pygame.display.update()
        clock.tick(15)

# Run the game
gameloop()
