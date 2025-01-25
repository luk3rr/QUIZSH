#!/usr/bin/env python3

# Filename: utils.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
END = "\033[0m"


# Utility functions for colored output
def print_blue(message, end="\n"):
    print(BLUE + message + END, end=end)


def print_red(message, end="\n"):
    print(RED + message + END, end=end)


def print_green(message, end="\n"):
    print(GREEN + message + END, end=end)


def print_yellow(message, end="\n"):
    print(YELLOW + message + END, end=end)
