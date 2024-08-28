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
    row=$(sqlite3 ~/Projects/QUIZSH/data/questions.db "SELECT question, answer FROM questions ORDER BY RANDOM() LIMIT 1;")

    question=$(echo $row | cut -d '|' -f 1)
    correct_answer=$(echo $row | cut -d '|' -f 2)

    echo -e "${YELLOW}$question${NC}"

    num_words=$(echo "$correct_answer" | wc -w)
    num_letters=$(echo "$correct_answer" | tr -d '[:space:]' | wc -m)

    echo -e "\t${BLUE}Hint: The answer has $num_words words and $num_letters letters.${NC}"

    echo -n "> "
    read user_answer

    if [ "$user_answer" = "$correct_answer" ]; then
        echo -e "${GREEN}Good!${NC}"
    else
        echo -e "${RED}Oops... Try again!${NC}"
        echo -e "${RED}The correct answer is: $correct_answer${NC}"
        ask_question
    fi
}

ask_question

# Calculate the time spent on the quiz
end_time=$(date +%s)
time_spent=$((end_time - start_time))
echo "Time spent: $time_spent s"
