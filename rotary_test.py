from rotary_irq_rp2 import RotaryIRQ
import time
from machine import Pin


r = RotaryIRQ(pin_num_clk=10, 
              pin_num_dt=12, 
              min_val=0, 
              max_val=25, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)

btn = Pin(16, Pin.IN, Pin.PULL_UP)

              
val_old = r.value()
while btn.value() == 1:
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        
    time.sleep_ms(50)
    
    
    
    
    