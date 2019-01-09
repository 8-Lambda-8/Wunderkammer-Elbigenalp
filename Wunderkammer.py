import RPi.GPIO as GPIO
import pygame, sys, os
import vlc, random
import time

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
	if(not playerTimelapse.is_playing()and not picsRunning):
		print("startingPics")
		playerStartWunderBox.stop()
		globals().update(picsRunning = True)
		Pics()
		StartWunderbox()
	
def InterruptTimelapse(x):
	print("InterruptZeitraffer")
	if(not playerTimelapse.is_playing()and not picsRunning):
		print("startingTimelapse")
		playerTimelapse.set_xwindow(win_id)
		playerStartWunderBox.stop()
		playerTimelapse.set_media(media_Timelapse)
		playerTimelapse.play()

GPIO.add_event_detect(BTN_Pics, GPIO.RISING, callback = InterruptPics, bouncetime = 20000)
GPIO.add_event_detect(BTN_Timelapse, GPIO.RISING, callback = InterruptTimelapse, bouncetime = 20000)

print ('')
print ('')
running = True
picsRunning = False
DEBUG = False

fadeDelay = 0.000005
Delay = 0.01

if DEBUG:
	fadeDelay = 0.00001
	Delay = 0.01

print("fadeDelay "+str(fadeDelay))
print("Delay "+str(Delay))
	
BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)

pygame.display.init()
infoObject = pygame.display.Info()

w = infoObject.current_w
h = infoObject.current_h
if DEBUG:
	w=16*40
	h=10*40

print("w: "+str(w)+" h: "+str(h))

screenRatio = w/h

colloms = 3
rows	= 3

numberPicsShown = 36

picW = int(w/rows)
picH = int(h/colloms)

print("picH: "+str(picH)+" picW: "+str(picW))

if DEBUG:
	screen = pygame.display.set_mode((w, h))
else:
	screen = pygame.display.set_mode((w, h),pygame.FULLSCREEN)
screen.fill(BLACK)

i = 0;

pygame.display.set_caption('Wunderkammer')

pygame.mouse.set_pos(w, h)
pygame.mouse.set_visible(False)

vlcInstanceTimelapse = vlc.Instance('--mouse-hide-timeout=0')
vlcInstanceWunderBox = vlc.Instance('--input-repeat=9999999', '--mouse-hide-timeout=0')
playerStartWunderBox = vlcInstanceWunderBox.media_player_new()
playerTimelapse = vlcInstanceTimelapse.media_player_new()

TL_window = playerTimelapse.get_xwindow()

win_id = pygame.display.get_wm_info()['window']
playerStartWunderBox.set_xwindow(win_id)
playerTimelapse.set_xwindow(win_id)

pygame.mixer.quit()

media_WunderBox = vlcInstanceWunderBox.media_new("StartWunderbox.mp4")
media_Timelapse = vlcInstanceTimelapse.media_new("Zeitraffer.mp4")
#if DEBUG:
	#media_WunderBox = vlcInstanceWunderBox.media_new("test.mp4")
	#media_Timelapse = vlcInstanceTimelapse.media_new("test2.mp4")
	
playerStartWunderBox.set_media(media_WunderBox)
playerTimelapse.set_media(media_Timelapse)

print(str(media_WunderBox.get_mrl()))

mylist = os.listdir('Bilder/')
cnt = len(mylist)
print (mylist)
print ('count: '+str(cnt))
PicUsed = cnt*[False]
PosUsed = 16*[False]

PicAtPos = [4*[""]for i in range(4)]
SizeOfPicAtPos = [4*[[0,0,0,0]]for i in range(4)]


        		
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

	xOffset = 0
	yOffset = 0
	
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
	#print('size: '+str(image.get_size()))
	
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
	#print("x"+str(x))
	#print("y"+str(y))
	
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
	screen.fill(BLACK)
	globals().update(mylist = os.listdir('Bilder/'))
	globals().update(cnt = len(mylist))
	globals().update(PicUsed = cnt*[False])
	globals().update(PosUsed = 16*[False])
	globals().update(PicAtPos = [4*[""]for i in range(4)])
	globals().update(SizeOfPicAtPos = [4*[[0,0,0,0]]for i in range(4)])
	
	pygame.display.quit()
	if DEBUG:
		globals().update(screen = pygame.display.set_mode((w, h)))
	else:
		globals().update(screen = pygame.display.set_mode((w, h),pygame.FULLSCREEN))
	
	pygame.mouse.set_pos(w, h)
	pygame.mouse.set_visible(False)
	
	pygame.display.update()
	
	numberPicsShown_ = numberPicsShown
	if cnt<numberPicsShown_:
		numberPicsShown_ = cnt
		
	pygame.mixer.init()
	pygame.mixer.music.load("127_full_free-to-dream_0127.wav")
	pygame.mixer.music.play(loops=-1, start=0.0)
	for i in range(numberPicsShown_-1):
		print ("")
		print ("ImageNr: "+str(i))
				
		bildAufbau()
		pygame.display.flip()
		
		fadeInPic()
		pygame.display.flip()
		time.sleep(Delay)
	time.sleep(1)
	pygame.mixer.music.stop()
	globals().update(picsRunning = False)
	
	
def StartWunderbox():
	screen.fill(BLACK)
	pygame.display.flip()
	#playerTimelapse.stop()#pause()
	playerStartWunderBox.set_media(media_WunderBox)
	playerStartWunderBox.play()
	

def EndReached(event):
	print("EndReached")
	pygame.display.flip()
	#StartWunderbox()
	playerTimelapse.set_xwindow(0)
	playerTimelapse.pause()
	#playerTimelapse.release()
	screen.fill(BLACK)
	pygame.display.flip()
	playerStartWunderBox.set_media(media_WunderBox)
	playerStartWunderBox.play()

events = playerTimelapse.event_manager()
events.event_attach(vlc.EventType.MediaPlayerEndReached, EndReached)

  	
try:

	StartWunderbox()
	while running:
		bla = 0
		
				
except (KeyboardInterrupt, SystemExit):
	globals().update(running = False)
	picsRunning = False
	GPIO.cleanup()
	print('\nQuit\n')
	pygame.quit()