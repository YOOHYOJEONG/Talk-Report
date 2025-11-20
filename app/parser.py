import re
from datetime import datetime

# 날짜 구분선
DATE_LINE_PATTERN = re.compile(r"-+\s*(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일.*-+")

# 메시지 패턴
MESSAGE_PATTERN = re.compile(
    r'^\[(.*?)\]\s*\[(오전|오후)\s*(\d{1,2}):(\d{2})\]\s*(.*)'
)

def parse_kakao_txt(text):
    messages = []
    current_date = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # 날짜 라인
        date_match = DATE_LINE_PATTERN.match(line)
        if date_match:
            year, month, day = date_match.groups()
            current_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            continue

        # 메시지 라인
        msg_match = MESSAGE_PATTERN.match(line)
        if msg_match and current_date:
            user, ampm, hour, minute, content = msg_match.groups()

            hour = int(hour)
            if ampm == "오후" and hour != 12:
                hour += 12
            if ampm == "오전" and hour == 12:
                hour = 0

            dt = datetime.strptime(
                f"{current_date} {hour:02d}:{minute}:00", "%Y-%m-%d %H:%M:%S"
            )

            messages.append({
                "user": user,
                "time": dt,
                "content": content
            })

    return messages