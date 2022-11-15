from __future__ import print_function

import time
from sr.robot import *

t = 1 # time
a_th = 4.0 
d_th = 0.4 
collected_tokens = [] #array to store marked silver tokens
visited_checkpoints = [] #array to store marked gold tokens
retard = lambda x : time.sleep(x) # lambda to retard actions

R = Robot()

# drive the robot directions
def drive(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	retard(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

# turn the robot directions
def turn(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	retard(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

#search for nearest token that hasn't already marked
def find_token(token_type, visited_tokens):
	dist = 100
	rot_y = 0
	token_code = -1

	for token in R.see():
		if token.dist < dist and token.info.marker_type is token_type and token.info.code not in visited_tokens:
			dist = token.dist
			rot_y = token.rot_y
			token_code = token.info.code

	if dist >= 100:    # no token found
		return -1, -1, token_code
	else:
		return dist, rot_y, token_code

#update robot position respected the interest token
def update_pos(target_code):
	for token in R.see():
		if token.info.code == target_code:
			return token.dist, token.rot_y
	return -1, -1

#scan for a silver token, grab it and trasport to a gold token
def collect_silver_tokens(n_tokens):
	drive(40, t*3)
	retard(1)

	lock = False
	token_code = -1
	e = 1

		#loop until all tokens are marked
	while n_tokens > 0:
		if not lock:
			dist, rot_y, token_code = find_token(MARKER_TOKEN_SILVER, collected_tokens)
			# if no token founded, move and turn incrementally until one is found
			while dist == -1 or token_code == -1:
				turn(30*e, t)
				drive(30*e, t)
				dist, rot_y, token_code = find_token(MARKER_TOKEN_SILVER, collected_tokens)
				if token_code != -1:
					print('Locked token')
				else:
					print('No silver token in range')
				retard(1)
				e += 0.2
		else:
			print('Found one!!')
			dist, rot_y = update_pos(token_code)

		e = 1
		lock = True

		#if close enough to the silver token, grab it and trasport to a gold token
		if dist < d_th:
			if R.grab():
				print('Grabbed token')
				retard(0.5)
				print('Moving token... ')
				drive(-30, t)
				turn(30, t)
				bring_to_checkpoint(token_code)
				n_tokens -= 1
				drive(-30, t)
				turn(45, t)
				lock = False
			else:
				print('Impossible to grab token!!')
				exit()
		
		elif rot_y < -a_th:     #if the robot is not well aligned with the token, we move it on the left or the right
			turn(-2, t)
		elif rot_y > a_th:
			turn(2, t)
		
		else:			#if the tobot is well aligned with the token, we go forward
			drive(30, t)

# bring the silver token to a gold token
def bring_to_checkpoint(token_code):
	checkpoint = False
	lock = False
	checkpoint_code = -1
	e = 1

	while not checkpoint:
		if not lock:
			dist, rot_y, checkpoint_code = find_token(MARKER_TOKEN_GOLD, visited_checkpoints)
			#if no token founded, move and turn incrementally until one is found
			while dist == -1 or checkpoint_code == -1:
				turn(30*e, t)
				drive(30*e, t)
				dist, rot_y, checkpoint_code = find_token(MARKER_TOKEN_GOLD, visited_checkpoints)
				if checkpoint_code != -1:
					print('Locked gold token')
				else:
					print('No gold token in range')
				e += 0.2
				retard(1)
		else:
			print('Moving to golden token')
			dist, rot_y = update_pos(checkpoint_code)

		e = 1
		lock = True

		# if close enough to the gold token, release the silver token and mark it as visited
		if dist < d_th * 1.5:
			checkpoint = True
			R.release()
			collected_tokens.append(token_code)
			visited_checkpoints.append(checkpoint_code)
			lock = False
		
		elif rot_y < -a_th:        #if the robot is not well aligned with the token, we move it on the left or the right
			turn(-2, t)
		elif rot_y > a_th:
			turn(2, t)
		
		else:			   #if the tobot is well aligned with the token, we go forward
			drive(30, t)


#collect_silver_tokens declarations
collect_silver_tokens(6)
print('All tokens have been successfully transported')
