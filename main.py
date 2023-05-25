#POC THAT THE PROJECT WORKS.

from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

import os
os.environ["OPENAI_API_KEY"] = ""

# Importing the necessary libraries for Google Drive integration
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate and create a GoogleDrive instance
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# Google Drive file ID for the PDF file
file_id = "12vhzQYTh4nWx-gUjC9T25zLqh3SrzRkF"

# Download the PDF file from Google Drive
file_path = "/Users/aryanpillai/PycharmProjects/pdfgpt/data/trial_1.pdf"
drive.CreateFile({'id': file_id}).GetContentFile(file_path)

# Read the downloaded PDF file
reader = PdfReader(file_path)

# Read data from the file and put them into a variable called raw_text
raw_text = ''
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

# We need to split the text that we read into smaller chunks so that during information retrieval we don't hit the token size limits.
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)

chain = load_qa_chain(OpenAI(), chain_type="stuff")

query = "who are the authors of the document?"
docs = docsearch.similarity_search(query)
answer = chain.run(input_documents=docs, question=query)
print(answer)

