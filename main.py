from datetime import datetime
import os
import pandas as pd

# まずは確実に動くテストデータ（または現在時刻）を記録するようにします


def get_trends():
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  # テストとして、現在の動作確認用データを強制的に作成します
  trends = [
      {"datetime": now, "keyword": "システム稼働テスト中"},
      {"datetime": now, "keyword": "トレンド自動取得"},
  ]
  return trends


def save_to_csv(trends):
  csv_file = "trend_log.csv"
  new_df = pd.DataFrame(trends)

  if os.path.exists(csv_file):
    existing_df = pd.read_csv(csv_file)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  else:
    new_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  print(f"成功: {len(trends)} 件のデータを保存しました。")


if __name__ == "__main__":
  trend_data = get_trends()
  save_to_csv(trend_data)
