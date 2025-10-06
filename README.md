
# IoT_Project_v2 - Investigation of IoT-Based Monitoring and Alert System for Machine Room Safety Using Raspberry Pi 


## Overview

Nowadays, technology is growing quickly. Many labs and machine rooms are used to test new techniques and systems. As a result, these places can have risks of fire because of using flammable materials and high electricity. To ensure the safety of the machine room, we suggest deploying a fire monitoring and alert system. This IoT monitoring and alert system was born from that. It include 2 parts: The Sensor Nodes, The Central Procesing. At The Sensor Nodes, sensor readings Temperature, Humidity, and Fire state values then encoded and send to wiresless communication. At the CPU, received the encoded message and deocode it, and also deploy web-based interface. The system automated warning notifications via email and using **Fuzzy Logic** combine with Threshold to evaluate the risk of Fire.

---

## System Features

- **Multi-sensor integration**: Flame Sensor - KY-026, Temperature, Humidity -  DHT11
- **Wireless transmission**: Basic raw RF - HC-12 at 433 MHz
- **Real-time monitoring**: Flask web-based
- **Threshold + Fuzzy Logic alerts**
- **Email notifications**
- **Touchscreen support**: ASUS ZenScreen
- **Remote access**: **VPN** - TailScale

---

## Architecture

**Sensor Node (STM32F103C8T6)**:
- Collecting enviroment data
- Encodes then transmits through HC-12

**Central Unit (Raspberry Pi 5)**:
- Receives then decodes message
- Deploy Web interface for user
- Alerts through email and sound using Threshold and **Fuzzy Logic**

---

## Technologies Used

- **Backend**: Python, Flask, SQLite
- **Frontend**: HTML/CSS/JavaScript
- **VPN**: TailScale
- **Microcontroller**: STM32 (C language with STM32CubeIDE, STM32CubeMX)
- **Encode**: MAVLink protocol, PKCS7, AES-256, LDPC, LFSR.
- **Central Processing Unit**: Raspberry Pi 5
---

## Deployment Summary

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

## Acknowledgements

I sincerely thank my thesis supervisor Mr. PHAM Ngoc Minh (IOIT), co-supervisor Mr. LE Nhu Chu Hiep (USTH), and Mr. NGO Duy Tan (VNSC) for their unwavering support and technical mentorship. Gratitude also to my friends HOANG Van Son, NGUYEN Trung Kien, NGUYEN Nhat Anh, DOAN Quang, HO Cong Thanh, and Ms. NGUYEN Minh Huong for their constant encouragement, and to my family for their unconditional love.

> “There’s nothing more rewarding than working with someone who is smarter than you are, so go find people who make you feel stupid in comparison.” — *Russell Merrick*

---

## Author

**Hoang Viet Thanh**  
University of Science and Technology of Hanoi  
Bachelor’s Thesis – ICT Major 
Academic Year: 2024–2025
