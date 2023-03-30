import network
import machine
import socket
from secrets import secrets
import rp2
import ubinascii

from machine import Pin, PWM, time_pulse_us,I2C,ADC
import time
import ssd1306
    

ir = Pin(16,Pin.IN)
led1 = Pin(8,Pin.OUT)

servo_1 = PWM(Pin(20))
servo_1.freq(50)
'''
servo_2 = PWM(Pin(21))
servo_2.freq(50)
'''

i2c = I2C(0,sda=Pin(4), scl=Pin(5))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

trig_pin = Pin(15, Pin.OUT) 
echo_pin = Pin(14, Pin.IN)

voltage_sensor = ADC(Pin(26,Pin.IN))

#GLOBAL VARIABLES
flag = 0
max_duty = 5000
min_duty = 1500
SOUND_SPEED=340 
TRIG_PULSE_DURATION_US=10
ref_voltage = 5.0
R1 = 30000.0
R2 = 7500.0

servo_1.duty_u16(min_duty)
#servo_2.duty_u16(min_duty)

###### Connect wifi ######
## Create a secrets.py file and create a secrets object with the ssid and pw of your network"
ssid = secrets['ssid']
pw   = secrets['pw'] 

rp2.country('IN')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)
wlan.connect(ssid, pw)

# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)

# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)
print('Listening on', addr) 

# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

countofconn = 0
while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        cl_file = conn.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        response = get_html('index.html')
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
        ir_read = ir.value()
        if ir_read == False:
            response = response.replace('Lid Closed', 'Lid Open')

            
                
        trig_pin.value(0)
        time.sleep_us(5)
        
        trig_pin.value(1)
        time.sleep_us(TRIG_PULSE_DURATION_US)
        trig_pin.value(0)

        ultrason_duration = time_pulse_us(echo_pin, 1, 30000) 
        distance_cm = round(SOUND_SPEED * ultrason_duration / 20000)

        display.text('Dustbin Closed', 0, 15, 1)
        #display.show()
        
        print(f"Free space : {distance_cm} cm")
        if distance_cm < 10:
            print("Dustbin full")
            display.text('Dustbin Full', 0, 25, 1)
            #display.show()
            response = response.replace('Not full', 'Full')
            led1.value(1)
        display.text(f"Free space: {distance_cm}", 0, 40, 1)
        #display.show()
        
        led1.value(0)
            #Send message to number

        
        response = response.replace('LevelReading', str(distance_cm))
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)

        #Battery code
        ## Read the Analog Input
        adc_value = voltage_sensor.read_u16()

        ##Determine voltage at ADC input
        adc_voltage  = (adc_value * ref_voltage) / 1024.0 

        ##Calculate voltage at divider input
        in_voltage = (adc_voltage / (R2/(R1+R2)))/100
        display.text(f"VOLTAGE: %.2f V" %in_voltage, 0, 0, 1)
        #display.show()
        time.sleep_ms(750)
        if ir_read == False:
            print("Opening dustbin")
            servo_1.duty_u16(max_duty)
            display.text('Dustbin Open', 0, 15, 1)
            display.show()
            #servo_2.duty_u16(max_duty)
            time.sleep(5)
            print("Closing dustbin")
            servo_1.duty_u16(min_duty)
            #`servo_2.duty_u16(min_duty)
        display.show()
        display.fill(0)    
        conn.close()
        countofconn += 1
        print(f'Connection:{countofconn}')
    except OSError as e:
        conn.close()
        s.close()
        print('Connection closed')    
    




