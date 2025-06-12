import requests
import json
import os

def convert_data(api_data):
    converted_data = []
    
    for item in api_data:
        # 曜日の変換マップ
        weekday_map = {
            "Mon": "月曜日",
            "Tue": "火曜日",
            "Wed": "水曜日",
            "Thu": "木曜日",
            "Fri": "金曜日",
            "Sat": "土曜日",
            "Sun": "日曜日",
            "Other": "その他"
        }
        
        # 曜日の処理
        weekdays = item.get("weekdays", [])
        weekday = weekdays[0] if weekdays else "Other"
        weekday_ja = weekday_map.get(weekday, "その他")
        
        # タグの処理
        tags = item.get("tags", [])
        genre = "技術系" if "tech" in tags else "学術系" if "academic" in tags else "その他"
        
        # ポスター画像の処理（空文字列の場合はNoneに変換）
        poster = item.get("poster_image", "")
        if poster == "":
            poster = None
            
        converted_item = {
            "ジャンル": genre,
            "曜日": weekday_ja,
            "イベント名": item.get("name", ""),
            "開始時刻": item.get("start_time", "")[:5],  # HH:MM形式に変換
            "開催周期": item.get("frequency", ""),
            "主催・副主催": item.get("organizers", ""),
            "Join先": item.get("group_url", "") or item.get("organizer_url", ""),
            "Discord": item.get("discord", ""),
            "Twitter": item.get("sns_url", ""),
            "ハッシュタグ": item.get("twitter_hashtag", ""),
            "ポスター": poster,
            "イベント紹介": item.get("description", "")
        }
        
        converted_data.append(converted_item)
    
    # 曜日とイベント名でソート
    weekday_order = ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "その他"]
    converted_data.sort(key=lambda x: (weekday_order.index(x["曜日"]), x["イベント名"]))
    
    return converted_data

if __name__ == '__main__':
    # 環境変数URLからURLを取得する
    url = os.environ.get('URL', 'https://vrc-ta-hub.com/api/v1/community/?format=json')
    
    # URLからデータを取得する
    response = requests.get(url)

    # 正常な応答であるか確認する
    response.raise_for_status()

    # JSONデータを取得する
    api_data = response.json()

    # データを変換
    converted_data = convert_data(api_data)

    # JSONデータをファイルに保存する
    with open('docs/sample.json', 'w', encoding='utf-8') as file:
        json.dump(converted_data, file, ensure_ascii=False, indent=4)

    print("JSONデータをsample.jsonに保存しました。")
