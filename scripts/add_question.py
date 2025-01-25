#!/usr/bin/env python3

# Filename: add_question.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import sqlite3
import sys
from utils import print_blue, print_red, print_green

# Check if the user provided the correct number of arguments
if len(sys.argv) < 3:
    print("Usage: python add_question.py <question> <correct_answer>")
    sys.exit(1)

# Get the question and the correct answer
question = sys.argv[1]
correct_answer = sys.argv[2]

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

db_path = "data/questions.db"
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        wrong_answer1 TEXT NOT NULL,
        wrong_answer2 TEXT NOT NULL,
        wrong_answer3 TEXT NOT NULL,
    )
    """
)

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
        INSERT INTO questions (question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        VALUES (?, ?, ?, ?, ?)
        """,
        (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3),
    )
    connection.commit()
    print_green("Question added successfully!")
except sqlite3.Error as e:
    print_red(f"Failed to add question: {e}")
finally:
    connection.close()
