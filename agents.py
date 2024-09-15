import os
from crewai import Agent
from langchain_upstage import ChatUpstage


class HospitalReceptionAgents:
    def __init__(self): 
        self.llm = ChatUpstage(model='solar-pro')

    def receptionist_agent(self):
        return Agent(
            role="Hospital Receptionist",
            goal="""Understand what a patient needs help with and provide the necessary information to assign a doctor 
            and only if necessary, admit to ICU.""",
            backstory="""A patient has come to the hospital and is describing their symptoms. Help him by understanding 
            his needs and assigning a doctor. Don't make them wait. Assign them instantly. 
            Select from these doctors available: 'Dr. Ajay, Orthopedic' available from 6:30am to 7am, 'Dr. Johnson, Orthopedic' 
            available from 3:30am to 5:30am, 'Dr. Brown, Cardiologist' available in the evening, 'Dr. Kumar, Physician' available now.
            Check if they need to be admitted to the ICU. there are 2 ICUs available. ICU1 has 2 beds and ICU2 has 3 beds. ICU1 
            is available from 6:30am to 7am, ICU2 is available from 3:30am to 5:30am. One is specialized in heart and the other 
            in orthopedic.""",
            llm=self.llm,
            verbose=True
        )
