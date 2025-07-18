#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
import os
from datetime import datetime

from fedlead_agent_crewai.crew import FedleadAgentCrewai

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
    load_dotenv(dotenv_path=env_path, override=True)
    
    inputs = {
        "username": os.getenv("LOGIN_USERNAME"),
        "password": os.getenv("LOGIN_PASSWORD"),
        "totp_secret": os.getenv("TOTP_SECRET")
    }

    try:
        crew_instance = FedleadAgentCrewai(inputs=inputs)
        result = crew_instance.crew().kickoff()
        return result or "Successfully ran fedlead_agent crew"
    except Exception as e:
        return f"Error: {e}"


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        FedleadAgentCrewai().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FedleadAgentCrewai().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        FedleadAgentCrewai().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
    
if __name__ == "__main__":
    run()
