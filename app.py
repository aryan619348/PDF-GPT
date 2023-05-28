from flask import Flask, request, jsonify, render_template, send_from_directory
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
from flask_cors import CORS
from waitress import serve
from flask import jsonify
from langchain.chat_models import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = ""
app = Flask(__name__)
CORS(app)

# Google Drive API credentials
API_KEY = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    # Get the file link and question from the request
    data = request.get_json()
    file_link = data['file_link']
    question = data['question']

    # Extract the file ID from the Google Drive link
    file_id = extract_file_id(file_link)

    # Download the PDF file from Google Drive
    pdf_bytes = download_pdf(file_id)

    # Read data from the file and put them into a variable called raw_text
    reader = PdfReader(BytesIO(pdf_bytes))
    raw_text = ''
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)

    # Create embeddings
    embeddings = OpenAIEmbeddings()
    docsearch = FAISS.from_texts(texts, embeddings)
    llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
    chain = load_qa_chain(llm, chain_type="stuff")

    # Perform the question answering
    docs = docsearch.similarity_search(question)
    answer = chain.run(input_documents=docs, question=question)

    # Return the answer as a JSON response
    return jsonify({'answer': answer})

def extract_file_id(drive_link):
    # Extract the file ID from the Google Drive link
    if "drive.google.com" in drive_link:
        file_id = drive_link.split("/")[-2]
        return file_id
    return None

def download_pdf(file_id):
    # Download the PDF file from Google Drive using the file ID
    drive_service = build('drive', 'v3', developerKey=API_KEY)
    request = drive_service.files().get_media(fileId=file_id)
    pdf_bytes = BytesIO()
    downloader = MediaIoBaseDownload(pdf_bytes, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return pdf_bytes.getvalue()

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.',
                               'ai-plugin.json',
                               mimetype='application/json')


@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')

if __name__ == '__main__':
    serve(app,host="0.0.0.0",port=80)
