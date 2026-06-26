import os
from dotenv import load_dotenv
from google import genai

# ─────────────────────────────────────────────
# LLM SETUP — Direct, no-nonsense connection
# ─────────────────────────────────────────────
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in .env file.")
        _client = genai.Client(api_key=api_key)
    return _client



# ─────────────────────────────────────────────
# BASE PROMPT TEMPLATE
# ─────────────────────────────────────────────
def base_prompt(role: str, query: str, context: str) -> str:
    ctx_section = f"CONTEXT:\n{context}\n" if context and context.strip() else ""
    return f"""You are an AI Study Assistant.

ROLE:
{role}

{ctx_section}USER QUESTION:
{query}

INSTRUCTIONS:
- Use the context as your primary source. If insufficient, use general knowledge.
- Be clear, structured, and concise.
- Do not add unnecessary preamble or filler text.

ANSWER:
"""

# ─────────────────────────────────────────────
# AGENT PROMPTS
# ─────────────────────────────────────────────
def explainer_prompt(query: str, context: str) -> str:
    return base_prompt(
        role="Explain concepts in simple, student-friendly language with clear examples.",
        query=query,
        context=context
    )

def planner_prompt(query: str, context: str) -> str:
    return base_prompt(
        role=(
            "Create a detailed, structured study plan with days, topics, and time allocation. "
            "Format timetables as Markdown tables with columns: | Day | Time | Topic | Task |"
        ),
        query=query,
        context=context
    )

def quiz_prompt(query: str, context: str) -> str:
    return f"""You are an AI quiz generator.

TASK:
{query}

CONTEXT:
{context if context and context.strip() else "Use your general knowledge about the topic."}

OUTPUT FORMAT (strict valid JSON, no other text):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "The correct option text",
      "explanation": "Why this answer is correct."
    }}
  ]
}}

Generate exactly the requested number of questions. Output only the JSON object, nothing else.
"""

def summary_prompt(query: str, context: str) -> str:
    return base_prompt(
        role="Summarize content into clear key points, definitions, and short revision notes.",
        query=query,
        context=context
    )

# ─────────────────────────────────────────────
# PROMPT SELECTOR
# ─────────────────────────────────────────────
def get_prompt(agent_type: str, query: str, context: str) -> str:
    if agent_type == "planner":
        return planner_prompt(query, context)
    elif agent_type == "quiz":
        return quiz_prompt(query, context)
    elif agent_type == "summary":
        return summary_prompt(query, context)
    else:
        return explainer_prompt(query, context)

# ─────────────────────────────────────────────
# CORE AGENT RUNNER — Clean & Simple
# ─────────────────────────────────────────────
def run_agent(query: str, agent_type: str, context: str = "", history: list = None) -> str:
    """
    Core function: builds prompt → calls LLM → returns response string.
    No CrewAI orchestration. No multi-agent chaining. Just clean LLM calls.
    """
    prompt = get_prompt(agent_type, query, context)
    
    if history:
        history_to_use = history[:-1] if history[-1].get("role") == "user" and history[-1].get("content") == query else history
        if history_to_use:
            hist_text = "CHAT HISTORY:\n"
            for msg in history_to_use:
                hist_text += f"{msg['role'].capitalize()}: {msg['content']}\n"
            hist_text += "\n\n"
            prompt = hist_text + prompt

    client = get_client()
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        result_text = response.text if hasattr(response, 'text') else str(response)
        return result_text if result_text.strip() else "⚠️ AI returned an empty response. Please try again."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"

# ─────────────────────────────────────────────
# LEGACY COMPATIBILITY — keeps all other files working
# ─────────────────────────────────────────────
def run_study_crew(task_description: str, task_type: str = "explain", context: str = "", history: list = None) -> str:
    """
    Drop-in replacement for the old CrewAI run_study_crew().
    Maps old task_type names → new agent_type names.
    All existing callers (quiz_ui, planner_ui, etc.) continue to work unchanged.
    """
    type_map = {
        "explain": "explainer",
        "plan":    "planner",
        "quiz":    "quiz",
        "summary": "summary",
    }
    agent_type = type_map.get(task_type, "explainer")
    return run_agent(task_description, agent_type, context, history)
