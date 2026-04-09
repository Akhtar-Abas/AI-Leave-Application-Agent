import os
from typing import TypedDict
from decouple import config
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# OpenRouter Configuration
llm = ChatOpenAI(
    model="google/gemini-2.0-flash-001",
    api_key=config("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

class ApplicationState(TypedDict):
    name: str
    position: str
    company: str
    reason: str
    days: int
    application_text: str

def generate_node(state: ApplicationState):
    prompt = f"Write a formal leave application for {state['name']}, working as {state['position']} at {state['company']}. Reason: {state['reason']}, Days: {state['days']}."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"application_text": response.content}

# Graph Setup
workflow = StateGraph(ApplicationState)
workflow.add_node("generate", generate_node)
workflow.set_entry_point("generate")
workflow.add_edge("generate", END)
app = workflow.compile()