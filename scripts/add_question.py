#!/usr/bin/env python3

# Filename: add_question.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import subprocess
import sys

from utils import prompt_success, prompt_with_input, prompt_without_input, prompt_error, db_connect, db_disconnect
from constants import (
    ADD_CATEGORY_SCRIPT,
    CREATE_CATEGORY_TABLE_QUERY,
    CREATE_QUESTIONS_TABLE_QUERY,
    PYTHON_INTERPRETER,
)


def add_question():
    """
    Add a question to the database
    """
    # Get the question and the correct answer

    question = prompt_with_input("Enter the question")
    correct_answer = prompt_with_input("Enter the correct answer")

    prompt_without_input("Question:")
    print(question)

    prompt_without_input("Correct answer:")
    print(correct_answer)

    confirmation = prompt_with_input("Is this question correct? (y/n)")

    if confirmation.lower() != "y":
        prompt_error("Aborting!")
        sys.exit(1)

    # Prompt for the wrong answers
    while True:
        wrong_answer1 = prompt_with_input("Enter the first wrong answer")
        wrong_answer2 = prompt_with_input("Enter the second wrong answer")
        wrong_answer3 = prompt_with_input("Enter the third wrong answer")

        prompt_without_input("First wrong answer:")
        print(wrong_answer1)

        prompt_without_input("Second wrong answer:")
        print(wrong_answer2)

        prompt_without_input("Third wrong answer:")
        print(wrong_answer3)

        confirmation = prompt_with_input("Are these the wrong answers? (y/n)")

        if confirmation.lower() == "y":
            break

    connection, cursor = db_connect()

    # Ensure that the tables exist
    cursor.execute(CREATE_CATEGORY_TABLE_QUERY)
    cursor.execute(CREATE_QUESTIONS_TABLE_QUERY)

    while True:
        prompt_without_input("Available categories:", end="\n")

        try:
            cursor.execute("SELECT id, name FROM category")
            categories = cursor.fetchall()

            if categories:
                for category in categories:
                    print(f"{category[0]}) {category[1]}")

                choice = prompt_with_input("Enter the category ID, or type 'new' to create a new category")

                if choice.lower() == "new":
                    prompt_without_input("Launching category creation script...")
                    subprocess.run([PYTHON_INTERPRETER, ADD_CATEGORY_SCRIPT])
                    continue

                elif choice.isdigit() and int(choice) in [
                    category[0] for category in categories
                ]:
                    cursor.execute("SELECT name FROM category WHERE id = ?", (choice,))
                    category_name = cursor.fetchone()[0]
                    category_id = choice
                    prompt_success(f"Category {category_name} selected successfully!")
                    break

                else:
                    prompt_error("Invalid input. Try again")
                    continue

            else:
                prompt_error("No categories available. Please add a category first")
                subprocess.run([PYTHON_INTERPRETER, ADD_CATEGORY_SCRIPT])
                continue

        except sqlite3.Error as e:
            prompt_error(f"Database error: {e}")
            sys.exit(1)

    # Check if the question already exists
    cursor.execute("SELECT COUNT(*) FROM questions WHERE question = ?", (question,))
    exists = cursor.fetchone()[0]

    if exists > 0:
        prompt_error("Question already exists in the database!")
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
        prompt_success("Question added successfully!")

    except sqlite3.Error as e:
        prompt_success(f"Failed to add question: {e}")

    finally:
        db_disconnect(connection)


if __name__ == "__main__":
    # Check if the user provided the correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python add_question.py <question> <correct_answer>")
        sys.exit(1)

    add_question()
