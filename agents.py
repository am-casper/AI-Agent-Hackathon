import os
from crewai import Agent
from langchain_upstage import ChatUpstage 
from textwrap import dedent


class HospitalReceptionAgents:
    def __init__(self): 
        self.llm = ChatUpstage(model='solar-pro')

    def receptionist_agent(self):
        return Agent(
            role="Hospital Receptionist",
            goal=dedent("""\
                        Help a patient by understanding their medical symptoms and assigning them a doctor.
                    """),
            backstory=dedent("""\
                        You are a hospital receptionist. You are the first point of contact for patients.
                        Patients come to you with their symptoms {symptom} and you assign them to the right doctor.
                        """),
            llm=self.llm,
            verbose=True
        )
    
    def icu_nurse_agent(self):
        return Agent(
            role="ICU Nurse",
            goal=dedent("""\
                        Help a patient by understanding their medical symptoms and assigning them to the ICU.
                    """),
            backstory=dedent("""\
                        You are an ICU nurse. You are responsible for assigning patients to the ICU.
                        Patients come to you with their symptoms {symptom} and you assign them to the right ICU.
                        It's not necessary to assign all patients to the ICU.
                        """),
            llm=self.llm,
            verbose=True
        )
        
    def manager_agent(self):
        return Agent(
            role="Manager",
            goal="Manage the hospital reception and ICU tasks. Return the final output as soon as possible. Don't put a lot of thought, do what your instincts say.",
            backstory="Compile {doctor} and {icu} and return the final output. Output should contain the doctor assigned to the patient and the ICU assigned (if any) to the patient.",
            llm=ChatUpstage(model='solar-pro'),
            verbose=True,
            # allow_delegation=True
            )
        
    def pharmacy_agent(self):
        return Agent(
            role="Pharmacist",
            goal="Help a patient by understanding their prescription and providing them with the right medicine.",
            backstory="You are a pharmacist. You are responsible for providing the right medicine to the patients. Patients describe the problem, you analyze and decide if they need doctor assistance, if no, you provide the medicine.",
            llm=ChatUpstage(model='solar-pro'),
            verbose=True
        )

