#!/bin/bash

# Run command
python gui_query_gpt.py --query_dir queries/rank_prompts_icl

# sleep for 5 seconds
sleep 5

# Run command
python gui_query_gpt.py --query_dir queries/crossings_prompts

# sleep for 5 seconds
sleep 5

# Run command
python gui_query_gpt.py --query_dir queries/transpose_prompts_icl
