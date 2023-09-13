#!/bin/bash

# jsonファイルを更新
python3 fetch_data.py

# # git の設定
# git config --local user.email "noricha-vr@gmail.com"
# git config --local user.name "noricha-vr"

# # sample.jsonが前回の状態から変更されているか確認
# CHANGES=$(git diff --name-only docs/sample.json)

# # CHANGES が空でない場合（つまり、sample.json が変更されている場合）のみコミット・プッシュを実行
# if [ ! -z "$CHANGES" ]; then
#   git add docs/sample.json
#   git commit -m "Add updated sample.json"
#   git push
# else
#   echo "No changes to commit"
# fi
