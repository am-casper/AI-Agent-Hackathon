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

crew1 = Crew(
    agents=[receptionist], 
    tasks=[reception],
    verbose=True,
    process=Process.sequential,  # Specifies the hierarchical management approach
    # memory=True,  # Enable memory usage for enhanced task execution
    # manager_agent=manager,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    )
crew2 = Crew(
    agents=[icu_nurse], 
    tasks=[icu],
    verbose=True,
    process=Process.sequential,  # Specifies the hierarchical management approach
    # memory=True,  # Enable memory usage for enhanced task execution
    # manager_agent=manager,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    )

crew3 = Crew(
    agents=[manager], 
    tasks=[maanger_task],
    verbose=True,
    process=Process.sequential,  # Specifies the hierarchical management approach
    # memory=True,  # Enable memory usage for enhanced task execution
    # manager_agent=manager,  # Optional: explicitly set a specific agent as manager instead of the manager_llm
    )

doctorAssigned = crew1.kickoff(inputs={
    'symptom': symptom
})

# print(doctorAssigned)

ICUAssigned = crew2.kickoff(inputs={
    'symptom': symptom
})

# print(ICUAssigned)

managerCrew = crew3.kickoff(inputs={
    "doctor": str(doctorAssigned),
    "icu": str(ICUAssigned)
})

print(managerCrew)
