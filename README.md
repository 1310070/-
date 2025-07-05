# -音声認識＋LCD表示システム（Raspberry Pi用）
概要
このプロジェクトは、Raspberry PiとUSBマイク、I2C接続のLCDディスプレイを使用し、
ボタンを押して音声を録音・認識し、「天気」「予定」などのキーワードに応じてLCDへ情報を表示するPythonアプリケーションです。

「天気」と話す → OpenWeatherMap APIで天気表示

「予定」と話す → Googleカレンダーから当日の予定を2件まで表示


必要なハードウェア
Raspberry Pi

USBマイク

I2C接続LCD（例：PCF8574ベースの16x2キャラクタ液晶）

ボタンスイッチ（GPIO接続）

インストール方法
1. 必要ライブラリのインストール
pip install gpiozero sounddevice speechrecognition requests RPLCD google-api-python-client google-auth-httplib2 google-auth-oauthlib
2. GoogleカレンダーAPIの設定
Google Cloud Consoleでプロジェクトを作成

「Google Calendar API」を有効化

OAuth2クライアントID（デスクトップアプリ）を作成し、credentials.jsonをRaspberry Piに保存
保存場所はスクリプト内で指定されているパス(/home/pi/ex7/credentials.json)に合わせてください

3. OpenWeatherMap APIキーの取得
OpenWeatherMapに登録し、APIキーを取得

app.py内のAPI_KEYに自分のキーをセット

4. ハードウェアの接続
ボタン：GPIO25（デフォルト設定、必要に応じて変更可能）

LCD：I2C接続、アドレス0x3f（変更する場合はLCD_ADDRを書き換え）

使い方
python3 app.py
「Push & Talk...」が表示されたらボタンを押す

「REC... 話して下さい」と表示される間に話しかける

話し終えたらボタンを離す

認識結果がLCDに短く表示され、
　キーワードが含まれていれば天気または予定がLCDに表示される

設定ファイル・ソースコード
app.py: メインプログラム

注意事項
初回のGoogleカレンダーAPI利用時は、認証ウィンドウが開きます

LCDやボタンの接続は、誤配線に注意してください

2025/07/05現在

変更の可能性あり
