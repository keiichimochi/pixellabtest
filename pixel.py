import requests
import json
import base64
import os
from dotenv import load_dotenv

def create_grass_field_image():
    # .envファイルから環境変数を読み込むナリ！
    load_dotenv()
    
    # 環境変数からAPIキーを取得するナリ！
    api_key = os.getenv('PIXELLAB_API_KEY')
    if not api_key:
        raise ValueError("PIXELLAB_API_KEYが設定されていないナリ！.envファイルを確認するナリ！")

    # APIのエンドポイントを設定するナリ！
    api_url = "https://api.pixellab.ai/v1/generate-image-pixflux"

    # プロンプトを設定して、素敵な草原を描写するナリ！
    prompt = "pixel art grass field, 32x32 resolution, bright green grass, sunny day, retro game style"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "description": prompt,
        "image_size": {
            "width": 32,
            "height": 32
        }
    }

    try:
        # APIリクエストを送信するナリ！
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        # レスポンスからbase64エンコードされた画像を取得するナリ！
        image_data = response.json()["image"]["base64"]
        
        # Base64データをデコードしてファイルに保存するナリ！
        # data:image/png;base64, の部分を除去するナリ！
        image_base64 = image_data.split(',')[1] if ',' in image_data else image_data
        with open("grass_field.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
        
        print("草原の画像が作成されたナリ！(｀・ω・´)ゞ")

    except Exception as e:
        print(f"エラーが発生してしまったナリ... (´;ω;｀) : {str(e)}")

if __name__ == "__main__":
    create_grass_field_image()