# Graphs with LLMs?

Acqure the data with 
```bash
❯ python gui_query_gpt.py --query_dir queries/rank_prompts
```

This will save all the text on screen (in a separate file for each query file) in a folder called `responses/`.

These files can be processed with 
```bash
❯ python process_responses.py --resp_dir responses/rank_prompts
```
Which will create a single file per query with only the model's output text, in a folder called `answers/`.