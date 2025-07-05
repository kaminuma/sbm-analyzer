# run.py

from app import create_app
import logging
from waitress import serve

app = create_app()

if __name__ == "__main__":
    # ロギングの設定を詳細に
    logging.basicConfig(level=logging.DEBUG)
    serve(app, host='0.0.0.0', port=5001)
