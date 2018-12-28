import RPi.GPIO as GPIO
import pygame, sys, os
import subprocess
import pyglet
import time, random
from moviepy.editor import *

#init GPIO
GPIO.cleanup()
BTN_Pics = 17
BTN_Timelapse = 18
#27
#22
#23

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_Pics, GPIO.IN)
GPIO.setup(BTN_Timelapse, GPIO.IN)

def InterruptPics(x):
	print("InterruptBilder")
	#Pics = True
	Pics()
	
def InterruptTimelapse(x):
	print("InterruptZeitraffer")
	Timelapse = True

GPIO.add_event_detect(BTN_Pics, GPIO.RISING, callback = InterruptPics, bouncetime = 200)
GPIO.add_event_detect(BTN_Timelapse, GPIO.RISING, callback = InterruptTimelapse, bouncetime = 200)



print ('')
print ('')
running = True
Pics = False
Timelapse = False

fadeDelay = 0.001
Delay = 2

BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)

pygame.display.init()
infoObject = pygame.display.Info()

w = 16*40#infoObject.current_w #1920
h = 9*40#infoObject.current_h #1200

print("w: "+str(w)+" h: "+str(h))

screenRatio = w/h

colloms = 4
rows	= 4

picW = int(w/rows)
picH = int(h/colloms)

print("picH: "+str(picH)+" picW: "+str(picW))
pygame.display.init()
screen = pygame.display.set_mode((w, h))#,pygame.FULLSCREEN)
screen.fill((BLACK))

i = 0;

pygame.display.set_caption('Wunderkammer')
pygame.font.init()
pygame.mouse.set_visible(False)

myfont = pygame.font.SysFont('Comic Sans MS', 30)

mylist = os.listdir('Bilder/')
cnt = len(mylist)
print (mylist)
print ('count: '+str(cnt))
PicUsed = cnt*[False]
PosUsed = 16*[False]

PicAtPos = [4*[""]for i in range(4)]
SizeOfPicAtPos = [4*[[0,0,0,0]]for i in range(4)]


#def text_to_screen(screen, text, x, y, size = 50,
#           color = (000, 000, 000), font_type = 'data/fonts/orecrusherexpand.ttf'):
#    try:
#        text = str(text)
#        font = pygame.font.Font(font_type, size)
#        text = font.render(text, True, color)
#        screen.blit(text, (x, y))
#
#    except Exception:
#        print ('Font Error, saw it coming')
        		
def bildAufbau():
	for x in range(4):
		for y in range (4):
			if PicAtPos[x][y] != "":
				img = pygame.image.fromstring(PicAtPos[x][y],(SizeOfPicAtPos[x][y][2], SizeOfPicAtPos[x][y][3]),"RGB")
				screen.blit(img,(picW*x+SizeOfPicAtPos[x][y][0],picH*y+SizeOfPicAtPos[x][y][1]))
			
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
			screen.blit(imageA,(x*picW+SizeOfPicAtPos[x][y][0],y*picH+SizeOfPicAtPos[x][y][1]))
			pygame.display.flip()
			time.sleep(fadeDelay)
		
	print('FadeIn')
	
	image = pygame.image.load('Bilder/'+mylist[rand]).convert()
	print('size: '+str(image.get_size()))
	
	xOffset = 0
	yOffset = 0
	
	if (image.get_width()/image.get_height())==screenRatio:
		image = pygame.transform.scale(image, (picW, picH))
		SizeOfPicAtPos[x][y] = [0,0,picW,picH]
		
	elif (image.get_width()/image.get_height())>screenRatio:
		h = int(picW/(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image, (picW, h))
		yOffset = int((picH-h)/2)
		SizeOfPicAtPos[x][y] = [0,yOffset,picW,h]
		
	elif (image.get_width()/image.get_height())<screenRatio:
		w = int(picH*(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image,(w, picH))
		xOffset = int((picW-w)/2)
		SizeOfPicAtPos[x][y] = [xOffset,0,w,picH]
		
	else:
		image = pygame.transform.scale(image, (picW, picH))
		SizeOfPicAtPos[x][y] = [0,0,picW,picH]		
		
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
		screen.blit(imageA,(x*picW+xOffset,y*picH+yOffset))
		pygame.display.flip()
		
		time.sleep(fadeDelay)
		 
	PicAtPos[x][y] = pygame.image.tostring(image,"RGB")
	pygame.display.flip()#pygame.display.update(Rect(x*480+xOffset, y*270+yOffset, 480, 270))

def	Pics():
	for i in range(48):
		print ("ImageNr: "+str(i))
		pygame.mouse.set_visible(False)
		
		bildAufbau()
		pygame.display.flip()
		
		fadeInPic()
		pygame.display.flip()
		time.sleep(Delay)
		
		Pics = False
	
try:
	while running:
	
		#print (GPIO.input(BTN_Pics))
 
		if Timelapse:
			clip = VideoFileClip('ZeitrafferFilm.mp4')
			clip.preview()
		
		#if Pics:
			#p = subprocess.Popen(Pics())
			
			#print ('')
			#print ('new')
					
			#bildAufbau()
			#pygame.display.flip()
			
			#fadeInPic()
			#pygame.display.flip()
			#time.sleep(2)
			
		clip = VideoFileClip('StartWunderbox.mp4')
		clip.preview()
		
		
except (KeyboardInterrupt, SystemExit):
	running = False
	GPIO.cleanup()
	print('\nQuit\n')
	pygame.quit()