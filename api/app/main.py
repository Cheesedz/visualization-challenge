
from app.util import supabase
from app.pipeline import LLMPipeline
from app.schema import Chat
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from fastapi import Request
from app.util import log_queue
import asyncio
import uuid

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

@app.post("/chat")
async def chat(chat: Chat):
    pipeline = LLMPipeline()
    file_content = None
    if chat.file is not None:
        file_content = await chat.file.read()
        file_content = file_content.decode('utf-8')
        if not file_content:
            file_content = None
    if file_content:
        chat.content = f"{chat.content}\n\nFile content:\n{file_content}"
        
    processed_task = await pipeline.task_analyze(chat.content)
    problem_type = json.loads(processed_task).get('task_type').get('type')
    plan = await pipeline.ui_planner(processed_task)
    final_code = await pipeline.ui_builder(problem_type, plan, optimize=True)
    # Write final_code to a HTML file
    # Generate a unique filename using uuid
    unique_id = str(uuid.uuid4())
    html_filename = f"final_code_{unique_id}.html"
    html_path = f"./template/{html_filename}"

    with open(html_path, "w", encoding="utf-8") as f:
        if isinstance(final_code, dict):
            f.write(json.dumps(final_code, ensure_ascii=False, indent=2))
        else:
            f.write(final_code)

    # Upload the HTML file to the Supabase bucket
    with open(html_path, "rb") as f:
        upload_result = (
            supabase.storage
            .from_("visualization-challenge")
            .upload(
                file=f,
                path=f"public/{html_filename}",
                file_options={"content-type": "text/html", "upsert": "true"}
            )
        )
        url = (
            supabase.storage
            .from_("avatars")
            .get_public_url(f"public/{html_filename}")
        )
    return { "url": url }

@app.get("/logs")
async def logs(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            try:
                log = await asyncio.wait_for(log_queue.get(), timeout=30.0)
                yield {
                    "event": "log",
                    "data": log,
                }
            except asyncio.TimeoutError:
                yield {"event": "ping", "data": "keep-alive"}
    return EventSourceResponse(event_generator())
