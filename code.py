import board
import neopixel
from adafruit_debouncer import Debouncer
from digitalio import DigitalInOut, Direction, Pull
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbowchase import RainbowChase

from adafruit_led_animation.color import RED, GREEN, BLUE, WHITE, BLACK, RAINBOW

# TODO: After some checking, the max current draw for the rainbow is 33mA at full
# brightness, and for white the max draw is 49mA. If we let the strip burn at full
# brightness, we could draw as much as 5.4A for rainbow stuff, and 8A for white.
# So we should cap the brightness at 90% globally, and 60% for pure white (not
# including white chase which only lights up some of the lights at once). This
# should keep the max current at 5A no matter what.

num_pixels = 162
pixels = neopixel.NeoPixel(board.GP28, num_pixels,
                           brightness=0.1, auto_write=True)

btn_pin = DigitalInOut(board.GP5)
btn_pin.direction = Direction.INPUT
btn_pin.pull = Pull.UP
button = Debouncer(btn_pin)

counter = 0

# This will advance the color from one pixel to the next
solid_white = Solid(pixels, WHITE, )
solid_red = Solid(pixels, RED)
solid_green = Solid(pixels, GREEN)
solid_blue = Solid(pixels, BLUE)
rainbow = Rainbow(pixels, speed=0, period=10)
chase_white = Chase(pixels, 0.75, color=WHITE, size=2, spacing=2)
chase_rainbow = RainbowChase(pixels, 0.75, size=2, spacing=2)
off = Solid(pixels, BLACK)

# TODO: the RAINBOW color is only six colors. See if we can construct something more fluid
color_cycle_rainbow = ColorCycle(pixels, 0.5, RAINBOW)

animations = [
  solid_white, solid_red, solid_green, solid_blue,
  rainbow,
  chase_white, chase_rainbow,
  color_cycle_rainbow,
  off
]

changed = True

while True:
  if changed:
    print(f'Displaying index {counter} with brightness {pixels.brightness}...')
    changed = False
  button.update()
  if button.rose:
    counter = (counter + 1) % len(animations)
    changed = True
    if counter == 0:
      # All White
      pixels.brightness = 0.1
    elif counter == 8:
      # Off
      pixels.brightness = 0
    else:
      # Normal
      pixels.brightness = 0.25

  animations[counter].animate()
