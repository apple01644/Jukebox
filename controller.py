import os, time
from ctypes import CFUNCTYPE, c_char_p, c_int, cdll

if os.name == 'posix':
    import RPi.GPIO as gpio


    class Controller:
        button_pins = [22, 33, 16, 18, ]

        def __init__(self, mp3_player):
            error_handler_template = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

            def py_error_handler(filename, line, function, err, fmt):
                pass

            c_error_handler = error_handler_template(py_error_handler)
            self.lib_sound = cdll.LoadLibrary('libasound.so')
            self.lib_sound.snd_lib_error_set_handler(c_error_handler)
            self.mp3_player = mp3_player

            gpio.setmode(gpio.BOARD)
            gpio.setwarnings(False)

            def on_click_prev(ch):
                mp3_player.prev_song()

            def on_click_next(ch):
                mp3_player.next_song()

            def on_click_big_button(ch):
                mp3_player.big_button()

            for button_pin in self.button_pins:
                gpio.setup(button_pin, gpio.IN)
            gpio.add_event_detect(self.button_pins[0], gpio.FALLING, callback=on_click_prev, bouncetime=600)
            gpio.add_event_detect(self.button_pins[1], gpio.FALLING, callback=on_click_next, bouncetime=600)
            #gpio.add_event_detect(self.button_pins[4], gpio.FALLING, callback=on_click_big_button, bouncetime=600)

        def loop(self):
            if gpio.input(self.button_pins[2]) == gpio.HIGH:
                self.mp3_player.volume_down()
            if gpio.input(self.button_pins[3]) == gpio.HIGH:
                self.mp3_player.volume_up()
            time.sleep(0.01)


else:
    class Controller:
        pass
        # May use only RaspberryPi
