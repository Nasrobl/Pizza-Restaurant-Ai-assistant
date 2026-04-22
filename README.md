# Restaurant Review AI

An AI-powered system for answering questions about restaurant reviews using LangChain, Ollama, and vector search.

## Features
- Conversational Q&A with memory
- Vector-based review retrieval
- Web search integration (RAG)
- REST API with FastAPI
- Web UI with Streamlit
- Batch preprocessing with spaCy
- Docker containerization

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

2. Ensure Ollama is running with llama3.2 model.

3. Run preprocessing:
   ```bash
   python preprocess.py
   ```

4. Run the API:
   ```bash
   python api.py
   ```

5. Run the Streamlit app (in another terminal):
   ```bash
   streamlit run streamlit_app.py
   ```

## Docker

Build and run:
```bash
docker build -t review-ai .
docker run -p 8000:8000 review-ai
```

## Deployment

- **Azure Container Apps**: Use Azure CLI to deploy the Docker image.
- **AWS ECS**: Push to ECR and deploy to ECS.

## Usage

- CLI: Run `python main.py`
- API: POST to `http://localhost:8000/ask` with JSON `{"question": "your question"}`
- Web: Open Streamlit app and ask questions.