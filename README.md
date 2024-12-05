# **sbm-Analyzer**

## **概要**
SBM-Analyzer は、生活記録データを AI 技術を活用して解析し、行動の傾向やカテゴリごとの行動時間を算出するツールです。分析結果は、ユーザーの指定した期間に基づき JSON フォーマットで提供され、今後も多様な分析機能を追加予定です。

---

## **機能**
1. **AIによるカテゴリ分類**:
   - 活動内容 (`name` または `contents`) をもとに自然言語処理 (NLP) を利用して自動的にカテゴリ分け。
   - モデル: Hugging Face の `zero-shot-classification` パイプラインを活用。
   - デフォルトカテゴリ例:
     - 運動
     - 仕事
     - 趣味
     - 休憩
     - その他

2. **期間指定のデータ解析**:
   - ユーザーが指定した期間内のデータを解析し、カテゴリごとの活動時間を算出。

3. **カテゴリ別時間計算**:
   - カテゴリに属する活動の合計時間を `X時間Y分` の形式で提供。

4. **拡張可能な分析機能**:
   - 今後のアップデートで、さらなる AI 活用による分析機能（例: 傾向分析、感情分析、月間データ可視化など）を予定。

---

## **今後の課題**
1. **エラーハンドリングの強化**:
   - JSON シリアライズにおける型変換の完全対応。
2. **拡張可能な分析機能の追加**:
   - 傾向分析、感情分析、可視化機能の導入。
3. **パフォーマンス向上**:
   - NLP モデルの効率化と処理速度の改善。

---

## **使用技術**
- **Python**: メインのアプリケーションロジック。
- **Flask**: 軽量な Web フレームワーク。
- **SQLAlchemy**: データベースとの連携。
- **Hugging Face Transformers**: NLP モデルの利用。
- **Waitress**: WSGI サーバー。

---

## **要約**
SBM-Analyzer は、ユーザーの日々の生活記録を AI で効率的に分析し、直感的に理解できる形式で結果を提供することを目的としています。今後も多彩な分析機能を追加予定です！