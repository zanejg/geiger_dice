from machine import Pin
import utime


# mainboard led
#led = Pin(25, Pin.OUT)


def led_sequence():
    led_pins = [20,17,18,19,]

    leds = [Pin(p, Pin.OUT) for p in led_pins]



    while True:
        for pin in leds:
            pin.high()
            utime.sleep(0.5)
        for pin in leds:
            pin.low()
        
        utime.sleep(0.5)

