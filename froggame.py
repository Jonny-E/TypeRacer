from __future__ import annotations
import random
import time
import json
import sys
from string import ascii_lowercase
from timeit import timeit
from typing import Any
# ------------------------------------------------------------------------

def gamemode() -> tuple[int | float, str]:
    while True:
        try:
            gamo = int(input("1. beginner (2s) \n2. normal (1s) \n3. hard(0.5s)\nEingabe: "))
            if gamo == 1:
                return 2, 'beginner', 
            elif gamo == 2:
                return 1, 'normal'
            elif gamo == 3:
                return 0.5, 'hard'
            else:
                input("error")
                gamemode()
        except (ValueError):
            input("Please enter number")

def input_player(gamios: int) -> int:
    time.sleep(random.randint(2, 3))
    ran_str = random.choice(ascii_lowercase)
    time1 = time.perf_counter()
    inp = input(f'type {ran_str}: ')
    time2 = time.perf_counter()
    if not valiate_input(validater=ran_str, inp=inp):
        return -1
    timedif = time2-time1
    if timedif < gamios:
        return 1
    else:
        return 0


def valiate_input(*, validater: str, inp: str) -> bool:
    if inp == validater:
        return True
    return False


class Frog:
    def __init__(self) -> None:
        self.posX = 0 #Ende bei 10
        self.wins = 0
        
    def springen(self, gamios: int) -> None:
        if self.posX < 3:
            self.posX += input_player(gamios)
            print(self.posX)
            self.springen(gamios)
        else:
            input("End")
            self.wins = self.wins + 1


def check_name(name: str, mode: str) -> bool:
    with open('highscoredb.json', 'r') as db:
        loaded_db = json.load(db)
    
    if name in loaded_db[mode]:
        return True
    return False

def sort_dict(dict):
    sorted_values = sorted(dict.values())
    sorted_dict = {}
    for i in sorted_values:
        for k in dict.keys():
            if dict[k] == i:
                sorted_dict[k] = dict[k]
                break
    return sorted_dict


def write_json(mode: str, player_name: str, time_took: str) -> None:
    with open('highscoredb.json', 'r') as db:
        loaded_db = json.load(db)
    
    if check_name(player_name, mode):
        if float(time_took) > float(loaded_db[mode][player_name]):
            return None

    loaded_db[mode][player_name] = time_took

    loaded_db[mode] = sort_dict(loaded_db[mode])

    with open('highscoredb.json', 'w') as db:
        json.dump(loaded_db, db, indent=4)

def start_again():
    if input("wanna start again? (y/n)") == "y":
        main()
    elif input("wanna start again? (y/n)") == "n":
        sys.exit(0)
    else: 
        start_again()

def main(*args: Any, **kwargs: Any) -> None:
    frog1 = Frog()
    gamemode_value, gamemode_name = gamemode()
    t1 = timeit(stmt='frog1.springen(gamemode_value)', globals={'frog1': frog1, 'gamemode_value': gamemode_value}, number=1)

    name_player = input("Enter username: ")

    if gamemode_name == 'beginner':
        write_json("beginner", name_player, str(t1))
    elif gamemode_name == 'normal':
        write_json("normal", name_player, str(t1))
    elif gamemode_name == 'hard':
        write_json("hard", name_player, str(t1))

    start_again()

    


if __name__ == '__main__':
    main()