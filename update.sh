#!/bin/bash
set -e

# jsonファイルを更新
python3 fetch_data.py

# フォーマットテスト（失敗時はデプロイ中止）
python3 test_format.py
