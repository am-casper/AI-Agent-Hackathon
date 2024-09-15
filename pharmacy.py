from dotenv import load_dotenv
from crewai import Crew, Process
from agents import HospitalReceptionAgents
from tasks import pharmacy_task  
import agentops

agentops.init()
load_dotenv()

symptom = input("Enter the symptom: ")

agents = HospitalReceptionAgents()

pharmacist = agents.pharmacy_agent()

pharmacy = pharmacy_task(pharmacist, symptom)

crew = Crew(
    agents=[pharmacist], 
    tasks=[pharmacy],
    verbose=True,
)

result = crew.kickoff()
print(result)
