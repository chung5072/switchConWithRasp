import time
import RPi.GPIO as GPIO
import subprocess
from flask import Flask, render_template, redirect

pin_num = 11

freq = 100.0
deg_min = 0.0
deg_max = 180.0
dc_min = 5.0
dc_max = 22.0

action = 0

def convert_dc(deg):
    return ((deg - deg_min) * (dc_max - dc_min) / (deg_max - deg_min) + dc_min)

def switchON():
    global action
    action = 1

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin_num, GPIO.OUT)

    p = GPIO.PWM(pin_num, freq)

    p.start(0)
    for deg in range(90, 29, -60):
        offDc_on = convert_dc(float(deg))
        p.ChangeDutyCycle(offDc_on)
        time.sleep(0.5)
    for deg in range(30, 91, 60):
        offDc_off = convert_dc(float(deg))
        p.ChangeDutyCycle(offDc_off)
        time.sleep(0.5)
    p.stop()

    GPIO.cleanup()

def switchOFF():
    global action
    action = 1

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(pin_num, GPIO.OUT)

    p = GPIO.PWM(pin_num, freq)

    p.start(0)
    for deg in range(90, 171, 80):
        onDc_on = convert_dc(float(deg))
        p.ChangeDutyCycle(onDc_on)
        time.sleep(0.5)
    for deg in range(170, 89, -80):
        onDc_off = convert_dc(float(deg))
        p.ChangeDutyCycle(onDc_off)
        time.sleep(0.5)
    p.stop()

    GPIO.cleanup()

app = Flask(__name__)

@app.route('/switch')
def index():
    return render_template('index.html')

@app.route('/turn_off/')
def turnOFF():
    switchOFF()

    global action
    if action == 1:
        action = 0

        return redirect('/switch')

@app.route('/turn_on/')
def turnON():
    switchON()

    global action
    if action == 1:
        action = 0

        return redirect('/switch')

@app.route('/home/')
def goHome():
    return redirect('/switch')

@app.route('/proc_down/')
def serverDOWN():
    return subprocess.call(["sudo", "pkill", "-15", "-ef", "app.py"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5486)
