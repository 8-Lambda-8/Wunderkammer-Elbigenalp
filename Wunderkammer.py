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

if len(sys.argv)>1:
        if sys.argv[1]=="--DEBUG":
                DEBUG = True

fadeDelay = 0.005
Delay = 2

if DEBUG:
	fadeDelay = 0.005
	Delay = 2

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

border = 4

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
PosUsed = gridPlaces*[False]


numberPicsShown_ = numberPicsShown
if cnt<numberPicsShown_:
	numberPicsShown_ = cnt
ImageOrder_List = numberPicsShown_*[0]
PosOrder_List = numberPicsShown_*[0]

def reRandomizeOrderLists():
	numberPicsShown_ = numberPicsShown
	if cnt<numberPicsShown_:
		numberPicsShown_ = cnt

	PosOrder_List_ = numberPicsShown_*[0]
	ii=0
	print("nrPicsShown:"+str(numberPicsShown_))
	print("loop: "+str(numberPicsShown_/(gridPlaces)))
	print("loopR:"+str(int(numberPicsShown_/(gridPlaces)))+" "+str(range(int(numberPicsShown_/(gridPlaces)))))
	for ii in range(int(numberPicsShown_/(gridPlaces))+1):
		randOrder = random.sample(range(gridPlaces), gridPlaces)
		print("xxx: "+str(randOrder))
		x = 0
		if ii>=int(numberPicsShown_/(gridPlaces)):
			print("x")
			x = gridPlaces-(numberPicsShown_-gridPlaces*ii)
		print("xxx: "+str(x)+" "+str(gridPlaces-x))
		for i in range(gridPlaces-x):
			print(str((gridPlaces)*ii+i)+"  "+str(ii)+"  "+str(i)+" :  "+str(randOrder[i]))
			PosOrder_List_[(gridPlaces)*ii+i] = randOrder[i]
		
	globals().update(PosOrder_List = PosOrder_List_)
	globals().update(ImageOrder_List = random.sample(range(len(mylist)), numberPicsShown_))
	print ("PosOrder_List: "+str(PosOrder_List)+str(len(PosOrder_List)))
	print ("ImageOrder_List: "+str(ImageOrder_List)+str(len(ImageOrder_List)))

PicAtPos = [rows*[""]for i in range(columns)]
SizeOfPicAtPos = [rows*[[0,0,0,0]]for i in range(columns)]

        		
def bildAufbau():
	for x in range(columns):
		for y in range (rows):
			if PicAtPos[x][y] != "":
				img = pygame.image.fromstring(PicAtPos[x][y],(SizeOfPicAtPos[x][y][2], SizeOfPicAtPos[x][y][3]),"RGB")
				screen.blit(img,(picW*x+SizeOfPicAtPos[x][y][0],picH*y+SizeOfPicAtPos[x][y][1]))
			
def posNrToXY(pos):
	y=int(pos/columns)
	x=pos-int(columns*y)	
	return [x,y]

def fadeInPic(nr):

	print(mylist[ImageOrder_List[nr]])

	#print ('ImageOrder: '+str(ImageOrder_List[nr]))
	print ('PosOrder:  '+str(PosOrder_List[nr]))

	x = posNrToXY(PosOrder_List[nr])[0]
	y = posNrToXY(PosOrder_List[nr])[1]

	print("x"+str(x))
	print("y"+str(y))
	
	xOffset = 0
	yOffset = 0


	if nr<gridPlaces:
		fadeOut = False
	else:
		fadeOut = True
		
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
	
	image = pygame.image.load('Bilder/'+mylist[ImageOrder_List[nr]]).convert()
	#print('size: '+str(image.get_size()))
	
	if (image.get_width()/image.get_height())==screenRatio:
		image = pygame.transform.scale(image, (picW-border*2, picH-border*2))
		SizeOfPicAtPos[x][y] = [0+border,0+border,picW-border*2,picH-border*2]
		
	elif (image.get_width()/image.get_height())>screenRatio:
		h = int((picW-border*2)/(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image, (picW-border*2, h))
		yOffset = int((picH-h)/2)
		SizeOfPicAtPos[x][y] = [0+border,yOffset,picW-border*2,h]
		
	elif (image.get_width()/image.get_height())<screenRatio:
		w = int((picH-border*2)*(image.get_width()/image.get_height()))
		image = pygame.transform.scale(image,(w, picH-border*2))
		xOffset = int((picW-w)/2)
		SizeOfPicAtPos[x][y] = [xOffset,0+border,w,picH-border*2]
		
	else:
		image = pygame.transform.scale(image, (picW-border*2, picH-border*2))
		SizeOfPicAtPos[x][y] = [0+border,0+border,picW-border*2,picH-border*2]		
			
	#pygame.display.flip()
	imageA = image
	i=0
	for i in range (255):
		#if	i % 10 == 0:
		#	print (i)
		screen.fill(BLACK)
		bildAufbau()
		imageA.set_alpha(i)
		#screen.blit(imageA,(x*picW+xOffset,y*picH+yOffset))
		screen.blit(imageA,(picW*x+SizeOfPicAtPos[x][y][0],picH*y+SizeOfPicAtPos[x][y][1]))
		pygame.display.flip()
		
		time.sleep(fadeDelay)
		
		 
	PicAtPos[x][y] = pygame.image.tostring(image,"RGB")
	pygame.display.flip()#pygame.display.update(Rect(x*480+xOffset, y*270+yOffset, 480, 270))

def	Pics():
	screen.fill(BLACK)
	globals().update(mylist = os.listdir('Bilder/'))
	globals().update(cnt = len(mylist))
	globals().update(PicUsed = cnt*[False])
	globals().update(PosUsed = gridPlaces*[False])
	globals().update(PicAtPos = [rows*[""]for i in range(columns)])
	globals().update(SizeOfPicAtPos = [rows*[[0,0,0,0]]for i in range(columns)])

	numberPicsShown_ = numberPicsShown
	if cnt<numberPicsShown_:
		numberPicsShown_ = cnt

	reRandomizeOrderLists()
	
	pygame.display.quit()
	if DEBUG:
		globals().update(screen = pygame.display.set_mode((w, h)))
	else:
		globals().update(screen = pygame.display.set_mode((w, h),pygame.FULLSCREEN))
	
	pygame.mouse.set_pos(w, h)
	pygame.mouse.set_visible(False)
	
	pygame.display.update()
		
	pygame.mixer.init()
	#pygame.mixer.music.load("127_full_free-to-dream_0127.wav")
	#pygame.mixer.music.play(loops=-1, start=0.0)

	for i in range(numberPicsShown_-1):
		print ("")
		print ("ImageNr: "+str(i))
				
		bildAufbau()
		pygame.display.flip()
		
		fadeInPic(i)
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