import game
import random

class ai_possib:
	#this class represents a possibility of the decision what the bot does
	def __init__(self, unit, forward, dice, smart=1337):
		self.unit = unit #which unit is this proposal about
		self.forward = forward #true if it's about moving forward
		self.dice = dice
		if smart == 1337:
			self.smart = self.determine_smart() #how smart would this proposal be
		else:
			self.smart = smart
	def determine_smart(self): #todo depends on com.rule_jumps
		smart = 0

		#position is relative to the spawn
		pos = unit.pos
		pos -= unit.player.nr*10
		pos %= 40

		#all the smart things
		#unit sitting on an enemy spawnpoint?
		if pos in [10,20,30]:
			if com.players[pos/10] != 0 and	not com.players[pos/10].all_out()):
				#unit should leave a dangerous spawn
				smart += 15
				if com.players[unit.pos/10].has_tripleroll():
					smart += 10

		if self.forward:
			endpos = pos+self.dice
		else:
			endpos = pos - self.dice
		endpos %= 40
		if endpos in [4,14]:#good jump
			would_jump = 2
		elif endpos in [24,34]:#bad jump
			would_jump = 1
		else:		#no jump
			would_jump = 0
			jumped_pos = 40
		if would_jump:
			jumped_pos = (endpos+20)%40
		
		#determine effective distance traveled
		if would_jump == 1:
			distance = self.dice -20
		elif would_ump == 2:
			distance = self.dice +20
		else:
			distance = self.dice
		#if you travelled backward distance is negative, but thats awwwwright

		killcount = 0
		esc_danger = 0 #amount of units that might have killed this unit
		new_danger = 0 #amount of units that might kill this unit after this
		for player in game.players:
			if not player: #empty
				continue
			if player == game.memo.act_pl: #own units
				continue
			#else
			for enemy in player.units:
				if enemy.cond != 1: #not alive
					continue
				if enemy.pos == endpos or jumped_pos == enemy.pos):#you'd kill him
					killcount += 1

				d = abs(enemy.pos-self.unit.pos)
				if (d in range(1,6) and player.must_spawn()) or (d in range(1,7)): 
					esc_danger += 1

				d = enemy.pos
				if jumped_pos == 40: d -= endpos
				else: d-= jumped_pos
				d = abs(d)
				if (d in range(1,6) and player.must_spawn()) or (d in range(1,7)): 
					new_danger += 1


		#smart += effective relative distance traveled
		if would_jump == 2:
			smart += 10
		elif would_jump == 1:
			smart -= 10
		if killcount == 1:
			smart += random.randint(15,30)
		elif killcount == 2:
			smart += random.randint(35,50)
		if not would_jump:
			if 4 in range(pos, endpos) or 14 in range(pos, endpos): #ignored good jump
				smart -= random.randint(4,7)
			elif 24 in range(pos, endpos) or 34 in range(pos, endpos):#ignored bad jump
				smart += random.randint(4,7)
		if pos >= 34:#distance to safe < 6
			smart += 5 * (40 - pos)
			smart += danger*5
		if pos <= 4:#distance to spawn <= 4
			smart += 3 * (5 - pos)
		if endpos >= 40:
			smart += 25
		if unit.cond == 2:
			smart += 42
		smart += (esc_danger-new_danger)*3
		return smart#todo
def do_turn(): #bot throws the dice, chooses what unit to move and does so	
	if game.memo.rolls == 0:#cant do a turn anymore anyway
		next_pl()
		return
	player = game.memo.act_pl

	if not game.rules.chessmod
		game.throw_the_dice("bot")
		if game.memo.may_spawn:
			possibs =game.memo.act_pl.units
			for i in [3,2,1,0]:
				if possibs[i].cond != 0:
					possibs.remove(i)
			selection = possibs[random.randint(0,len(possibs)-1)]
			game.actio([3],game.memo.act_pl,selection)
			return
		else:
			#ordinary turn
			selection = find_smartest(player,game.memo.dice)[0:2]
			game.actio([selection[1],game.memo.dice], player, selection[0])
			return

	else:
		selection = find_smartest_chess(player)[0:2]
		game.throw_the_dice(selection[1])
		game.actio([selection[1],game.memo.dice],player,selection[0])
		return



def do_after_turn():#TODO
	player = game.memo.act_pl
	if com.has_to_die: #ignored the fact, that one had to kill
		possibs = []
		for i in range(0,4):
			u = player.units[i]
			if u.threatened[0] or u.threatened[1]:
				possibs.append([i])
		#select the least important unit to die
		#least important is the unit that is behind the most
		for i in range(0, len(possibs)-1):#get the relative position of the unit
			pos_e = player.units[possibs[i]].pos
			pos_e -= com.act_player*10
			possibs[i].append(pos_e)
		#select the one with min(possibs[i][1])

	if com.rolls >= 1:#another roll
		self.do_turn()
		return
	else:#next player
		next_pl("bot")
	return



#1:forward;2:backward
def find_smartest(player,dice):
	for u in player.units:
	#ai_possib():def __init__(self, unit, forward, dice, smart=1337):
		

	return [selection, forward, smart]
def find_smartest_chess(player):
	dice = 1
	selection = player.units[0]
	smart = -1337
	forth = True
	for d in range(1,7):
		result = find_smartest(player,d)
		if result[2] > smart:
			smart = result[2]
			dice = d
			selection = result[0]
			forth = result[1]
	return [selection, forward, dice]
