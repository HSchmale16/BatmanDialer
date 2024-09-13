import board
import time
from digitalio import DigitalInOut, Direction, Pull

need_to_print = 0
count = 0
inpin = DigitalInOut(board.GP15)

last_state = False
true_state = False
last_state_change_time = 0
cleared = 0

# Dial Rotate Has Finished
# 100 milliseconds
DIAL_ROTATE_FINISH_NS = 100 * 1000 * 1000
# 10 milliseconds
DEBOUNCE_DELAY = 1 * 1000 * 1000

inpin.direction = Direction.INPUT


while True:
    reading = inpin.value
    # print(reading)

    delta_t = time.monotonic_ns() - last_state_change_time
    if delta_t > DIAL_ROTATE_FINISH_NS and need_to_print:
        print("Dial Rotate Finished ", count)
        need_to_print = 0
        cleared = 0
        count = 0
    
    if reading != last_state:
        last_state_change_time = time.monotonic_ns()

    delta_t = time.monotonic_ns() - last_state_change_time
    if delta_t > DEBOUNCE_DELAY:
        if reading != true_state:
            true_state = reading
            if true_state:
                count += 1
                need_to_print = 1
                print("Count: ", count)
            else:
                print("Count: ", count)
    last_state = reading


