import os
import argparse

from pathlib import Path

queries_base_dir = "queries"
answers_base_dir = "answers"


def main(args: dict):
    resp_dir = args["resp_dir"]
    if len(os.listdir(resp_dir)) == 0:
        print("No responses found in " + resp_dir)
        return

    # Directory management
    res_path_name = Path(resp_dir).name
    queries_dir = os.path.join(queries_base_dir, res_path_name)
    answers_dir = os.path.join(answers_base_dir, res_path_name)
    os.makedirs(answers_dir, exist_ok=True)
    print("Corresponding queries dir: " + queries_dir)
    print("Corresponding answers dir: " + answers_dir)

    for resp_file in os.listdir(resp_dir):
        all_text = ""
        with open(os.path.join(resp_dir, resp_file), "r") as f:
            all_text = f.read()

        all_text = all_text.split("Regenerate response")[0]

        # Remove the query from the response
        with open(os.path.join(queries_dir, resp_file), "r") as f:
            query = f.read()

        answer = all_text.split(query)[1].strip()

        # Save answers to file
        with open(os.path.join(answers_dir, resp_file), "w") as f:
            f.write(answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resp_dir", type=str, required=True)
    arguments = parser.parse_args()
    main(vars(arguments))
