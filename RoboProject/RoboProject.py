import serial
import time
import pyautogui

ArduinoSerial = serial.Serial('COM3', 9600)
time.sleep(2)

'''
while 1:
    incoming = str (ArduinoSerial.readline())
    print(incoming)
'''