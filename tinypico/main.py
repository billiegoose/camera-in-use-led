from machine import SPI, Pin
import tinypico as TinyPICO

from dotstar import DotStar
import time, random, micropython, gc

import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness = 0.25 ) # Just one DotStar, quarter brightness
# Turn on the power to the DotStar
TinyPICO.set_dotstar_power( True )

# Say hello
print("\nHello from TinyPICO!")
print("--------------------\n")

# Show some info on boot 
print("Battery Voltage is {}V".format( TinyPICO.get_battery_voltage() ) )
print("Battery Charge State is {}\n".format( TinyPICO.get_battery_charging() ) )

# Show available memory
print("Memory Info - micropython.mem_info()")
print("------------------------------------")
micropython.mem_info()

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, "tinypico")

def on_rx(v):
    for statement in str(v, 'utf-8').split(';'):
        args = statement.split(',')
        cmd = args.pop(0)
        if (cmd == 'on' and len(args) == 4):
            TinyPICO.set_dotstar_power( True )
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            a = float(args[3])
            dotstar[0] = ( r, g, b, a )
            p.send('ack')
        elif (cmd == 'off'):
            TinyPICO.set_dotstar_power( False )
            p.send('ack')
        else:
            p.send('nack')
        print("RX", v)

p.on_write(on_rx)
