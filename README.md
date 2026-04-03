# AI Virtual Interviewer

A real-time AI-powered technical interviewer built with Streamlit and OpenAI.

## Features
- **Dynamic Question Generation**: Creates role-specific questions on the fly.
- **AI Evaluation**: Scores answers (0-10) and provides detailed feedback.
- **Performance Analytics**: Visualizes performance with interactive charts.

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key**:
   - Create a `.env` file (copy from `.env.example`).
   - Add your `OPENAI_API_KEY`.
   - OR enter it in the UI sidebar.

3. **Run Application**:
   ```bash
   streamlit run app.py
   ```

## Deployment within Docker
```bash
docker build -t ai-interviewer .
docker run -p 8501:8501 ai-interviewer
```
