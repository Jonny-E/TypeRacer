from __future__ import annotations
import random
import time
import json
import sys
import colorama
import subprocess
import platform
from string import ascii_lowercase
from timeit import timeit
from typing import Any
# ------------------------------------------------------------------------

clear = lambda: subprocess.run('cls' if platform.system() == 'Windows' else 'clear', shell=True, check=True)

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

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
        
    def springen(self, gamios: int) -> None:
        if self.posX < 10:
            print(self.posX, " von 10")
            self.posX += input_player(gamios)
            clear()
            self.springen(gamios)
            
        else:
            print(self.posX, "von 10")
            input("End")
            clear()


def check_name(name: str, mode: str) -> bool:
    with open('highscoredb.json', 'r') as db:
        loaded_db = json.load(db)
    
    if name in loaded_db[mode]:
        return True
    return False

def sort_dict(json_dict):
    return dict(sorted(json_dict.items(), key=lambda item: item[1]))

def print_db(db, name_player):
    iterator = iter(db.items())
    for i in range(5):
        x = next(iterator)
        if x[0] == name_player:

            print(bcolors.OK, x)
        else:
            print(bcolors.RESET, x)

def write_json(mode: str, player_name: str, time_took: str) -> None:
    with open('highscoredb.json', 'r') as db:
        loaded_db = json.load(db)
    
    if check_name(player_name, mode):
        if float(time_took) > float(loaded_db[mode][player_name]):
            print_db(loaded_db[mode], player_name)
            return None

    loaded_db[mode][player_name] = time_took

    loaded_db[mode] = sort_dict(loaded_db[mode])

    with open('highscoredb.json', 'w') as db:
        json.dump(loaded_db, db, indent=4)
    print_db(loaded_db[mode], player_name)

def start_again():
    x = input("wanna start again? (y/n)")
    if x == "y":
        clear()
        main()
    elif x == "n":
        sys.exit(0)
    else: 
        clear()
        start_again()

def main(*args: Any, **kwargs: Any) -> None:
    frog1 = Frog()
    gamemode_value, gamemode_name = gamemode()
    clear()
    t1 = timeit(stmt='frog1.springen(gamemode_value)', globals={'frog1': frog1, 'gamemode_value': gamemode_value}, number=1)

    name_player = input("Enter username: ")
    clear()
    if gamemode_name == 'beginner':
        write_json("beginner", name_player, str(t1))
    elif gamemode_name == 'normal':
        write_json("normal", name_player, str(t1))
    elif gamemode_name == 'hard':
        write_json("hard", name_player, str(t1))

    start_again()

    


if __name__ == '__main__':
    main()