from dotenv import load_dotenv
from crewai import Crew
from agents import HospitalReceptionAgents
from tasks import reception_task

load_dotenv()

symptom = input("Enter the symptom: ")

agents = HospitalReceptionAgents()

receptionist = agents.receptionist_agent()

reception = reception_task(receptionist, symptom)

crew = Crew(agents=[receptionist], tasks=[reception])

result = crew.kickoff()

print(result)
