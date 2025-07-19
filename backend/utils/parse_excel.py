import pandas as pd
from datetime import datetime

def parse_users_excel(file_path: str) -> list[dict]:
    df = pd.read_excel(file_path)
    df = df.fillna(None)

    result = []
    for _, row in df.iterrows():
        user = {
            "user_id": int(row["user_id"]),
            "alias": row["alias"],
            "mail": row["mail"],
            "name": row["name"],
            "surname": row["surname"],
            "patronymic": row["patronymic"],
            "phone_number": row["phone_number"],
            "citizens": row["citizens"],
            "duty_to_work": str(row["duty_to_work"]) if row["duty_to_work"] else None,
            "duty_status": str(row["duty_status"]) if row["duty_status"] else None,
            "grant_amount": int(row["grant_amount"]) if row["grant_amount"] else None,
            "duty_period": int(row["duty_period"]) if row["duty_period"] else None,
            "company": row["company"],
            "position": row["position"],
            "start_date": parse_date(row["start_date"]),
            "end_date": parse_date(row["end_date"]),
            "salary": int(row["salary"]) if row["salary"] else None,
        }
        result.append(user)
    return result

def parse_date(value):
    if pd.isna(value) or value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").date()
    except:
        return None
