from crewai import Agent
from .planner_agent import get_llm

def create_quiz_agent():
    return Agent(
        role='Quiz Generator',
        goal='Create challenging and educational quizzes, MCQs, and short-answer questions from provided materials.',
        backstory='You are a strict but fair examiner who knows exactly how to test a student\'s true understanding of a subject. You always provide correct answers and explanations.',
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )
