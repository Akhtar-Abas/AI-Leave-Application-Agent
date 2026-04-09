# 🚀 AI Leave Application Agent (LangGraph + Gemini)

An intelligent HR assistant that automates leave applications through an **Agentic Workflow**. Built with **LangGraph** for iterative feedback loops and **Gemini 2.0 Flash** for reasoning.

## ✨ Key Features
- **Agentic Workflow:** Uses LangGraph to manage the "Draft -> Review -> Refine" cycle.
- **Human-in-the-Loop:** Allows users to provide real-time feedback to the AI.
- **Strict Quality Control:** An automated Reviewer Node ensures no placeholders (like [Date]) are left.
- **Professional PDF Export:** Generates clean, ready-to-print PDFs.

## 🛠️ Tech Stack
- **Backend:** Django
- **AI Logic:** LangGraph, LangChain
- **LLM:** Google Gemini 2.0 (via OpenRouter)
- **Formatting:** ReportLab (PDF)

## 🚀 How to Run
1. Clone the repo: `git clone [your-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `OPENROUTER_API_KEY` to a `.env` file.
4. Run server: `python manage.py runserver`