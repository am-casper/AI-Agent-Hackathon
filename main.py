from dotenv import load_dotenv
from crewai import Crew
from agents import receptionist_agent
from tasks import reception_task

load_dotenv()

symptom = input("Enter the symptom: ")

receptionist = receptionist_agent()

reception = reception_task(receptionist, symptom)

crew = Crew(agents=[receptionist], tasks=[reception])

result = crew.kickoff()

print(result)
