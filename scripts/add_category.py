#!/usr/bin/env python3

# Filename: add_category.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3

from utils import (
    prompt_success,
    prompt_with_input,
    prompt_without_input,
    prompt_error,
    db_connect,
    db_disconnect,
)
from constants import CREATE_CATEGORY_TABLE_QUERY


def show_categories():
    """
    Show the current categories
    """
    connection, cursor = db_connect()

    # show the current categories
    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    prompt_without_input("Current categories:", end="\n")

    for category in categories:
        print(f"{category[0]}) {category[1]}")

    db_disconnect(connection)


def add_category():
    """
    Add a new category to the database
    """
    connection, cursor = db_connect()

    try:
        cursor.execute(CREATE_CATEGORY_TABLE_QUERY)

        show_categories()

        new_category = prompt_with_input("Enter the name of the new category")

        if not new_category:
            prompt_error("Category name cannot be empty")
            return

        try:
            cursor.execute("INSERT INTO category (name) VALUES (?)", (new_category,))
            connection.commit()

            prompt_success(f"Category '{new_category}' added successfully!")

        except sqlite3.IntegrityError:
            prompt_error(f"Category '{new_category}' already exists")

    except sqlite3.Error as e:
        prompt_error("Failed to add category. An database error occurred: {e}")

    finally:
        db_disconnect(connection)


if __name__ == "__main__":
    add_category()
