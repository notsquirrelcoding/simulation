"""Import dependencies"""
import json
# import consolemenu
# import keyboard
# from termcolor import colored


def main():
    """The main function where all the magic happens"""

    with open("options.json", encoding="utf8") as option_file:
        options = json.load(option_file)
        option_manager = OptionManager(**options)
        print(option_manager.get_keyset("math"))

        # keysets = options["sets"]
        # selected_integer = consolemenu.SelectionMenu.get_selection(keysets)

        # # The last option is to add and len()-1 is the last option
        # if selected_integer == len(keysets) - 1:
        #     pass
        # else:
        #     keyset = keysets[selected_integer]
        #     for key, value in options[keyset].items():
        #         keyboard.add_abbreviation(key, value)

        #     msg = f"Currently running keyset '{keysets[selected_integer]}'"
        #     print(colored(msg, "red", attrs=["bold"]))
        #     keyboard.wait()


class OptionManager(object):
    """A class that manages `options.json`"""

    def __init__(self, _keyset_list: list, _keysets: dict) -> None:
        self._keyset_list = _keyset_list
        self._keysets = _keysets

    def write(self) -> None:
        """Writes the data in this class back to `options.json`."""

        with open("options.json", "w", encoding="utf8") as options_file:
            class_as_json = self.__to_json()
            options_file.write(class_as_json)

    def get_all_keysets(self) -> list:
        """Returns all the keysets from `options.json`"""
        return self._keysets

    def get_keyset(self, name: str) -> dict:
        """Returns a specific keyset given a name."""
        return self._keysets.get(name)

    def __to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
