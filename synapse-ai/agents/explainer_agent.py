from crewai import Agent
from .planner_agent import get_llm

def create_explainer_agent():
    return Agent(
        role='Expert Explainer',
        goal='Explain complex concepts clearly using analogies and simple terms.',
        backstory='You are an incredibly patient and knowledgeable tutor. Your superpower is taking advanced topics and making them understandable for beginners without losing technical accuracy.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )
