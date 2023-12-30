from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from dotenv import find_dotenv, load_dotenv
import pinecone
import os

load_dotenv(find_dotenv())

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV")
)

DATA_PATH = "data/"
# DB_FAISS_PATH = 'vectorstore/db_faiss'
INDEX_NAME = "chatbot-med-indx"

if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(name=INDEX_NAME, metric="cosine", dimension=384)



# Create vector database
def create_vector_db():
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    db = Pinecone.from_documents(texts, embeddings, index_name=INDEX_NAME)
    

if __name__ == "__main__":
    create_vector_db()


# from dotenv import find_dotenv, load_dotenv
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.document_loaders import DirectoryLoader, PyPDFLoader

# load_dotenv(find_dotenv())


# DATA_PATH = 'data/'
# DB_FAISS_PATH = 'vectorstore/db_faiss'

# def create_vector_db():
#     embeddings = OpenAIEmbeddings()
#     loader = DirectoryLoader(
#         DATA_PATH, glob='*.pdf', loader_cls=PyPDFLoader)

#     documents = loader.load()
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=0)

#     texts = text_splitter.split_documents(documents)

#     db = FAISS.from_documents(texts, embeddings)
#     db.save_local(DB_FAISS_PATH)


# if __name__ == "__main__":
#     create_vector_db()