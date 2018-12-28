#import RPi.GPIO as GPIO
import pygame, sys, os
import time
import random
from pygame.locals import *
import moviepy
from moviepy.editor import *


#GPIO.cleanup()
print ('')
print ('')
running = True
Pics = False
Timelapse = False

BTN_Timelapse = 1
BTN_Pics = 2

BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)

w = 1920
h = 1200

screenRatio = w/h

colloms = 4
rows	= 4

picW = int(w/rows)
picH = int(h/colloms)

print("picH: "+str(picH)+" picW: "+str(picW))
pygame.display.init()
#pygame.movie.init()
screen = pygame.display.set_mode((w, h))#,pygame.NOFRAME)#,pygame.FULLSCREEN)
screen.fill((BLACK))

i = 0;

pygame.display.set_caption('Wunderkammer')
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

mylist = os.listdir('Bilder/')
cnt = len(mylist)
print (mylist)
print ('count: '+str(cnt))
PicUsed = cnt*[False]
PosUsed = 16*[False]

PicAtPos = [4*[""]for i in range(4)]
SizeOfPicAtPos = [4*[[0,0,0,0]]for i in range(4)]
	#xoffset ,yoffset, width, height
	

def text_to_screen(screen, text, x, y, size = 50,
            color = (000, 000, 000), font_type = 'data/fonts/orecrusherexpand.ttf'):
    try:
        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception:
        print ('Font Error, saw it coming')
        		
def bildAufbau():
	for x in range(4):
		for y in range (4):
			if PicAtPos[x][y] != "":
				img = pygame.image.fromstring(PicAtPos[x][y],(SizeOfPicAtPos[x][y][2], SizeOfPicAtPos[x][y][3]),"RGB")
				screen.blit(img,(480*x+SizeOfPicAtPos[x][y][0],270*y+SizeOfPicAtPos[x][y][1]))
			
def posNrToXY(pos):
	y=0
	x=pos
	if pos>3:
		y=1
		x=pos-4
	if pos>7:
		y=2
		x=pos-8
	if pos>11:
		y=3
		x=pos-12
	
	return [x,y]

def fadeInPic():
		
	while True:
		rand = random.randint(0,cnt-1)
		if PicUsed[rand]==False:
			break
	
	fadeOut = True
	for i in range(15):
		if PosUsed[i]==False:
			fadeOut = False
	
	while True:	
		pos = random.randint(0,15)
		if PosUsed[pos]==False or fadeOut:
			break
	
	x = posNrToXY(pos)[0]
	y = posNrToXY(pos)[1]
		
	if fadeOut:
		print('FadeOut')
		imageA = pygame.image.fromstring(PicAtPos[x][y],(SizeOfPicAtPos[x][y][2], SizeOfPicAtPos[x][y][3]),"RGB")
		PicAtPos[x][y] = ""
		for i in reversed(range (255)):
			screen.fill(BLACK)
			bildAufbau()
			imageA.set_alpha(i)
			screen.blit(imageA,(x*480+SizeOfPicAtPos[x][y][0],y*270+SizeOfPicAtPos[x][y][1]))
			pygame.display.flip()
			time.sleep(0.001)
		
	print('FadeIn')
	
	image = pygame.image.load('Bilder/'+mylist[rand]).convert()
	print('size: '+str(image.get_size()))
	
	xOffset = 0
	yOffset = 0
	
	if (image.get_width()/image.get_height())==(16/9):
		image = pygame.transform.scale(image, (480, 270))
		SizeOfPicAtPos[x][y] = [0,0,480,270]
		
	elif (image.get_width()/image.get_height())==(9/16):
		image = pygame.transform.scale(image, (152, 270))
		xOffset = 164
		SizeOfPicAtPos[x][y] = [xOffset,0,152,270]
		
	elif (image.get_width()/image.get_height())>(16/9):
		h = int(480/(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image, (480, h))
		yOffset = int((270-h)/2)
		SizeOfPicAtPos[x][y] = [0,yOffset,480,h]
		
	elif (image.get_width()/image.get_height())<(16/9):
		w = int(270*(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image,(w, 270))
		xOffset = int((480-w)/2)
		SizeOfPicAtPos[x][y] = [xOffset,0,w,270]
		
	else:
		image = pygame.transform.scale(image, (480, 270))
		SizeOfPicAtPos[x][y] = [0,0,480,270]		
		
	print ('rand: '+str(rand))
	print ('pos:  '+str(pos))
	
	PicUsed[rand] = True
	PosUsed[pos] = True
		
	print(mylist[rand])
	print("x"+str(x))
	print("y"+str(y))
	
	#pygame.display.flip()
	imageA = image
	i=0
	for i in range (255):
		#if	i % 10 == 0:
		#	print (i)
		screen.fill(BLACK)
		bildAufbau()
		imageA.set_alpha(i)
		screen.blit(imageA,(x*480+xOffset,y*270+yOffset))
		pygame.display.flip()
		
		time.sleep(0.001)
		 
	PicAtPos[x][y] = pygame.image.tostring(image,"RGB")
	pygame.display.flip()#pygame.display.update(Rect(x*480+xOffset, y*270+yOffset, 480, 270))

try:
	while running:
	
		
		
		while Timelapse:
			clip = VideoFileClip('TIMELAPSE VID.xxx')
			clip.preview()
		
		while Pics:
			print ('')
			print ('new')
			
			bildAufbau()
			pygame.display.flip()
			
			fadeInPic()
			pygame.display.flip()
			time.sleep(2)
		
		clip = VideoFileClip('fangstuhl_ORF.mp4')
		clip.preview()
		
		
except (KeyboardInterrupt, SystemExit):
	p1.stop()
	p2.stop()
	running = False
	#GPIO.cleanup()
	print('\nQuit\n')
	pygame.quit()