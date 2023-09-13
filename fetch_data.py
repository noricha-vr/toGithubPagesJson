import requests
import json


if __name__ == '__main__':
    # 指定されたURL
    url = 'https://script.googleusercontent.com/macros/echo?user_content_key=eXBNGH5vxSbknxFPu0XdCHVJ_-ylFAAJez3-qsTD0Bqa6l_9C_-2AnuIhhJ2yyC1_rH0GpKfR0GuJLoyJ0jg9usnCdBwXs0ym5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnN9ca9CEOuXBb9p37hhwT2PaSCyLnbWkW-356mZJYYpLUPBy31-xkM-8AZcRbgUJK2syXgBr3L9Ti5fQSKjhzOadz_ORPUypytz9Jw9Md8uu&lib=M0Pe-JIfEhKXuDG58t6bPxj8rQg-QTqZL'
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
