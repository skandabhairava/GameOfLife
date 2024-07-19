#!/usr/bin/env python3

import pygame
import sys
from copy import deepcopy

# initialize it
pygame.init()

CELLS = 70
BLANK_BOARD = [[False for _ in range(CELLS)] for _ in range(CELLS)]
BOARD = deepcopy(BLANK_BOARD)
BOARD_backup = deepcopy(BLANK_BOARD)

# 1 2 3
# 4 x 5
# 6 7 8
def check_neighbor(x, y, board, neighbor_id):
    if neighbor_id in (1, 2, 3) and y <= 0:
        return False
    if neighbor_id in (6, 7, 8) and y >= len(board) - 1:
        return False
    if neighbor_id in (1, 4, 6) and x <= 0:
        return False
    if neighbor_id in (3, 5, 8) and x >= len(board[0]) - 1:
        return False
    
    if neighbor_id == 1:
        return board[y-1][x-1]
    elif neighbor_id == 2:
        return board[y-1][x]
    elif neighbor_id == 3:
        return board[y-1][x+1]
    elif neighbor_id == 4:
        return board[y][x-1]
    elif neighbor_id == 5:
        return board[y][x+1]
    elif neighbor_id == 6:
        return board[y+1][x-1]
    elif neighbor_id == 7:
        return board[y+1][x]
    elif neighbor_id == 8:
        return board[y+1][x+1]

def update(board: list[list[bool]]):

    global BOARD_backup
    BOARD_backup = deepcopy(board)

    for row_num, rows in enumerate(BOARD):
        for col_num, item in enumerate(rows):
            neighbors = [check_neighbor(col_num, row_num, BOARD, neighbor_id) for neighbor_id in range(1, 9)]
            neighbors_count = neighbors.count(True)

            #rules
            # 1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
            # 2. Any live cell with two or three live neighbors lives on to the next generation.
            # 3. Any live cell with more than three live neighbors dies, as if by overpopulation.
            # 4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.

            if item == True:

                # 1.
                if neighbors_count < 2:
                    BOARD_backup[row_num][col_num] = False
                    ...

                # 3.
                if neighbors_count > 3:
                    BOARD_backup[row_num][col_num] = False

            if item == False and neighbors_count == 3:
                BOARD_backup[row_num][col_num] = True


def flip():
    global BOARD
    BOARD = deepcopy(BOARD_backup)

#uservevent
update_event = pygame.USEREVENT + 1

#states
GLOBAL_PAUSE = True
MOUSE_HOLD = False
LAST_HOLD = (-1, -1)

# configurations
frames_per_second = 30
window_height_width = CELLS * 10

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# creating window
display = pygame.display.set_mode((window_height_width, window_height_width))

# creating our frame regulator
clock = pygame.time.Clock()

pygame.display.set_caption("Conway's Game of Life (Paused)")
pygame.time.set_timer(update_event, 100)

# forever loop
while True:

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == update_event and not GLOBAL_PAUSE:
            update(BOARD)
            flip()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not GLOBAL_PAUSE:
            GLOBAL_PAUSE = True
            pygame.display.set_caption("Conway's Game of Life (Paused)")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and GLOBAL_PAUSE:
            GLOBAL_PAUSE = False
            MOUSE_HOLD = False
            LAST_HOLD = (-1, -1)
            pygame.display.set_caption("Conway's Game of Life (Playing)")

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and GLOBAL_PAUSE:
            BOARD = deepcopy(BLANK_BOARD)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and GLOBAL_PAUSE:
            MOUSE_HOLD = True
            pos = event.pos[0]//10, event.pos[1]//10

            if (pos[0] < 0 or pos[0] >= CELLS) or (pos[1] < 0 or pos[1] >= CELLS): continue

            BOARD[pos[1]][pos[0]] = not BOARD[pos[1]][pos[0]]
            LAST_HOLD = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            MOUSE_HOLD = False
            LAST_HOLD = (-1, -1)

        elif MOUSE_HOLD and event.type == pygame.MOUSEMOTION and GLOBAL_PAUSE:
            pos = event.pos[0]//10, event.pos[1]//10

            if (pos[0] < 0 or pos[0] >= CELLS) or (pos[1] < 0 or pos[1] >= CELLS): continue
            if LAST_HOLD == pos:
                continue

            # i am not going to check if in bounds, as the game creates both board and screen of suitable size.
            BOARD[pos[1]][pos[0]] = not BOARD[pos[1]][pos[0]]
            LAST_HOLD = pos
            

    # frame Drawing
    display.fill(BLACK)    

    for row_num, rows in enumerate(BOARD):
        for col_num, item in enumerate(rows):
            if item == True:
                pygame.draw.rect(display, WHITE, pygame.Rect(col_num * 10, row_num * 10, 10, 10))

    # frame clock ticking
    pygame.display.flip()

    clock.tick(frames_per_second)
