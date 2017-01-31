# -*- coding: utf-8 -* 
import time, math
import numpy as np
import cv2
import key_num as k

def convert_time(nowtime) :								# 残り時間（秒）をxx時間xx分xx秒表記（str）に返還する
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

def convert_second(h, m, s) :							# h時間m分s秒をxx秒で出力する
	out = h * 3600 + m * 60 + s
	return out

def circle(i,r) :										# 半径rの円，i度の弧の上の座標を求める
	theta = i-90
	x = r * math.cos(math.radians(theta)) + 250
	x = int(round(x, 0))
	y = r * math.sin(math.radians(theta)) + 250
	y = int(round(y, 0))
	return (x, y)

WINDOW_NAME = "timer"									# ウィンドウの名前
WINDOW_SIZE = (500, 500)								# ウィンドウのサイズ
LENGTH = WINDOW_SIZE[0]

BLACK = (0, 0, 0)										# 色設定（黒）
WHITE = (255, 255, 255)									# 色設定（白）

RAD = LENGTH / 2										# 時間バー（円）の外径
INSIDE_RAD = 200										# 時間バー（円）の内径

frame = np.zeros([LENGTH, LENGTH, 3], dtype=np.uint8)	# 表示ウィンドウの作成
frame.fill(255)											# ウィンドウを白にする
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)			# ウィンドウをHSV返還

# Hue55-0のグラデーションで線を描くため，線を使って円を描く
for i in xrange(360) :
	hue = 55 - (i / 8)									# Hueを段階的に0に近づける
	cv2.line(frame, circle(i, INSIDE_RAD), circle(i, RAD), (hue, 255, 255), 5, 0)
frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)			# ウィンドウをBGRに再変換
frame2 = frame.copy()

# テキストの各種設定
TEXT_POSITION = (105, 260)
FONT = cv2.FONT_HERSHEY_PLAIN
FONT_SIZE = 3
FONT_BOLD = 3
EDGE = cv2.CV_AA

target = convert_second(0, 0, 45)						# タイマー時間

# ベルを鳴らす時間
#bell = [convert_second(0, 15, 0), convert_second(0, 20, 0), convert_second(0, 30, 0)]
bell = [10, 20, 30]
bell = sorted(bell)
flag_bell = 0

bar = 0													# タイマーの進行状況
stop = 1												# 停止管理用のフラグ
reset = -1												# リセット用のフラグ

start = time.time()										# 開始時間
time_flag = start										# 停止時の時間管理

passed = 0												# 経過時間
dst = frame.copy()
cv2.putText(dst, convert_time(target), TEXT_POSITION, FONT, FONT_SIZE, BLACK, FONT_BOLD, EDGE)

while True :
	if stop == -1 :
		dst = frame.copy()

		cv2.line(frame, circle(bar, INSIDE_RAD-10), circle(bar, RAD+10), WHITE, 5, 0)

		passed = time.time() - start
		t = target - passed
		timer = convert_time(t)

		cv2.putText(dst, timer, TEXT_POSITION, FONT, FONT_SIZE, BLACK, FONT_BOLD, EDGE)

	if flag_bell <= len(bell)-1 :
		if bell[flag_bell] == round(passed, 0) :
			print("bell")
			flag_bell += 1

	bar = 360 * (passed / target)

	cv2.imshow(WINDOW_NAME, dst)

	key = cv2.waitKey(33)

	if key == k.esc or passed == target :				# escで終了
		cv2.destroyAllWindows()
		exit()
	elif key == k.space :								# spaceで一時停止/再開
		stop *= -1
		if stop == 1 :
			time_flag = time.time()
		elif stop == -1 and reset == -1 :
			stop_time = time.time() - time_flag
			start += stop_time
		else :											# 初期化
			reset = -1
			bar = 0
			passed = 0
			flag_bell = 0
			start = time.time()
			time_flag = start

	elif key == k.enter and stop == 1 :					# enterで初期化
		reset = 1
		dst = frame2.copy()
		frame = frame2.copy()
		cv2.putText(dst, convert_time(target), TEXT_POSITION, FONT, FONT_SIZE, BLACK, FONT_BOLD, EDGE)
		
	