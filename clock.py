# -*- coding: utf-8 -* 

import time, math
import numpy as np
import cv2

HEIGHT = 700					# height
WIDTH = 600						# width
CHANNEL = 3						# color-channel
	
CENTER = (300, 300)				# center of clock

RAD = 5							# radians of circle

BLACK = (0, 0, 0)				# color(BGR)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (255, 255, 0)

def hour(h, m, s, r=250) :		# clock needle of hour(hour, minute, second, rad)
	global CENTER
	hour = h % 12 - 3
	theta = 360 / 12 * hour + (m * 60 + s) / 120.0
	x = r * math.cos(math.radians(theta)) + CENTER[0]
	x = int(round(x, 0))
	y = r * math.sin(math.radians(theta)) + CENTER[0]
	y = int(round(y, 0))
	return (x, y)

def minute(h, m, s ,r=250) :	# clock needle of minute(hour, minute, second, rad)
	global CENTER
	minute = m % 60 + 45
	theta = 360 / 60 * minute + (s * 0.1)
	x = r * math.cos(math.radians(theta)) + CENTER[0]
	x = int(round(x, 0))
	y = r * math.sin(math.radians(theta)) + CENTER[0]
	y = int(round(y, 0))
	return (x, y)

def second(h, m, s ,r=250) :	# clock needle of second(hour, minute, second, rad)
	global CENTER
	second = s % 60 + 45
	theta = 360 / 60 * second
	x = r * math.cos(math.radians(theta)) + CENTER[0]
	x = int(round(x, 0))
	y = r * math.sin(math.radians(theta)) + CENTER[0]
	y = int(round(y, 0))
	return (x, y)

def time_text(h, m, s) :
	if h <= 10 :
		h = "0" + str(h)
	else :
		h = str(h)

	if m <= 10 :
		m = "0" + str(m)
	else :
		m = str(m)

	if s <= 10 :
		s = "0" + str(s)
	else :
		s = str(s)

	nowtime = h + " : " + m + " : " + s
	return nowtime

frame = np.zeros([HEIGHT, WIDTH, CHANNEL])
frame.fill(255)

cv2.circle(frame, (300, 300), RAD, BLACK, thickness=RAD*2)

for i in xrange(60) :
	cv2.line(frame, minute(0, i, 0, r=200), minute(0, i, 0), BLUE, 3, cv2.CV_AA)
for i in xrange(12) :
	cv2.line(frame, hour(i, 0, 0, r=200), hour(i, 0, 0), RED, 5, cv2.CV_AA)

while True :
	clock = frame.copy()

	t = time.localtime()

	h = t.tm_hour
	m = t.tm_min
	s = t.tm_sec

	cv2.line(clock, CENTER, hour(h, m, s, r=150), BLACK, 10, cv2.CV_AA)
	cv2.line(clock, CENTER, minute(h, m, s, r = 200), BLACK, 5, cv2.CV_AA)
	cv2.line(clock, CENTER, second(h, m, s), BLACK, 2, cv2.CV_AA)

	nowtime = time_text(h, m, s)
	cv2.putText(clock, nowtime, (150, 650), cv2.FONT_HERSHEY_PLAIN, 3, BLACK, 3, cv2.CV_AA)

	cv2.imshow("clock", clock)	
	
	key = cv2.waitKey(100)
	if key != -1 :
		break

cv2.destroyWindow("clock")
exit()