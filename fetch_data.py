import requests
import json
import os
if __name__ == '__main__':
    # 環境変数URLからURLを取得する
    url = os.environ.get('URL')
    # URLからデータを取得する
    response = requests.get(url)

    # 正常な応答であるか確認する
    response.raise_for_status()

    # JSONデータを取得する
    data = response.json()

    # JSONデータをファイルに保存する
    with open('docs/sample.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print("JSONデータをsample.jsonに保存しました。")
