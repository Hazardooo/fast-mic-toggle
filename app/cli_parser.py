from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
import argparse


class CommandType(Enum):
    LIST_MICS = auto()
    CREATE_CONFIG = auto()
    TOGGLE = auto()
    DELETE_CONFIG = auto()
    INTERACTIVE = auto()


@dataclass(frozen=True)
class Command:
    type: CommandType
    args: tuple[int, ...] = ()


class CLIParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(description="fast-mic-toggle")
        self._parser.add_argument('option', nargs='?', type=int)
        self._parser.add_argument('args', nargs='*', type=int)

    def parse(self, argv: list[str]) -> Command:
        args = self._parser.parse_args(argv[1:])

        if args.option is None:
            return Command(CommandType.INTERACTIVE)

        match args.option:
            case 1:
                return Command(CommandType.LIST_MICS)
            case 2:
                return Command(CommandType.CREATE_CONFIG, tuple(args.args))
            case 3:
                return Command(CommandType.TOGGLE)
            case 4:
                return Command(CommandType.DELETE_CONFIG)
            case _:
                self._parser.print_help()
                raise SystemExit(1)
