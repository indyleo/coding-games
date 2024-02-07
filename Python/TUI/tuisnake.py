#!/bin/env python3
# TUI snake game
import random
import curses

def draw_menu(stdscr):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    title = "Snake Game - Press SPACE to start, Q to quit"
    stdscr.addstr(sh // 2, sw // 2 - len(title) // 2, title, curses.A_BOLD)
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord(' '):
        return True
    elif key == ord('q') or key == ord('Q'):
        return False
    return draw_menu(stdscr)

def draw_game_over(stdscr):
    stdscr.clear()
    sh, sw = stdscr.getmaxyx()
    game_over_text = "Game Over - Press ENTER to play again, Q to quit"
    stdscr.addstr(sh // 2, sw // 2 - len(game_over_text) // 2, game_over_text, curses.A_BOLD)
    stdscr.refresh()
    key = stdscr.getch()
    if key == curses.KEY_ENTER or key in [10, 13]:
        return True
    elif key == ord('q') or key == ord('Q'):
        return False
    return draw_game_over(stdscr)

def main(stdscr):
    curses.curs_set(0)
    stdscr.timeout(100)  # Set a timeout for getch() to make the game smoother

    while True:
        if not draw_menu(stdscr):
            break

        # Initialize the screen
        sh, sw = stdscr.getmaxyx()
        w = curses.newwin(sh, sw, 0, 0)
        w.keypad(1)
        w.timeout(100)

        # Initial snake position and direction
        snake_start_length = 3
        snake = [(sh // 2, sw // 2 - i) for i in range(snake_start_length)]
        snake_direction = 0  # 0: up, 1: right, 2: down, 3: left

        # Initial food position
        food = (random.randint(1, sh - 2), random.randint(1, sw - 2))

        while True:
            # Get user input
            key = w.getch()

            # Handle user input to change snake direction
            if key == curses.KEY_UP and snake_direction != 2:
                snake_direction = 0
            elif key == curses.KEY_RIGHT and snake_direction != 3:
                snake_direction = 1
            elif key == curses.KEY_DOWN and snake_direction != 0:
                snake_direction = 2
            elif key == curses.KEY_LEFT and snake_direction != 1:
                snake_direction = 3

            # Move the snake
            head = snake[0]
            if snake_direction == 0:
                new_head = (head[0] - 1, head[1])
            elif snake_direction == 1:
                new_head = (head[0], head[1] + 1)
            elif snake_direction == 2:
                new_head = (head[0] + 1, head[1])
            elif snake_direction == 3:
                new_head = (head[0], head[1] - 1)

            snake.insert(0, new_head)

            # Check for collisions
            if (
                new_head[0] in [0, sh - 1]
                or new_head[1] in [0, sw - 1]
                or new_head in snake[1:]
            ):
                break

            # Check for food
            if new_head == food:
                food = (random.randint(1, sh - 2), random.randint(1, sw - 2))
            else:
                snake.pop()

            # Draw everything
            w.clear()
            w.border(0)
            w.addch(food[0], food[1], curses.ACS_PI)
            for s in snake:
                w.addch(s[0], s[1], curses.ACS_CKBOARD)

            w.refresh()

        if not draw_game_over(stdscr):
            break

curses.wrapper(main)


