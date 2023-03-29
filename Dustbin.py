from machine import Pin, PWM, time_pulse_us
import time

ir = Pin(16,Pin.IN)
led1 = Pin(8,Pin.OUT)

servo_1 = PWM(Pin(20))
servo_1.freq(50)
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
    '''
    if ir.value() == False:
        flag = not flag
        if flag == 0:
            print("Closing dustbin")
            #set duty cycle of servo to min value
            servo_1.duty_u16(min_duty)
            servo_2.duty_u16(min_duty)
        else:
            print("Opening dustbin")
            #set duty cycle of servo to max value
            servo_1.duty_u16(max_duty)
            servo_2.duty_u16(max_duty)
        time.sleep_ms(750)
    '''
    if ir.value() == False:
        print("Opening dustbin")
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

    print(f"Distance : {distance_cm} cm")
    if distance_cm < 10:
        print("Dustbin full")
        led1.value(1)
        time.sleep_ms(750)
    
    led1.value(0)
        #Send message to number
    time.sleep_ms(750)
    
