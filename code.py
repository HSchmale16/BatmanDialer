import audiobusio
# import audiocore
import wifi
import socketpool
import ssl
import synthio
# import adafruit_requests
import board
import countio
import time
import gc



def nearestTo4(x):
    rem = x % 4
    if rem < 2:
        return x - rem
    else:
        return x + 4 - rem


# Count rising edges only.
pin_counter = countio.Counter(board.GP15, edge=countio.Edge.FALL)
# Reset the count after 100 counts.
last_value = 0
time_last_number_added = time.monotonic_ns()
MAX_TIME_BETWEEN_DIGITS = int(1e9 * 4)
LAST_INCREMENT_THRESHOLD = int(1e9 * 0.25)
last_increment = 0

dialed = []

def reset_dialer_numbers():
    global last_value, time_last_number_added, last_increment
    last_value = 0
    time_last_number_added = time.monotonic_ns()
    last_increment = time.monotonic_ns()
    dialed.clear()

def dialer_check():
    global last_value, time_last_number_added, last_increment
    count = pin_counter.count

    # It has been incremented
    if count != last_value:
        print("Count incr", count)
        last_increment = time.monotonic_ns()
        last_value = count
    
    # We will wait for up to half a second to see if the count is stable
    delta_t = time.monotonic_ns() - last_increment
    if delta_t > LAST_INCREMENT_THRESHOLD and count != 0:
        print("Count: ", count, delta_t / 1e9)
        pin_counter.reset()

        excess = count % 4
        actual_number = count // 4

        print("Conforming ", actual_number, " Excess: ", excess)

        return actual_number
    return None




# Setup Wifi
# wifi.radio.connect(,)
# pool = socketpool.SocketPool(wifi.radio)
# requests = adafruit_requests.Session(pool, ssl.create_default_context())


audio = audiobusio.I2SOut(board.GP0, board.GP1, board.GP2)

amp_env_fast = synthio.Envelope(
    attack_time=0.1,
    sustain_level=0.5,
    release_time=0.2
)

synth = synthio.Synthesizer(channel_count=1, sample_rate=22050, envelope=amp_env_fast)
audio.play(synth)

print("Starting the Secret Batman Dialer")
print("Hold on to your pants as you guess the codes that make it do things")

playing_note = 0
note_held_for = 0
last_result_at = time.monotonic_ns()
buffer = ""

while True:
    if playing_note > 0:
        note_held_for += 1
        if note_held_for > 10:
            synth.release(playing_note)
            playing_note = 0
            note_held_for = 0
    
    result = dialer_check()
    if result is not None:
        print("Result: ", result, "MemFree: ", gc.mem_free())
        if playing_note > 0:
            synth.stop(playing_note)
            playing_note = 0
            note_held_for = 0
        
        playing_note = result + 60
        synth.press(playing_note)
        

    time.sleep(0.1)

    





