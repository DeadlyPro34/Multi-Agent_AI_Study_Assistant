# SynapseAI - Multi-Agent AI Study Assistant

## Overview
SynapseAI is a premium, multi-agent study assistant designed to transform static study materials into dynamic, interactive learning experiences. By leveraging advanced AI orchestration, it analyzes uploaded documents and provides personalized study plans, detailed explanations, concise summaries, and interactive quizzes. All of this is wrapped in a sleek, modern glassmorphic interface to ensure a distraction-free and engaging study environment.

## Features
- **Intelligent Document Processing**: Upload and process PDF study materials seamlessly.
- **Multi-Agent Orchestration**: Utilizes specialized AI agents for distinct educational tasks:
  - *Planner Agent*: Creates structured study schedules and topic outlines.
  - *Explainer Agent*: Breaks down complex concepts into easy-to-understand explanations.
  - *Summarizer Agent*: Condenses large volumes of text into key takeaways.
  - *Quizzer Agent*: Generates interactive quizzes to test knowledge retention.
- **RAG Pipeline**: Integrates ChromaDB for fast document querying and accurate context retrieval.
- **Modern UI/UX**: A highly responsive, glassmorphic frontend built with Streamlit.
- **Robust Task Management**: Asynchronous processing and background task handling to ensure the UI remains smooth during heavy AI generation.

## Tech Stack
- **Frontend**: Streamlit
- **Backend/Logic**: Python
- **AI Framework**: CrewAI, LangChain
- **LLM**: Google Gemini 3.1 Pro
- **Vector Database**: ChromaDB

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/synapse-ai.git
   cd synapse-ai
   ```

2. **Create a virtual environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   Create a `.env` file in the root directory and configure your API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the project**
   ```bash
   streamlit run app.py
   ```

## Usage
1. Launch the application and open the provided `localhost` link in your browser.
2. Upload a PDF document containing your study material via the sidebar or main upload section.
3. Select the AI Agent you wish to interact with (Planner, Explainer, Summarizer, or Quizzer).
4. Use the chat interface to ask questions, request summaries, or take generated quizzes based on your document.

## Project Structure
```text
synapse-ai/
├── agents/             # CrewAI agent logic and role definitions
├── assets/             # Static assets like logos and images
├── components/         # Modular Streamlit UI components (Navbar, Cards, Upload)
├── database/           # Local ChromaDB vector storage
├── styles/             # Custom CSS files for glassmorphic styling
├── utils/              # Helper functions (e.g., PDF text extraction)
├── app.py              # Main Streamlit application entry point
├── requirements.txt    # Required Python packages
└── .env                # Environment variables configuration
```

## Configuration
The following environment variable is required to run the AI agents:
- `GEMINI_API_KEY`: Your Google Gemini API key.

## Future Improvements
- Support for additional file formats (e.g., DOCX, PPTX).
- User authentication to save and resume individual study sessions.
- Integration of web search tools to allow agents to supplement document knowledge with real-time web data.
- Implementation of a student progress tracking and analytics dashboard.

## Contributing
Contributions are always welcome! Feel free to fork the repository, create a feature branch, and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
