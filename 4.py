import random
import os
import math
import time
import json

def save_game():
    filename = input("Zadejte název souboru pro uložení (bez koncovky .txt): ").strip() + ".txt"
    state = {
        'maze': maze,
        'player_x': player_x,
        'player_y': player_y,
        'target_x': target_x,
        'target_y': target_y,
        'traps': list(traps),
        'enemies': enemies,
        'potions': list(potions),
        'lives': lives,
        'include_traps': include_traps,
        'include_enemies': include_enemies,
        'fog_of_war_enabled': fog_of_war_enabled,
        'screen_width': screen_width,
        'screen_height': screen_height
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(state, f)
    print(f"Hra uložena do souboru {filename}.")

def load_game():
    filename = input("Zadejte název souboru pro načtení (včetně přípony .txt): ").strip()
    with open(filename, "r", encoding="utf-8") as f:
        state = json.load(f)
    print(f"Hra načtena ze souboru {filename}.")
    return state

# ASCII art obrazovky
start_screen = """
######################################################################
#           ____    ____       _       ________  ________            #
#          |_   \\  /   _|     / \\     |  __   _||_   __  |           #
#            |   \\/   |      / _ \\    |_/  / /    | |_ \\_|           #
#            | |\\  /| |     / ___ \\      .'.' _   |  _| _            #
#           _| |_\\/_| |_  _/ /   \\ \\_  _/ /__/ | _| |__/ |           #
#          |_____||_____||____| |____||________||________|           #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                         - stiskněte Enter -                        #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
######################################################################
"""

win_screen = """
######################################################################
#           ____    ____       _       ________  ________            #
#          |_   \\  /   _|     / \\     |  __   _||_   __  |           #
#            |   \\/   |      / _ \\    |_/  / /    | |_ \\_|           #
#            | |\\  /| |     / ___ \\      .'.' _   |  _| _            #
#           _| |_\\/_| |_  _/ /   \\ \\_  _/ /__/ | _| |__/ |           #
#          |_____||_____||____| |____||________||________|           #
#                                                                    #
#                                                                    #
#                           VYHRÁL JSI!                             #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
######################################################################
"""

game_over_screen = """
######################################################################
#           ____    ____       _       ________  ________            #
#          |_   \\  /   _|     / \\     |  __   _||_   __  |           #
#            |   \\/   |      / _ \\    |_/  / /    | |_ \\_|           #
#            | |\\  /| |     / ___ \\      .'.' _   |  _| _            #
#           _| |_\\/_| |_  _/ /   \\ \\_  _/ /__/ | _| |__/ |           #
#          |_____||_____||____| |____||________||________|           #
#                                                                    #
#                                                                    #
#                                                                    #
#                        KONEC HRY!                                #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
#                                                                    #
######################################################################
"""

def generate_maze(width, height):
    maze = [[" □ " for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if y % 3 == 0 and x % 3 == 0:
                maze[y][x] = " ■ "
    for y in range(height):
        for x in range(width):
            if maze[y][x] == " ■ ":
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

def find_open_corner(maze, width, height, corner):
    if corner == "top-left":
        x_range, y_range = range(0, width // 3), range(0, height // 3)
    elif corner == "top-right":
        x_range, y_range = range(width - 1, width - width // 3 - 1, -1), range(0, height // 3)
    elif corner == "bottom-left":
        x_range, y_range = range(0, width // 3), range(height - 1, height - height // 3 - 1, -1)
    else:
        x_range, y_range = range(width - 1, width - width // 3 - 1, -1), range(height - 1, height - height // 3 - 1, -1)
    for y in y_range:
        for x in x_range:
            if maze[y][x] == " □ ":
                return x, y
    return None, None

def find_random_open_tile(maze, width, height, exclude_positions):
    attempts = 0
    while attempts < 1000:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if maze[y][x] == " □ " and (x, y) not in exclude_positions:
            return x, y
        attempts += 1
    return None, None

def fog_modifier(x, y, player_x, player_y):
    d = math.sqrt((x - player_x) ** 2 + (y - player_y) ** 2)
    if d < 4:
        return ""
    else:
        return None

def print_maze_with_entities(maze, player_x, player_y, target_x, target_y, traps, enemies, potions, lives):
    print("Životy:", lives)
    for y in range(len(maze)):
        row_str = ""
        for x in range(len(maze[y])):
            entity = None
            if x == player_x and y == player_y:
                entity = "\033[94m ■ \033[0m"
            elif x == target_x and y == target_y:
                entity = "\033[93m ■ \033[0m"
            elif (x, y) in traps:
                entity = "\033[91m ■ \033[0m"
            elif any(ex == x and ey == y for (ex, ey, _) in enemies):
                entity = "\033[95m ■ \033[0m"
            elif (x, y) in potions:
                entity = "\033[92m P \033[0m"
            if entity is not None:
                row_str += entity
            else:
                if fog_of_war_enabled:
                    modifier = fog_modifier(x, y, player_x, player_y)
                    if modifier is None:
                        row_str += " . "
                    else:
                        row_str += maze[y][x]
                else:
                    row_str += maze[y][x]
        print(row_str)

def move_enemies(enemies, player_x, player_y, maze, width, height):
    new_enemies = []
    for ex, ey, axis in enemies:
        if axis == 'h':
            dx = 0
            if player_x < ex:
                dx = -1
            elif player_x > ex:
                dx = 1
            new_ex, new_ey = ex + dx, ey
            if 0 <= new_ex < width and maze[ey][new_ex] != " ■ ":
                new_enemies.append((new_ex, ey, 'v'))
            else:
                new_enemies.append((ex, ey, 'v'))
        else:
            dy = 0
            if player_y < ey:
                dy = -1
            elif player_y > ey:
                dy = 1
            new_ey, new_ex = ey + dy, ex
            if 0 <= new_ey < height and maze[new_ey][ex] != " ■ ":
                new_enemies.append((ex, new_ey, 'h'))
            else:
                new_enemies.append((ex, ey, 'h'))
    return new_enemies

# --- Výběr nové nebo načtení uložené hry ---
loaded = False
choice = input("Nová hra (n) nebo načíst hru (l)? ").lower().strip()
if choice == 'l':
    state = load_game()
    loaded = True

if not loaded:
    # hlavní menu (nová hra)
    print("Vyberte velikost bludiště:")
    print("1: Malé (11x11)")
    print("2: Střední (17x17)")
    print("3: Velké (21x21)")
    size_choice = input("Zadejte volbu (1/2/3): ").strip()
    if size_choice == "1":
        maze_size = 11
    elif size_choice == "3":
        maze_size = 21
    else:
        maze_size = 17  # volba 2 nebo neplatny vstup

    traps_choice = input("Mají být v bludišti pasti? (a/n): ").lower().strip()
    include_traps = traps_choice == "a"

    enemies_choice = input("Mají být v bludišti nepřátelé? (a/n): ").lower().strip()
    include_enemies = enemies_choice == "a"

    fog_choice = input("Má být zapnuto 'fog of war'? (a/n): ").lower().strip()
    fog_of_war_enabled = fog_choice == "a"

    screen_width = maze_size
    screen_height = maze_size

    lives = 3

    print(start_screen)
    input("Stiskněte Enter...")

    maze = generate_maze(screen_width, screen_height)

    corner_choices = [("top-left", "bottom-right"), ("top-right", "bottom-left")]
    player_corner, target_corner = random.choice(corner_choices)
    player_x, player_y = find_open_corner(maze, screen_width, screen_height, player_corner)
    target_x, target_y = find_open_corner(maze, screen_width, screen_height, target_corner)
    if player_x is None or target_x is None:
        print("Chyba: Nelze najít vhodné počáteční pozice.")
        exit()

    traps = set()
    if include_traps:
        exclude = {(player_x, player_y), (target_x, target_y)}
        for _ in range(5):
            tx, ty = find_random_open_tile(maze, screen_width, screen_height, exclude)
            if tx is None:
                break
            traps.add((tx, ty))
            exclude.add((tx, ty))

    enemies = []
    if include_enemies:
        exclude = {(player_x, player_y), (target_x, target_y)} | traps
        for _ in range(3):
            ex, ey = find_random_open_tile(maze, screen_width, screen_height, exclude)
            if ex is None:
                break
            axis = random.choice(['h', 'v'])
            enemies.append((ex, ey, axis))
            exclude.add((ex, ey))

    potions = set()
    exclude_p = {(player_x, player_y), (target_x, target_y)} | traps | {(ex, ey) for ex, ey, _ in enemies}
    for _ in range(3):
        px, py = find_random_open_tile(maze, screen_width, screen_height, exclude_p)
        if px is None:
            break
        potions.add((px, py))
        exclude_p.add((px, py))
else:
    # načtení proměnných ze stavu
    maze = state['maze']
    player_x = state['player_x']
    player_y = state['player_y']
    target_x = state['target_x']
    target_y = state['target_y']
    traps = set(tuple(t) for t in state['traps'])
    enemies = [tuple(e) for e in state['enemies']]
    potions = set(tuple(p) for p in state['potions'])
    lives = state['lives']
    include_traps = state['include_traps']
    include_enemies = state['include_enemies']
    fog_of_war_enabled = state['fog_of_war_enabled']
    screen_width = state['screen_width']
    screen_height = state['screen_height']

# Hlavní herní smyčka s možností uložení
while True:
    print_maze_with_entities(maze, player_x, player_y, target_x, target_y, traps, enemies, potions, lives)

    if player_x == target_x and player_y == target_y:
        print(win_screen)
        break

    move = input("Pohyb (WASD) nebo 'save' pro uložení: ").lower().strip()
    if move == 'save':
        save_game()
        continue

    new_x, new_y = player_x, player_y
    if move == 'w':
        new_y -= 1
    elif move == 'a':
        new_x -= 1
    elif move == 's':
        new_y += 1
    elif move == 'd':
        new_x += 1
    else:
        continue

    if 0 <= new_x < screen_width and 0 <= new_y < screen_height:
        if maze[new_y][new_x] != " ■ ":
            player_x, player_y = new_x, new_y

    if (player_x, player_y) in potions:
        potions.remove((player_x, player_y))
        lives += 1
        print("Sebral jsi lektvar! Život obnoven, nyní máš", lives, "životů.")
        time.sleep(1)

    if (player_x, player_y) in traps:
        lives -= 1
        print("Spadl jsi do pasti! Ztratil jsi 1 život. Zbývá ti", lives, "životů.")
        time.sleep(1)
        if lives <= 0:
            print(game_over_screen)
            break

    enemies = move_enemies(enemies, player_x, player_y, maze, screen_width, screen_height)

    if any(ex == player_x and ey == player_y for (ex, ey, _) in enemies):
        lives -= 1
        print("Náraz s nepřítelem! Ztratil jsi 1 život. Zbývá ti", lives, "životů.")
        time.sleep(1)
        if lives <= 0:
            print(game_over_screen)
            break
