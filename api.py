from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import DuckDuckGoSearchRun
from vector import retriever
import uvicorn

app = FastAPI(title="Restaurant Review AI API")

# Web search tool and LLM are created when the app starts
prompt = ChatPromptTemplate.from_template(
    """
You are an expert in answering questions about pizza restaurants. Use the provided reviews and external knowledge to answer accurately.

Relevant reviews: {reviews}

External knowledge: {web_info}

{question}
"""
)

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    return InMemoryChatMessageHistory()

@app.on_event("startup")
async def startup_event():
    app.state.model = OllamaLLM(model="llama3.2")
    app.state.search_tool = DuckDuckGoSearchRun()
    app.state.runnable = RunnableWithMessageHistory(
        prompt | app.state.model,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        reviews = retriever.invoke(request.question)
        reviews_text = "\n".join([doc.page_content for doc in reviews])
        
        # Web search for additional info
        web_results = app.state.search_tool.run(f"restaurant pizza {request.question}")
        
        result = app.state.runnable.invoke(
            {"question": request.question, "reviews": reviews_text, "web_info": web_results},
            config={"configurable": {"session_id": request.session_id}}
        )
        return {"answer": result, "reviews": [doc.page_content for doc in reviews], "web_info": web_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Restaurant Review AI API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)