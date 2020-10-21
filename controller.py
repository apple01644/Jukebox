import os, time

if os.name == 'posix':
    import RPi.GPIO as gpio
    from ctypes import CFUNCTYPE, c_char_p, c_int, cdll


class Controller:
    button_pins = [22, 33, 16, 18, ]
    big_button_pressed = False
    mp3_player = None

    def __init__(self, mp3_player):
        self.mp3_player = mp3_player
        if os.name == 'posix':
            error_handler_template = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

            def py_error_handler(filename, line, function, err, fmt):
                pass

            c_error_handler = error_handler_template(py_error_handler)
            self.lib_sound = cdll.LoadLibrary('libasound.so')
            self.lib_sound.snd_lib_error_set_handler(c_error_handler)

            gpio.setmode(gpio.BOARD)
            gpio.setwarnings(False)

            def on_click_prev(ch):
                mp3_player.prev_song()

            def on_click_next(ch):
                mp3_player.next_song()

            def on_click_big_button(ch):
                self.big_button_pressed = True

            gpio.setup(29, gpio.IN, pull_up_down=gpio.PUD_UP)

            for button_pin in self.button_pins:
                gpio.setup(button_pin, gpio.IN)

            gpio.add_event_detect(self.button_pins[0], gpio.FALLING, callback=on_click_prev, bouncetime=600)
            gpio.add_event_detect(self.button_pins[1], gpio.FALLING, callback=on_click_next, bouncetime=600)
            gpio.add_event_detect(29, gpio.FALLING, callback=on_click_big_button, bouncetime=10)

    def loop(self):
        if os.name == 'posix':
            if gpio.input(self.button_pins[2]) == gpio.HIGH:
                self.mp3_player.volume_down()
            if gpio.input(self.button_pins[3]) == gpio.HIGH:
                self.mp3_player.volume_up()
            if self.big_button_pressed:
                self.mp3_player.big_button()
                self.big_button_pressed = False
            time.sleep(0.01)
        else:
            res = input('1. Prev Song\n'
                        '2. Next Song\n'
                        '3. Random Song\n')
            if res == '1':
                self.mp3_player.prev_song()
            elif res == '2':
                self.mp3_player.next_song()
            elif res == '3':
                self.mp3_player.big_button()
