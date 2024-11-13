#!/usr/bin/env sh

# Filename: add_question.sh
# Created on: June 20, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

# This script adds a new question to the database. It receives the question
# text and the correct answer as arguments. The script will then ask the user
# for the wrong answers and add the question to the database

. scripts/utils.sh

# Check if the user provided the correct number of arguments
if [ $# -lt 1 ]; then
	echo "Usage: $0 <question> <correct_answer>"
	exit 1
fi

# Get the question and the correct answer
question="$1"
correct_answer="$2"

# Confirm the question and the answer
echo "Question: $question"
echo "Correct answer: $correct_answer"
print_blue "Is this question correct? (y/n): " -n

read confirmation

if [ "$confirmation" != "y" ]; then
	print_red "Aborting!"
	exit 1
fi

# Prompt for the two wrong answers
while true; do
	echo -n "Enter the first wrong answer: "
	read wrong_answer1
	echo -n "Enter the second wrong answer: "
	read wrong_answer2
	echo -n "Enter the third wrong answer: "
	read wrong_answer3

	echo "First wrong answer: $wrong_answer1"
	echo "Second wrong answer: $wrong_answer2"
	echo "Third wrong answer: $wrong_answer3"

	print_blue "Are these the wrong answers? (y/n): " -n
	read confirmation

	if [ "$confirmation" = "y" ]; then
		break
	fi
done

# Create the table if it does not exist
sqlite3 data/questions.db <<EOF
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL,
    wrong_answer3 TEXT NOT NULL
);
EOF

exists=$(sqlite3 data/questions.db "SELECT COUNT(*) FROM questions WHERE question='$question';")

if [ "$exists" -ne 0 ]; then
	print_red "Question already exists in the database!"
	exit 1
fi

# Insert the question with answers into the database
sqlite3 data/questions.db <<EOF
INSERT INTO questions (question, answer, wrong_answer1, wrong_answer2, wrong_answer3) VALUES
    ('$question', '$correct_answer', '$wrong_answer1', '$wrong_answer2', '$wrong_answer3')
EOF

# Check if the question was added successfully
if [ $? -eq 0 ]; then
	print_green "Question added successfully!"
else
	print_red "Failed to add question!"
fi
