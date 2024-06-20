#!/usr/bin/env sh

# Filename: add_question.sh
# Created on: June 20, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

# This script adds a new question to the database. It receives the question
# text and the correct answer as arguments. The script will then ask the user
# for the wrong answers and add the question to the database.


RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Check if the user provided the correct number of arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <question> <correct_answer>"
    exit 1
fi

# Get the question and the correct answer
question="$1"
correct_answer="$2"

# Confirm the question and the answer
echo "Question: $question"
echo "Correct answer: $correct_answer"
echo "Is this question correct? (y/n)"

read confirmation

if [ "$confirmation" != "y" ]; then
    echo -e "${RED}Aborting!${NC}"
    exit 1
fi

# Check database connection
if [ ! -f data/questions.db ]; then
    echo -e "${RED}Database not found!${NC}"
    exit 1
fi

# Create the table if it does not exist
sqlite3 data/questions.db <<EOF
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
EOF

exists=$(sqlite3 data/questions.db "SELECT COUNT(*) FROM questions WHERE question='$question';")

if [ "$exists" -ne 0 ]; then
    echo -e "${RED}Question already exists in the database!${NC}"
    exit 1
fi


# Insert the question into the database
sqlite3 data/questions.db <<EOF
INSERT INTO questions (question, answer) VALUES
    ('$question', '$correct_answer');
EOF

# Check if the question was added successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Question added successfully!${NC}"
else
    echo -e "${RED}Failed to add question!${NC}"
fi
