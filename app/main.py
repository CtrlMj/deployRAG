# import Essential dependencies
import streamlit as sl
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import os
import threading
from prometheus_client import start_http_server
from custom_metrics import (
    chat_requests_total,
    chat_request_latency_seconds,
    chat_request_tokens,
)
import time

# from dotenv import load_dotenv


# load_dotenv()
# function to load the vectordatabase
def load_knowledgeBase(db_faiss_path="./vectorstore/db_faiss"):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local(
        db_faiss_path, embeddings, allow_dangerous_deserialization=True
    )
    return db


# function to load the OPENAI LLM
def load_llm():
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY")
    )
    return llm


# creating prompt template using langchain
def load_prompt():
    prompt = """ You need to answer the question in the sentence as same as in the pdf content.
    Given below is the context and question of the user.
    context = {context}
    question = {question}
    if the answer is not in the pdf answer "Not sure about that"
        """
    prompt = ChatPromptTemplate.from_template(prompt)
    return prompt


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def create_rag_chain():
    retriever = load_knowledgeBase().as_retriever()
    llm = load_llm()
    prompt = load_prompt()
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return rag_chain


if __name__ == "__main__":
    threading.Thread(target=start_http_server, args=(8502,), daemon=True).start()
    sl.header("welcome to the 📝PDF bot")
    sl.write("🤖 You can chat by Entering your queries ")
    rag_chain = create_rag_chain()

    query = sl.text_input("Enter some text")

    if query:
        chat_requests_total.inc()
        start_time = time.time()
        response = rag_chain.invoke(query)
        latency = time.time() - start_time
        chat_request_latency_seconds.observe(latency)
        chat_request_tokens.observe(response.usage_metadata["total_tokens"])
        sl.write(response.content)
