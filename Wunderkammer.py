import RPi.GPIO as GPIO
import pygame, sys, os
import vlc, random
import time, threading

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
	print("")
	print("InterruptBilder")
	if( not picsRunning): #not playerTimelapse.is_playing()and
		print("startingPics")
		playerStartWunderBox.pause()#stop()
		playerTimelapse.pause()
		globals().update(picsRunning = True)
		#print ("picsRunning: "+str(picsRunning))
		
		stop_event = threading.Event()
		PicsThread = threading.Thread(target=Pics, args=(123,stop_event))
		PicsThread.start()
		#Pics()
	
def InterruptTimelapse(x):
	print("")
	print("InterruptZeitraffer")
	if(not playerTimelapse.is_playing()): #and not picsRunning):
		print("startingTimelapse")
		globals().update(picsRunning = False)
		stop_event.set()
		playerTimelapse.set_xwindow(win_id)
		playerStartWunderBox.stop()
		playerTimelapse.set_media(media_Timelapse)
		playerTimelapse.play()

GPIO.add_event_detect(BTN_Pics, GPIO.RISING, callback = InterruptPics, bouncetime = 2000)
GPIO.add_event_detect(BTN_Timelapse, GPIO.RISING, callback = InterruptTimelapse, bouncetime = 2000)


running = True
picsRunning = False
DEBUG = False

if len(sys.argv)>1:
        if sys.argv[1]=="--DEBUG":
                DEBUG = True

#fadeDelay = 0.0000005
#Delay = 0.0005

fadeDelay = 0.0000001
Delay = 0.0001

if DEBUG:
	fadeDelay = 0.00000005
	Delay = 0.00005
	
print ('')
print ('')
print("fadeDelay "+str(fadeDelay))
print("Delay "+str(Delay))
	
BLACK = ( 0, 0, 0)
WHITE = ( 230, 230, 230)

pygame.display.init()
infoObject = pygame.display.Info()

w = infoObject.current_w
h = infoObject.current_h
if DEBUG:
	w=16*80
	h=9*80

print("w: "+str(w)+" h: "+str(h))

screenRatio = w/h

columns = 3
rows	= 3

gridPlaces = columns*rows

numberPicsShown = 36-9

border = 4

picW = int(w/rows)
picH = int(h/columns)

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

if DEBUG:
	if "test.mp4"in os.listdir():
		media_WunderBox = vlcInstanceWunderBox.media_new("test.mp4")
	if "test2.mp4"in os.listdir():
		media_Timelapse = vlcInstanceTimelapse.media_new("test2.mp4")
	
playerStartWunderBox.set_media(media_WunderBox)
playerTimelapse.set_media(media_Timelapse)

mylist = os.listdir('Bilder/')
cnt = len(mylist)
print("")
print ("Image List:"+str(mylist))
print("")
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
	#print("loopR:"+str(int(numberPicsShown_/(gridPlaces)))+" "+str(range(int(numberPicsShown_/(gridPlaces)))))
	for ii in range(int(numberPicsShown_/(gridPlaces))+1):
		randOrder = random.sample(range(gridPlaces), gridPlaces)
		#print("randOrder: "+str(randOrder))
		xxx = 0
		if ii>=int(numberPicsShown_/(gridPlaces)):
			xxx = gridPlaces-(numberPicsShown_-gridPlaces*ii)
		#print("xxx: "+str(xxx)+" "+str(gridPlaces-xxx))
		for i in range(gridPlaces-xxx):
			#print(str((gridPlaces)*ii+i)+"  "+str(ii)+"  "+str(i)+" :  "+str(randOrder[i]))
			PosOrder_List_[(gridPlaces)*ii+i] = randOrder[i]
		
	globals().update(PosOrder_List = PosOrder_List_)
	globals().update(ImageOrder_List = random.sample(range(len(mylist)), numberPicsShown_))
	print ("PosOrder_List: "+str(PosOrder_List)+str(len(PosOrder_List)))
	print ("ImageOrder_List: "+str(ImageOrder_List)+str(len(ImageOrder_List)))

PicAtPos = [rows*[""]for i in range(columns)]
SizeOfPicAtPos = [rows*[[0,0,0,0]]for i in range(columns)]

        		
def bildAufbau(alpha=255):	
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
	
	imageRect = pygame.Rect(picW*x,picH*y,picW,picH)
	
	print("x"+str(x))
	print("y"+str(y))
	
	xOffset = 0
	yOffset = 0
	
	image = pygame.image.load('Bilder/'+mylist[ImageOrder_List[nr]]).convert()
	
		

	if nr>gridPlaces:
		print('FadeOut')
		
		imageA = pygame.image.fromstring(PicAtPos[x][y],(SizeOfPicAtPos[x][y][2], SizeOfPicAtPos[x][y][3]),"RGB")
		#PicAtPos[x][y] = ""
		for i in reversed(range (int(254/2))):
			
			#screen.fill(BLACK)
			#bildAufbau()
			
			pygame.draw.rect(screen,BLACK,imageRect)
			
			imageA.set_alpha(i*2)
			screen.blit(imageA,(x*picW+SizeOfPicAtPos[x][y][0],y*picH+SizeOfPicAtPos[x][y][1]))
			pygame.display.update(imageRect)
			time.sleep(fadeDelay)
			if not picsRunning:
				return
	
	if (image.get_width()/image.get_height())>screenRatio:
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
	
	print('FadeIn')
				
	imageA = image
	PicAtPos[x][y] = pygame.image.tostring(image,"RGB")
	
	for i in range (int(254/2)):
	
		pygame.draw.rect(screen,BLACK,imageRect)
		
		imageA.set_alpha(i*2)
		screen.blit(imageA,(picW*x+SizeOfPicAtPos[x][y][0],picH*y+SizeOfPicAtPos[x][y][1]))
		pygame.display.update(imageRect)
		
		time.sleep(fadeDelay)
		if not picsRunning:
			return
		
	
	bildAufbau()
	pygame.display.flip()

def fadeOutAll():
	print('')
	print('FadeOutAll')
	print('')
	print('')
	for i in reversed(range (int(254/2))):
		screen.fill(BLACK)
		bildAufbau(i*2)
		#imageA.set_alpha(i)
		#screen.blit(imageA,(x*picW+SizeOfPicAtPos[x][y][0],y*picH+SizeOfPicAtPos[x][y][1]))
		pygame.display.flip()
		time.sleep(fadeDelay)
	
def	Pics(abcde, stop_event):

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
	pygame.mixer.music.load("127_full_free-to-dream_0127.wav")
	pygame.mixer.music.play(loops=-1, start=0.0)

	for i in range(numberPicsShown_-1):
		print ("")
		print ("ImageNr: "+str(i))
						
		fadeInPic(i)
		time.sleep(Delay)
		
		if not picsRunning:
			return
			
	time.sleep(1)
	fadeOutAll()	
	pygame.mixer.music.stop()
	globals().update(picsRunning = False)
	StartWunderbox()
	return
		
def StartWunderbox():
	print("")
	print("StartWunderbox")
	screen.fill(BLACK)
	pygame.display.flip()	
	playerStartWunderBox.set_media(media_WunderBox)
	playerStartWunderBox.play()
	
def EndReached(event):
	print("")
	print("EndReached")
	pygame.display.flip()
	playerTimelapse.pause()
	
	#playerTimelapse.release()
	StartWunderbox()

events = playerTimelapse.event_manager()
events.event_attach(vlc.EventType.MediaPlayerEndReached, EndReached)

stop_event= threading.Event()
PicsThread = threading.Thread(target=Pics, args=(123,stop_event))
PicsThread.daemon = True
  	
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