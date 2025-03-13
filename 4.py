import random
width = 70
height = 20
title = """
######################################################################
#           ____    ____       _       ________  ________            #
#          |_   \  /   _|     / \     |  __   _||_   __  |           #
#            |   \/   |      / _ \    |_/  / /    | |_ \_|           #
#            | |\  /| |     / ___ \      .'.' _   |  _| _            #
#           _| |_\/_| |_  _/ /   \ \_  _/ /__/ | _| |__/ |           #
#          |_____||_____||____| |____||________||________|           #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                    - press any key to start -                      #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
######################################################################
"""
print(title)
input()

import random


def generate_maze(width=70, height=20):
    # Adjust dimensions to be odd for proper maze carving.
    if width % 2 == 0:
        width -= 1
    if height % 2 == 0:
        height -= 1

    # Create a grid filled with walls.
    maze = [['#'] * width for _ in range(height)]

    # Start at position (1, 1); this is our first path cell.
    start_x, start_y = 1, 1
    maze[start_y][start_x] = ' '

    # Define possible movement directions (skipping one cell each time).
    directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]

    # Use a stack for DFS (depth-first search).
    stack = [(start_x, start_y)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < width - 1 and 0 < ny < height - 1:
                if maze[ny][nx] == '#':  # Unvisited cell.
                    neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[y + dy // 2][x + dx // 2] = ' '  # Remove wall between.
            maze[ny][nx] = ' '
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze


def print_maze(maze):
    # Using Unicode block for walls and ANSI escape codes for color.
    # ANSI code "\033[1;37m" sets bold white; "\033[0m" resets formatting.
    for row in maze:
        line = ""
        for cell in row:
            if cell == '#':
                # Print walls as a bold white full block.
                line += "\033[1;37m█\033[0m"
            else:
                # Print paths as empty space.
                line += " "
        print(line)


if __name__ == '__main__':
    maze = generate_maze(70, 20)
    print_maze(maze)
