#!/usr/bin/env sh

# Filename: utils.sh
# Created on: November 13, 2024
# Author: Lucas Araújo <araujolucas@dcc.ufmg.br>

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Print functions
# Usage: print_<color> "message" "options"
print_red() {
	echo -e $2 "${RED}$1${NC}"
}

print_green() {
	echo -e $2 "${GREEN}$1${NC}"
}

print_yellow() {
	echo -e $2 "${YELLOW}$1${NC}"
}

print_blue() {
	echo -e $2 "${BLUE}$1${NC}"
}
