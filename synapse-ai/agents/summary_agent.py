from crewai import Agent
from .planner_agent import get_llm

def create_summary_agent():
    return Agent(
        role='Content Summarizer',
        goal='Extract key concepts, definitions, and highlights to create concise revision notes.',
        backstory='You are a master of efficiency. You can read a 100-page document and extract the 5 pages of absolute essential information needed to pass an exam.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )
