import os
from typing import TypedDict
from decouple import config
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# OpenRouter Setup
OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# LLM Initialization
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)

# 1. State Definition
class ApplicationState(TypedDict):
    name: str
    position: str
    company: str
    reason: str
    days: int
    application_text: str
    feedback: str      # AI reviewer ki feedback ya user ki instruction
    retry_count: int   # Counter for safety

# 2. Node: Generator
def generate_application(state: ApplicationState):
    # .get use karein taake agar pehli bar key na ho to crash na kare
    current_feedback = state.get('feedback', "")
    count = state.get('retry_count', 0)
    
    print(f"--- AI is drafting (Attempt {count + 1}) ---")
    
    prompt = f"""
    Write a formal leave application letter.
    Details: Name: {state['name']}, Position: {state['position']}, Company: {state['company']}, Reason: {state['reason']}, Days: {state['days']}
    
    Current Draft: {state.get('application_text', 'None')}
    
    INSTRUCTIONS/FEEDBACK: {current_feedback if current_feedback else 'Create a fresh professional draft.'}
    
    Task: Rewrite or update the application. 
    STRICT RULES:
    - DO NOT use placeholders like [Date], [Recipient Name], or brackets [].
    - Use realistic dates for April 2026.
    - Be professional and concise.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "application_text": response.content, 
        "retry_count": count + 1
    }

# 3. Node: Reviewer
def review_application(state: ApplicationState):
    print("--- AI Reviewer is checking quality ---")
    draft = state.get('application_text', "")
    
    review_prompt = f"""
    Review this application for placeholders or unprofessional tone:
    "{draft}"
    
    If it has ANY square brackets [] or placeholders like '[Date]', reply exactly with 'REJECTED: [Reason]'.
    If it is perfect, reply exactly with 'APPROVED'.
    """
    response = llm.invoke([HumanMessage(content=review_prompt)])
    return {"feedback": response.content}

# 4. Router Function
def decide_to_finish(state: ApplicationState):
    feedback = state.get('feedback', "").upper()
    # Agar APPROVED hai ya 3 attempts pure ho gaye hain
    if "APPROVED" in feedback or state.get('retry_count', 0) >= 3:
        print("--- Logic Finished ---")
        return END
    
    return "generate"

# 5. Graph Construction
def build_agent():
    workflow = StateGraph(ApplicationState)

    workflow.add_node("generate", generate_application)
    workflow.add_node("review", review_application)

    workflow.set_entry_point("generate")
    workflow.add_edge("generate", "review")

    workflow.add_conditional_edges(
        "review",
        decide_to_finish,
        {
            "generate": "generate",
            END: END
        }
    )

    return workflow.compile()

app = build_agent()