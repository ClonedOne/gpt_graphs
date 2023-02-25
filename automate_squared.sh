#!/bin/bash

# Run command
python gui_query_gpt.py --query_dir queries/transpose_prompts_no_steps_median_continuation

# sleep for 5 seconds
sleep 5

# Run command
python gui_query_gpt.py --query_dir queries/transpose_prompts_steps_median_continuation

# sleep for 5 seconds
sleep 5

# Run command
# python gui_query_gpt.py --query_dir queries/crossings_prompts_steps
