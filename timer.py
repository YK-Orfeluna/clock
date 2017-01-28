# -*- coding: utf-8 -* 
import time, math
import numpy as np
import cv2

def convert_time(nowtime) :
	hour = int(math.floor(nowtime / (60*60)))
	if hour < 10 :
		hour = "0" + str(hour)

	minute = int(math.floor(nowtime / 60))
	if minute < 10 :
		minute = "0" + str(minute)

	second = int(math.floor(nowtime % 60))
	if second < 10 :
		second = "0" + str(second)

	point = int(round(math.modf(nowtime)[0]*100, 0)) 
	if point < 10 :
		point = "0" + str(point)
	out = str(hour) + ":" + str(minute) + ":" + str(second) + ":" + str(point)
	return out

def circle(i,r) :	# clock needle of second(hour, minute, second, rad)
	theta = i-90
	x = r * math.cos(math.radians(theta)) + 250
	x = int(round(x, 0))
	y = r * math.sin(math.radians(theta)) + 250
	y = int(round(y, 0))
	return (x, y)

WINDOW_NAME = "timer"
WINDOW_SIZE = (500, 500)
LENGTH = WINDOW_SIZE[0]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RAD = LENGTH / 2
INSIDE_RAD = 200

frame = np.zeros([LENGTH, LENGTH, 3], dtype=np.uint8)
frame.fill(255)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

for i in xrange(360) :
	hue = 55 - (i / 8)
	print hue
	cv2.line(frame, circle(i, INSIDE_RAD), circle(i, RAD), (hue, 255, 255), 5, 0)
frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)

TEXT_POSITION = (105, 260)
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 3
FONT_BOLD = 3
EDGE = cv2.CV_AA

target = 60	* 1	# sec., min.
start = time.time()

i = 0
while True :
	dst = frame.copy()

	cv2.line(frame, circle(i, INSIDE_RAD), circle(i, RAD), WHITE, 5, 0)

	passed = time.time() - start
	t = target - passed
	timer = convert_time(t)

	cv2.putText(dst, timer, TEXT_POSITION, FONT, FONT_SIZE, BLACK, FONT_BOLD, EDGE)

	cv2.imshow(WINDOW_NAME, dst)
	key = cv2.waitKey(33)
	if key != -1 :
		break

	i = 360 * (passed / target)


exit()

