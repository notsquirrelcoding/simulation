import json
from termcolor import colored
import consolemenu
import keyboard

def main():
    options = json.load(open("options.json"))
    sets = options["sets"]
    menu = consolemenu.SelectionMenu.get_selection(sets)

    if menu == len(sets):
        print("add")
    else:
        set = sets[menu]
        for key, value in options[set].items():
            keyboard.add_abbreviation(key, value)
        keyboard.wait()


if __name__ == "__main__":
    main()