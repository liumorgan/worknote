import time
import pyautogui as gui
screenWidth, screenHeight = gui.size()
currentMouseX, currentMouseY = gui.position()
i=0
j=0
while True:
	gui.moveTo(1031,556)
	currentMouseX, currentMouseY = gui.position()
	print "open move to:", currentMouseX, ",",currentMouseY
	gui.click()
	while j < 425:
		print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),"j = ", j, "/", 425
		j=j+1
		if j%20 == 0:
			gui.moveTo(j,j)
		time.sleep(1)
	j = 0
	gui.moveTo(736,369)
	currentMouseX, currentMouseY = gui.position()
	print "over move to:", currentMouseX, ",",currentMouseY
	gui.click()
	gui.moveTo(1041,151)
	currentMouseX, currentMouseY = gui.position()
	print "close move to:", currentMouseX, ",",currentMouseY
	gui.click()
	i=i+1
	print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),i, "	", i*425
	time.sleep(1)