import streamlit as st
from io import BytesIO
from PyPDF2 import PdfReader
from streamlit_option_menu import option_menu
from Chat import Chat
from History import History
from langchain_community.vectorstores.faiss import FAISS 
from langchain.text_splitter import RecursiveCharacterTextSplitter  
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

if "main" not in st.session_state:
    st.session_state.main = None
    
class Main:
    def __init__(self):
        print("Main class called")
            
    def checkPDF(self, pdf):
        return pdf is not None

    def get_pdf_text(self, pdf):
            texts = ""
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                texts += page.extract_text()
            return texts

    # dividing the texts into chunks
    def get_text_chunks(self, texts):
        text_splittter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = text_splittter.split_text(texts)
        return chunks

    def get_vector_store(self, chunks, store_name):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embedding=embeddings)
        # vector_store.save_local(f"faiss_index/{store_name}")
        return vector_store

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
    

def main(app):
    uploaded_pdf = False
    st.set_page_config(page_title="ChatPDF", page_icon="📑", layout="wide")
    with st.sidebar:
        st.title("Chat with PDF 📑")
        pdf = st.file_uploader(label=":blue[select PDF to upload]", type="pdf")
        if pdf:
            if app.checkPDF(pdf):
                pdf_copy = BytesIO(pdf.read()) 
                store_name = pdf.name[:-4]
                with st.spinner("Processing"):
                    raw_texts = app.get_pdf_text(pdf=pdf)
                    text_chunks = app.get_text_chunks(texts=raw_texts)
                    vectorstore = app.get_vector_store(chunks=text_chunks, store_name=store_name)
                    chat = Chat(store_name=store_name, pdf_copy=pdf_copy, vector_store=vectorstore)
                    history = History()
                st.success("PDF Successfully Uploaded 😁")
                st.balloons()
                uploaded_pdf = True
                
            page = option_menu(
                    menu_title="Options",
                    options=["Chat", "History"],
                    icons=["chat-dots-fill", "clock-history"],
                    menu_icon="list",
                    default_index=0,
                    styles={
                        "container": {"padding": "8!important", "background-color": "#06141B"},
                        "icon": {"color" : "white", "font-size": "23px"},
                        "nav-link": {"color" : "white", "font-size" : "20px", "text-align": "left", "margin" : "0px", "--hover-color": "#2D2828"},
                        "nav-link-selected": {"background-color": "brown", "border" : "1px solid black"}
                    }
                    
                )
    if uploaded_pdf:       
        pages = {"Chat": chat.app, "History": history.app}
        if page in pages:
            pages[page]()


if __name__ == '__main__':
    if st.session_state.main is None:
        st.session_state.main = Main()
    main(app=st.session_state.main)


