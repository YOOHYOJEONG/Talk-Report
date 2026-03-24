from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.parser import iter_kakao_messages
from app.analysis import (
    aggregate_messages,
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

    start_date = form.get("start_date", "").strip()
    end_date = form.get("end_date", "").strip()

    if not start_date or not end_date:
        return JSONResponse(
            {"error": "시작일과 종료일을 모두 입력해 주세요."},
            status_code=400
        )

    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return JSONResponse(
            {"error": "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식을 사용해 주세요."},
            status_code=400
        )

    if start_dt > end_dt:
        return JSONResponse(
            {"error": "시작일은 종료일보다 늦을 수 없습니다."},
            status_code=400
        )
    total = 0
    user_count = {}
    hour_count = {hour: 0 for hour in range(24)}

    for file in sorted(files, key=lambda f: f.filename):
        raw = await file.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("cp949")

        result = aggregate_messages(
            iter_kakao_messages(text.splitlines()),
            start_dt,
            end_dt,
        )
        total += result["total"]

        for user, count in result["user_count"].items():
            user_count[user] = user_count.get(user, 0) + count

        for hour, count in result["hour_count"].items():
            hour_count[hour] += count

    return JSONResponse({
        "total": total,
        "user_count": user_count,
        "hour_count": hour_count
    })
