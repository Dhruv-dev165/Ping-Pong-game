import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Pong Game")

# Define paddle and ball properties
paddle_speed = 10
ball_speed_x, ball_speed_y = 5, 5

# Define paddles and ball
left_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Game variables
left_score = 0
right_score = 0
game_time = 60  # Game time in seconds

# Font for displaying text
font = pygame.font.SysFont("Arial", 30)

# Function to display scores and timer
def display_scores():
    left_text = font.render(f"Player 1: {left_score}", True, WHITE)
    right_text = font.render(f"Player 2: {right_score}", True, WHITE)
    timer_text = font.render(f"Time: {game_time}", True, WHITE)

    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4 - right_text.get_width(), 20))
    screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, 20))

# Function to move the ball
def move_ball():
    global ball_speed_x, ball_speed_y, left_score, right_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y

    # Ball out of bounds (left or right side)
    if ball.left <= 0:
        right_score += 1
        reset_ball()

    if ball.right >= WIDTH:
        left_score += 1
        reset_ball()

    # Ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x = -ball_speed_x

# Reset ball position after scoring
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = -ball_speed_x
    ball_speed_y = 5

# Function to move paddles
def move_paddles():
    keys = pygame.key.get_pressed()

    # Move left paddle (W/S for up/down)
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= paddle_speed
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += paddle_speed

    # Move right paddle (Up/Down arrows)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed

# Function to check if time is over and display winner
def check_time():
    global left_score, right_score, game_time
    if game_time <= 0:
        if left_score > right_score:
            winner_text = font.render("Player 1 Wins!", True, WHITE)
        elif right_score > left_score:
            winner_text = font.render("Player 2 Wins!", True, WHITE)
        else:
            winner_text = font.render("It's a Tie!", True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        time.sleep(3)  # Wait for 3 seconds before closing the game
        pygame.quit()
        sys.exit()

# Game loop
clock = pygame.time.Clock()
last_time = time.time()

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update game time every second
    current_time = time.time()
    if current_time - last_time >= 1:
        game_time -= 1
        last_time = current_time

    # Move paddles and ball
    move_paddles()
    move_ball()

    # Fill the screen with background color
    screen.fill(BACKGROUND_COLOR)

    # Draw paddles, ball, scores, and timer
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    display_scores()

    # Check if time is over and determine winner
    check_time()

    # Update the display
    pygame.display.update()

    # Control the frame rate
    clock.tick(FPS)
