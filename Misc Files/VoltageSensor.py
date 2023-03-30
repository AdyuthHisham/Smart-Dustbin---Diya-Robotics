from machine import Pin, I2C,ADC
from time import sleep

voltage_sensor = ADC(Pin(26,Pin.IN))
R1 = 30000.0;
R2 = 7500.0;
ref_voltage = 5.05

#Battery code
## Read the Analog Input
while True:
    adc_value = voltage_sensor.read_u16()

    ##Determine voltage at ADC input
    adc_voltage  = (adc_value * ref_voltage) / 1024.0 

    ##Calculate voltage at divider input
    in_voltage = (adc_voltage / (R2/(R1+R2)))/100
    print(f"VOLTAGE: {in_voltage}")
    sleep(1)
