from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.parser import parse_kakao_txt
from app.analysis import filter_by_date, count_messages_by_user, count_messages_by_hour
from datetime import datetime

app = FastAPI()

# ⭐ static 파일 제공 설정 (필수)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def index():
    return FileResponse("app/static/index.html")


@app.post("/analyze")
async def analyze(request: Request):
    form = await request.form()
    file = form["file"].file.read().decode("utf-8")

    start_date = form["start_date"]
    end_date = form["end_date"]

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    messages = parse_kakao_txt(file)
    filtered = filter_by_date(messages, start_dt, end_dt)

    message_list = [{
        "user": m["user"],
        "time": m["time"].strftime("%Y-%m-%d %H:%M:%S"),
        "content": m["content"],
    } for m in filtered]

    user_count = count_messages_by_user(filtered)
    hour_count = count_messages_by_hour(filtered)

    return JSONResponse({
        "messages": message_list,
        "total": len(filtered),
        "user_count": user_count,
        "hour_count": hour_count
    })