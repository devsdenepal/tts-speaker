import sys
import pyttsx3
import time
import threading

def s_print(text, speed=0.092, stop_event=None):
    for char in text:
        if stop_event and stop_event.is_set():
            break
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)

def on_start(name):
    print('Speaking:', name)

def on_end(name, completed):
    if completed:
        print('Finished speaking:', name)
    else:
        print('Speech interrupted:', name)

def play_audio(text, speed=130, stop_event=None):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed) # Adjust this value to change the TTS speed
    engine.connect('started-utterance', lambda name: on_start(text[:engine._last_start_index]))
    engine.connect('finished-utterance', on_end)
    engine.say(text)
    try:
        engine.runAndWait()
    except KeyboardInterrupt:
        engine.stop()
    finally:
        if stop_event:
            stop_event.set()

if len(sys.argv) != 2:
    print("Usage: python text_to_speech.py <path/to/text/file>")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f:
        text = f.read()
except FileNotFoundError:
    print("Error: File not found")
    sys.exit(1)

stop_event = threading.Event()
t1 = threading.Thread(target=s_print, args=(text, 0.092, stop_event))
t2 = threading.Thread(target=play_audio, args=(text, 130, stop_event))

t2.start()
time.sleep(1) # add delay to allow TTS to start before printing text
t1.start()

try:
    while t2.is_alive() or t1.is_alive():
        time.sleep(0.1)
except KeyboardInterrupt:
    stop_event.set()

t2.join()
t1.join()
