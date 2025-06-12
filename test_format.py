import json
import os
from typing import List, Dict, Any

def test_json_format(json_file_path: str) -> bool:
    """
    JSONファイルが期待するフォーマットに準拠しているかテストする
    
    Args:
        json_file_path: テスト対象のJSONファイルパス
    
    Returns:
        bool: テストが成功した場合True
    """
    print(f"テスト対象ファイル: {json_file_path}")
    
    # 期待するフィールドとその型
    expected_fields = {
        "ジャンル": str,
        "曜日": str,
        "イベント名": str,
        "開始時刻": str,
        "開催周期": str,
        "主催・副主催": str,
        "Join先": str,
        "Discord": str,
        "Twitter": str,
        "ハッシュタグ": str,
        "ポスター": (str, type(None)),  # str または None
        "イベント紹介": str
    }
    
    # 期待する曜日の値
    valid_weekdays = ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "その他"]
    
    # 期待するジャンルの値
    valid_genres = ["技術系", "学術系", "その他"]
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"読み込み成功: {len(data)} 件のイベントデータ")
        
        # データが配列であることを確認
        if not isinstance(data, list):
            print("❌ エラー: データがリスト形式ではありません")
            return False
        
        # 各イベントをチェック
        errors = []
        for i, event in enumerate(data):
            # 辞書形式であることを確認
            if not isinstance(event, dict):
                errors.append(f"イベント {i}: 辞書形式ではありません")
                continue
            
            # 必須フィールドの存在確認
            for field, expected_type in expected_fields.items():
                if field not in event:
                    errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): フィールド '{field}' が存在しません")
                    continue
                
                # 型チェック
                value = event[field]
                if isinstance(expected_type, tuple):
                    # 複数の型を許可する場合
                    if not any(isinstance(value, t) for t in expected_type):
                        errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): フィールド '{field}' の型が不正です (期待: {expected_type}, 実際: {type(value)})")
                else:
                    if not isinstance(value, expected_type):
                        errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): フィールド '{field}' の型が不正です (期待: {expected_type}, 実際: {type(value)})")
            
            # 余分なフィールドのチェック
            extra_fields = set(event.keys()) - set(expected_fields.keys())
            if extra_fields:
                errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): 余分なフィールドが存在します: {extra_fields}")
            
            # 曜日の値チェック
            if "曜日" in event and event["曜日"] not in valid_weekdays:
                errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): 無効な曜日 '{event['曜日']}'")
            
            # ジャンルの値チェック
            if "ジャンル" in event and event["ジャンル"] not in valid_genres:
                errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): 無効なジャンル '{event['ジャンル']}'")
            
            # 開始時刻のフォーマットチェック（HH:MM形式）
            if "開始時刻" in event:
                time = event["開始時刻"]
                if not (len(time) == 5 and time[2] == ":" and 
                       time[:2].isdigit() and time[3:].isdigit()):
                    errors.append(f"イベント {i} ({event.get('イベント名', '不明')}): 開始時刻のフォーマットが不正 '{time}' (期待: HH:MM)")
        
        # エラーの報告
        if errors:
            print("\n❌ フォーマットエラーが見つかりました:")
            for error in errors[:10]:  # 最初の10件まで表示
                print(f"  - {error}")
            if len(errors) > 10:
                print(f"  ... 他 {len(errors) - 10} 件のエラー")
            return False
        
        # ソート順のチェック
        print("\n✅ すべてのフィールドとフォーマットが正しいです")
        
        # 曜日順のチェック
        weekday_order = ["日曜日", "月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "その他"]
        prev_weekday_index = -1
        prev_event_name = ""
        
        for i, event in enumerate(data):
            weekday = event["曜日"]
            event_name = event["イベント名"]
            weekday_index = weekday_order.index(weekday)
            
            if weekday_index < prev_weekday_index:
                print(f"⚠️  警告: イベントの曜日順が正しくない可能性があります (イベント {i}: {event_name})")
            elif weekday_index == prev_weekday_index and event_name < prev_event_name:
                print(f"⚠️  警告: 同じ曜日内でイベント名順が正しくない可能性があります (イベント {i}: {event_name})")
            
            prev_weekday_index = weekday_index
            prev_event_name = event_name
        
        print(f"\n✅ テスト成功: すべてのチェックをパスしました")
        return True
        
    except FileNotFoundError:
        print(f"❌ エラー: ファイル '{json_file_path}' が見つかりません")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ エラー: JSONの解析に失敗しました: {e}")
        return False
    except Exception as e:
        print(f"❌ エラー: 予期しないエラーが発生しました: {e}")
        return False


def test_fetch_data_output():
    """fetch_data.pyの出力をテストする"""
    print("=== fetch_data.py 出力フォーマットテスト ===\n")
    
    # テスト用のAPIレスポンスデータ
    test_api_data = [
        {
            "name": "テストイベント1",
            "weekdays": ["Mon"],
            "tags": ["tech"],
            "start_time": "21:00:00",
            "frequency": "毎週",
            "organizers": "テスト主催者",
            "group_url": "https://example.com/group",
            "discord": "https://discord.gg/test",
            "sns_url": "https://x.com/test",
            "twitter_hashtag": "#テスト",
            "poster_image": "https://example.com/poster.jpg",
            "description": "テスト説明"
        },
        {
            "name": "テストイベント2",
            "weekdays": ["Sun"],
            "tags": ["academic"],
            "start_time": "22:30:00",
            "frequency": "隔週",
            "organizers": "テスト主催者2",
            "organizer_url": "https://example.com/organizer",
            "discord": "",
            "sns_url": "",
            "twitter_hashtag": "",
            "poster_image": None,
            "description": ""
        }
    ]
    
    # fetch_data.pyのconvert_data関数をインポートして実行
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from fetch_data import convert_data
    
    # データ変換
    converted_data = convert_data(test_api_data)
    
    # 一時ファイルに保存
    test_output_path = "test_output.json"
    with open(test_output_path, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=4)
    
    # フォーマットテスト実行
    result = test_json_format(test_output_path)
    
    # 変換結果の表示
    print("\n--- 変換結果サンプル ---")
    print(json.dumps(converted_data[0], ensure_ascii=False, indent=2))
    
    # クリーンアップ
    if os.path.exists(test_output_path):
        os.remove(test_output_path)
    
    return result


if __name__ == "__main__":
    # 既存のsample.jsonのテスト
    print("=== 既存のsample.jsonフォーマットテスト ===\n")
    sample_result = test_json_format("docs/sample.json")
    
    print("\n" + "="*50 + "\n")
    
    # fetch_data.pyの出力テスト
    fetch_result = test_fetch_data_output()
    
    # 総合結果
    print("\n" + "="*50)
    print("=== 総合テスト結果 ===")
    if sample_result and fetch_result:
        print("✅ すべてのテストが成功しました！")
        exit(0)
    else:
        print("❌ 一部のテストが失敗しました")
        exit(1)