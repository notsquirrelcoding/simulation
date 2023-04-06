"""Import dependencies"""
import json
# import consolemenu
# from termcolor import colored
# from option_manager import OptionManager
import time
from rich.console import Console

def main():
    """The main function where all the magic happens"""
    console = Console()
    console.rule("[bold white]Menu")
    


    # with open("options.json", encoding="utf8") as option_file:
    #     options = json.load(option_file)
    #     option_manager = OptionManager(**options)
    #     selected_integer = consolemenu.SelectionMenu.get_selection(option_manager.get_all_keysets())
    #     match selected_integer:
    #         case 0:
    #             add_option_menu(option_manager)

    #     option_manager.write()

# def add_option_menu(option_manager: OptionManager):
#     """A function that handles the frontend for user input"""

#     keyset_name = str(input("Enter the name of the keyset:"))
#     if not option_manager.keyset_exists(keyset_name):
#         print(colored(f"Keyset '{keyset_name}' does not exist.", "red", attrs=["bold"]))
#         return

#     while True:
#         keystroke = str(input("Enter the keystroke. (To end enter 'end')"))
#         if keystroke == "end":
#             break
#         typee = str(input("Enter the phrase: "))
#         option_manager.add_entry(keyset_name, keystroke, typee)
    

if __name__ == "__main__":
    main()
