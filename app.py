from langchain_community.llms import Ollama
import streamlit as st

llm=Ollama(model="llama3")

st.title("Chatbot using Llama3")

prompt = st.text_area("Enter your prompt:")

if st.button("Generate"):
    if prompt:
        # specific instructions to the prompt
        modified_prompt = f"Respond concisely with health-oriented advice: {prompt}"
        with st.spinner("Generating response..."):
            st.write_stream(llm.stream(modified_prompt,stop=['<|eot_id|>']))



