import pygame
import moviepy
from moviepy.editor import *

w = 1920
h = 1080
pygame.display.init()
screen = pygame.display.set_mode((w, h))
screen.fill((BLACK))

pygame.display.set_caption('Hello World!')

time.sleep(1)

clip = VideoFileClip('VID_20160918_175359.mp4')
clip.preview()

pygame.quit()