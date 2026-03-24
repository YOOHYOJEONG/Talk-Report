from collections import Counter

# 날짜 필터
def filter_by_date(messages, start_dt, end_dt):
    return [m for m in messages if start_dt <= m["time"] <= end_dt]

# 사용자별 메시지 수
def count_messages_by_user(messages):
    counter = Counter(m["user"] for m in messages)
    return dict(counter)

# 시간대별 메시지 수
def count_messages_by_hour(messages):
    hour_counter = Counter(m["time"].hour for m in messages)

    # 0~23시 전체 채우기 (비어 있는 시간은 0)
    return {hour: hour_counter.get(hour, 0) for hour in range(24)}

def aggregate_messages(messages, start_dt, end_dt):
    total = 0
    user_counter = Counter()
    hour_counter = Counter()

    for message in messages:
        message_time = message["time"]
        if not (start_dt <= message_time <= end_dt):
            continue

        total += 1
        user_counter[message["user"]] += 1
        hour_counter[message_time.hour] += 1

    return {
        "total": total,
        "user_count": dict(user_counter),
        "hour_count": {hour: hour_counter.get(hour, 0) for hour in range(24)},
    }
