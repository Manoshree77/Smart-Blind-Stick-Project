import network
import urequests
import utime
import time
from machine import Pin, PWM, time_pulse_us

# ====== Wi-Fi Credentials ======
ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'

# ====== Telegram Bot Details ======
bot_token = 'YOUR_BOT_TOKEN'
chat_id = 'YOUR_CHAT_ID'
message_text = 'Emergency! The button has been pressed.'

# ====== Pin Setup ======
button = Pin(13, Pin.IN, Pin.PULL_UP)  # Emergency button
TRIG = Pin(15, Pin.OUT)  # Ultrasonic trigger
ECHO = Pin(14, Pin.IN)   # Ultrasonic echo
buzzer = PWM(Pin(16))    # Buzzer
servo = PWM(Pin(17))     # Servo

# ====== Buzzer and Servo Setup ======
buzzer.freq(1000)
buzzer.duty_u16(0)  # Buzzer OFF
servo.freq(50)
servo.duty_u16(1500)  # Neutral position

# ====== Wi-Fi Connection ======
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to WiFi...')
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        utime.sleep(1)
print('Connected to WiFi:', wlan.ifconfig())

# ====== Helper Functions ======

def read_distance():
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()
    duration = time_pulse_us(ECHO, 1, 30000)
    if duration > 0:
        return (duration / 2) / 29.1
    return None

def move_servo():
    print("Static object detected - moving servo")
    servo.duty_u16(2500)
    time.sleep(1)
    servo.duty_u16(1500)

def send_telegram_alert():
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message_text}"
    try:
        response = urequests.get(url)
        print("Telegram message sent:", response.text)
        response.close()
        return True
    except Exception as e:
        print("Error sending Telegram message:", e)
        return False

# ====== Variables ======
THRESHOLD = 30  # cm
STATIC_WAIT_TIME = 3  # seconds
message_sent = False
prev_distance = None
still_start = None

# ====== Main Loop ======
while True:
    # --- Emergency Button Handling ---
    if not button.value():  # Button pressed
        if not message_sent:
            print("Button pressed. Sending Telegram alert...")
            if send_telegram_alert():
                message_sent = True
        utime.sleep(0.5)
    else:
        message_sent = False  # Reset on release

    # --- Obstacle Detection ---
    distance = read_distance()
    if distance:
        print("Distance: {:.2f} cm".format(distance))
        if distance < THRESHOLD:
            buzzer.duty_u16(32768)  # Buzzer ON
            if prev_distance and abs(distance - prev_distance) < 0.5:
                if still_start is None:
                    still_start = time.time()
                elif time.time() - still_start >= STATIC_WAIT_TIME:
                    move_servo()
                    still_start = None
            else:
                still_start = None  # Movement detected, reset
        else:
            buzzer.duty_u16(0)
            still_start = None
    else:
        print("No echo received")
        buzzer.duty_u16(0)

    prev_distance = distance
    time.sleep(0.5)
