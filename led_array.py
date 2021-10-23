from machine import Pin
import time

class led_sequence():
    led_pins = [20,17,18,19,]
    sequence =[
        [0,0,0,0],
        [0,0,0,1],
        [0,0,1,0],
        [0,0,1,1],
        [0,1,0,0],
        [0,1,0,1],
        [0,1,1,0],
        [0,1,1,1],
        [1,0,0,0],
        [1,0,0,1],
        [1,0,1,0],
        [1,0,1,1],
        [1,1,0,0],
        [1,1,0,1],
        [1,1,1,0],
        [1,1,1,1],
    ]
    def __init__(self):
        self.leds = [Pin(p, Pin.OUT) for p in self.led_pins]
        [p.low() for p in self.leds]
        self.seq_place = 0
        
    def light_all(self):
        [p.high() for p in self.leds]
        
    def light_none(self):
        [p.low() for p in self.leds]    
    
    def set_place(self,place):
        if (place < 0) or (place > len(self.sequence)-1):
            raise ValueError("Place must be an index within " + 
                             "the sequence array (len ={})".format(len(self.sequence)))
        self.seq_place = place
        
    
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
        time.sleep(0.5)
