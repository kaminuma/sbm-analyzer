# app/__init__.py

from flask import Flask
from app.config import Config
from app.routes import bp
import logging
from transformers import pipeline
import torch

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ルーティングを登録
    app.register_blueprint(bp)

    # ロギングの設定
    logging.basicConfig(level=logging.DEBUG)

    # AIモデルの初期化
    try:
        app.config['NLI_PIPELINE'] = pipeline(
            "zero-shot-classification",
            model="joeddav/xlm-roberta-large-xnli",
            device=0 if torch.cuda.is_available() else -1  # GPUが利用可能な場合はGPUを使用
        )
        logging.debug("AIモデルの初期化に成功しました。")
    except Exception as e:
        logging.error(f"AIモデルの初期化に失敗しました: {e}")
        raise e  # アプリケーション起動を中断

    # カテゴリの定義
    app.config['CATEGORIES'] = [
    "運動", "仕事", "学習", "趣味", 
    "食事", "睡眠", "買い物", "娯楽"
    ]

    return app
