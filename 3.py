import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_field(rows, cols, fill_percent):
    """Vytvoří počáteční pole s daným procentem zaplnění (živé buňky = 1, mrtvé buňky = 0)."""
    field = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            cell = 1 if random.random() < (fill_percent / 100.0) else 0
            row.append(cell)
        field.append(row)
    return field

def print_field(field):
    """Vykreslí pole pomocí ctverců:
       živá buňka: "  ■  "
       mrtvá buňka: "  □  " """
    for row in field:
        line = "".join("  ■  " if cell == 1 else "  □  " for cell in row)
        print(line)

def count_neighbors(field, row, col, rows, cols):
    """Spočítá počet živých sousedů pro buňku na pozici (row, col)."""
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                count += field[i][j]
    return count

def next_generation(field, rows, cols):
    """Vypočítá další generaci podle pravidel Conwayovy Hry Života."""
    new_field = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            neighbors = count_neighbors(field, i, j, rows, cols)
            if field[i][j] == 1:
                # Buňka přežije pouze pokud má 2 nebo 3 sousedy.
                if neighbors < 2 or neighbors > 3:
                    new_field[i][j] = 0
                else:
                    new_field[i][j] = 1
            else:
                # Mrtvá buňka se oživí, pokud má přesně 3 sousedy.
                if neighbors == 3:
                    new_field[i][j] = 1
                else:
                    new_field[i][j] = 0
    return new_field

# Hlavní menu
print("Conwayova Hra Života")
size = int(input("Zadejte velikost pole (např. 20 pro 20x20): ").strip())
fill_percent = float(input("Zadejte procento zaplnění (0-100): ").strip())
iterations = int(input("Zadejte počet iterací simulace: ").strip())

rows = size
cols = size
field = create_field(rows, cols, fill_percent)

# Simulace
for gen in range(1, iterations + 1):
    clear_screen()
    print(f"Generace {gen}")
    print_field(field)
    field = next_generation(field, rows, cols)
    time.sleep(0.2)

print("Simulace skončila.")
