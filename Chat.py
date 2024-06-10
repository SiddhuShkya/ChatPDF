import os
import base64
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from templates import css, bot_template, user_template
from streamlit_option_menu import option_menu
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores.faiss import FAISS 
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI


    
class Chat:
    
    def __init__(self, store_name=None, pdf_copy=None, vector_store=None):
        self.store_name = store_name
        self.pdf_copy = pdf_copy
        self.vector_store = vector_store
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.st.session_state.chat_history = []
        print("Chat class called")
        
    def check_embedding(self, store_name):
        return os.path.exists(f"./faiss_index/{store_name}")

    
    def get_conversational_chain(self):
        prompt_template = '''
        Answer the question as detailed as possible from the provided context. Make sure to provide all the details. If the answer is not available in the context, reply with "Answer is not available in the context". Don't provide the wrong answer.\n\n
        
        Context: {context}
        Question: {question}
        
        Answer: 
        '''
        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt, document_variable_name="context")
        return chain
    
    def get_timestamp(self):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return timestamp 

    # Function to handle user input and retrieve responses
    def user_input(self, user_question, store_name):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        # new_db = FAISS.load_local(f"faiss_index/{store_name}", embeddings=embeddings, allow_dangerous_deserialization=True)
        docs = self.vector_store.similarity_search(user_question)
        chain = self.get_conversational_chain()
        response = chain.invoke(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )
        answer = response["output_text"]
        self.st.session_state.chat_history.append({
            'question': user_question,
            'answer': answer,
            'time': self.get_timestamp()
        })
        # Accessing dictionary keys directly
        last_interaction = self.st.session_state.chat_history[-1]
        st.write(user_template.replace("{{MSG}}", last_interaction['question']), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", last_interaction['answer']), unsafe_allow_html=True)

        
    def get_pdf_display(self, pdf_copy):
        pdf_copy.seek(0)
        base64_pdf = base64.b64encode(pdf_copy.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="950" height="800" type="application/pdf">'
        pdf_copy.seek(0)
        return pdf_display

    def app(self):
        st.title("Chat 💬")
        st.write("---")
        st.markdown(css, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([43, 1, 56], gap='small')
        with col1:
            with st.form(key='user_question_form'):
                user_question = st.text_input(":blue[Your Question :]", key="user_input")
                submit_button = st.form_submit_button(label='Ask')
            if submit_button:
                if self.store_name is not None:
                    with st.spinner("Generating answer..."):
                        self.user_input(user_question, store_name=self.store_name)
                else:
                    st.warning("Please upload and process a PDF first.")
            if st.session_state.chat_history and len(st.session_state.chat_history) > 0 and not submit_button:
                last_interaction = st.session_state.chat_history[-1]
                st.write(user_template.replace("{{MSG}}", last_interaction['question']), unsafe_allow_html=True)
                st.write(bot_template.replace("{{MSG}}", last_interaction['answer']), unsafe_allow_html=True)
        with col3:
            if self.pdf_copy:
                st.markdown(self.get_pdf_display(pdf_copy=self.pdf_copy), unsafe_allow_html=True)
        

if __name__ == '__main__':
    main()
