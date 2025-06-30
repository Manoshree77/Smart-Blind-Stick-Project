# Blind Stick Project

This project details the development of a MicroPython-based smart stick designed to assist individuals with visual impairments. The system incorporates an ultrasonic sensor for obstacle detection, which triggers a buzzer to alert the user of nearby hazards. Additionally, a servo motor provides tactile feedback in the presence of static obstructions. An emergency button is integrated to transmit real-time alerts via Telegram, thereby enhancing user safety.

---

## Features

- Obstacle detection utilizing an ultrasonic sensor  
- Audible alerts through a buzzer for imminent obstacles  
- Servo motor activation for static object identification  
- Emergency notification system via Telegram messaging  
- Wireless communication enabled by ESP32/ESP8266 microcontrollers  

---

## Hardware Components

- ESP32 or ESP8266 microcontroller  
- HC-SR04 ultrasonic sensor  
- Buzzer  
- Servo motor  
- Push button  
- Appropriate power supply  

---

## Software Libraries

- MicroPython modules: `network`, `urequests`, `machine`, `time`, `utime`  

---

## Setup Instructions

### 1. Flash MicroPython  
Refer to the official MicroPython documentation for flashing instructions: https://micropython.org/download/

### 2. Upload Program Code  
Transfer the `blind_stick.py` script to the microcontroller using suitable tools, such as:  
- Thonny IDE  
- uPyCraft  
- ampy  

### 3. Configure Wi-Fi and Telegram Credentials  
Edit the following parameters in the script prior to deployment:

```python
ssid = 'YourWiFiName'
password = 'YourWiFiPassword'
bot_token = 'YourTelegramBotToken'
chat_id = 'YourChatID'
```

---

This system exemplifies the integration of embedded systems and IoT technology to address accessibility challenges for visually impaired individuals.



How It Works
When the distance to an object is less than 30cm, the buzzer activates.

If the object stays in place for more than 3 seconds, the servo motor reacts.

If the emergency button is pressed, a Telegram alert is instantly sent.
