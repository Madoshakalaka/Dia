import os
import sys
import time
import unittest
import pyglet

with open(os.devnull, 'w') as f:
    # disable stdout
    oldstdout = sys.stdout
    sys.stdout = f

    import pygame

    # enable stdout
    sys.stdout = oldstdout

class MyTestCase(unittest.TestCase):
	def test_soundplay(self):
		pygame.mixer.init()
		pygame.mixer.music.load(os.path.join('..', 'assets', 'click.wav'))


		pygame.mixer.music.play(0)

		time.sleep(1)
		pygame.mixer.music.play(0)

		pygame.mixer.music.stop()
if __name__ == '__main__':
	unittest.main()
