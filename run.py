# run.py

from app import create_app
import logging
from waitress import serve
import os

app = create_app()

if __name__ == "__main__":
    # ロギングの設定を詳細に
    logging.basicConfig(level=logging.DEBUG)
    
    # 環境変数からポートを取得（デフォルトは5000）
    port = int(os.getenv('PORT', 5000))
    
    serve(app, host='0.0.0.0', port=port)
