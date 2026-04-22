import streamlit as st
import requests
import json

st.title("🍕 Restaurant AI Chat")

st.write("Chat with our AI about pizza restaurants!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask about pizza restaurants..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post("http://localhost:8000/ask", json={"question": prompt, "session_id": "streamlit_chat"})
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    reviews = data["reviews"]
                    web_info = data["web_info"]
                    
                    # Format the response
                    full_response = f"**Answer:** {answer}\n\n**Relevant Reviews:**\n" + "\n".join(f"- {review}" for review in reviews)
                    if web_info:
                        full_response += f"\n\n**Web Info:** {web_info}"
                    
                    st.markdown(full_response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                else:
                    error_msg = "Sorry, I couldn't get a response. Please try again."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.write("---")
st.write("Powered by FastAPI with LangChain and Ollama.")