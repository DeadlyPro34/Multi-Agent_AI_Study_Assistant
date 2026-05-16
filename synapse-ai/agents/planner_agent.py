import os
from crewai import Agent, LLM
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Shared LLM getter used by all agents."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in .env file.")
    return LLM(
        model="gemini/gemini-2.0-flash",
        temperature=0.7,
        api_key=api_key,
        max_retries=3
    )

def create_planner_agent():
    return Agent(
        role='Study Planner',
        goal='Create realistic and optimized study schedules.',
        backstory='You are an expert academic coach who creates clear, actionable study plans.',
        verbose=False,
        allow_delegation=False,
        llm=get_llm()
    )
