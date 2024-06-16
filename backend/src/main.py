from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from .Claude3Connector import Claude3Connector
from .GeminiConnector import GeminiConnector

from dotenv import load_dotenv
import os

load_dotenv('.env')

app = FastAPI()

# Amazon Bedrock (Claude)
client = Claude3Connector(
    aws_access_key=os.environ.get("aws_access_key_id"),
    aws_secret_key=os.environ.get("aws_secret_access_key"),
    aws_session_token=None,
    aws_region=os.environ.get("aws_region"),
)

# Gemini
gclient = GeminiConnector(
    google_api_key=os.environ.get("GOOGLE_API_KEY"),
    model_key="flash"
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# pydanticを利用するパターン
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


class Chat(BaseModel):
    message: str


@app.on_event("startup")
def startup():
    pass


@app.on_event("shutdown")
def shutdown():
    pass


# サンプルデータ返すだけ
@app.get("/")
def read_root():
    return {
        "title": "サンプルデータ",
        "text": "テキストデータ",
        "list": [1, 2, 3, 4, 5],
    }


# update機能を想定したサンプル
@app.put("/items/{item_id}")
def items(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


# claude3, geminiアクセスサンプル。要設定。
@app.post("/chat")
def chat(Chat: Chat):
    # Claudeに問い合わせ
    resp_claude = client.query(Chat.message)

    # Geminiに問い合わせ
    resp_gemini = gclient.query(Chat.message)

    return {
        "message_claude": resp_claude,
        "message_gemini": resp_gemini
    }

