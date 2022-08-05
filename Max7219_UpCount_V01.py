'''
 Demonstrates the use of MAX7219, digits of 7 Segment display.
 
 * Demonstrate "4 Digit Up Count" at the interval of 100mS.
 * Starting with 9950
 * Resets after it reaches 10000

 The Raspberry Pi Pico circuit connection for MAX7219:

 * MAX7219 VCC pin to VBUS
 * MAX7219 GND pin to GND
 * MAX7219 DIN pin to digital GPIO3
 * MAX7219 CS pin to digital GPIO5
 * MAX7219 CLOCK pin to digital GPIO2

 Name:- M.Pugazhendi
 Date:-  08thJul2021
 Version:- V0.1
 e-mail:- muthuswamy.pugazhendi@gmail.com
'''

# Import MicroPython libraries of PIN and SPI
from machine import Pin, SPI

# Import MicoPython MAX7219, 8 digit, 7segment library
import max7219_8digit

# Import timer library
import time

#Intialize the SPI
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)

#Initialize count variable with 9950 as initial value
count=9950

# Create display instant
display = max7219_8digit.Display(spi, ss)

# Unconditionally execute the loop
while True:
 
 # Prefix "UP -" and add "count variable" as string
 temp = "UP -" + str(count)
 
 # Write the string into display buffer
 display.write_to_buffer(temp)
 
 # Write the buffer into MAX7219
 display.display()
 
 # Increment the count
 count = count + 1
 
 # Validate the count value. If exceeds 10000, reset it it zero.
 if count == 10000:
     count = 0
     
 # Sleep for about 100mS.   
 time.sleep(0.1)
 