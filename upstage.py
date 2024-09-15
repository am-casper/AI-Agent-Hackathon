import os
import requests
from crewai import Agent, Task, Crew
from langchain_community.chat_models.solar import SolarChat
from langchain_upstage import ChatUpstage
import datetime

SOLAR_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"  # Replace with the actual URL
SOLAR_API_KEY = os.getenv("SOLAR_API_KEY")  # Replace with the actual API key

# solar = SolarChat(model='solar-pro')
solar = ChatUpstage(model='solar-pro')


def solar_task_function(task):
    prompt = task.description
    headers = {
        "Authorization": f"Bearer {SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 1 # Adjust as needed
    }
    response = requests.post(SOLAR_API_URL, headers=headers, json=data)
    response_json = response.json()
    return response_json.get("choices", [{}])[0].get("text", "No response from Solar API")

# Define CrewAI agents
receptionistAgent = Agent(
    role="Hospital Receptionist",
    goal="Understand what a patient needs help with and provide the necessary information to assign a doctor and only if necessary, admit to ICU.",
    backstory=f"""A patient has come to the hospital and is describing their symptoms. 
    Help him by understanding his needs and assigning a doctor. 
    Don't make them wait. Assign them instantly. Allot the doctor based on their availability. 
    Select from these doctors available: 'Dr. Ajay, Orthopedic' available from 6:30am to 7am, 'Dr. Johnson, Orthopedic' available from 3:30am to 5:30am, 'Dr. Brown, Cardiologist' available in the evening, 'Dr. Kumar, Physician' available now.
    Check if they need to be admitted to the ICU. there are 2ICUs available. ICU1 has 2 beds and ICU2 has 3 beds. ICU1 is available from 6:30am to 7am, ICU2 is available from 3:30am to 5:30am. One is specialised in heart and the other in orthopedic.""",
    llm=solar,
    verbose=True
)

symptom = input("Enter the symptom: ")
# Define CrewAI tasks
receptionTask = Task(
    description=symptom,
    agent=receptionistAgent,
    function=solar_task_function,  # Using Solar API
    expected_output="I am sorry to hear that. Let me understand your symptoms."
)


# Create CrewAI Crew and assign the tasks
crew = Crew(agents=[receptionistAgent, ], tasks=[receptionTask, ])

result = crew.kickoff()
print(result)
