# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このプロジェクトは、VRC-TA-HUBのAPIから技術系・学術系イベントデータを取得し、GitHub Pagesで表示するためのJSONファイルに変換するシステムです。

## 主要コマンド

### 開発環境のセットアップ
```bash
# uvで仮想環境を作成
uv venv

# 依存関係のインストール
uv pip install -r requrements.txt
```

### データ取得・変換
```bash
# APIからデータを取得してJSONに変換
source .venv/bin/activate && python fetch_data.py

# または update.sh を実行
./update.sh
```

### テスト実行
```bash
# フォーマットテストを実行
source .venv/bin/activate && python test_format.py
```

## アーキテクチャ

### データフロー
1. **APIデータ取得**: `https://vrc-ta-hub.com/api/v1/community/?format=json` から生データを取得
2. **データ変換**: `fetch_data.py`の`convert_data()`関数で日本語形式に変換
   - 曜日を英語から日本語に変換（Mon→月曜日）
   - タグからジャンルを判定（tech→技術系、academic→学術系）
   - 曜日順→イベント名順でソート
3. **JSON出力**: `docs/sample.json`に固定フォーマットで保存
4. **Web表示**: `docs/index.html`がJSONを読み込んで表示

### 出力JSONスキーマ
```json
{
  "ジャンル": "技術系|学術系|その他",
  "曜日": "日曜日|月曜日|...|その他",
  "イベント名": "string",
  "開始時刻": "HH:MM",
  "開催周期": "string",
  "主催・副主催": "string",
  "Join先": "string",
  "Discord": "string",
  "Twitter": "string",
  "ハッシュタグ": "string",
  "ポスター": "string|null",
  "イベント紹介": "string"
}
```

### GitHub Actions
- `.github/workflows/schedule.yml`: 手動実行（workflow_dispatch）でデータ更新
- Python 3.11環境でupdate.shを実行し、gh-pagesブランチにデプロイ

## 重要な注意点
- **出力フォーマットの厳守**: `docs/sample.json`と完全に同じスキーマで出力する必要がある
- **ポスター画像**: 空文字列の場合は`null`に変換
- **ソート順**: 曜日（日→月→...→その他）→イベント名のアルファベット順
- **文字コード**: UTF-8で出力（ensure_ascii=False）