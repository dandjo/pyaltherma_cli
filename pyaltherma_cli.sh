#!/bin/bash

source ~/.venv/pyaltherma_cli/bin/activate
python3 $(dirname "$(realpath "$0")")/pyaltherma_cli.py $@
deactivate
