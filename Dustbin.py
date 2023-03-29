from machine import Pin, PWM, time_pulse_us,I2C
import ssd1306
import time

ir = Pin(16,Pin.IN)

servo_1 = PWM(Pin(20))
servo_1.freq(50)

i2c = I2C(0,sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

'''
servo_2 = PWM(Pin(21))
servo_2.freq(50)
'''
#GLOBAL VARIABLES
flag = 0
max_duty = 5000
min_duty = 1500
SOUND_SPEED=340 
TRIG_PULSE_DURATION_US=10

trig_pin = Pin(15, Pin.OUT) 
echo_pin = Pin(14, Pin.IN)

servo_1.duty_u16(min_duty)
#servo_2.duty_u16(min_duty)

while True:
 
    if ir.value() == False:
        print("Opening dustbin")
        display.text('Dustbin Open', 0, 15, 1)
        display.show()
        servo_1.duty_u16(max_duty)
        #servo_2.duty_u16(max_duty)
        time.sleep(5)
        print("Closing dustbin")
        servo_1.duty_u16(min_duty)
        #`servo_2.duty_u16(min_duty)
        
    trig_pin.value(0)
    time.sleep_us(5)
    
    trig_pin.value(1)
    time.sleep_us(TRIG_PULSE_DURATION_US)
    trig_pin.value(0)

    ultrason_duration = time_pulse_us(echo_pin, 1, 30000) 
    distance_cm = SOUND_SPEED * ultrason_duration / 20000
    
    display.text('Dustbin Closed', 0, 15, 1)
    display.show()
    
    print(f"Distance : {distance_cm} cm")
    if distance_cm < 10:
        print("Dustbin full")
        display.text('Dustbin Full', 0, 25, 1)
        display.show()
        time.sleep_ms(750)
    display.text(f"DISTANCE: {distance_cm}", 0, 40, 1)
    display.show()
    time.sleep_ms(750)
    display.fill(0) 
    
