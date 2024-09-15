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
                        Patients come to you with their symptoms and you assign them to the right doctor.
                        """),
            llm=self.llm,
            verbose=True
        )
