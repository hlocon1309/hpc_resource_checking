#!/bin/sh

WHITE='\033[0;37m'
LGREEN='\033[1;32m'
LCYAN='\033[1;36m'

set -e
printf "Python Version: "
python3 --version
printf "${WHITE}\nInstalling Virtual Environment ... "
python3 -m venv src/venv
printf "${LGREEN}Done\n"
printf "${WHITE}Installing Requirements\n${LCYAN}"
cd src
python3 -m pip install -r ../requirements.txt
printf "${WHITE}... ${LGREEN}Done\n${WHITE}"