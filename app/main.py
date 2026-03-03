from __future__ import annotations

from core import Core
from cli_parser import CLIParser, CommandType
from menu import InteractiveMenu, MenuOption
from commands import CommandExecutor


class Application:
    def __init__(self):
        self._core = Core()
        self._parser = CLIParser()
        self._menu = InteractiveMenu()
        self._executor = CommandExecutor(self._core)

    def run(self, argv: list[str]) -> None:
        command = self._parser.parse(argv)

        if command.type == CommandType.INTERACTIVE:
            self._interactive_loop()
        else:
            self._execute_command(command)

    def _execute_command(self, command) -> None:
        match command.type:
            case CommandType.LIST_MICS:
                self._executor.list_mics()
            case CommandType.CREATE_CONFIG:
                self._executor.create_config(command.args)
            case CommandType.TOGGLE:
                self._executor.toggle()
            case CommandType.DELETE_CONFIG:
                self._executor.delete_config()

    def _interactive_loop(self) -> None:
        while True:
            self._menu.show()
            option = self._menu.get_input()

            if option is None:
                continue

            match option:
                case MenuOption.LIST:
                    self._executor.list_mics()
                case MenuOption.CONFIG:
                    indices = self._menu.get_mic_indices()
                    if indices:
                        self._executor.create_config(indices)
                case MenuOption.TOGGLE:
                    self._executor.toggle()
                case MenuOption.DELETE:
                    self._executor.delete_config()
                case MenuOption.EXIT:
                    print("Exiting... 👋")
                    break


def main():
    app = Application()
    app.run(__import__('sys').argv)


if __name__ == "__main__":
    main()
