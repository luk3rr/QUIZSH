#!/usr/bin/env python3

# Filename: utils.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3

from constants import BLUE, RED, GREEN, YELLOW, END, FULL_DB_PATH


# Utility functions for colored output
def print_blue(message, end="\n"):
    print(BLUE + message + END, end=end)


def print_red(message, end="\n"):
    print(RED + message + END, end=end)


def print_green(message, end="\n"):
    print(GREEN + message + END, end=end)


def print_yellow(message, end="\n"):
    print(YELLOW + message + END, end=end)


def prompt_with_input(prompt, end=" "):
    """
    Prompt the user with a message and return the input
    """
    print_blue("> " + prompt + ":", end=end)
    return input().strip()


def prompt_without_input(prompt, end=" "):
    """
    Prompt the user with a message and return the input
    """
    print_yellow(prompt, end=end)

def prompt_error(prompt, end="\n"):
    """
    Prompt the user with a message and return the input
    """
    print_red(prompt, end=end)

def prompt_success(prompt, end="\n"):
    """
    Prompt the user with a message and return the input
    """
    print_green(prompt, end=end)

def db_connect():
    """
    Connect to the SQLite database
    """
    connection = sqlite3.connect(FULL_DB_PATH)
    cursor = connection.cursor()
    return connection, cursor


def db_disconnect(connection):
    """
    Disconnect from the SQLite database
    """
    connection.close()
