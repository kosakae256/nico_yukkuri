# とりあえず、動画を一覧で取ってくる。
import requests
import csv

URL = "https://public-api.commons.nicovideo.jp/v1/tree/nc236011/relatives/children"# ?_offset=0&_limit=200&with_meta=1&_sort=-id&only_mine=0"
SUM = 80000
LIMIT = 200

# テスト用
def test():
    params = {'_offset': 0, '_limit': 1, 'with_meta': 1, '_sort': '-id', "fields": "viewCounter"}
    r = requests.get(URL, params=params)

    r.encoding = r.apparent_encoding
    data = r.json()
    print(data)
    print(data["data"]["children"]["contents"][0]["watchURL"]) # データ取るテスト
    print(data["data"]["children"]["contents"][0]["title"])
    print(data["data"]["children"]["contents"][0]["created"])
    print(data["data"]["children"]["contents"][0]["description"])
    

# 本番
def main():
    # ファイル書き込み
    with open('./data.csv', "w",encoding='utf-8') as f:
        writer = csv.DictWriter(f, ["URL", "タイトル", "作成日時", "概要欄"])
        writer.writeheader()

        # 検索最大数から、何回検索するかを算出
        for i in range(0,SUM//LIMIT):
            # 検索パラメータ。オフセットで調整
            params = {'_offset': i*LIMIT, '_limit': 200, 'with_meta': 1, '_sort': '-id', 'only_mine': 0}

            # リクエスト
            r = requests.get(URL, params=params)

            # エンコード(しないとバグる)とdataにjsonデータを格納
            r.encoding = r.apparent_encoding
            resp_data = r.json()
            data_len = len(resp_data["data"]["children"]["contents"])

            print(f"-------API取得{i+1}回目 データ数: {data_len}-------")

            # 取得データ分ループ(dataには動画データ)
            for data in resp_data["data"]["children"]["contents"]:
                # 各種データ取得
                url = data["watchURL"]
                title = data["title"]
                create_datetime = data["created"]
                description = data["description"]

                # 書き込み
                writer.writerow({'URL': url, 'タイトル': title, '作成日時': create_datetime, '概要欄': description})



if __name__ == "__main__":
    # main()
    test()