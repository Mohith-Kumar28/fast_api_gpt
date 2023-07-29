from fastapi import FastAPI
from llama_index import GPTSimpleVectorIndex
from langchain import OpenAI
from pydantic import BaseModel
from decouple import config
import os

app = FastAPI()

# Load OpenAI API key from the environment variable
OPENAI_API_KEY = config('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Load the index only once, outside the view, for better performance
index = GPTSimpleVectorIndex.load_from_disk('index.json')


class QuestionRequest(BaseModel):
    question: str


@app.post("/chat/")
def chat_api(question_req: QuestionRequest):
    query = question_req.question
    response = index.query(query)
    # response_from_ai = openai_client.get_ai_response(
    #     query)  # Call the OpenAI API for additional response
    return {"response": response.response}
