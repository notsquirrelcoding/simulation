"""This is the module that holds the `OptionManager` class."""
import json


class OptionManager:
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

    def add_keyset(self, keyset_name: str, keyset: dict) -> None:
        """Adds a keyset to the list."""
        self._keysets.update({keyset_name: keyset})

    def add_entry(self, keyset_name: str, keystroke: str, typee: str) -> None:
        """Adds a macro entry given a `keyset_name`."""
        if not self.keyset_exists(keyset_name):
            return
        self._keysets[keyset_name].update({keystroke: typee})

    def keyset_exists(self, keyset: str) -> bool:
        """Returns a boolean indicating whether a given keyset exists."""
        return keyset in self._keyset_list
    def __to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    