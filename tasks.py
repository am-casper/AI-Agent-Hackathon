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

def load_icus_from_csv(csv_file):
        """Load ICU data from a CSV file and return a list of ICU dictionaries."""
        icus = []
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                icus.append({
                    'id': row['id'],
                    'icu_no': row['icu number'],
                    'capacity': int(row['capacity']),
                    'specialization': row['specialization'],
                    'start_time': parse_time(row['start time']),
                    'end_time': parse_time(row['end time'])
                })
        return icus

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
        verbose=True,
        expected_output=dedent(f"""\
            A single word describing the doctor assigned to the patient based on their symptom.
        """),
    )

def icu_task(agent, symptom):
    icu_file='icu.csv'
    icus = load_icus_from_csv(icu_file)
    
    icu_info = "\n".join(
        [f"ICU {icu['icu_no']} ({icu['specialization']}) available from {icu['start_time']} to {icu['end_time']}" for icu in icus]
    )
    
    return Task(
        description=dedent(f"""\
            A patient comes to the ICU with symptom {symptom}. 
            The ICU nurse needs to understand the symptom and assign the patient to the ICU.
            The patient can come any time of the day.
            Available ICUs: {icu_info}
        """),
        agent=agent,
        verbose=True,
        expected_output=dedent(f"""\
            A single word describing the ICU assigned to the patient based on their symptom.
        """),
    )
    
def manager_task(agent):
    return Task(
        description="Manage the hospital reception and ICU tasks. Return the final output as soon as possible. Don't put a lot of thought, do what your instincts say.",
        agent=agent,
        verbose=True,
        expected_output="A single word describing the doctor and ICU assigned to the patient based on their symptom.",
    )