```markdown
# Open MenudevOAS 3.1.0 Pixel Lab API

## 概要

このAPIは、AIによって生成されたピクセルアート画像、回転、アニメーションなどの作成を行うためのエンドポイントを提供します。これにより、アプリケーションがピクセルアート生成機能を簡単に統合できるようになります。

## Pythonクライアント

利便性のために、アプリケーションとの統合を簡素化するためのPythonクライアントライブラリが用意されています。インストール手順と例については、[GitHubリポジトリ]([GitHubリポジトリへのリンク]) を参照してください。

```bash
pip install pixellab
```

## 認証

APIは、シンプルなトークンベースの認証システムを使用します。アカウントを作成した後、[アカウント設定]でAPIトークンを見つけることができます。このトークンを、Bearer認証スキームを使用してすべてのAPIリクエストに含めてください。

```bash
curl -X POST https://api.pixellab.ai/v1/generate-image-pixflux \
    -H "Authorization: Bearer YOUR_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "description": "かわいいドラゴン",
        "image_size": {"width": 128, "height": 128}
    }'
```

または、Pythonクライアントを使用します。

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")
client.generate_image_pixflux(
    description="かわいいドラゴン",
    image_size=dict(width=128, height=128),
)
```

## サポートされているモデル

*   **Generate Image Bitforge:** 参照画像を使用してカスタムアートスタイルを適用します。
*   **Generate Image Pixflux:** テキスト記述からピクセルアートを生成します。
*   **Animate (skeleton):** スケルトンポーズから4フレームのアニメーションを生成します。
*   **Inpaint:** 既存のピクセルアートを編集および変更します。
*   **Rotate:** オブジェクトまたはキャラクターを回転させます。

## サーバー

*   **ベースURL:** `https://api.pixellab.ai/v1`
*   **認証:** Bearerトークン

## クライアントライブラリ

*   Shell
*   Ruby
*   Node.js
*   PHP
*   Python
*   Libcurl
*   HttpClient
*   RestSharp
*   clj-http
*   NewRequest
*   HTTP/1.1
*   AsyncHttp
*   java.net.http
*   OkHttp
*   Unirest
*   Fetch
*   Axios
*   ofetch
*   jQuery
*   XHR
*   OkHttp
*   Fetch
*   Axios
*   ofetch
*   undici
*   NSURLSession
*   Cohttp
*   cURL
*   Guzzle
*   Invoke-WebRequest
*   Invoke-RestMethod
*   http.client
*   Requests
*   httr
*   net::http
*   Curl
*   Wget
*   HTTPie
*   NSURLSession
*   More

## Generate Image

### Generate Image エンドポイント

*   `POST /generate-image-pixflux`
*   `POST /generate-image-bitforge`

### Generate image (pixflux)

提供されたパラメータに基づいてピクセルアート画像を作成します。プラグインでは "Create image (new)" と呼ばれます。

*   サポートされる画像サイズ: 最小面積 32x32、最大面積 400x400
*   サポートされる機能:
    *   初期画像
    *   強制パレット
    *   透明な背景

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")

