#!/usr/bin/env python3

# Filename: settings.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import os

from utils import (
    print_blue,
    print_red,
    print_green,
    print_yellow,
    db_connect,
    db_disconnect,
)
from constants import (
    Setting,
    FULL_DB_PATH,
    CREATE_SETTINGS_TABLE_QUERY,
    INSERT_DEFAULT_SETTINGS_QUERY,
)


def set_category():
    """
    Set the category for the questions
    """
    connection, cursor = db_connect()

    print_yellow("Choose a category for the questions:")

    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    while True:
        if categories:
            for category in categories:
                print(f"{category[0]}) {category[1]}")

            # O usuario deve digitar o id da categoria para mostrar questoes apenas daquela categoria
            # Se ele digitar 'all', todas as questoes serao mostradas
            print_blue(
                "> Choose a category or type 'all' to set all questions as possible: ",
                end="",
            )
            category_id = input()

            if category_id.isdigit():
                print_green("Category {} set successfully!".format(category_id))
                return category_id

            elif category_id.lower() == "all":
                print_green("All questions will be asked!")
                return "all"

            else:
                print_red("Invalid category id!")
                continue
        else:
            print_red("No categories available")
            return None

    db_disconnect(connection)


def show_settings():
    """
    Show the current settings
    """
    connection, cursor = db_connect()

    # Ensure that the settings table exists and has the default settings
    cursor.execute(CREATE_SETTINGS_TABLE_QUERY)
    cursor.execute(INSERT_DEFAULT_SETTINGS_QUERY)

    cursor.execute("SELECT id, name, value FROM settings")
    settings = cursor.fetchall()

    print_yellow("Current settings:")
    for setting in settings:
        print(f"{setting[0]}): {setting[1]} = {setting[2]}")

    print_blue(
        "> What setting would you like to change? (Enter ID or 'exit' to quit): ",
        end="",
    )
    user_choice = input()

    if user_choice.lower() == "exit":
        return

    if user_choice.isdigit():
        setting_id = int(user_choice)
        cursor.execute("SELECT name, value FROM settings WHERE id = ?", (setting_id,))
        setting = cursor.fetchone()

        if setting:
            setting_name, setting_value = setting

            print_yellow(f"Current value for {setting_name}: {setting_value}")

            if setting_id == Setting.FILTER_BY_CATEGORY_ID_ON_TABLE.value:
                new_value = set_category()

                if new_value is not None:
                    cursor.execute(
                        "UPDATE settings SET value = ? WHERE id = ?",
                        (new_value, setting_id),
                    )
                    connection.commit()
                    print_green(f"Setting '{setting_name}' updated successfully!")
                else:
                    print_red("Invalid new value")
        else:
            print_red("Invalid setting ID")

    else:
        print_red("Invalid input")

    db_disconnect(connection)


if __name__ == "__main__":
    show_settings()
