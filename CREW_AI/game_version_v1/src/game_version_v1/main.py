#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from game_version_v1.crew import GameVersionV1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    inputs = {}
    try:
        crew_instance = GameVersionV1().crew()
        result = crew_instance.kickoff(inputs=inputs)

        # Save HTML if game_developer output is present
        if 'game_creation_task' in result:
            game_code = result['game_creation_task']
            with open('game.html', 'w', encoding='utf-8') as f:
                f.write(strip_markdown_code_block(game_code))

    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def strip_markdown_code_block(content):
    # Remove triple backticks and optional language specifier
    lines = content.strip().splitlines()
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)