response = client.generate_image_pixflux(
    description="かわいいドラゴン",
    image_size=dict(width=128, height=128),
)
response.image.pil_image()
```

**リクエストボディ (application/json):**

**GenerateImagePixfluxRequest:**

| パラメータ          | 型      | 必須  | デフォルト | 説明                                                                                                        |
| ------------------ | -------- | ---- | -------- | --------------------------------------------------------------------------------------------------------- |
| description        | string   | YES  |          | 生成する画像のテキスト記述                                                                                           |
| negative_description | string   | NO   | ""       | 生成された画像で回避する内容のテキスト記述                                                                                      |
| image_size         | object   | YES  |          | [ImageSize](#imagesize)オブジェクト                                                                                         |
| text_guidance_scale | number   | NO   | 8        | テキスト記述にどれだけ忠実に従うか (min: 1, max: 20)                                                                             |
| outline            | object  | NO   |          | [Outline](#outline)スタイル参照 (弱ガイダンス)                                                                      |
| shading            | object  | NO   |          | [Shading](#shading)スタイル参照 (弱ガイダンス)                                                                      |
| detail             | object  | NO   |          | [Detail](#detail)スタイル参照 (弱ガイダンス)                                                                       |
| view               | object  | NO   |          | [CameraView](#cameraview) カメラ視点 (弱ガイダンス)                                                                    |
| direction          | object  | NO   |          | [Direction](#direction) 被写体の方向 (弱ガイダンス)                                                                      |
| isometric          | boolean  | NO   | false    | 等角投影で生成するか (弱ガイダンス)                                                                                            |
| no_background      | boolean  | NO   | false    | 透明な背景で生成するか (200x200以上の領域では空白の背景になります)                                                                     |
| init_image         | object   | NO   |          | [Base64Image](#base64image) 初期画像 (base64エンコードされた画像)                                                                   |
| init_image_strength| integer  | NO   | 300      | 初期画像の影響の強さ (min: 1, max: 999)                                                                                     |
| color_image        | object   | NO   |          | [Base64Image](#base64image) 強制カラーパレット。パレットに使用される色を含む画像 (base64エンコードされた画像) |
| seed               | integer  | NO   |          | 開始ノイズを決定するシード                                                                                                |

**ImageSize:**

| パラメータ  | 型     | 必須  | 説明                               |
| --------- | ------- | ---- | ---------------------------------- |
| width     | integer | YES  | 画像の幅                           |
| height    | integer | YES  | 画像の高さ                           |

**Base64Image:**

| パラメータ | 型           | 必須  | 説明                       |
| -------- | ----------- | ---- | -------------------------- |
| type     | Literal["base64"] | YES | 常に "base64" で画像エンコードタイプを示す |
| base64   | string      | YES  | base64エンコードされた画像データ      |

**Outline, Shading, Detail, CameraView, Direction:**

これらは列挙型で、具体的な値はAPIドキュメントを参照してください。

**レスポンス:**

*   **200:** 画像の生成に成功 (application/json)
*   **401:** 無効なAPIトークン
*   **402:** クレジット不足
*   **422:** バリデーションエラー
*   **429:** リクエストが多すぎます
*   **529:** レート制限を超えました

**レスポンススキーマ:**

```json
{
  "image": {
    "type": "base64",
    "base64": "data:image/png;base64,..."
  },
  "usage": {
    "type": "credits",
    "credits": 1
  }
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/generate-image-pixflux \
    --request POST \
    --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
    --header 'Content-Type: application/json' \
    --data '{"description": "","negative_description": "","image_size": {"width": 1,"height": 1},"text_guidance_scale": 8,"outline": "single color black outline","shading": "flat shading","detail": "low detail","view": "side","direction": "north","isometric": false,"no_background": false,"init_image": {"type": "base64","base64": ""},"init_image_strength": 300,"color_image": {"type": "base64","base64": ""},"seed": 1}'
```

### Generate image (bitforge)

提供されたパラメータに基づいてピクセルアート画像を生成します。プラグインでは "Generate image (style)" と呼ばれます。

*   サポートされる画像サイズ: 最大面積 200x200
*   サポートされる機能:
    *   スタイル画像
    *   インペイント
    *   初期画像
    *   強制パレット
    *   透明な背景

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")

response = client.generate_image_bitforge(
    description="かわいいドラゴン",
    image_size=dict(width=128, height=128),
)
response.image.pil_image()
```

**リクエストボディ (application/json):**

**GenerateImageBitforgeRequest:**

| パラメータ          | 型      | 必須  | デフォルト | 説明                                                                                                        |
| ------------------ | -------- | ---- | -------- | --------------------------------------------------------------------------------------------------------- |
| description        | string   | YES  |          | 生成する画像のテキスト記述                                                                                           |
| negative_description | string   | NO   | ""       | 生成された画像で回避する内容のテキスト記述                                                                                      |
| image_size         | object   | YES  |          | [ImageSize](#imagesize)オブジェクト                                                                                         |
| text_guidance_scale | number   | NO   | 3        | テキスト記述にどれだけ忠実に従うか (min: 1, max: 20)                                                                             |
| extra_guidance_scale | number | NO   | 3        | スタイル参照にどれだけ忠実に従うか (min: 0, max: 20)                                                                               |
| style_strength     | number   | NO   | 0        | スタイル転送の強度 (0-100)                                                                                                 |
| outline            | object   | NO   |          | [Outline](#outline)スタイル参照                                                                           |
| shading            | object   | NO   |          | [Shading](#shading)スタイル参照                                                                           |
| detail             | object   | NO   |          | [Detail](#detail)スタイル参照                                                                           |
| view               | object   | NO   |          | [CameraView](#cameraview) カメラ視点                                                                        |
| direction          | object   | NO   |          | [Direction](#direction) 被写体の方向                                                                         |
| isometric          | boolean  | NO   | false    | 等角投影で生成するか                                                                                                 |
| oblique_projection | boolean  | NO   | false    | 斜投影で生成するか                                                                                                 |
| no_background      | boolean  | NO   | false    | 透明な背景で生成するか                                                                                                 |
| coverage_percentage | number   | NO   |          | キャンバスをカバーする割合 (min: 0, max: 100)                                                                                    |
| init_image         | object   | NO   |          | [Base64Image](#base64image) 初期画像 (base64エンコードされた画像)                                                                    |
| init_image_strength| integer  | NO   | 300      | 初期画像の影響の強さ (min: 1, max: 999)                                                                                     |
| style_image        | object   | NO   |          | [Base64Image](#base64image) スタイル転送の参照画像 (base64エンコードされた画像)                                                                |
| inpainting_image   | object   | NO   |          | [Base64Image](#base64image) インペイントされる参照画像 (base64エンコードされた画像)                                                          |
| mask_image         | object   | NO   |          | [Base64Image](#base64image) インペイント/マスク画像 (黒と白の画像、白がモデルがインペイントする場所を示す) (base64エンコードされた画像) |
| color_image        | object   | NO   |          | [Base64Image](#base64image) 強制カラーパレット。パレットに使用される色を含む画像 (base64エンコードされた画像) |
| seed               | integer  | NO   |          | 開始ノイズを決定するシード                                                                                                |

**レスポンス:**

*   **200:** 画像の生成に成功 (application/json)
*   **401:** 無効なAPIトークン
*   **402:** クレジット不足
*   **422:** バリデーションエラー
*   **429:** リクエストが多すぎます
*   **529:** レート制限を超えました

**レスポンススキーマ:**
```json
{
  "image": {
    "type": "base64",
    "base64": "data:image/png;base64,..."
  },
  "usage": {
    "type": "credits",
    "credits": 1
  }
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/generate-image-bitforge \
  --request POST \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"description": "","negative_description": "","image_size": {"width": 1,"height": 1},"text_guidance_scale": 3,"extra_guidance_scale": 3,"style_strength": 0,"outline": "single color black outline","shading": "flat shading","detail": "low detail","view": "side","direction": "north","isometric": false,"oblique_projection": false,"no_background": false,"coverage_percentage": 1,"init_image": {"type": "base64","base64": ""},"init_image_strength": 300,"style_image": {"type": "base64","base64": ""},"inpainting_image": {"type": "base64","base64": ""},"mask_image": {"type": "base64","base64": ""},"color_image": {"type": "base64","base64": ""},"seed": 1}'
```

## Animate

### Animate エンドポイント

*   `POST /animate-with-skeleton`

### Generate animation using skeletons

提供されたパラメータに基づいてピクセルアートアニメーションを作成します。プラグインでは "Animate (skeleton)" と呼ばれます。

*   サポートされる画像サイズ:
    *   16x16
    *   32x32
    *   64x64
    *   128x128
*   サポートされる機能:
    *   インペイント
    *   初期画像
    *   強制パレット

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")

response = client.animate_with_skeleton(
    view="side",
    direction="south",
    image_size=dict(width=64, height=64),
    reference_image=reference_image,
    inpainting_images=existing_animation_frames,
    mask_images=mask_images,
    skeleton_keypoints=skeleton_keypoints,
)
images = [image.pil_image() for image in response.images]
```

**リクエストボディ (application/json):**

**AnimateWithSkeletonRequest:**

| パラメータ             | 型      | 必須  | デフォルト | 説明                                                                                                             |
| --------------------- | -------- | ---- | -------- | -------------------------------------------------------------------------------------------------------------- |
| image_size            | object   | YES  |          | [ImageSize](#imagesize)オブジェクト                                                                                              |
| reference_guidance_scale| number   | NO   | 1.1      | テキスト記述にどれだけ忠実に従うか (min: 1, max: 20)                                                                                |
| pose_guidance_scale   | number   | NO   | 3        | スタイル参照にどれだけ忠実に従うか (min: 1, max: 20)                                                                                |
| view                  | object   | NO   |          | [CameraView](#cameraview) カメラ視点                                                                                  |
| direction             | object   | NO   |          | [Direction](#direction) 被写体の方向                                                                                   |
| isometric             | boolean  | NO   | false    | 等角投影で生成するか                                                                                                  |
| oblique_projection    | boolean  | NO   | false    | 斜投影で生成するか                                                                                                  |
| init_images           | array    | NO   |          | [Base64Image](#base64image) の配列。初期画像 (base64エンコードされた画像)                                                           |
| init_image_strength   | integer  | NO   | 300      | 初期画像の影響の強さ (min: 1, max: 999)                                                                                          |
| skeleton_keypoints    | array    | YES  |          | スケルトンポイントの配列                                                                                                  |
| reference_image       | object   | YES  |          | [Base64Image](#base64image) 参照画像 (base64エンコードされた画像)                                                                    |
| inpainting_images     | array    | NO   | [null, null, null, null] | [Base64Image](#base64image) の配列。接続されたスケルトンでモデルを示すために使用される画像 (base64エンコードされた画像) |
| mask_images           | array    | NO   |          | [Base64Image](#base64image) の配列。インペイント/マスク画像 (白がモデルがインペイントする場所を示す) (base64エンコードされた画像)     |
| color_image           | object   | NO   |          | [Base64Image](#base64image) 強制カラーパレット。パレットに使用される色を含む画像 (base64エンコードされた画像)                                                                |
| seed                  | integer  | NO   |          | 開始ノイズを決定するシード                                                                                                    |

**レスポンス:**

*   **200:** 画像の生成に成功 (application/json)
*   **401:** 無効なAPIトークン
*   **402:** クレジット不足
*   **422:** バリデーションエラー
*   **429:** リクエストが多すぎます
*   **529:** レート制限を超えました

**レスポンススキーマ:**
```json
{
    "images": [
        {
            "type": "base64",
            "base64": "data:image/png;base64,..."
        },
        {
            "type": "base64",
            "base64": "data:image/png;base64,..."
        },
         {
            "type": "base64",
            "base64": "data:image/png;base64,..."
        },
        {
            "type": "base64",
            "base64": "data:image/png;base64,..."
        }
    ],
  "usage": {
    "type": "credits",
    "credits": 1
  }
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/animate-with-skeleton \
  --request POST \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"image_size": {"width": 1,"height": 1},"reference_guidance_scale": 1.1,"pose_guidance_scale": 3,"view": "side","direction": "east","isometric": false,"oblique_projection": false,"init_images": [{"type": "base64","base64": ""}],"init_image_strength": 300,"skeleton_keypoints": [[{"x": 1,"y": 1,"label": "NOSE","z_index": 0}]],"reference_image": {"type": "base64","base64": ""},"inpainting_images": [null,null,null,null],"mask_images": [{"type": "base64","base64": ""}],"color_image": {"type": "base64","base64": ""},"seed": 1}'
```

## Rotate

### Rotate エンドポイント

*   `POST /rotate`

### Rotate character or object

提供されたパラメータに基づいてピクセルアート画像を回転させます。プラグインでは "Rotate" と呼ばれます。

*   サポートされる画像サイズ:
    *   16x16
    *   32x32
    *   64x64
    *   128x128
*   サポートされる機能:
    *   初期画像
    *   強制パレット

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")

response = client.rotate(
    from_view="side",
    to_view="side",
    from_direction="south",
    to_direction="east",
    image_size=dict(width=16, height=16),
    from_image=image_of_subject_facing_south,
)
response.image.pil_image()
```

**リクエストボディ (application/json):**

**RotateRequest:**

| パラメータ            | 型      | 必須  | デフォルト | 説明                                                                                                             |
| --------------------- | -------- | ---- | -------- | -------------------------------------------------------------------------------------------------------------- |
| image_size            | object   | YES  |          | [ImageSize](#imagesize)オブジェクト                                                                                              |
| image_guidance_scale  | number   | NO   | 3        | 参照画像にどれだけ忠実に従うか (min: 1, max: 20)                                                                             |
| from_view             | object   | NO   |          | [CameraView](#cameraview) 回転元のカメラ視点                                                                           |
| to_view               | object   | NO   |          | [CameraView](#cameraview) 回転先のカメラ視点                                                                           |
| from_direction        | object   | NO   |          | [Direction](#direction) 回転元の被写体の方向                                                                            |
| to_direction          | object   | NO   |          | [Direction](#direction) 回転先の被写体の方向                                                                            |
| isometric             | boolean  | NO   | false    | 等角投影で生成するか                                                                                                  |
| oblique_projection    | boolean  | NO   | false    | 斜投影で生成するか                                                                                                  |
| init_image            | object   | NO   |          | [Base64Image](#base64image) 初期画像 (base64エンコードされた画像)                                                                      |
| init_image_strength   | integer  | NO   | 300      | 初期画像の影響の強さ (min: 1, max: 999)                                                                                          |
| mask_image            | object   | NO   |          | [Base64Image](#base64image) インペイント/マスク画像。初期画像が必要です! (白がモデルがインペイントする場所を示す) (base64エンコードされた画像) |
| from_image            | object   | YES  |          | [Base64Image](#base64image) 回転元の参照画像 (base64エンコードされた画像)                                                               |
| color_image           | object   | NO   |          | [Base64Image](#base64image) 強制カラーパレット。パレットに使用される色を含む画像 (base64エンコードされた画像)                                                                |
| seed                  | integer  | NO   |          | 開始ノイズを決定するシード                                                                                                    |

**レスポンス:**

*   **200:** 画像の生成に成功 (application/json)
*   **401:** 無効なAPIトークン
*   **402:** クレジット不足
*   **422:** バリデーションエラー
*   **429:** リクエストが多すぎます
*   **529:** レート制限を超えました

**レスポンススキーマ:**
```json
{
  "image": {
    "type": "base64",
    "base64": "data:image/png;base64,..."
  },
  "usage": {
    "type": "credits",
    "credits": 1
  }
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/rotate \
  --request POST \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"image_size": {"width": 1,"height": 1},"image_guidance_scale": 3,"from_view": "side","to_view": "side","from_direction": "south","to_direction": "east","isometric": false,"oblique_projection": false,"init_image": {"type": "base64","base64": ""},"init_image_strength": 300,"mask_image": {"type": "base64","base64": ""},"from_image": {"type": "base64","base64": ""},"color_image": {"type": "base64","base64": ""},"seed": 1}'
```

## Inpaint

### Inpaint エンドポイント

*   `POST /inpaint`

### Inpaint image

提供されたパラメータに基づいてピクセルアート画像を作成します。プラグインでは "Inpaint" と呼ばれます。

*   サポートされる画像サイズ: 最大面積 200x200
*   サポートされる機能:
    *   インペイント
    *   初期画像
    *   強制パレット
    *   透明な背景

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")

response = client.inpaint(
    description="翼のある少年",
    image_size=dict(width=16, height=16),
    inpainting_image=image_of_boy_without_wings,
    mask_image=mask_image,
)
response.image.pil_image()
```

**リクエストボディ (application/json):**

**InpaintRequest:**

| パラメータ            | 型      | 必須  | デフォルト | 説明                                                                                                             |
| --------------------- | -------- | ---- | -------- | -------------------------------------------------------------------------------------------------------------- |
| description           | string   | YES  |          | 生成する画像のテキスト記述                                                                                           |
| negative_description  | string   | NO   | ""       | 生成された画像で回避する内容のテキスト記述                                                                                      |
| image_size            | object   | YES  |          | [ImageSize](#imagesize)オブジェクト                                                                                              |
| text_guidance_scale   | number   | NO   | 3        | テキスト記述にどれだけ忠実に従うか (min: 1, max: 10)                                                                             |
| extra_guidance_scale  | number   | NO   | 3        | スタイル参照にどれだけ忠実に従うか (min: 0, max: 20)                                                                               |
| outline               | object   | NO   |          | [Outline](#outline)スタイル参照                                                                           |
| shading               | object   | NO   |          | [Shading](#shading)スタイル参照                                                                           |
| detail                | object   | NO   |          | [Detail](#detail)スタイル参照                                                                           |
| view                  | object   | NO   |          | [CameraView](#cameraview) カメラ視点                                                                        |
| direction             | object   | NO   |          | [Direction](#direction) 被写体の方向                                                                         |
| isometric             | boolean  | NO   | false    | 等角投影で生成するか                                                                                                 |
| oblique_projection    | boolean  | NO   | false    | 斜投影で生成するか                                                                                                 |
| no_background         | boolean  | NO   | false    | 透明な背景で生成するか                                                                                                 |
| init_image            | object   | NO   |          | [Base64Image](#base64image) 初期画像 (base64エンコードされた画像)                                                                  |
| init_image_strength   | integer  | NO   | 300      | 初期画像の影響の強さ (min: 1, max: 999)                                                                                     |
| inpainting_image      | object   | YES  |          | [Base64Image](#base64image) インペイントされる参照画像 (base64エンコードされた画像)                                                          |
| mask_image            | object   | YES  |          | [Base64Image](#base64image) インペイント/マスク画像。 (白がモデルがインペイントする場所を示す) (base64エンコードされた画像)    |
| color_image           | object   | NO   |          | [Base64Image](#base64image) 強制カラーパレット。パレットに使用される色を含む画像 (base64エンコードされた画像)                                                                |
| seed                  | integer  | NO   |          | 開始ノイズを決定するシード                                                                                                |

**レスポンス:**

*   **200:** 画像の生成に成功 (application/json)
*   **401:** 無効なAPIトークン
*   **402:** クレジット不足
*   **422:** バリデーションエラー
*   **429:** リクエストが多すぎます
*   **529:** レート制限を超えました

**レスポンススキーマ:**
```json
{
  "image": {
    "type": "base64",
    "base64": "data:image/png;base64,..."
  },
  "usage": {
    "type": "credits",
    "credits": 1
  }
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/inpaint \
  --request POST \
  --header 'Authorization: Bearer YOUR_SECRET_TOKEN' \
  --header 'Content-Type: application/json' \
  --data '{"description": "","negative_description": "","image_size": {"width": 1,"height": 1},"text_guidance_scale": 3,"extra_guidance_scale": 3,"outline": "single color black outline","shading": "flat shading","detail": "low detail","view": "side","direction": "north","isometric": false,"oblique_projection": false,"no_background": false,"init_image": {"type": "base64","base64": ""},"init_image_strength": 300,"inpainting_image": {"type": "base64","base64": ""},"mask_image": {"type": "base64","base64": ""},"color_image": {"type": "base64","base64": ""},"seed": 1}'
```

## Account

### Account エンドポイント

*   `GET /balance`

### Get balance

アカウントの現在の残高を返します。

**Pythonクライアントの使用例:**

```python
import pixellab

client = pixellab.Client(secret="YOUR_API_TOKEN")
balance = client.get_balance()
print(f"現在の残高: {balance.usd} USD")
```

**レスポンス:**

*   **200:** 残高の取得に成功 (application/json)
*   **401:** 無効なAPIトークン

**レスポンススキーマ:**

```json
{
    "usd": 100
}
```

**cURL の例:**
```bash
curl https://api.pixellab.ai/v1/balance --header 'Authorization: Bearer YOUR_SECRET_TOKEN'
```
```
