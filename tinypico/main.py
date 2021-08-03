from machine import SPI, Pin
import tinypico as TinyPICO
import machine

from dotstar import DotStar
import time, random, micropython, gc

import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
spi = SPI(
    sck=Pin(TinyPICO.DOTSTAR_CLK),
    mosi=Pin(TinyPICO.DOTSTAR_DATA),
    miso=Pin(TinyPICO.SPI_MISO),
)
# Create a DotStar instance
dotstar = DotStar(spi, 1, brightness=0.25)  # Just one DotStar, quarter brightness

# Say hello
print("--------------------\n")
machine.freq(80000000)
print("Machine freq: {}\n".format(machine.freq()))

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("woke from a deep sleep")

# Show some info on boot
print("Battery Voltage is {}V".format(TinyPICO.get_battery_voltage()))
print("Battery Charge State is {}\n".format(TinyPICO.get_battery_charging()))

## Show available memory
# print("Memory Info - micropython.mem_info()")
# print("------------------------------------")
# micropython.mem_info()

ble = bluetooth.BLE()
p = BLESimplePeripheral(ble, "tinypico")

light_on = False


def on_rx(v):
    global light_on
    print("RX", v)
    fail = False
    for statement in str(v, "utf-8").split(";"):
        args = statement.split(",")
        cmd = args.pop(0)
        if cmd == "on" and len(args) == 4:
            light_on = True
            TinyPICO.set_dotstar_power(True)
            r = int(args[0])
            g = int(args[1])
            b = int(args[2])
            a = float(args[3])
            dotstar[0] = (r, g, b, a)
        elif cmd == "off":
            light_on = False
            TinyPICO.set_dotstar_power(False)
        elif cmd == "bat":
            p.send("{}".format(TinyPICO.get_battery_voltage()))
        else:
            fail = True
    if not fail:
        p.send("ack")
    else:
        p.send("nack")


p.on_write(on_rx)


def on_interval(t):
    print("light_on: {}".format(light_on))
    if not light_on:
        print("light off... might as well sleep for a bit")
        machine.deepsleep(30000)


timer0 = machine.Timer(0)
timer0.init(period=30000, mode=machine.Timer.PERIODIC, callback=on_interval)
