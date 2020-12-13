import RPi.GPIO as GPIO
import time

switchNF = raw_input("Enter Code: ")

GPIO.setmode(GPIO.BOARD)

pin_num = 11

GPIO.setup(pin_num, GPIO.OUT)

freq = 100.0
deg_min = 0.0
deg_max = 180.0
dc_min = 5.0
dc_max = 22.0

def convertDC(deg):
    return ((deg - deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min)

p=GPIO.PWM(pin_num, freq)

p.start(0)

"""
for deg in range(0, 181, 30):
    dcH = convertDC(float(deg))
    p.ChangeDutyCycle(dcH)
    time.sleep(1)
"""

if switchNF == "r":
    for deg in range(80, 101, 10):
        dcR = convertDC(float(deg))
        p.ChangeDutyCycle(dcR)
        time.sleep(1)
elif switchNF == "o":
    for deg in range(90, 29, -60):
        dcO = convertDC(float(deg))
        p.ChangeDutyCycle(dcO)
        time.sleep(0.5)
    for deg in range(30, 91, 60):
        dcO = convertDC(float(deg))
        p.ChangeDutyCycle(dcO)
        time.sleep(0.5)
elif switchNF == "f":
    for deg in range(90, 171, 80):
        dcF = convertDC(float(deg))
        p.ChangeDutyCycle(dcF)
        time.sleep(0.5)
    for deg in range(170, 89, -80):
        dcF = convertDC(float(deg))
        p.ChangeDutyCycle(dcF)
        time.sleep(0.5)
else:
     pass

p.stop()

GPIO.cleanup()
