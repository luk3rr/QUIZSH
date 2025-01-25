#!/usr/bin/env python3

# Filename: add_question.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import subprocess
import sys

from utils import print_blue, print_red, print_green, db_connect, db_disconnect
from constants import (
    ADD_CATEGORY_SCRIPT,
    LOCAL_DB_PATH,
    CREATE_CATEGORY_TABLE_QUERY,
    CREATE_QUESTIONS_TABLE_QUERY,
    PYTHON_INTERPRETER,
)


def add_question():
    """
    Add a question to the database
    """
    # Get the question and the correct answer

    print_blue("> Enter the question: ", end="")
    question = input().strip()

    print_blue("> Enter the correct answer: ", end="")
    correct_answer = input().strip()

    print(f"Question: {question}")
    print(f"Correct answer: {correct_answer}")
    print_blue("Is this question correct? (y/n): ", end="")
    confirmation = input()

    if confirmation.lower() != "y":
        print_red("Aborting!")
        sys.exit(1)

    # Prompt for the wrong answers
    while True:
        wrong_answer1 = input("Enter the first wrong answer: ")
        wrong_answer2 = input("Enter the second wrong answer: ")
        wrong_answer3 = input("Enter the third wrong answer: ")

        print(f"First wrong answer: {wrong_answer1}")
        print(f"Second wrong answer: {wrong_answer2}")
        print(f"Third wrong answer: {wrong_answer3}")

        print_blue("Are these the wrong answers? (y/n): ", end="")
        confirmation = input()

        if confirmation.lower() == "y":
            break

    connection, cursor = db_connect()

    # Ensure that the tables exist
    cursor.execute(CREATE_CATEGORY_TABLE_QUERY)
    cursor.execute(CREATE_QUESTIONS_TABLE_QUERY)

    while True:
        print("Available categories:")
        try:
            cursor.execute("SELECT id, name FROM category")
            categories = cursor.fetchall()

            if categories:
                for category in categories:
                    print(f"{category[0]}) {category[1]}")

                print_blue(
                    "Enter the category ID, or type 'new' to create a new category: ",
                    end="",
                )
                choice = input()

                if choice.lower() == "new":
                    print_blue("Launching category creation script...")
                    subprocess.run([PYTHON_INTERPRETER, ADD_CATEGORY_SCRIPT])
                    continue

                elif choice.isdigit() and int(choice) in [
                    category[0] for category in categories
                ]:
                    cursor.execute("SELECT name FROM category WHERE id = ?", (choice,))
                    category_name = cursor.fetchone()[0]
                    category_id = choice
                    print_green(f"Category '{category_name}' selected")
                    break
                else:
                    print_red("Invalid input. Try again")
                    continue

            else:
                print_red("No categories available. Please add a category first")
                subprocess.run([PYTHON_INTERPRETER, ADD_CATEGORY_SCRIPT])
                continue
        except sqlite3.Error as e:
            print_red(f"Database error: {e}")
            sys.exit(1)

    # Check if the question already exists
    cursor.execute("SELECT COUNT(*) FROM questions WHERE question = ?", (question,))
    exists = cursor.fetchone()[0]

    if exists > 0:
        print_red("Question already exists in the database!")
        connection.close()
        sys.exit(1)

    # Insert the question with answers into the database
    try:
        cursor.execute(
            """
            INSERT INTO questions (question, answer, wrong_answer1, wrong_answer2, wrong_answer3, category_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                question,
                correct_answer,
                wrong_answer1,
                wrong_answer2,
                wrong_answer3,
                category_id,
            ),
        )
        connection.commit()
        print_green("Question added successfully!")
    except sqlite3.Error as e:
        print_red(f"Failed to add question: {e}")
    finally:
        db_disconnect(connection)


if __name__ == "__main__":
    # Check if the user provided the correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python add_question.py <question> <correct_answer>")
        sys.exit(1)

    add_question()
