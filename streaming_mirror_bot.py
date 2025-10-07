import streamlit as st
import random
import time

st.title("Streaming echo chat with Session management")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Streamed response emulator - now echoes the user input
    def response_generator(user_input):
        # Echo the user's input with a prefix
        echo_response = f"You said: {user_input}"
        for word in echo_response.split():
            yield word + " "
            time.sleep(0.05)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        # Check if write_stream is available (Streamlit >= 1.31.0)
        if hasattr(st, 'write_stream'):
            response = st.write_stream(response_generator(prompt))
        else:
            # Fallback for older versions
            response_placeholder = st.empty()
            full_response = ""
            for chunk in response_generator(prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.05)
            response_placeholder.markdown(full_response)
            response = full_response
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
