#!/usr/bin/env python3

# Filename: add_category.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import os

from utils import print_blue, print_red, print_green, db_connect, db_disconnect
from constants import FULL_DB_PATH, CREATE_CATEGORY_TABLE_QUERY

def show_categories():
    """
    Show the current categories
    """
    connection, cursor = db_connect()

    # show the current categories
    cursor.execute("SELECT id, name FROM category")
    categories = cursor.fetchall()

    print_blue("Current categories:")
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

        print_blue("> Enter the name of the new category: ", end="")
        new_category = input().strip()

        if not new_category:
            print_red("Category name cannot be empty.")
            return

        try:
            cursor.execute("INSERT INTO category (name) VALUES (?)", (new_category,))
            connection.commit()
            print_green(f"Category '{new_category}' added successfully!")
        except sqlite3.IntegrityError:
            print_red(f"The category '{new_category}' already exists.")

    except sqlite3.Error as e:
        print_red(f"Database error: {e}")
    finally:
        db_disconnect(connection)


if __name__ == "__main__":
    add_category()
