#!/usr/bin/env python3

# Filename: settings.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

from utils import (
    db_connect,
    db_disconnect,
    prompt_error,
    prompt_success,
    prompt_with_input,
    prompt_without_input,
)
from constants import (
    Setting,
    CREATE_SETTINGS_TABLE_QUERY,
    INSERT_DEFAULT_SETTINGS_QUERY,
)


def set_category():
    """
    Set the category for the questions
    """
    connection, cursor = db_connect()

    prompt_without_input("Choose a category for the questions:", end="\n")

    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    db_disconnect(connection)

    while True:
        if categories:
            for category in categories:
                print(f"{category[0]}) {category[1]}")

            # If the user types 'all', all questions will be shown.
            # If the user types a category id, only questions from that category will
            # be shown
            category_id = prompt_with_input(
                "Choose a category or type 'all' to set all questions as possible",
            )

            if category_id.isdigit():
                prompt_success(f"Succesfully set category to {category_id}")
                prompt_success("Questions will be filtered by category")
                return category_id

            elif category_id.lower() == "all":
                prompt_success("All questions will be asked!")
                return "all"

            else:
                prompt_error("Invalid category id!")
                continue
        else:
            prompt_error("No categories available")
            return None


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

    prompt_without_input("Current settings:", end="\n")
    for setting in settings:
        print(f"{setting[0]}): {setting[1]} = {setting[2]}")

    user_choice = prompt_with_input(
        "What setting would you like to change? (Enter ID or 'q' to quit)"
    )

    if user_choice.lower() == "q":
        return

    if user_choice.isdigit():
        setting_id = int(user_choice)
        cursor.execute("SELECT name, value FROM settings WHERE id = ?", (setting_id,))
        setting = cursor.fetchone()

        if setting:
            setting_name, setting_value = setting

            prompt_without_input(f"Current value for {setting_name}: {setting_value}", end="\n")

            if setting_id == Setting.FILTER_BY_CATEGORY_ID_ON_TABLE.value:
                new_value = set_category()

                if new_value is not None:
                    cursor.execute(
                        "UPDATE settings SET value = ? WHERE id = ?",
                        (new_value, setting_id),
                    )
                    connection.commit()
                    prompt_success(f"Setting '{setting_name}' updated successfully!")

                else:
                    prompt_error("Invalid new value")
        else:
            prompt_error("Invalid setting ID")

    else:
        prompt_error("Invalid input")

    db_disconnect(connection)


if __name__ == "__main__":
    show_settings()
