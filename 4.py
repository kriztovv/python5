import random
screenwidth = int(70/3)
screenheight = 20

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


def generate_maze(width, height):
    # Create a maze matrix filled with path characters "□"
    maze = [["□" for _ in range(width)] for _ in range(height)]
    maze2 = [["□" for _ in range(width)] for _ in range(height)]
    maze3 = [["□" for _ in range(width)] for _ in range(height)]

    # Create the initial pattern with walls and paths.
    # Walls are drawn with "■" and paths with "□"
    for y in range(height):
        for x in range(width):
            if y % 3 == 0:
                if x % 3 == 0:
                    maze[y][x] = " ■ "  # Wall
                else:
                    maze[y][x] = " □ "  # Path
            else:
                maze[y][x] = " □ "  # Path

    for y in range(height):
        for x in range(width):
            if y % 3 == 0:
                if x % 3 == 0:
                    maze2[y][x] = " ■ "  # Wall
                else:
                    maze2[y][x] = " □ "  # Path
            else:
                maze2[y][x] = " □ "  # Path

    # Attempt to add some extra random walls
    for y in range(height):
        for x in range(width):  # Use 'width' instead of 'width * 3'
            if maze2[y][x] == " ■ ":
                rand = random.randint(1, 4)
                if rand == 1 and x + 1 < width:
                    maze3[y][x + 1] = " ■ "
                    maze[y][x + 1] = " ■ "
                elif rand == 2 and x - 1 >= 0:
                    maze3[y][x - 1] = " ■ "
                    maze[y][x - 1] = " ■ "
                elif rand == 3 and y + 1 < height:
                    maze3[y + 1][x] = " ■ "
                    maze[y + 1][x] = " ■ "
                elif rand == 4 and y - 1 >= 0:
                    maze3[y - 1][x] = " ■ "
                    maze[y - 1][x] = " ■ "

    for y in range(height):
        for x in range(width):  # Use 'width' instead of 'width * 3'
            if maze3[y][x] == " ■ ":
                rand = random.randint(1, 4)
                if rand == 1 and x + 1 < width:
                    maze[y][x + 1] = " ■ "
                elif rand == 2 and x - 1 >= 0:
                    maze[y][x - 1] = " ■ "
                elif rand == 3 and y + 1 < height:
                    maze[y + 1][x] = " ■ "
                elif rand == 4 and y - 1 >= 0:
                    maze[y - 1][x] = " ■ "
    return maze

def print_maze(matrix):
    for row in matrix:
        print(''.join(row))  # Print each row as a single string

if __name__ == '__main__':
    maze = generate_maze(screenwidth, screenheight)
    print_maze(maze)
