
from app.pipeline import LLMPipeline
from app.schema import Chat
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.post("/chat/")
async def chat(chat: Chat):
    pipeline = LLMPipeline()
    processed_task = await pipeline.task_analyze(chat.content)
    plan = await pipeline.ui_planner(processed_task)
    # return {"plan": plan}
    final_code = await pipeline.ui_builder(plan, optimize=True)
    print(f'type of output ', type(final_code))
    return { "final_code": final_code }
