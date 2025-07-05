import gpiozero
import sounddevice as sd
import speech_recognition as sr
import requests
import time
import io
from RPLCD.i2c import CharLCD
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import datetime
import os

# --- 設定 ---
BUTTON_PIN = 25
SAMPLE_RATE = 16000
CITY_NAME = "Your city" #choose from OpenWeatherMap
API_KEY = "Your API key" # copy and paste from OpenWeeatherMap
LCD_ADDR = 0x3f

# Google Calendar API用
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = '/home/pi/ex7/credentials.json'  # パスは自分の環境に合わせて
TOKEN_FILE = '/home/pi/ex7/token.json'

# --- LCD初期化 ---
lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDR, port=1, cols=16, rows=2, charmap='A00', backlight_enabled=True)

# --- ボタン初期化 ---
btn = gpiozero.Button(BUTTON_PIN, pull_up=False)

# --- 音声認識初期化 ---
rec = sr.Recognizer()

def record_audio():
    """ボタン押してる間だけ録音→AudioData返す"""
    buf = io.BytesIO()
    def callback(indata, frames, time_, status):
        buf.write(indata)
        if not btn.is_pressed:
            raise sd.CallbackStop()
    with sd.RawInputStream(samplerate=SAMPLE_RATE, dtype='int16', channels=1, callback=callback):
        while btn.is_pressed:
            time.sleep(0.01)
    return sr.AudioData(buf.getvalue(), SAMPLE_RATE, 2)  # 2byte=16bit

def recognize(audio_data):
    """Google Speech Recognitionで認識（日本語）"""
    try:
        return rec.recognize_google(audio_data, language='ja-JP')
    except Exception as e:
        print("音声認識エラー:", e)
        return ""

def get_weather():
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={API_KEY}&lang=ja&units=metric'
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        temp = int(round(data['main']['temp']))         # 気温（整数で表示）
        humidity = data['main']['humidity']             # 湿度
        print(f"kitakataの気温: {temp}℃")
        print(f"湿度: {humidity}%")
        return f"deg : {temp}", f"hum : {humidity}"
    else:
        print("天気情報の取得に失敗しました。")
        return "天気取得失敗", ""

def get_today_events():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now().astimezone()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + datetime.timedelta(days=1)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=today_start.isoformat(),
        timeMax=today_end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        print("本日の予定：なし")
        return "予定なし", ""

    output = []
    for event in events[:2]:  # 2件まで
        start = event['start'].get('dateTime', event['start'].get('date'))
        t = start[11:16] if "T" in start else "終日"
        summary = event.get("summary", "（無題）")
        entry = f"{t} {summary}"
        print("予定:", entry)
        output.append(entry[:16])
    if len(output) == 1:
        return output[0], ""
    else:
        return output[0], output[1]

def lcd_show(line1, line2=""):
    lcd.clear()
    lcd.write_string(line1[:16])
    lcd.crlf()
    lcd.write_string(line2[:16])

# --- メインループ ---
lcd_show("Push & Talk...")

while True:
    btn.wait_for_press()
    lcd_show("REC...", "話して下さい")
    audio_data = record_audio()
    lcd_show("解析中...")
    text = recognize(audio_data)
    print("認識結果:", text)
    lcd_show(">> " + text[:13])
    time.sleep(1)

    # --- キーワード判定 ---
    if "天気" in text:
        line1, line2 = get_weather()
        print("LCD表示:", line1, line2)
        lcd_show(line1, line2)
    elif "予定" in text:
        line1, line2 = get_today_events()
        print("LCD表示:", line1, line2)
        lcd_show(line1, line2)
    else:
        print("キーワードなし")

    time.sleep(2)
    lcd_show("Push & Talk...")
