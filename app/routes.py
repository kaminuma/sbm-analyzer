# app/routes.py

from flask import Blueprint, request, jsonify
from app.analysis import fetch_data_by_period, calculate_total_time_per_category
import logging

bp = Blueprint("api", __name__, url_prefix="/api/v1")

def validate_date(date_text):
    from datetime import datetime
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@bp.route("/analysis/category", methods=["GET"])
def analyze_category():
    try:
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        user_id = request.args.get("user_id")

        if not start_date or not end_date or not user_id:
            logging.warning("Missing required parameters")
            return jsonify({"error": "Missing required parameters"}), 400

        if not (validate_date(start_date) and validate_date(end_date)):
            logging.warning("Invalid date format")
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

        data = fetch_data_by_period(start_date, end_date, user_id)
        if data is not None:
            # カテゴリ別合計時間を計算
            total_time = calculate_total_time_per_category(data)

            # 活動データを辞書形式に変換
            activities = data.to_dict(orient="records")

            # レスポンスの構築
            response = {
                "activities": activities,
                "total_time_per_category": total_time
            }

            return jsonify(response)
        else:
            logging.error("Failed to fetch data")
            return jsonify({"error": "Failed to fetch data"}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": str(e)}), 500
