from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.parser import parse_kakao_txt
from app.analysis import (
    filter_by_date,
    count_messages_by_user,
    count_messages_by_hour,
)
from datetime import datetime
from typing import List
from pathlib import Path


app = FastAPI()

# static 파일 제공
app.mount("/static", StaticFiles(directory="app/static"), name="static")

BASE_DIR = Path(__file__).resolve().parent        # talk_report/app
PROJECT_ROOT = BASE_DIR.parent                   # talk_report

app.mount(
    "/assert",
    StaticFiles(directory=PROJECT_ROOT / "assert"),
    name="assert"
)


@app.get("/")
async def index():
    return FileResponse("app/static/index.html")


@app.post("/analyze")
async def analyze(request: Request):
    form = await request.form()

    files: List[UploadFile] = form.getlist("files")

    if not files:
        return JSONResponse(
            {"error": "업로드된 파일이 없습니다."},
            status_code=400
        )

    start_date = form["start_date"]
    end_date = form["end_date"]

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    combined_text = ""

    for file in sorted(files, key=lambda f: f.filename):
        raw = await file.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp949")

        combined_text += text + "\n"

    messages = parse_kakao_txt(combined_text)
    filtered = filter_by_date(messages, start_dt, end_dt)

    user_count = count_messages_by_user(filtered)
    hour_count = count_messages_by_hour(filtered)

    return JSONResponse({
        "total": len(filtered),
        "user_count": user_count,
        "hour_count": hour_count
    })