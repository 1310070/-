
# 音声認識＋LCD表示システム（Raspberry Pi用）

## 概要
このプロジェクトは、Raspberry PiとUSBマイク、I2C接続のLCDディスプレイを使用し、  
ボタンを押して音声を録音・認識し、「天気」「予定」などのキーワードに応じてLCDへ情報を表示するPythonアプリケーションです。

- 「天気」と話す → OpenWeatherMap APIで天気表示  
- 「予定」と話す → Googleカレンダーから当日の予定を2件まで表示

## 必要なハードウェア
- Raspberry Pi  
- USBマイク  
- I2C接続LCD（例：PCF8574ベースの16x2キャラクタ液晶）  
- ボタンスイッチ（GPIO接続）  

## インストール方法

1. **必要ライブラリのインストール**
    ```bash
    pip install gpiozero sounddevice speechrecognition requests RPLCD google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

2. **GoogleカレンダーAPIの設定**
    - Google Cloud Consoleでプロジェクトを作成
    - 「Google Calendar API」を有効化
    - OAuth2クライアントID（デスクトップアプリ）を作成し、`credentials.json`をRaspberry Piに保存  
      ※ 保存場所はスクリプト内で指定されているパス（`/home/pi/ex7/credentials.json`）に合わせてください

3. **OpenWeatherMap APIキーの取得**
    - OpenWeatherMapに登録し、APIキーを取得
    - `app.py`内の`API_KEY`に自分のキーをセット

4. **ハードウェアの接続**
    - ボタン：GPIO25（デフォルト設定、必要に応じて変更可能）
    - LCD：I2C接続、アドレス0x3f（変更する場合は`LCD_ADDR`を書き換え）

## 使い方
```bash
python3 app.py
```
## 実行結果
```bash
pi@raspberrypi:~/ex7 $ python3 app.py
認識結果: 天気
kitakataの気温: 32℃
湿度: 59%
LCD表示: deg : 32 hum : 59
認識結果: 予定
予定: 13:00 Valorant
LCD表示: 13:00 Valorant 
認識結果: 天気
kitakataの気温: 32℃
湿度: 59%
LCD表示: deg : 32 hum : 59
```
