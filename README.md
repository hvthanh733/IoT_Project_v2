
# 🔥 IoT_Project_v2 - Fire Monitoring & Alert System Using Raspberry Pi

## 📌 Overview

This project is a **real-time IoT-based fire monitoring and alert platform**, designed for critical environments like machine rooms. It integrates multiple distributed sensor nodes and uses secure low-power RF communication (HC-12 modules) to transmit data to a Raspberry Pi. Sensor readings (temperature, humidity, and fire state) are processed and displayed via a web-based interface. The system includes automated warning notifications via email and supports fuzzy logic for nuanced fire risk analysis.

---

## 🧠 System Features

- **Multi-sensor integration** (KY-026 flame sensor, DHT11 temperature/humidity)
- **Wireless transmission** with HC-12 at 433 MHz
- **Data security** using AES-256 encryption, LDPC, LFSR scrambling
- **Real-time monitoring** via a Flask web app
- **Threshold + Fuzzy Logic alerts**
- **Email notifications** and dashboard warning
- **User system**: Admin/user login, alert management, export logs
- **Touchscreen support** (ASUS ZenScreen)
- **Remote access** using VPN (TailScale)

---

## 🧪 Architecture

**Sensor Node (STM32F103C8T6)**:
- Reads sensor data
- Encodes with MAVLink
- Encrypts, scrambles, and transmits via HC-12

**Central Unit (Raspberry Pi 5)**:
- Receives + decodes packets
- Parses values and stores in SQLite
- Visualizes data through Flask dashboard
- Alerts via email and interface

---

## ⚙️ Technologies Used

- Python, Flask, SQLite
- STM32 (C language with STM32CubeIDE)
- MAVLink protocol
- AES-256 (ECB), LDPC, LFSR
- HTML/CSS/JavaScript frontend
- TailScale VPN

---

## 📂 Deployment Summary

To install:

```bash
# Virtual Environment
python3 -m venv venv
source venv/bin/activate

# Libraries
pip install adafruit-circuitpython-dht python-dotenv flask jwt flask-sqlalchemy zlapi RPi.GPIO flask_login
sudo apt install libgpiod-dev python3-lgpio liblgpio1
```

---

## 🙏 Acknowledgements

I sincerely thank my thesis supervisor Mr. PHAM Ngoc Minh (IOIT), co-supervisor Mr. LE Chu Nhu Hiep (USTH), and Mr. NGO Duy Tan (VNSC) for their unwavering support and technical mentorship. Gratitude also to my friends Son, Kien, Anh, Quang, and Ms. Huong for their constant encouragement, and to my family for their unconditional love.

> “There’s nothing more rewarding than working with someone who is smarter than you are, so go find people who make you feel stupid in comparison.” — *Russell Merrick*

---

## 📘 Author

**Hoang Viet Thanh**  
University of Science and Technology of Hanoi  
Bachelor’s Thesis – ICT Major  
Academic Year: 2024–2025
