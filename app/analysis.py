import pandas as pd
from sqlalchemy import create_engine
from app.config import Config
import logging
from flask import current_app

def fetch_data_by_period(start_date, end_date, user_id):
    query = """
    SELECT name, contents, date, start_time, end_time
    FROM activities
    WHERE user_id = %s
      AND date >= %s
      AND date <= %s
      AND is_deleted = false
    """

    try:
        logging.debug("Before executing query")
        engine = create_engine(
            Config.SQLALCHEMY_DATABASE_URI,
            connect_args={"connect_timeout": 60},
            pool_pre_ping=True
        )
        with engine.connect() as connection:
            data = pd.read_sql_query(
                query,
                connection,
                params=(user_id, start_date, end_date)
            )
        logging.debug("After executing query")
        logging.debug(f"Data fetched: {data.head()}")
    except Exception as e:
        logging.error(f"Error in pd.read_sql: {e}")
        return None

    try:
        logging.debug("Converting start_time and end_time to datetime")
        data["date"] = pd.to_datetime(data["date"])
        data["start_time"] = pd.to_timedelta(data["start_time"])
        data["end_time"] = pd.to_timedelta(data["end_time"])
        data["start_datetime"] = data["date"] + data["start_time"]
        data["end_datetime"] = data["date"] + data["end_time"]
        logging.debug("Datetime conversion successful")
    except Exception as e:
        logging.error(f"Error in datetime conversion: {e}")
        return None

    try:
        logging.debug("Converting Timedelta and Datetime columns to strings for JSON serialization")
        data["start_time"] = data["start_time"].astype(str)
        data["end_time"] = data["end_time"].astype(str)
        data["start_datetime"] = data["start_datetime"].dt.strftime('%Y-%m-%dT%H:%M:%S')
        data["end_datetime"] = data["end_datetime"].dt.strftime('%Y-%m-%dT%H:%M:%S')
        logging.debug("Conversion successful")
    except Exception as e:
        logging.error(f"Error in converting columns for JSON serialization: {e}")
        return None

    # カテゴリ分類を実施
    try:
        logging.debug("Starting category classification")
        nli_pipeline = current_app.config['NLI_PIPELINE']
        categories = current_app.config['CATEGORIES']

        sequences = data.apply(
            lambda row: (
              str(row['name']) if pd.notna(row['name']) else ''
            ) + ' ' + (
              str(row['contents']) if pd.notna(row['contents']) else ''
            ),
            axis=1
        ).tolist()

        if not sequences:
            logging.debug("No valid sequences found for classification, skipping categorization.")
            data['category'] = 'その他'
            return data

        classifications = nli_pipeline(
            sequences=sequences,
            candidate_labels=categories,
            multi_label=False  ##(Transformersのバージョン対応)
        )

        # 各活動にカテゴリを追加
        data['category'] = [
            result['labels'][0] if result['scores'][0] >= 0.5 else 'その他'
            for result in classifications
        ]

        logging.debug("Category classification successful")
    except Exception as e:
        logging.error(f"Error in category classification: {e}")
        data['category'] = 'エラー'
        return data

    # 最終返却前に再度、データフレームがJSONシリアライズ可能な形になっているかを確認
    # （この時点では timedelta はないが、念のため datetime などがあればここで文字列化/削除）

    return data


def calculate_total_time_per_category(data):
    try:
        logging.debug("Calculating total time per category")

        # 再度datetime型に変換
        data["start_datetime"] = pd.to_datetime(data["start_datetime"])
        data["end_datetime"] = pd.to_datetime(data["end_datetime"])

        # duration計算
        data["duration"] = data["end_datetime"] - data["start_datetime"]
        data["duration_seconds"] = data["duration"].dt.total_seconds()

        # カテゴリごとの合計秒数計算
        total_seconds_per_category = data.groupby("category")["duration_seconds"].sum().reset_index()

        # 秒数 -> 時間形式文字列
        total_seconds_per_category["total_time"] = total_seconds_per_category["duration_seconds"].apply(
            lambda x: f"{int(x//3600)}時間{int(x%3600//60)}分"
        )

        logging.debug(f"Serialized data example before drop: {total_seconds_per_category}")

        # 不要なカラム削除
        total_seconds_per_category = total_seconds_per_category.drop("duration_seconds", axis=1)

        logging.debug(f"Serialized data example after drop: {total_seconds_per_category}")
        logging.debug("Total time calculation successful")

        # ここで data 内の非シリアライズ可能列を文字列に変換
        # durationはTimedelta、start_datetime/end_datetimeはdatetimeになっているので文字列化する
        data["duration"] = data["duration"].astype(str)
        data["start_datetime"] = data["start_datetime"].dt.strftime('%Y-%m-%dT%H:%M:%S')
        data["end_datetime"] = data["end_datetime"].dt.strftime('%Y-%m-%dT%H:%M:%S')

        return total_seconds_per_category.to_dict(orient="records")

    except Exception as e:
        logging.error(f"Error in calculating total time per category: {e}")
        return []
