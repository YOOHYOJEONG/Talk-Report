import re
from datetime import datetime


# 날짜 구분선 (PC)
DATE_LINE_PATTERN = re.compile(
    r"-+\s*(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일.*-+"
)

# PC 카카오톡 내보내기
PC_MESSAGE_PATTERN = re.compile(
    r'^\[(?P<user>[^\]]+)\]\s*'
    r'\[(?P<ampm>오전|오후)\s*(?P<hour>\d{1,2}):(?P<minute>\d{2})\]\s*'
    r'(?P<content>.*)'
)

# 모바일 카카오톡 내보내기
MOBILE_MESSAGE_PATTERN = re.compile(
    r'^(?P<year>\d{4})\.\s*(?P<month>\d{1,2})\.\s*(?P<day>\d{1,2})\.\s*'
    r'(?P<hour>\d{1,2}):(?P<minute>\d{2}),\s*'
    r'(?P<user>[^:]+)\s*:\s*(?P<content>.*)'
)


def parse_kakao_txt(text: str):
    messages = []
    current_date = None

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        # 날짜 구분선 (PC)
        date_match = DATE_LINE_PATTERN.match(line)
        if date_match:
            year, month, day = date_match.groups()
            current_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            continue

        # PC 메시지
        pc_match = PC_MESSAGE_PATTERN.match(line)
        if pc_match and current_date:
            user = pc_match.group("user")
            ampm = pc_match.group("ampm")
            hour = int(pc_match.group("hour"))
            minute = pc_match.group("minute")
            content = pc_match.group("content")

            if ampm == "오후" and hour != 12:
                hour += 12
            if ampm == "오전" and hour == 12:
                hour = 0

            dt = datetime.strptime(
                f"{current_date} {hour:02d}:{minute}:00",
                "%Y-%m-%d %H:%M:%S"
            )

            messages.append({
                "user": user,
                "time": dt,
                "content": content
            })
            continue

        # 모바일 메시지
        mobile_match = MOBILE_MESSAGE_PATTERN.match(line)
        if mobile_match:
            year = int(mobile_match.group("year"))
            month = int(mobile_match.group("month"))
            day = int(mobile_match.group("day"))
            hour = int(mobile_match.group("hour"))
            minute = int(mobile_match.group("minute"))

            user = mobile_match.group("user")
            content = mobile_match.group("content")

            dt = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute
            )

            messages.append({
                "user": user,
                "time": dt,
                "content": content
            })
            continue

    return messages
