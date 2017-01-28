# -*- coding: utf-8 -* 

import time, math
import numpy as np
import cv2

HEIGHT = 700					# height
WIDTH = 600						# width
CHANNEL = 3						# color-channel
	
CENTER = (300, 300)				# center of clock

RAD = 5							# radians of circle

RAD_OUT = 250
RAD_IN = 200

BLACK = (0, 0, 0)				# color(BGR)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
YELLOW = (0, 255, 255)
MAGENTA = (255, 0, 255)
CYAN = (255, 255, 0)

EDGE = cv2.CV_AA

WINDOW = "Clock"

class Clock() :
	def __init__(self) :
		self.frame = np.zeros([HEIGHT, WIDTH, CHANNEL])
		self.frame.fill(255)
		self.h = 0
		self.m = 0
		self.s = 0

	def hour(self, r) :		# clock needle of hour(hour, minute, second, rad)
		hour = self.h % 12 - 3
		theta = 360 / 12 * hour + (self.m * 60 + self.s) / 120.0
		x = r * math.cos(math.radians(theta)) + CENTER[0]
		x = int(round(x, 0))
		y = r * math.sin(math.radians(theta)) + CENTER[0]
		y = int(round(y, 0))
		return (x, y)

	def minute(self, r) :	# clock needle of minute(hour, minute, second, rad)
		minute = self.m % 60 + 45
		theta = 360 / 60 * minute + (self.s * 0.1)
		x = r * math.cos(math.radians(theta)) + CENTER[0]
		x = int(round(x, 0))
		y = r * math.sin(math.radians(theta)) + CENTER[0]
		y = int(round(y, 0))
		return (x, y)

	def second(self, r) :	# clock needle of second(hour, minute, second, rad)
		second = self.s % 60 + 45
		theta = 360 / 60 * second
		x = r * math.cos(math.radians(theta)) + CENTER[0]
		x = int(round(x, 0))
		y = r * math.sin(math.radians(theta)) + CENTER[0]
		y = int(round(y, 0))
		return (x, y)

	def time_text(self) :
		if self.h <= 10 :
			h = "0" + str(self.h)
		else :
			h = str(self.h)

		if self.m <= 10 :
			m = "0" + str(self.m)
		else :
			m = str(self.m)

		if self.s <= 10 :
			s = "0" + str(self.s)
		else :
			s = str(self.s)

		nowtime = h + " : " + m + " : " + s
		return nowtime

	def background(self) :
		cv2.circle(self.frame, (300, 300), RAD, BLACK, -1, EDGE)

		for i in xrange(60) :
			self.m = i
			cv2.line(self.frame, self.minute(RAD_IN), self.minute(RAD_OUT), BLUE, 3, EDGE)
		self.m = 0
		for i in xrange(12) :
			self.h = i
			cv2.line(self.frame, self.hour(RAD_IN), self.hour(RAD_OUT), RED, 5, EDGE)

	def main(self) :
		self.background()

		while True :
			clock = self.frame.copy()

			t = time.localtime()

			self.h = t.tm_hour
			self.m = t.tm_min
			self.s = t.tm_sec

			cv2.line(clock, CENTER, self.hour(150), BLACK, 10, EDGE)
			cv2.line(clock, CENTER, self.minute(RAD_IN), BLACK, 5, EDGE)
			cv2.line(clock, CENTER, self.second(RAD_OUT), BLACK, 2, EDGE)

			nowtime = self.time_text()
			cv2.putText(clock, nowtime, (150, 650), cv2.FONT_HERSHEY_PLAIN, 3, BLACK, 3, EDGE)

			cv2.imshow(WINDOW, clock)	
			
			key = cv2.waitKey(100)
			if key != -1 :
				cv2.destroyWindow(WINDOW)
				exit()

if __name__ == "__main__" :
	app = Clock()
	app.main()