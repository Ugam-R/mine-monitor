import serial

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

print("Connected to Arduino!")
print("Waiting for sensor data...\n")

while True:
    data = arduino.readline().decode('utf-8', errors='ignore').strip()

    if data:
        print(data)