#!/usr/bin/env python3

# Filename: csv_to_sqlite.py
# Created on: November 11, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import csv
import sqlite3
import argparse

parser = argparse.ArgumentParser(description='Importa dados de um arquivo CSV para um banco de dados SQLite.')
parser.add_argument('csv_file', type=str, help='Nome do arquivo CSV a ser importado')
parser.add_argument('db_file', type=str, help='Nome do arquivo de banco de dados SQLite')

args = parser.parse_args()

# Connect to database
conn = sqlite3.connect(args.db_file)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL,
    wrong_answer3 TEXT NOT NULL
)
''')

# Read CSV file and insert data into database, if it doesn't exist
with open(args.csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('SELECT 1 FROM questions WHERE question = ?', (row['question'],))
        if cursor.fetchone() is None:  # If the question doesn't exist in the database
            wrong_answer1 = row.get('wrong_answer1')
            wrong_answer2 = row.get('wrong_answer2')
            wrong_answer3 = row.get('wrong_answer3')

            cursor.execute('''
                INSERT INTO questions (question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['question'], row['answer'], wrong_answer1, wrong_answer2, wrong_answer3))
        else:
            print(f"A pergunta '{row['question']}' já existe no banco de dados e foi ignorada.")

conn.commit()
conn.close()

print("Dados importados com sucesso para o banco de dados SQLite.")
