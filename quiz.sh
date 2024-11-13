#!/usr/bin/env sh

# Filename: quiz.sh
# Created on: June 20, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

# This script is a simple quiz game that asks questions from a SQLite database.

. scripts/utils.sh

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
    print_yellow "$question"
    for i in "${!answers[@]}"; do
        echo "$i) ${answers[$i]}"
    done

    # Read user's answer
    print_blue "> Choose the correct answer (0-3): " -n
    read user_choice

    # Check if the answer is correct
    if [ "$user_choice" -eq "$correct_index" ]; then
        print_green "Good!"
    else
        print_red "Oops... Try again!"
        print_blue "The correct answer was: $correct_answer"
        ask_question
    fi
}

ask_question

# Calculate the time spent on the quiz
end_time=$(date +%s)
time_spent=$((end_time - start_time))
echo "Time spent: $time_spent s"
