import copy


# Funkce pro převod bodů na textové skóre podle tenisových pravidel.
def get_game_score(p1, p2):
    # Pokud ani jeden nedosáhl 3 bodů, použijeme přímý převod.
    mapping = {0: "0", 1: "15", 2: "30", 3: "40"}
    if p1 < 3 and p2 < 3:
        return mapping[p1], mapping[p2]
    # Pokud oba mají minimálně 3 body:
    if p1 >= 3 and p2 >= 3:
        if p1 == p2:
            return "40", "40"  # deuce
        elif p1 - p2 == 1:
            return "Adv", "40"
        elif p2 - p1 == 1:
            return "40", "Adv"
    # Ostatní případy – použijeme mapping
    return mapping.get(p1, str(p1)), mapping.get(p2, str(p2))


# Funkce pro kontrolu vítězství v aktuální hře
def check_game_win(p1, p2):
    # Hráč vyhrává hru, pokud má alespoň 4 body a vede alespoň o 2
    if p1 >= 4 and p1 - p2 >= 2:
        return 1
    if p2 >= 4 and p2 - p1 >= 2:
        return 2
    return 0


# Funkce pro kontrolu vítězství v setu (minimálně 6 her a 2 hry náskok)
def check_set_win(g1, g2):
    if g1 >= 6 and g1 - g2 >= 2:
        return 1
    if g2 >= 6 and g2 - g1 >= 2:
        return 2
    return 0


# Funkce pro zobrazení aktuálního skóre v ASCII tabulce
def print_score(state):
    # state obsahuje: points1, points2, games1, games2, sets1, sets2
    p1, p2 = state['points1'], state['points2']
    g1, g2 = state['games1'], state['games2']
    s1, s2 = state['sets1'], state['sets2']

    game_score = get_game_score(p1, p2)

    # Vytvoříme ASCII tabulku
    border = "+" + "-" * 18 + "+" + "-" * 18 + "+"
    header = "|{:^18}|{:^18}|".format("Hráč 1", "Hráč 2")
    score_row = "|{:^18}|{:^18}|".format(f"Bod: {game_score[0]}", f"Bod: {game_score[1]}")
    games_row = "|{:^18}|{:^18}|".format(f"Hry: {g1}", f"Hry: {g2}")
    sets_row = "|{:^18}|{:^18}|".format(f"Sety: {s1}", f"Sety: {s2}")

    print(border)
    print(header)
    print(border)
    print(score_row)
    print(games_row)
    print(sets_row)
    print(border)


# Funkce pro zobrazení menu
def print_menu():
    print("\nMenu:")
    print("1 - Bod pro hráče 1")
    print("2 - Bod pro hráče 2")
    print("3 - Opravit (Undo poslední akci)")
    print("4 - Zobrazit aktuální skóre")
    print("5 - Konec")


def main():
    # Inicializace stavu
    state = {
        'points1': 0,
        'points2': 0,
        'games1': 0,
        'games2': 0,
        'sets1': 0,
        'sets2': 0
    }

    # Seznam historií pro undo – ukládáme kopii stavu před každou akcí.
    history = [copy.deepcopy(state)]

    print("Aplikace pro rozhodčí tenis")

    while True:
        print_menu()
        volba = input("Zadejte volbu: ").strip()

        if volba == "1":
            # Bod pro hráče 1
            state['points1'] += 1
            history.append(copy.deepcopy(state))
        elif volba == "2":
            # Bod pro hráče 2
            state['points2'] += 1
            history.append(copy.deepcopy(state))
        elif volba == "3":
            # Oprava poslední akce (undo)
            if len(history) > 1:
                history.pop()  # odebereme poslední stav
                state = copy.deepcopy(history[-1])
                print("Poslední akce byla opravena.")
            else:
                print("Nelze opravit – žádná předchozí akce.")
        elif volba == "4":
            print_score(state)
            continue
        elif volba == "5":
            print("Konec aplikace.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")
            continue

        # Po každém bodu zkontrolujeme, zda někdo vyhrál hru.
        game_winner = check_game_win(state['points1'], state['points2'])
        if game_winner:
            if game_winner == 1:
                state['games1'] += 1
                print("Hráč 1 vyhrál hru!")
            else:
                state['games2'] += 1
                print("Hráč 2 vyhrál hru!")
            # Resetujeme body
            state['points1'] = 0
            state['points2'] = 0
            history.append(copy.deepcopy(state))

            # Kontrola vítězství setu
            set_winner = check_set_win(state['games1'], state['games2'])
            if set_winner:
                if set_winner == 1:
                    state['sets1'] += 1
                    print("Hráč 1 vyhrál set!")
                else:
                    state['sets2'] += 1
                    print("Hráč 2 vyhrál set!")
                # Resetujeme hry
                state['games1'] = 0
                state['games2'] = 0
                history.append(copy.deepcopy(state))

        # Vykreslíme aktuální skóre
        print_score(state)



main()
