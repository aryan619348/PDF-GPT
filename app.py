from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from PyPDF2 import PdfReader
from langchain.callbacks import get_openai_callback
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

API_KEY = os.getenv('GOOGLE_API_KEY')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("pdfgpt.html", {"request": request})

@app.post("/process_pdf")
async def process_pdf(request: Request):
    data = await request.json()
    file_link = data["file_link"]
    question = data["question"]

    file_id = extract_file_id(file_link)
    pdf_bytes = download_pdf(file_id)

    reader = PdfReader(BytesIO(pdf_bytes))
    raw_text = ""
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            raw_text += text

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    texts = text_splitter.split_text(raw_text)
    with get_openai_callback() as cb:
        embeddings = OpenAIEmbeddings()
        docsearch = FAISS.from_texts(texts, embeddings)
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
        chain = load_qa_chain(llm, chain_type="stuff")

        docs = docsearch.similarity_search(question)
        answer = chain.run(input_documents=docs, question=question)
        print(cb)
    return JSONResponse(content={"answer": answer})

def extract_file_id(drive_link):
    if "drive.google.com" in drive_link:
        file_id = drive_link.split("/")[-2]
        return file_id
    return None

def download_pdf(file_id):
    drive_service = build("drive", "v3", developerKey=API_KEY)
    request = drive_service.files().get_media(fileId=file_id)
    pdf_bytes = BytesIO()
    downloader = MediaIoBaseDownload(pdf_bytes, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    return pdf_bytes.getvalue()

