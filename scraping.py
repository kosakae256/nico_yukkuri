from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

"""
url = 'https://www.nicovideo.jp/watch/sm38256842'
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")
text = soup.head.find('script', class_='LdJson').text

json_dict = json.loads(text)
print("視聴回数: ", json_dict["interactionStatistic"][0]["userInteractionCount"])
print("マイリスト数: ", json_dict["interactionStatistic"][1]["userInteractionCount"])
print("コメント数: ", json_dict["commentCount"])
"""

def main():
    df = pd.read_csv('data.csv')

    urls = []
    watches = []
    mylists = []
    comments = []
    for i, url in enumerate(df["URL"]):
        print(i)
        urls.append(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.head.find('script', class_='LdJson').text
        json_dict = json.loads(text)
        watches.append(json_dict["interactionStatistic"][0]["userInteractionCount"])
        mylists.append(json_dict["interactionStatistic"][1]["userInteractionCount"])
        comments.append(json_dict["commentCount"])

    df2 = pd.DataFrame({
        "URL": urls,
        "watch": watches,
        "mylist": mylists,
        "comment": comments
    })

    print(df2)
        

if __name__ == "__main__":
    main()