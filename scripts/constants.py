#!/usr/bin/env python3

# Filename: constants.py
# Created on: January 25, 2025
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

import os
from enum import Enum

# Colors for colored output
BLUE = "\033[94m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
END = "\033[0m"

DATA_DIR = "data"
SCRIPTS_DIR = "scripts"

# Path to the SQLite database
LOCAL_DB_PATH = DATA_DIR + "/questions.db"
FULL_DB_PATH = os.path.expanduser("~") + "/Projects/QUIZSH/" + LOCAL_DB_PATH

PYTHON_INTERPRETER = "python3"
ADD_CATEGORY_SCRIPT = SCRIPTS_DIR + "/add_category.py"
ADD_QUESTION_SCRIPT = SCRIPTS_DIR + "/add_question.py"

CREATE_CATEGORY_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
"""

CREATE_QUESTIONS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    wrong_answer1 TEXT NOT NULL,
    wrong_answer2 TEXT NOT NULL,
    wrong_answer3 TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES category (id)
)
"""

CREATE_SETTINGS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    value TEXT NOT NULL
)
"""

INSERT_DEFAULT_SETTINGS_QUERY = """
INSERT OR IGNORE INTO settings (id, name, value)
VALUES (1, 'FILTER_BY_CATEGORY', 'all');
"""


class Setting(Enum):
    """
    Enum class for the settings in the database
    """

    FILTER_BY_CATEGORY_ID_ON_TABLE = 1
