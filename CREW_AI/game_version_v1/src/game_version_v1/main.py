#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

sys.path.append(os.path.abspath("/content/drive/MyDrive/game_version_v1/src"))

from game_version_v1.crew import GameVersionV1
# from crewai.output import CrewOutput

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    inputs = {
        "template_path": "../../Game Template.html",
        "platform": "mobile + desktop",
        "difficulty": "intermediate",
        "player_features": ["torchlight", "dynamic maze", "hidden keys"]
    }

    with open(inputs["template_path"], "r") as file:
      template_content = file.read()

    inputs["html_template"] = template_content

    try:
      crew_obj = GameVersionV1().crew()

      result = crew_obj.kickoff(inputs=inputs)

      output_dir = "game_outputs"
      os.makedirs(output_dir, exist_ok=True)

      for task in crew_obj.tasks:
        task_output = task.output
        task_name = task.name.replace(" ", "_").lower()
        filename = f"{task_name}_output.txt"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, "w") as f:
            f.write(str(task_output or "No output."))

      with open("game_outputs/crew_output.txt", "w") as f:
          f.write(str(result))
      print("Output saved to 'game_outputs/crew_output.txt'")
    except Exception as e:
        raise Exception(f"❌ Error running crew: {e}")

if __name__ == "__main__":
    run()
