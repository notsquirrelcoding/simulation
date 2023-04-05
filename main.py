"""Import dependencies"""
import json
import consolemenu
import keyboard
from termcolor import colored


def main():
    """The main function where all the magic happens"""

    with open("options.json", encoding="utf8") as option_file:
        options = json.load(option_file)
        option_manager = OptionManager(**options)
        selected_integer = consolemenu.SelectionMenu.get_selection(option_manager.get_all_keysets())
        match selected_integer:
            case 0:
                option_manager.add_keyset("test", {"a": "b", "c": "d"})
        option_manager.write()


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
        return self._keyset_list

    def get_keyset(self, name: str) -> dict:
        """Returns a specific keyset given a name."""
        return self._keysets.get(name)

    def add_keyset(self, keyset_name: str, keyset: dict):
        """Adds a keyset to the list."""
        self._keysets.update({keyset_name: keyset})

    def __to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
