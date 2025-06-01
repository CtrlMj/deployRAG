#import Essential dependencies
import streamlit as sl
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import threading
from prometheus_client import start_http_server
from metrics import chat_requests_total, chat_request_latency_seconds, chat_request_tokens
import time
# from dotenv import load_dotenv

# load_dotenv()
#function to load the vectordatabase
def load_knowledgeBase():
    embeddings=OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
    DB_FAISS_PATH = './vectorstore/db_faiss'
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    return db
        
#function to load the OPENAI LLM
def load_llm():
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=os.getenv('OPENAI_API_KEY'))
    return llm

#creating prompt template using langchain
def load_prompt():
    prompt = """ You need to answer the question in the sentence as same as in the  pdf content. . 
    Given below is the context and question of the user.
    context = {context}
    question = {question}
    if the answer is not in the pdf answer "i donot know what the hell you are asking about"
        """
    prompt = ChatPromptTemplate.from_template(prompt)
    return prompt


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def process_query(query, knowledgeBase, llm, prompt):
    chat_requests_total.inc()
    start_time = time.time()
    #getting only the chunks that are similar to the query for llm to produce the output
    similar_embeddings = knowledgeBase.similarity_search(query)
    similar_embeddings = FAISS.from_documents(documents=similar_embeddings, embedding=OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY')))
    #creating the chain for integrating llm,prompt,stroutputparser
    retriever = similar_embeddings.as_retriever()
    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
        )
    
    response = rag_chain.invoke(query)
    latency = time.time() - start_time
    chat_request_latency_seconds.observe(latency)
    chat_request_tokens.observe(response.usage_metadata['total_tokens'])
    return response.content

if __name__=='__main__':
    threading.Thread(target=start_http_server, args=(8502,), daemon=True).start()
    sl.header("welcome to the 📝PDF bot")
    sl.write("🤖 You can chat by Entering your queries ")
    knowledgeBase=load_knowledgeBase()
    llm=load_llm()
    prompt=load_prompt()
    
    query=sl.text_input('Enter some text')
    
    
    if (query):
        answer = process_query(query, knowledgeBase, llm, prompt)
        sl.write(answer)
            
        
        
        
        