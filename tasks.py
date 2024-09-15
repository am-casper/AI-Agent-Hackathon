import os
import requests
from crewai import Task


def reception_task(agent, symptom):
    return Task(
        description=symptom,
        agent=agent,
        # function=solar_task_function,  # Using Solar API
        expected_output="I am sorry to hear that. Let me understand your symptoms."
    )
