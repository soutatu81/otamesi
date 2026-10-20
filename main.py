from datetime import datetime
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

# 広範囲のトレンド（日本または世界）がまとまっているTwittrendのページ
URL = "https://twitrend.jp/"


def get_trends():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }
  try:
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trends = []

    # ページ内からトレンドになりそうなキーワードを広く抽出
    for a in soup.select("a"):
      text = a.get_text(strip=True)
      if 2 <= len(text) <= 25 and not text.startswith("http"):
        if text not in [t["keyword"] for t in trends]:
          trends.append({"datetime": now, "keyword": text})

    # もしうまく取れなかった場合のフォールバック
    if not trends:
      trends.append(
          {"datetime": now, "keyword": "トレンド取得件数0件（構造確認要）"}
      )

    return trends[:50]
  except Exception as e:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [{"datetime": now, "keyword": f"エラー: {str(e)}"}]


def save_to_csv(trends):
  csv_file = "trend_log.csv"
  new_df = pd.DataFrame(trends)

  if os.path.exists(csv_file):
    existing_df = pd.read_csv(csv_file)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  else:
    new_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  print(f"成功: {len(trends)} 件のトレンドを保存しました。")


if __name__ == "__main__":
  trend_data = get_trends()
  save_to_csv(trend_data)
