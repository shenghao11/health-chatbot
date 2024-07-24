import streamlit as st
from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Custom CSS to hide Streamlit menu and watermark
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)   

def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """    
    
    # Get Groq API key
    #groq_api_key ='api_key'
    groq_api_key=st.secrets['API_TOKEN']
    
    # The title and greeting message of the Streamlit application
    st.title("Health Chatbot")
    st.write("Hello! I'm your friendly chatbot. You can ask me any health related question!")
    
    system_prompt = "Respond concisely with health-oriented advice, and limit the output to 500 characters."
    model = 'llama3-8b-8192'
    conversational_memory_length = 10
    
    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)
    
    # session state variable
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    else:
        for message in st.session_state.chat_history:
            memory.save_context(
                {'input': message['human']},
                {'output': message['AI']}
            )
    
    with st.form(key='chat_form'):
        user_question = st.text_input("Ask a question:")
        submit_button = st.form_submit_button("Enter")

    # If the form is submitted (either by pressing Enter key or clicking the button),
    if submit_button and user_question:
        
        # Initialize Groq Langchain chat object and conversation
        groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
        )
        
        # Construct a chat prompt template using various components
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),  # This is the persistent system prompt that is always included at the start of the chat.
                MessagesPlaceholder(variable_name="chat_history"),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.
                HumanMessagePromptTemplate.from_template("{human_input}"),  # This template is where the user's current input will be injected into the prompt.
            ]
        )
        
        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        conversation = LLMChain(
            llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
            prompt=prompt,  # The constructed prompt template.
            verbose=True,   # Enables verbose output, which can be useful for debugging.
            memory=memory,  # The conversational memory object that stores and manages the conversation history.
        )
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation.predict(human_input=user_question)
        
        # Limit the response to 500 characters
        limited_response = response[:500]
        
        message = {'human': user_question, 'AI': limited_response}
        st.session_state.chat_history.append(message)
        
        st.write(limited_response)

if __name__ == "__main__":
    main()



