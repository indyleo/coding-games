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

# Game variables
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
PADDLE_SPEED = 8

# Define objects
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
player1_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Set up clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move player paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1_paddle.top > 0:
        player1_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and player1_paddle.bottom < HEIGHT:
        player1_paddle.y += PADDLE_SPEED

    if keys[pygame.K_UP] and player2_paddle.top > 0:
        player2_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and  player2_paddle.bottom < HEIGHT:
        player2_paddle.y += PADDLE_SPEED

    if keys[pygame.K_q]:
        pygame.quit()
        sys.exit()

    # Move the ball
    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision with walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1

    # Ball collision with paddles
    if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
        BALL_SPEED_X *= -1

    # Ball out of bounds - Player Missed
    if ball.left <= 0:
        ball.center = (WIDTH//2, HEIGHT//2)
        BALL_SPEED_X *= random.choice((1, -1))

    # Ball out of bounds - Opponent Missed
    if ball.right >= WIDTH:
        ball.center = (WIDTH//2, HEIGHT//2)
        BALL_SPEED_X *= random.choice((1, -1))

    # Draw everything
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, player1_paddle)
    pygame.draw.rect(WIN, WHITE, player2_paddle)
    pygame.draw.ellipse(WIN, WHITE, ball)
    pygame.draw.aaline(WIN, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
