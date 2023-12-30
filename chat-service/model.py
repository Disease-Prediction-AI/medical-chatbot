from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import RetrievalQA
import sys
import os
from dotenv import find_dotenv, load_dotenv
from langchain.llms import HuggingFaceHub
from llm import EducationalLLM
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import pinecone
from typing import List
from pydantic import BaseModel

load_dotenv(find_dotenv())
INDEX_NAME = "chatbot-med-indx"
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

ROLE_CLASS_MAP = {
    "assistant": AIMessage,
    "user": HumanMessage,
    "system": SystemMessage
}

class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    conversation: List[Message]

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that I don't know, don't try to make up an answer.

Context: {context}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context'])
    system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)
    return system_message_prompt    


def create_messages(conversation):
    return [ROLE_CLASS_MAP[message.role](content=message.content) for message in conversation]

#format docs
def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        formatted_doc = "Source: " + doc.metadata['source']
        formatted_docs.append(formatted_doc)
    return '\n'.join(formatted_docs)

#Loading the model
def load_llm():
    # llm = HuggingFaceHub(repo_id="facebook/bart-large-cnn", model_kwargs={"temperature":0, "max_length":180 })
    llm = EducationalLLM()
    return llm


#output function
def get_answer(conversation):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",model_kwargs={'device':'cuda'})
    query = conversation.conversation[-1].content
    db = Pinecone.from_existing_index(INDEX_NAME, embeddings)
    retriever = db.as_retriever()
    docs = retriever.get_relevant_documents(query=query)
    docs = format_docs(docs=docs)
    prompt = set_custom_prompt().format(context=docs)
    messages = [prompt] + create_messages(conversation=conversation.conversation)
    llm = load_llm()
    response = llm(messages)
    return response



if __name__ == "__main__":
    response = get_answer(sys.argv[1])

    print(response)
