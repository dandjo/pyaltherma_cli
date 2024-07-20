#!/bin/bash

source ~/.venv/pyaltherma_cli/bin/activate
python3 -m pyaltherma_cli $@
deactivate
