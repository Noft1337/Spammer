import Xlib.error
from pynput.keyboard import Controller, Key
from pynput import mouse
import multiprocessing
import time


PROCESSES = []
# Waiting time before the program starts (in seconds)
WAIT = 5
# Waiting time between strokes (in seconds)
DELAY = 0.01


def exit_program(code=0):
    print("Exiting program...")
    for process in PROCESSES:
        process.terminate()
    exit(code)


def pause(*args):
    print("Mouse Clicked")
    raise KeyboardInterrupt


def press_and_release(keyboard: Controller, key):
    keyboard.press(key)
    keyboard.release(key)


def spam_sequence():
    time.sleep(WAIT)
    counter = 0
    while True:
        counter += 1
        print(f"#{counter}")
        time.sleep(DELAY)
        keyboard = Controller()
        paste(keyboard)


def paste(keyboard: Controller):
    keyboard.press(Key.ctrl_l)
    press_and_release(keyboard, 'v')
    keyboard.release(Key.ctrl_l)
    press_and_release(keyboard, Key.enter)


def listen_for_mouse():
    time.sleep(WAIT)
    try:
        with mouse.Listener(on_click=pause) as listener:
            listener.join()
    except Xlib.error.ConnectionClosedError:
        raise KeyboardInterrupt


def main():
    spammer_p = multiprocessing.Process(target=spam_sequence)

    try:
        spammer_p.start()
        PROCESSES.append(spammer_p)
        listen_for_mouse()
    except KeyboardInterrupt:
        exit_program()


if __name__ == '__main__':
    main()
