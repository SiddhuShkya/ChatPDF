import streamlit as st 
from templates import css, bot_template, user_template
    
    
if "chat_history" not in st.session_state:
     st.session_state.chat_history = []
    
class History:
    
    def __init__(self):
        print("History class called")
    
    def app(self):
        st.title("History ⌛")
        st.write("---")
        # Add a select box to choose sorting order
        c1, c2, c3 = st.columns([2, 6, 2], gap='small')
        st.markdown(css, unsafe_allow_html=True)
        with c2:
            sort_order = st.selectbox(":green[Sort by:]", ["Newest to Oldest", "Oldest to Newest"])
            # Sort the chat history based on the selected order
            chat_history = st.session_state.chat_history
            if sort_order == "Newest to Oldest":
                sorted_history = sorted(chat_history, key=lambda x: x['time'], reverse=True)
            else:
                sorted_history = sorted(chat_history, key=lambda x: x['time'])
            # Display the sorted chat history
            for response in sorted_history:
                st.subheader(f':blue[{response["time"]}]')
                st.write(user_template.replace("{{MSG}}", response['question']), unsafe_allow_html=True)
                st.write(bot_template.replace("{{MSG}}", response['answer']), unsafe_allow_html=True)
                st.write("---")



        