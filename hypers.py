import argparse
from contextlib import suppress
import inspect
import os
import sys
from copy import deepcopy

parser = argparse.ArgumentParser()
cmdline_parser = deepcopy(parser)

VALID_TYPES = (int, float, bool, str, list)
CMDLINE_ARGS = tuple(s.replace("--", '').split("=")[0] for s in sys.argv[1:] if "=" in s)
YELLOW = 33
BLUE   = 34
PURPLE = 35

COMMAND_LINE_ARGS = []
DEFAULT_ARGS      = []
CONFIG_ARGS       = []

FILE_LIST = {}

# see https://www.geeksforgeeks.org/how-to-add-colour-to-text-python/
def color(test_str, ansi_code):
    return f"\33[{ansi_code}m{test_str}\33[0m"

HEADER = f"""\
{'-' * 40}HyperParams{'-' * 40}
{' ' * 25}(color code: \
{color('default', BLUE)}, \
{color('config',  PURPLE)}, \
{color('command_line', YELLOW)})\
{' ' * 30}
"""

FOOTER = f"{'-' * 90}\n"

def get_code(test_str):
    if test_str in COMMAND_LINE_ARGS:
        return YELLOW
    elif test_str in CONFIG_ARGS:
        return PURPLE
    else:
        return BLUE

def member_filter(x):
    return isinstance(x, VALID_TYPES) and x != "__main__"  # catch main manually

def read_config(file):
    variables = {}
    if "--" in file:
        raise ValueError(f"{file} is not a valid argument.")

    if not os.path.isfile(file):
        raise ValueError(f"{file} is not a valid file.")

    with open(file) as f:
        exec(f.read(), variables)

    return {k:v for k, v in variables.items() if not k.startswith('_')}

def induce_bool(value):
    if value.lower() in ('yes', 'true', 't', 'y'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n'):
        return False
    else:
        raise ValueError

def induce_type(value):
    for t in [induce_bool, int, float]:
        with suppress(ValueError):
            return t(value)
    return value

def set_type(string_input):
    string_input = string_input.split(',')
    if len(string_input) == 1:
        return induce_type(string_input[0])
    else:
        return list(map(induce_type, string_input))

def add_argument(parser, name, value) -> None:
    parser.add_argument(f"--{name}", default=value, type=set_type)


class Hypers:
    def __init__(self) -> None:
        for name, value in self._get_members():
            add_argument(parser, name, value)
            if name in CMDLINE_ARGS:
                add_argument(cmdline_parser, name, value)
        self.parse_args()
        print(self)

    def __str__(self):
        files = [f"- Reading {count} arguments from {file}\n" for file, count in FILE_LIST.items()]
        args = [f"{color(k, get_code(k))}: {v}\n" for k, v in self.__dict__.items()]
        return "".join([HEADER, *files, *args, FOOTER])

    def _get_members(self):
        yield from inspect.getmembers(self, member_filter)

    def _load_default_args(self, default_args):
        for name, value in vars(default_args).items():
            setattr(self, name, value)

    def _handle_special_args(self, argv):
        if "--unobserved" in argv:
            argv.remove("--unobserved")

    def _load_config_args(self, argv):
        for config in argv:
            self._parse_config_file(config)

    def _parse_config_file(self, file):
        variables = read_config(file)
        for name, value in variables.items():
            setattr(self, name, value)
            CONFIG_ARGS.append(name)
        FILE_LIST[file] = len(variables)

    def _load_cmdline_args(self, cmdline_args):
        for name, value in vars(cmdline_args).items():
            setattr(self, name, value)

    def parse_args(self, args=None) -> None:
        default_args, argv = parser.parse_known_args(args)
        cmdline_args, argv = cmdline_parser.parse_known_args(args)
        DEFAULT_ARGS.extend(default_args.__dict__.keys())
        COMMAND_LINE_ARGS.extend(cmdline_args.__dict__.keys())

        # order matters here, load default, then file, then commandline args
        self._load_default_args(default_args)
        self._handle_special_args(argv)
        self._load_config_args(argv)
        self._load_cmdline_args(cmdline_args)

    def to_dict(self):
        return dict(self.__dict__.items())

    def merge_from_dict(self, d):
        self.__dict__.update(d)



