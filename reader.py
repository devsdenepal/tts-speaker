
def s_print(text, speed=0.001):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
try:
    with open(sys.argv[1], 'r') as f:
        text = f.read()
s_print(text)