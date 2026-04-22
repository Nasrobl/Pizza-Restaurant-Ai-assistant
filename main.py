from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import RetrievalQA
from vector import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about pizza restaurants:

here are some reviews : {reviews}

here is the question to answer : {question}
"""

prompt = ChatPromptTemplate.from_template(template)

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    return InMemoryChatMessageHistory()

runnable = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

while True:
    question = input("Ask your question (q to quit): ")
    if question == "q":
        break
    reviews = retriever.invoke(question)
    reviews_text = "\n".join([doc.page_content for doc in reviews])
    result = runnable.invoke({"reviews": reviews_text, "question": question}, config={"configurable": {"session_id": "cli"}})
    print(result)