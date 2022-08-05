from machine import Pin
import utime


# mainboard led
#led = Pin(25, Pin.OUT)


class led_sequence():
    led_pins = [20,17,18,19,]
    sequence =[
        [1,1,1,1],
        [0,0,0,1],
        [0,0,1,0],
        [0,1,0,0],
        [1,0,0,0],
    ]
    def __init__(self):
        self.leds = [Pin(p, Pin.OUT) for p in self.led_pins]
        [p.low() for p in self.leds]
        self.seq_place = 0
    
    def seq_next(self):
        self.seq_place += 1
        if self.seq_place > (len(self.sequence)-1):
            self.seq_place = 0
        led_states = self.sequence[self.seq_place]
        for pinnum,pin in enumerate(self.leds):
            if(led_states[pinnum]):
                pin.high()
            else:
                pin.low()



def led_run():
    
    ledseq = led_sequence()
    
    while True:
        ledseq.seq_next()
        utime.sleep(0.5)


TIME_WINDOW = 60000

def click_ctr():
    ledseq = led_sequence()
    tickctr= []
    
    btn = Pin(15, Pin.IN, Pin.PULL_DOWN)
    
    
    while True:
        # look for the button press
        if btn.value() == 1:
            now = utime.ticks_ms()
            tickctr.append(now)
            for tick in tickctr:
                if utime.ticks_diff(now,tick) > TIME_WINDOW:
                    tickctr.remove(tick)
            
            print("Counts per minute= {}".format(len(tickctr)))
            ledseq.seq_next() # leds to next
            #utime.sleep(0.1) # debounce wait
            while btn.value() == 1: # wait for release
                pass
            
            
            
        

