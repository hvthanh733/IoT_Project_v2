# IoT_Project_v2

<!-- venv -->
python3 -m venv venv
source venv/bin/activate

<!-- adafruit-circuitpython-dht -->
pip install adafruit-circuitpython-dht
sudo apt install libgpiod-dev


<!-- lgpio -->
<!-- No venv -->
sudo apt update
sudo apt install python3-lgpio
sudo apt update
sudo apt install liblgpio1 python3-lgpio

<!-- .env -->
pip install python-dotenv

<!-- flask -->
pip install flask

<!-- jwt -->
pip install jwt

<!-- sqlalchemy -->
pip install flask-sqlalchemy


<!-- zlapi -->
pip install zlapi


<!--  -->
pip install RPi.GPIO
pip install flask_login

[Block2]
sensor1 = Temperature & Humidity
sensor2 = Fire
GPIO1 = D16
GPIO2 = 12

[Block3]
sensor1 = Temperature & Humidity
sensor2 = Fire
GPIO1 = D17
GPIO2 = 27

[Block4]
sensor1 = Temperature & Humidity
sensor2 = Fire
GPIO1 = D4
GPIO2 = 14
