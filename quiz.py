#!/usr/bin/env python3

# Filename: quiz.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import random
import time
import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

from scripts.utils import (
    print_blue,
    print_red,
    print_green,
    print_yellow,
    db_connect,
    db_disconnect,
)
from scripts.add_question import add_question
from scripts.add_category import add_category
from scripts.settings import show_settings


def get_filter_category():
    """
    Get the current filter category from settings
    """
    connection, cursor = db_connect()

    cursor.execute("SELECT value FROM settings WHERE name = 'FILTER_BY_CATEGORY'")
    filter_category = cursor.fetchone()

    db_disconnect(connection)

    if filter_category:
        return filter_category[0]
    return "all"  # Default is "all" if no setting is found


def ask_question():
    """
    Ask a random question to the user
    """
    connection, cursor = db_connect()

    filter_category = get_filter_category()

    if filter_category == "all":
        cursor.execute(
            """
            SELECT question, answer, wrong_answer1, wrong_answer2, wrong_answer3
            FROM questions
            ORDER BY RANDOM() LIMIT 1
            """
        )
    else:
        cursor.execute(
            """
            SELECT question, answer, wrong_answer1, wrong_answer2, wrong_answer3
            FROM questions
            WHERE category_id = ?
            ORDER BY RANDOM() LIMIT 1
            """,
            (filter_category,),
        )

    row = cursor.fetchone()

    if not row:
        print_red("No questions available in the database.")
        connection.close()
        return

    question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3 = row

    answers = [correct_answer, wrong_answer1, wrong_answer2, wrong_answer3]
    random.shuffle(answers)

    correct_index = answers.index(correct_answer)

    print_yellow(question)
    for i, answer in enumerate(answers):
        print(f"{i}) {answer}")

    print_blue("> Choose the correct answer (0-3): ", end="")
    user_choice = input()

    if user_choice.isdigit() and int(user_choice) == correct_index:
        print_green("Good!")
    else:
        print_red("Oops... Try again!")
        print_blue(f"The correct answer was: {correct_answer}")
        ask_question()

    db_disconnect(connection)


def main():
    # Criação do parser de argumentos
    parser = argparse.ArgumentParser(description="Quiz Application")

    # Adicionando os parâmetros esperados
    parser.add_argument(
        "-gq", "--get-question", action="store_true", help="Get a random question"
    )
    parser.add_argument(
        "-aq", "--add-question", action="store_true", help="Add a new question"
    )
    parser.add_argument(
        "-ac", "--add-category", action="store_true", help="Add a new category"
    )
    parser.add_argument(
        "-s", "--settings", action="store_true", help="Show and modify settings"
    )

    args = parser.parse_args()

    if args.get_question:
        print("Fetching a random question...")

        start_time = time.time()
        ask_question()
        end_time = time.time()

        time_spent = int(end_time - start_time)
        print(f"Time spent: {time_spent} s")

    elif args.add_question:
        print("Adding a new question...")
        add_question()

    elif args.add_category:
        print("Adding a new category...")
        add_category()

    elif args.settings:
        print("Showing and modifying settings...")
        show_settings()

    else:
        print("No valid option selected. Use --help for usage instructions.")


if __name__ == "__main__":
    main()
