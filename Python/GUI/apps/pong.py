#!/bin/env python3
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)

# Game variables
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
PADDLE_SPEED = 8
SQUARE_SIZE = 50

# Define objects
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
player1_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Load sound files
paddle_hit_sound = pygame.mixer.Sound("./Sounds/paddle_hit.wav")
window_edge_sound = pygame.mixer.Sound("./Sounds/border_hit.wav")

# The Background
def draw_grid(surface):
    for x in range(0, WIDTH, SQUARE_SIZE * 2):
        for y in range(0, HEIGHT, SQUARE_SIZE * 2):
            pygame.draw.rect(surface, GRAY, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(surface, WHITE, (x + SQUARE_SIZE, y, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(surface, WHITE, (x, y + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(surface, GRAY, (x + SQUARE_SIZE, y + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# The Score
def draw_score(surface, player1_score, player2_score):
    font = pygame.font.SysFont(None, 36)
    player1_text = font.render(f"Player 1: {player1_score}", True, BLACK)
    player2_text = font.render(f"Player 2: {player2_score}", True, BLACK)
    
    # Get the width of the rendered text surfaces
    player1_width = player1_text.get_width()
    player2_width = player2_text.get_width()
    
    # Calculate the x-coordinate for player 1's text
    player1_x = (WIDTH // 2 - player1_width) // 2
    # Calculate the x-coordinate for player 2's text
    player2_x = WIDTH // 2 + (WIDTH // 2 - player2_width) // 2
    
    # Blit the score text surfaces onto the screen
    surface.blit(player1_text, (player1_x, 20))
    surface.blit(player2_text, (player2_x, 20))

# Controls
def display_controls():
    controls_text = [
        "Controls:",
        "Player 1:",
        "   Move Up: W",
        "   Move Down: S",
        "Player 2:",
        "   Move Up: Up Arrow",
        "   Move Down: Down Arrow",
        "Back to Menu: Backspace"
    ]

    running = True
    while running:
        WIN.fill(WHITE)
        font = pygame.font.SysFont(None, 36)
        y = 100
        for text in controls_text:
            text_surface = font.render(text, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH//2, y))
            WIN.blit(text_surface, text_rect)
            y += 40
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return  # Return to main menu
# Menu function
def display_menu():
    menu_font = pygame.font.SysFont(None, 50)
    menu_title = menu_font.render("Pong Game", True, BLACK)
    menu_sub = menu_font.render("Press ENTER to play", True, BLACK)
    menu_sub_quit = menu_font.render("Press Q to quit", True, BLACK)
    menu_sub_controls = menu_font.render("Press C to controls", True, BLACK)
        
    # Draw the grid background
    WIN.fill(WHITE)
    draw_grid(WIN)

    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False  # Exit menu on Enter key
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    display_controls()
                    

        WIN.blit(menu_title, (WIDTH//2 - menu_title.get_width()//2, HEIGHT//2 - menu_title.get_height()))
        WIN.blit(menu_sub, (WIDTH//2 - menu_sub.get_width()//2, HEIGHT//2))
        WIN.blit(menu_sub_quit, (WIDTH//2 - menu_sub_quit.get_width()//2, HEIGHT//2 + menu_sub.get_height()))
        WIN.blit(menu_sub_controls, (WIDTH//2 - menu_sub_controls.get_width()//2, HEIGHT//2 + 2*menu_sub.get_height()))
        pygame.display.update()

# Game loop
def game_loop(BALL_SPEED_X, BALL_SPEED_Y):
    # Initialize player score
    player1_score = 0
    player2_score = 0
    
    # Define player paddles
    player1_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Set up clock
    clock = pygame.time.Clock()

    # Flag to determine if in menu or game
    in_menu = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and not in_menu:
                    in_menu = display_menu()  # Update in_menu based on menu status
                
        if in_menu:  # Skip the game loop if in_menu is True
            continue        # Move player paddle
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_paddle.top > 0:
            player1_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
            player1_paddle.y += PADDLE_SPEED

        if keys[pygame.K_UP] and player2_paddle.top > 0:
            player2_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and  player2_paddle.bottom < HEIGHT:
            player2_paddle.y += PADDLE_SPEED

        # Move the ball
        ball.x += BALL_SPEED_X
        ball.y += BALL_SPEED_Y

        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED_Y *= -1
            window_edge_sound.play()  # Play window edge sound

        # Ball collision with paddles
        if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
            BALL_SPEED_X *= -1
            paddle_hit_sound.play()  # Play paddle hit sound

        # Ball out of bounds - Player Missed
        if ball.left <= 0:
            ball.center = (WIDTH//2, HEIGHT//2)
            BALL_SPEED_X *= random.choice((1, -1))
            player2_score += 1
            player1_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            window_edge_sound.play()

        # Ball out of bounds - Opponent Missed
        if ball.right >= WIDTH:
            ball.center = (WIDTH//2, HEIGHT//2)
            BALL_SPEED_X *= random.choice((1, -1))
            player1_score += 1
            player1_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
            window_edge_sound.play()

        # Draw everything
        WIN.fill(WHITE)
        draw_grid(WIN)
        draw_score(WIN, player1_score, player2_score)
        pygame.draw.rect(WIN, BLACK, player1_paddle)
        pygame.draw.rect(WIN, BLACK, player2_paddle)
        pygame.draw.ellipse(WIN, BLACK, ball)
        pygame.draw.aaline(WIN, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Run the menu function before entering the game loop
in_menu = display_menu()
game_loop(BALL_SPEED_X, BALL_SPEED_Y)

# Quit Pygame
pygame.quit()
