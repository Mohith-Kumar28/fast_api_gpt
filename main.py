# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from llama_index import GPTSimpleVectorIndex
# from langchain import OpenAI
# from pydantic import BaseModel
# from decouple import config
# import os

# app = FastAPI()


# ## Set allowed origins
# origins = [config('ALLOWED_ORIGINS')]

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load OpenAI API key from the environment variable
# OPENAI_API_KEY = config('OPENAI_API_KEY')
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
 
# # Load the index only once, outside the view, for better performance
# index = GPTSimpleVectorIndex.load_from_disk('index.json')




# class QuestionRequest(BaseModel):
#     question: str


# @app.post("/chat/")
# def chat_api(question_req: QuestionRequest):
#     query = question_req.question
#     # print('Answer like a person,'+query)



    
#     response = index.query('Answer like you are thje person answering the asked question,       question:'+query)
#     # response_from_ai = openai_client.get_ai_response(
#     #     query)  # Call the OpenAI API for additional response
#     return {"response": response.response}
 








from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index import GPTSimpleVectorIndex,ServiceContext,LLMPredictor,PromptHelper
from langchain import OpenAI
from pydantic import BaseModel
from decouple import config
import os

app = FastAPI()
## Set allowed origins
input_string = config('ALLOWED_ORIGINS')
# output_array = [config('ALLOWED_ORIGIN_FRONTEND'),config('ALLOWED_ORIGIN_BACKEND')]
# print(output_array)


# print(output_array)  # Output: item1,item2


origins = [input_string]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key from the environment variable
OPENAI_API_KEY = config('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
 
# Load the index only once, outside the view, for better performance

# set maximum input size
max_input_size = 4096
# set number of output tokens
num_outputs = 1000
# set maximum chunk overlap
max_chunk_overlap = 20
# set chunk size limit
chunk_size_limit = 600 

# define prompt helper
prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

# define LLM
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
index = GPTSimpleVectorIndex.load_from_disk('index.json',service_context=service_context)




class QuestionRequest(BaseModel):
    question: str


@app.post("/chat/")
def chat_api(question_req: QuestionRequest):
    query = question_req.question
    response = index.query('Answer like you are the person answering the asked question and be concise unless you are asked to explain in detail,       question:'+query)
    # response_from_ai = openai_client.get_ai_response(
    #     query)  # Call the OpenAI API for additional response
    return {"response": response.response}
 










#  from fastapi import FastAPI
# from llama_index import (
#        VectorStoreIndex,
#     SimpleDirectoryReader,
#     LLMPredictor,
#     ServiceContext
# )
# from llama_index.query_engine.multistep_query_engine import MultiStepQueryEngine
# from llama_index.indices.query.query_transform.base import StepDecomposeQueryTransform
# from langchain import OpenAI
# from pydantic import BaseModel
# from decouple import config
# import os
# import openai

# app = FastAPI()

# # Load OpenAI API key from the environment variable
# OPENAI_API_KEY = config('OPENAI_API_KEY')
# openai.api_key=OPENAI_API_KEY
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# # Load the index only once, outside the view, for better performance
# # load documents
# documents = SimpleDirectoryReader(
#     "data"
# ).load_data()
# index = VectorStoreIndex.from_documents(documents)


# class QuestionRequest(BaseModel):
#     question: str


# @app.post("/chat/")
# def chat_api(question_req: QuestionRequest):
#     query = question_req.question
#         # response = index.query(query)

#     gpt3 = OpenAI(temperature=0, model="text-davinci-003")
#     service_context_gpt3 = ServiceContext.from_defaults(llm=gpt3)
#     step_decompose_transform_gpt3 = StepDecomposeQueryTransform(
#         LLMPredictor(llm=gpt3), verbose=True
#     )

#     query_engine = index.as_query_engine(service_context=service_context_gpt3)
#     query_engine = MultiStepQueryEngine(
#         query_engine=query_engine,
#         query_transform=step_decompose_transform_gpt3,
#         # index_summary=index_summary,
#     )

#     response = query_engine.query( query )
#     print(response)

#     # response_from_ai = openai_client.get_ai_response(
#     #     query)  # Call the OpenAI API for additional response
#     return {"response": response.response}
 