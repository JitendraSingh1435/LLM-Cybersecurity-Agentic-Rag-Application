
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import sys
import os
import webbrowser
import threading
import uvicorn

# ==================================================
# Add Project Root
# ==================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# ==================================================
# Import Pipelines
# ==================================================

from standard_rag.basic_rag import basic_rag_pipeline
from agentic_rag.agent_graph import agentic_rag_pipeline
from utils.evaluator import evaluate_standard_rag, evaluate_agentic_rag

# ==================================================
# FastAPI App
# ==================================================

app = FastAPI()

# ==================================================
# Static Files
# ==================================================

app.mount(
    "/static",
    StaticFiles(directory="ui/static"),
    name="static"
)

# ==================================================
# Request Model
# ==================================================

class QueryRequest(BaseModel):
    query: str
    model_choice: str = "ollama"

# ==================================================
# HOME ROUTE
# ==================================================

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("ui/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

# ==================================================
# ASK ROUTE
# ==================================================

@app.post("/ask")
async def ask_question(data: QueryRequest):

    question = data.query
    model_choice = data.model_choice

    # Standard RAG
    rag_result = basic_rag_pipeline(question, model_choice)
    rag_metrics = evaluate_standard_rag(question, rag_result["answer"], rag_result["context"])

    # Agentic RAG
    agentic_result = agentic_rag_pipeline(question, model_choice)
    agentic_metrics = evaluate_agentic_rag(question, agentic_result["answer"], agentic_result["context"])

    return {

        "rag_answer": rag_result["answer"],
        "rag_context": rag_result["context"],
        "rag_sources": rag_result["sources"],
        "rag_metrics": rag_metrics,

        "agentic_answer": agentic_result["answer"],
        "agentic_context": agentic_result["context"],
        "agentic_sources": agentic_result["sources"],
        "rewritten_queries": agentic_result["rewritten_queries"],
        "agentic_metrics": agentic_metrics

    }

# ==================================================
# AUTO OPEN BROWSER
# ==================================================

def open_browser():
    webbrowser.open("http://127.0.0.1:8000")

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    threading.Timer(1.5, open_browser).start()

    uvicorn.run(
        "ui.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

# from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel

# import sys
# import os

# # Add project root to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# # Import your pipelines
# from standard_rag.basic_rag import basic_rag_pipeline
# from agentic_rag.agent_graph import agentic_rag_pipeline

# app = FastAPI()

# # =========================
# # Static Files
# # =========================
# app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# # =========================
# # Templates
# # =========================
# templates = Jinja2Templates(directory="ui/templates")


# # =========================
# # Request Model
# # =========================
# class QueryRequest(BaseModel):
#     query: str


# # =========================
# # Home Route
# # =========================
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):

#     return templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )


# # =========================
# # Ask Route
# # =========================
# @app.post("/ask")
# async def ask_question(data: QueryRequest):

#     question = data.query

#     # Standard RAG
#     # rag_answer = basic_rag_pipeline(question)
#     rag_result = basic_rag_pipeline(question)

#     # Agentic RAG
#     # agentic_answer = agentic_rag_pipeline(question)

#     agentic_result = agentic_rag_pipeline(question)


#     # return {
#     #     "rag_answer": rag_answer,
#     #     "agentic_answer": agentic_answer
#     # }

#     return {

#     "rag_answer": rag_result["answer"],
#     "rag_context": rag_result["context"],
#     "rag_sources": rag_result["sources"],

#     "agentic_answer": agentic_result["answer"],
#     "agentic_context": agentic_result["context"],
#     "agentic_sources": agentic_result["sources"],
#     "rewritten_queries": agentic_result["rewritten_queries"]

# }
