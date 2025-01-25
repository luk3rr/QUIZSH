#!/usr/bin/env python3

# Filename: quiz.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import random
import time
import os

from scripts.utils import print_blue, print_red, print_green, print_yellow


def ask_question():
    """
    Ask a random question to the user
    """
    db_path = os.path.join("data", "questions.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT question, answer, wrong_answer1, wrong_answer2, wrong_answer3
        FROM questions
        ORDER BY RANDOM() LIMIT 1
        """
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

    connection.close()


if __name__ == "__main__":
    start_time = time.time()
    ask_question()
    end_time = time.time()

    time_spent = int(end_time - start_time)
    print(f"Time spent: {time_spent} s")
