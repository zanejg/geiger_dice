from machine import Pin,SPI
import time

import led_array
import max7219_8digit
from rotary_irq_rp2 import RotaryIRQ


TIME_WINDOW = 60000
           
class ClickCounter():
    tickctr= []
    
    def __init__(self):
        pass
    
    def add_click(self):
        # detected a click
        now = time.ticks_ms()
        self.tickctr.append(now)
        for tick in self.tickctr:
            if time.ticks_diff(now,tick) > TIME_WINDOW:
                self.tickctr.remove(tick)
    
    def get_clicks_in_window(self):
        return len(self.tickctr)
    


###########################################################
########           Dice Sides                       #######
###########################################################
# the allowable numbers of sides for our dice
dice_sides = [
    2,4,6,8,10,12,20,100
]


###########################################################
########           Box State                        #######
###########################################################
box_state = {
    "mode":"counter", # either counter or dice
    "dice_thrown": False, # set to True at release of big button
    "left_digits": "ctr ",
    'dice_side_idx':2 # the index into dice_sides array
}

            

###########################################################
###               Display                           #######
###########################################################
#Intialize the SPI for the display
spi = SPI(0, baudrate=10000000, polarity=1, phase=0, sck=Pin(2), mosi=Pin(3))
ss = Pin(5, Pin.OUT)
# init the display
display = max7219_8digit.Display(spi, ss)

def write_right(the_str):
    if len(the_str) > 4:
        the_str = the_str[:4]
    if len(the_str) < 4:
        for i in range(0,4-len(the_str)):
            the_str+=" "
        
    display.write_to_buffer("{}{}".format(box_state['left_digits'],
                                              the_str))
    display.display()
    
def write_left(the_str):
    # leaves right side blank
    if len(the_str) > 4:
        the_str = the_str[:4]
    if len(the_str) < 4:
        for i in range(0,4-len(the_str)):
            the_str+=" "
        
    box_state['left_digits'] = the_str
    display.write_to_buffer("{}    ".format(the_str))
    display.display()


###########################################################
###            Geiger Counter                       #######
###########################################################
# this will pulse high on Geiger click
click_detector = Pin(15, Pin.IN, Pin.PULL_DOWN)
click_ctr = ClickCounter()
def click_callback(p):
    # what to do when we get a click from the Geiger counter
    click_ctr.add_click()
    if box_state['mode'] == "counter":
        # display.write_to_buffer("{}{}".format(box_state['left_digits'],
        #                                       click_ctr.get_clicks_in_window()))
        write_right("{}".format(click_ctr.get_clicks_in_window()))
        display.display()
        
    if box_state['dice_thrown'] == True:
        # then we have detected a click and the dice has been cast
        # so we need to stop the loop and get the current value of the loop 
        # and display it
        print("in loop stop")
        box_state["dice_thrown"]= False
        dice_side_number = dice_sides[box_state['dice_side_idx']]
        
        write_right("{}".format((time.ticks_us()%dice_side_number)+1))
                                              
    
click_detector.irq(trigger=Pin.IRQ_RISING,handler=click_callback)


###########################################################
###             Big Button                          #######
###########################################################
# set up big button
big_button = Pin(21, Pin.IN, Pin.PULL_UP)

def big_button_callback(p):
    # the big button has been pressed
    # first handle the debounce
    big_button.irq(handler=None)
    ledseq.light_all()
    
    # wait for button to setlle
    big_button_count = 0
    while big_button_count < 2:
        time.sleep(0.1)
        # check if button pressed
        if big_button.value() == 0:
            big_button_count+=1
    
    # The big button has been pressed properly
    # now check that we are in dice mode
    if box_state['mode'] == "dice":
        # # if we are then we "throw the dice"
        box_state['dice_thrown'] = True
        write_right("8888")
        
    
    # now wait for the release of the button
    # wait for button to settle
    big_button_count = 0
    while big_button_count < 2:
        time.sleep(0.1)
        # check if button released
        if big_button.value() == 1:
            big_button_count+=1
    
    
    
    big_button.irq(trigger=Pin.IRQ_FALLING, handler=big_button_callback)


big_button.irq(trigger=Pin.IRQ_FALLING, handler=big_button_callback)




###########################################################
###               LED Array                         #######
###########################################################
# init the LED array
ledseq = led_array.led_sequence()
###########################################################
###             Rotary Switch                       #######
###########################################################
# init the rotary switch
rotary = RotaryIRQ(pin_num_clk=10, 
        pin_num_dt=12, 
        min_val=0, 
        max_val=len(dice_sides)-1, 
        reverse=True, 
        range_mode=RotaryIRQ.RANGE_WRAP)
rotary.set(value=box_state['dice_side_idx'])



# and its button
rotary_btn = Pin(16, Pin.IN, Pin.PULL_UP)

def rotary_button_callback(p):
    rotary_btn.irq(handler=None)
    if  box_state['mode'] == "counter":
        box_state['mode'] = "dice"
        write_left("d{}--".format(dice_sides[box_state['dice_side_idx']]))
        
    elif box_state['mode'] == "dice":
        box_state['mode'] = "counter"
        write_left("ctr ")
        write_right("{}".format(click_ctr.get_clicks_in_window()))
    # display.write_to_buffer("{}{}".format(box_state['left_digits'],
    #                                       right_digits))
    
    display.display()
    rotary_button_count = 0
    while rotary_button_count < 2:
        time.sleep(0.1)
        # check if button released
        if rotary_btn.value() == 1:
            rotary_button_count+=1
    rotary_btn.irq(trigger=Pin.IRQ_FALLING, handler=rotary_button_callback)
    
    
    
    
rotary_btn.irq(trigger=Pin.IRQ_FALLING, handler=rotary_button_callback)
                            
###########################################################

def rotary_listener():
                
    #val_old = rotary.value()
    if box_state['mode'] == 'dice':
        val_new = rotary.value()
        
        if box_state['dice_side_idx'] != val_new:
            box_state['dice_side_idx'] = val_new
            print('result =', val_new)
            dice_side_count = dice_sides[box_state['dice_side_idx']]
            
            write_left("d{}--".format(dice_side_count))
            
        time.sleep_ms(50)
        
rotary.add_listener(rotary_listener)






        

###########################################################
###########################################################