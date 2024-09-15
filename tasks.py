import os
import requests
from crewai import Task
from textwrap import dedent
import csv
from datetime import time

def load_doctors_from_csv(csv_file):
        """Load doctor data from a CSV file and return a list of doctor dictionaries."""
        doctors = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                start_time = parse_time(row['start time'])
                end_time = parse_time(row['end time'])
                doctors.append({
                    'id': row['id'],
                    'name': row['name'],
                    'degree': row['degree'],
                    'start_time': start_time,
                    'end_time': end_time
                })
        return doctors

def parse_time(time_str):
        """Convert a time string (e.g. '06:30:00') into a time object."""
        hours, minutes, seconds = map(int, time_str.split(':'))
        return time(hour=hours, minute=minutes, second=seconds)


def reception_task(agent, symptom):
    csv_file = 'doctors.csv'
    doctors = load_doctors_from_csv(csv_file)

    doctor_info = "\n".join(
        [f"{doc['name']} ({doc['degree']}) available from {doc['start_time']} to {doc['end_time']}" for doc in doctors]
    )
    return Task(
        description=dedent(f"""\
            A patient comes to the hospital reception with symptom {symptom}. 
            The receptionist needs to understand the symptom and assign the patient to the right doctor. 
            The patient can come any time of the day.
            Available doctors: {doctor_info}
        """),
        agent=agent,
        expected_output=dedent(f"""\
            A single word describing the doctor assigned to the patient based on their symptom.
        """),
    )
