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
