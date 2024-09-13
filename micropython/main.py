import network
import urequests
from time import sleep
import random
import gc

def connect():
    ssid = "SchmaleFi"
    password = "slowshrub108"

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print(wlan.ifconfig())

def free_mem():
    gc.collect()
    print(gc.mem_free())

def list_free_disk():
    import os
    x = os.statvfs('/')
    free_mem = x[0] * x[3]
    used_mem = x[0] * (x[2] - x[3])
    print(free_mem, used_mem)

connect()
list_free_disk()
free_mem()

# while True:
#     i = str(random.randint(0, 1000))

#     free_mem()
#     res = urequests.get(f"https://www.henryschmale.org/tag/?value=secret&id=" + i)
#     print(res.status_code)
    