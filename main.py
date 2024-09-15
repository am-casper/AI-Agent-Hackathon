from dotenv import load_dotenv
from crewai import Crew, Process
from agents import HospitalReceptionAgents
from tasks import icu_task, reception_task, manager_task    
import agentops

agentops.init()
load_dotenv()

symptom = input("Enter the symptom: ")

agents = HospitalReceptionAgents()

receptionist = agents.receptionist_agent()
icu_nurse = agents.icu_nurse_agent()
manager = agents.manager_agent()

reception = reception_task(receptionist, symptom)
icu = icu_task(icu_nurse, symptom)
maanger_task = manager_task(manager)

crew = Crew(
    agents=[receptionist, icu_nurse], 
    tasks=[reception, icu],
    verbose=True,
    process=Process.sequential,  # Specifies the hierarchical management approach
    # memory=True,  # Enable memory usage for enhanced task execution
    manager_agent=manager,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    )

result = crew.kickoff()

print(result)
