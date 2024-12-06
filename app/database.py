## 将来的にDB接続部分はこちらに移行してリファクタリング予定
## 現在使われていません。

import pandas as pd
from sqlalchemy import create_engine
from app.config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
                       connect_args={"connect_timeout": 60},
                       pool_pre_ping=True
                       )

try:
    with engine.connect() as connection:
        print("Before executing query")
        data = pd.read_sql(text(query).execution_options(timeout=60), connection, params={"user_id": user_id, "start_date": start_date, "end_date": end_date})
        print("After executing query")
        print(data.head())
except Exception as e:
    print(f"Error in pd.read_sql: {e}")
    

def fetch_data_by_period(start_date, end_date, user_id):
    query = """
    SELECT name, details, date, start_time, end_time
    FROM activities
    WHERE user_id = :user_id
      AND date >= :start_date
      AND date <= :end_date
    """



    try:
        print("Before executing query")
        data = pd.read_sql(query, engine)
        print("After executing query")
        print(data.head())  # データが取得できているか確認
    except Exception as e:
        print(f"Error in pd.read_sql: {e}")

    # start_timeとend_timeをdatetimeに変換
    data["start_datetime"] = pd.to_datetime(data["date"] + " " + data["start_time"])
    data["end_datetime"] = pd.to_datetime(data["date"] + " " + data["end_time"])
    return data
