import gradio as gr
import requests
import json
import base64
import os
from dotenv import load_dotenv
from PIL import Image
import io
from google.cloud import translate_v2 as translate
import uuid
import re

def translate_to_english(text):
    # Google Translate クライアントを初期化するナリ！
    translate_client = translate.Client()
    
    try:
        # 日本語から英語に翻訳するナリ！
        result = translate_client.translate(
            text,
            target_language='en',
            source_language='ja'
        )
        # 翻訳結果から特殊文字を除去するナリ！
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', result['translatedText'])
        return cleaned_text
    except Exception as e:
        print(f"翻訳でエラーが発生したナリ... (´;ω;｀) : {str(e)}")
        return text  # エラーの場合は元のテキストを返すナリ！

def create_pixel_art(prompt, width, height):
    # .envファイルから環境変数を読み込むナリ！
    load_dotenv()
    
    # 環境変数からAPIキーを取得するナリ！
    api_key = os.getenv('PIXELLAB_API_KEY')
    if not api_key:
        raise ValueError("PIXELLAB_API_KEYが設定されていないナリ！.envファイルを確認するナリ！")

    # APIのエンドポイントを設定するナリ！
    api_url = "https://api.pixellab.ai/v1/generate-image-pixflux"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 8の倍数に丸めるナリ！
    width = (width // 8) * 8
    height = (height // 8) * 8
    
    # サイズの制限をチェックするナリ！
    if width < 32 or height < 32:
        raise ValueError("サイズは最小32x32ピクセルが必要ナリ！")
    if width > 400 or height > 400:
        raise ValueError("サイズは最大400x400ピクセルまでナリ！")

    # プロンプトから特殊文字を除去するナリ！
    cleaned_prompt = re.sub(r'[^\x00-\x7F]+', '', prompt)
    
    payload = {
        "description": cleaned_prompt,  # クリーンなプロンプトを使用
        "image_size": {
            "width": width,
            "height": height
        },
        "no_background": True
    }

    try:
        # APIリクエストを送信するナリ！
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        # レスポンスからbase64エンコードされた画像を取得するナリ！
        image_data = response.json()["image"]["base64"]
        
        # Base64データをデコードしてPIL Imageに変換するナリ！
        image_base64 = image_data.split(',')[1] if ',' in image_data else image_data
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))

        # assetsフォルダがなければ作成するナリ！
        os.makedirs("assets", exist_ok=True)
        
        # より安全なファイル名を生成するナリ！
        try:
            safe_filename = str(uuid.uuid4())[:8]  # ランダムなIDを生成
            filename = f"assets/pixel_{safe_filename}.png"
            print(f"ファイル名をエンコードしてみるナリ！: {filename}")
            # エンコーディングのテストをするナリ！
            filename.encode('latin-1')
        except UnicodeEncodeError as e:
            print(f"問題のある文字列ナリ！: {repr(filename)}")
            print(f"エンコードできない文字の位置ナリ！: {e.start}-{e.end}")
            print(f"エンコードできない文字ナリ！: {repr(filename[e.start:e.end])}")
            raise

        # 画像を保存するナリ！
        image.save(filename)
        print(f"画像を保存したナリ！: {filename}")
        
        return filename

    except Exception as e:
        print(f"エラーが発生してしまったナリ... (´;ω;｀) : {str(e)}")
        print(f"エラーの種類ナリ！: {type(e)}")
        if hasattr(e, '__traceback__'):
            import traceback
            print("詳細なエラー情報ナリ！:")
            traceback.print_tb(e.__traceback__)
        return None

def list_generated_images():
    # assetsフォルダ内の画像を一覧表示するナリ！
    if not os.path.exists("assets"):
        return []
    
    image_files = [os.path.join("assets", f) for f in os.listdir("assets") if f.endswith(('.png', '.jpg', '.jpeg'))]
    return image_files

def create_ui():
    with gr.Blocks() as app:
        gr.Markdown("# ピクセルアートジェネレーター (｀・ω・´)ゞ")
        
        with gr.Row():
            with gr.Column():
                prompt_input = gr.Textbox(
                    label="どんなピクセルアートを作りたいナリ？", 
                    placeholder="例: かわいい猫、ドット絵風の城など..."
                )
                
                # 翻訳されたテキストを表示するナリ！
                translated_text = gr.Textbox(
                    label="英語に翻訳されたプロンプト",
                    interactive=False
                )
                
                with gr.Row():
                    width_input = gr.Slider(
                        minimum=8,
                        maximum=400,
                        step=8,
                        value=32,
                        label="横幅（ピクセル）",
                    )
                    height_input = gr.Slider(
                        minimum=8,
                        maximum=400,
                        step=8,
                        value=32,
                        label="縦幅（ピクセル）",
                    )
                
                generate_btn = gr.Button("生成するナリ！", variant="primary")
            
            with gr.Column():
                output_image = gr.Image(label="生成されたピクセルアート")
        
        gallery = gr.Gallery(
            label="生成されたピクセルアート一覧", 
            show_label=True,
            columns=4,
            height=400,
            value=list_generated_images()
        )
        
        def generate_and_update(prompt, width, height):
            try:
                # プロンプトを翻訳するナリ！
                english_prompt = translate_to_english(prompt)
                
                # 翻訳されたプロンプトを渡すナリ！
                image_path = create_pixel_art(english_prompt, width, height)
                if image_path:
                    return [english_prompt, image_path, list_generated_images()]
                return [english_prompt, None, list_generated_images()]
            except ValueError as e:
                gr.Warning(str(e))
                return [None, None, list_generated_images()]
        
        generate_btn.click(
            fn=generate_and_update,
            inputs=[prompt_input, width_input, height_input],
            outputs=[translated_text, output_image, gallery]
        )
    
    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
    )
