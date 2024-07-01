import streamlit as st
import replicate
import os

# App title
st.set_page_config(page_title="🦙💬 Llama 2 Chatbot")

# Set your Replicate API token
os.environ['REPLICATE_API_TOKEN'] = 'r8_4yonhGlo0t5hKRkv0myJCLXnevxhsOE3IZxrx'

# Model and parameters
llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
temperature = 0.1
top_p = 0.9
max_length = 120

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant."
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# User-provided prompt
prompt = st.text_area("Enter your prompt:")
if st.button("Generate"):
    with st.spinner("Generating response..."):
        response = generate_llama2_response(prompt)
        full_response = ''.join(response)
        st.write(full_response)
