#!/usr/bin/env sh

# Filename: quiz.sh
# Created on: June 20, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

# This script is a simple quiz game that asks questions from a SQLite database.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Calculate the time spent on the quiz
start_time=$(date +%s)

ask_question() {
    # Fetch question and answers from the database
    row=$(sqlite3 ~/Projects/QUIZSH/data/questions.db "SELECT question, answer, wrong_answer1, wrong_answer2, wrong_answer3 FROM questions ORDER BY RANDOM() LIMIT 1;")

    question=$(echo $row | cut -d '|' -f 1)
    correct_answer=$(echo $row | cut -d '|' -f 2)
    wrong_answer1=$(echo $row | cut -d '|' -f 3)
    wrong_answer2=$(echo $row | cut -d '|' -f 4)
    wrong_answer3=$(echo $row | cut -d '|' -f 5)

    # Prepare the answer options array
    answers=("$correct_answer" "$wrong_answer1" "$wrong_answer2" "$wrong_answer3")

    # Shuffle the answer options and keep track of the correct answer's index
    for i in $(seq 0 3); do
        j=$((RANDOM % 4))
        temp=${answers[$i]}
        answers[$i]=${answers[$j]}
        answers[$j]=$temp
    done

    # Find the index of the correct answer in the shuffled array
    for i in "${!answers[@]}"; do
        if [ "${answers[$i]}" = "$correct_answer" ]; then
            correct_index=$i
            break
        fi
    done

    # Display the question and answer options
    echo -e "${YELLOW}$question${NC}"
    for i in "${!answers[@]}"; do
        echo "$i) ${answers[$i]}"
    done

    # Read user's answer
    echo -n "> Choose the correct answer (0-3): "
    read user_choice

    # Check if the answer is correct
    if [ "$user_choice" -eq "$correct_index" ]; then
        echo -e "${GREEN}Good!${NC}"
    else
        echo -e "${RED}Oops... Try again!${NC}"
        echo -e "${RED}The correct answer was: $correct_answer${NC}"
        ask_question
    fi
}

ask_question

# Calculate the time spent on the quiz
end_time=$(date +%s)
time_spent=$((end_time - start_time))
echo "Time spent: $time_spent s"
