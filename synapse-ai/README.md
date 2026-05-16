# SynapseAI – Multi-Agent AI Study Assistant

SynapseAI is a modern, futuristic, and premium AI SaaS application built to revolutionize the way students study. Powered by a multi-agent AI architecture, it helps you digest heavy study materials, organize your schedules, and test your knowledge interactively.

![SynapseAI Cover](assets/logo/cover-placeholder.png)

## Features

- **Multi-Agent Collaboration:** Dedicated agents for Planning, Explaining, Summarizing, and Quizzing.
- **RAG-Powered Chat:** Upload your PDFs, and chat with your documents directly. The system retrieves precise context for accurate answers.
- **Automated Quizzes:** Generate MCQs and short-answer questions from uploaded materials to test your knowledge.
- **Study Planner:** Create structured, optimized study plans tailored to your syllabus.
- **Premium UI/UX:** A futuristic glassmorphic dark-mode dashboard providing a real AI SaaS feel.
- **Conversational Memory:** AI remembers context throughout your study session.

## Tech Stack

- **Frontend:** Streamlit
- **Backend Framework:** Python
- **AI Agent Framework:** CrewAI
- **LLM:** Google Gemini API
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **PDF Processing:** PyPDF2

## Architecture Overview

SynapseAI utilizes a pipeline where user documents are processed, chunked, and embedded into a ChromaDB vector store. When users interact with the app, their queries are augmented with relevant document contexts (RAG) and passed to specialized CrewAI agents.

## Installation Guide

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/synapse-ai.git
   cd synapse-ai
   ```

2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Copy `.env.example` to `.env` and configure your API keys.
   ```bash
   cp .env.example .env
   ```
   *Add your Google Gemini API key to the `.env` file.*

## Running the Application

Start the Streamlit application by running:
```bash
streamlit run app.py
```

## Deployment Guide

### Streamlit Cloud
1. Push this repository to GitHub.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click "New app", select your repository, branch, and set the main file path to `app.py`.
4. Add your `.env` secrets in the Streamlit Cloud advanced settings.
5. Deploy!

## Future Improvements
- Voice input / Text-to-speech integration
- Study streak tracker & productivity analytics
- Authentication system
- Flashcard generation and export functionality

## Contribution Guidelines
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
