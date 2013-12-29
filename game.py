import random

import surface
import plun
import network
players = [plun.player(0), plun.player(1), plun.player(2), plun.player(3)]

#contains all gamelogicfunctions and ruleflags

def get_unit_bypos(pos,cond):
	for u in memo.act_pl.units:
		if u.pos == pos and u.cond == cond:
			return u
	return 4

def victory(player):
	for i in range(0,4):
		if player.units[i].cond != 2:
			return False
	#what to do for victory
	surface.set_msg("Congratulations\n"+player.name+"\nwins the match")
	print("SIEG", player.name)
	return True




def next_pl(a):
	n = 0
	for p in players:
		if p != 0 and not p.done():
			n += 1
	if n == 0:#game definitely over
		name = memo.act_pl.name #TODO
		surface.content.set_text(name +" \nhas won the game")
		surface.game_over_win.show_all()
		surface.show_dice_throw(0)
		surface.allow_nextpl(False)
		#show a window and end the game
	else:
		memo.nextplayer()
		while(memo.act_pl.done()):
			memo.nextplayer()
#	memo.nextplayer()
	surface.show_dice_throw(0)
	if not a == "nw":#called by GUI
		network.send("e")
	surface.allow_nextpl(False)
	surface.set_msg(memo.get_plstr()+"\nhas to do the turn!")

	# Make sure that the grave of the other players is grey      
	surface.restrict_to_player(memo.act_pl.nr)

	memo.act_pl.set_threats(0)
	if memo.act_pl.has_tripleroll():
		memo.rolls = 3
	else:
		memo.rolls = 1

	#player must have a free spawnpoint
	if not (memo.act_pl.spawn_is_free() or memo.act_pl.all_out()):#modus tollens
		surface.set_msg(memo.act_pl.name+"("+memo.act_pl.get_color()+")\nMake room at\nyour Spawnpoint")
	#what controls the current player
	if memo.act_pl.isa_bot():
		memo.act_pl.control.do_turn()
	#elif network?
	else:#human
		if network.hasPlayer(memo._plcnt):#my player
			surface.set_dice_sens(True,memo.act_pl)
		else:
			pass#wait for network input
	return


def select_unit(n):
	if network.hasPlayer(memo.act_pl.nr):
		memo.selection = n


def throw_the_dice(b,inp=False):
	memo.kills = 0#reset kills
	#print b,inp
	if not rules.chessmod:
		del b
		if inp == False:#own input
			memo.dice = random.randint(1,6)
			network.send("d"+str(memo.dice))
		else:#input from host through network
			memo.dice = inp 
		memo.act_pl.roll_log.append(memo.dice)
		if memo.dice != 6:
			memo.rolls -= 1
		surface.show_dice_throw(memo.dice)
		memo.act_pl.set_threats(memo.dice)
		#for u in memo.act_pl.units:
		#	print u.threatened
		if ((memo.dice == 6 or memo.act_pl.has_roll_flush() ) and 
		(not memo.act_pl.all_out() and memo.act_pl.spawn_is_free())):#must spawn
			if memo.dice == 6:
				memo.rolls = 1
			else:
				memo.rolls = 0
			for u in memo.act_pl.units:#bugfix
				u.threatened = [False,False]
			memo.may_spawn = True
			#threats are cleared in actio()
			surface.set_msg(memo.act_pl.name+"\n("+memo.act_pl.get_color()+")\nSpawn now.")
			surface.set_dice_sens(False, True)
			return
		
		possibs = False
		for i in range(0,4):
			if memo.act_pl.units[i].can_do(memo.dice):
				possibs = True
				break
		if not possibs:
			if memo.rolls == 0:#round over
				surface.set_dice_sens(False,True)
				if network.hasPlayer(memo._plcnt):
					surface.allow_nextpl(True)
			#else roll the dice another time so don't change any permissions
			return
		#else (player can do something)
		surface.allow_nextpl(False)
		surface.set_dice_sens(False, True)
		
	else: #chessmod on
		memo.rolls = 0
		memo.dice = surface.identify_roll(b)
		surface.show_dice_throw(memo.dice)
		surface.set_dice_sens(False,memo.act_pl)
		memo.act_pl.set_threats(7)
		if memo.dice == 6 and (not memo.act_pl.all_out() and memo.act_pl.spawn_is_free()):
			memo.may_spawn = True
			surface.set_msg("You may spawn\nright now.")			

		return



def actio(doing, player,unit,fr = False):#move forward, backward, or spawn


#doing:consists of [1,1-6] , [2,1-6] or [3]
#returns
#0 :not possible
#1 :did it, got another roll
#2 :did it, next_pl
	
	########
	
	if type(doing) != list:
		
		doing = [doing,memo.dice]
	if player == None:
		player = memo.act_pl
	if unit == None:
		unit = memo.selection
	elif unit in range(4):
		unit = memo.act_pl.units[unit]
	#print doing,player,unit
	########
	#check if some rules inhibit this action
	#must keep spawn free
	if fr == False:#kommt von der GUI
		network.send("z"+str(unit.nr)+str(doing[0]))
		if not network.hasPlayer(player.nr):
			return
	if not player.spawn_is_free() and not player.all_out():#must clear the spawnpoint
		if doing[0] == 3:
			return False
		#selection must be the one on the spawn or the last in a chain who blocks
		for i in range(0,4):
			if player.units[i].pos == player.nr*10 and player.units[i].cond == 1:#sits on spawn
				u = player.units[i]
				break
		while not u.can_do(doing[1]):#TODO bug endlosschleife
			#probably doing[1] is wrong
			#or if statement in forloop always False
			for i in range(0,4):
				if player.units[i].pos == (u.pos+memo.dice)%40 and player.units[i].cond == 1:#unit[i] blocks
					u = player.units[i]
					break
			#succes, got the blocking unit
		if unit != u:#fail
			return False
	#must spawn
	if memo.dice == 6 and not memo.act_pl.all_out() and doing[0] != 3 and player.spawn_is_free():
		surface.set_msg(memo.get_plstr()+"\nYou must\nspawn now")
		return False



	if doing[0] == 1:#forward
		mov = unit.move(doing[1], True)
		if mov == False or memo.suicide:#can't move forward or expecting suicide
			return False
		else:
			surface.moving_render(unit,player,doing)
			unit.pos = mov[0]
			unit.cond = mov[1]
			#if not network.hosting:
			
			
	elif doing[0] == 2:#backward
		if not unit.threatened[1] or memo.suicide:#can't move backward
			return False
		else:
			mov = unit.move(doing[1], False)
			surface.moving_render(unit,player,doing)
			unit.pos = mov[0]
			#if not network.hosting:
			#network.send("z"+str(unit.nr)+str(doing[0]))
	elif doing[0] == 3:#spawn
		if memo.suicide:
			return
		fl = unit.spawn()
		if not fl:#spawn did not work	
			return False
		else:#spawned
			surface.render(unit.nr+player.nr*4, 0, 4)#empty home
			surface.render(unit.pos, 1, player.nr)#fill spawn
			if not rules.chessmod:
				for i in range(0,4):#erase threats if you spawned
					player.units[i].threatened = [False,False]
			if 6 not in memo.act_pl.roll_log:#spawned by flush
				if network.hasPlayer(memo._plcnt):#my player
					surface.allow_nextpl(True)
			after_actio(doing, unit, player)
			#if not network.hosting:
			#network.send("z"+str(unit.nr)+str(doing[0]))
			if memo.rolls <= 0:#next_pl
				return 2
			else:
				return 1

	elif doing[0] == 4:#suicide
		if not (True in unit.threatened and memo.suicide):
			return False
		surface.render(unit.pos,unit.cond,4)
		unit.die()
		surface.render(unit.pos,0,player.nr)
		#after_actio isnt even necessary
		if player.isa_bot():
			player.control.do_after_turn()
		elif network.hasPlayer(memo._plcnt):#my player
			surface.allow_nextpl(True)
		memo.suicide = False
		#network.send("z"+str(unit.nr)+str(doing[0]))


	else:#this should never happen
		print "actio else???"
		return False
	

def after_actio(doing, unit, player):#kills, jumps, kills, checks for threats
#	for u in player.units:
#		print u.threatened
	#and calls next_pl if its a bot
	bot = player.isa_bot()

	fl_kill = [False]
	#kill
	pr = []
	for i in range(4):
		if True in player.units[i].threatened:
			pr.append(i)
	#print pr;del pr
	if unit.cond == 1:#must be on the field
		for i in range(0,4):
			if i == player.nr or type(players[i]) == int:
				continue
			for u in range(0,4):
				if players[i].units[u].cond != 1:
					continue
				if players[i].units[u].pos == unit.pos:
					players[i].units[u].die()#killed an enemy
					surface.kill(players[i].units[u])
					fl_kill[0] = True
					break
			if fl_kill[0]:#can't kill more than once (jumps later)
				break
	if doing[0] != 3:#moved
		#short check if game is over
		victory(player)#actually only when moving forward but who cares

		#jump
		fl_kill.append(unit.jump())

		#kill again
		if fl_kill[1]:#jumped
			surface.jump_render(unit.pos)
		
			fl_kill[1] = False
			for i in range(0,4):
				if i == player.nr or type(players[i]) == int:
					continue
				for u in range(0,4):
					if players[i].units[u].cond != 1:#not on the field
						continue
					if players[i].units[u].pos == unit.pos:#same position
						players[i].units[u].die()#killed an enemy
						surface.kill(players[i].units[u])
						fl_kill[1] = True
						break
				if fl_kill[1]:
					break

		if not False in fl_kill:#hoooray you killed somebody
			pass
			
		#threat
		if True not in fl_kill: #didnt kill
			for i in range(0,4):
				if True in player.units[i].threatened:
					surface.set_msg(player.name + "\nYou missed a threat!")
					memo.suicide = True
					if bot:
						player.control.do_after_turn()
					return


	if bot:
		player.control.do_after_turn()
		return

	if memo.rolls <= 0:#next player
		if network.hasPlayer(memo._plcnt):#my player
			surface.allow_nextpl(True)
		return
	else:
		if network.hasPlayer(memo._plcnt):
			surface.set_dice_sens(True, memo.act_pl)#release the dice for another roll
		surface.show_dice_throw(0)
		return


class memory():
	def __init__(self):
		self.newgame()
	def nextplayer(self):
		self._plcnt += 1#private playercounter allows to adress the active player directly
		self._plcnt %= 4
		while type(players[self._plcnt]) == int:
			self._plcnt += 1
			self._plcnt %= 4
		self.act_pl = players[self._plcnt]
		self.selection = 4
		self.may_spawn = False 
		self.suicide = False
		if self.act_pl.has_tripleroll():
			self.rolls = 3
		else:
			self.rolls = 1
		self.roll_log = []
		self.dice = 0

	def newgame(self):
		self._plcnt = -1#dont worry will immediately be increased
		self.nextplayer()
		self.may_spawn = False 
		self.suicide = False
	def get_plstr(self):
		return self.act_pl.name+"("+self.act_pl.get_color()+")"

class rule():
	def __init__(self):
		self.reset()
	def reset(self):
		self.jumps = True
		self.chessmod = False



def newgame():
	#for p in players:
	#	if type(p) != int:
	#		p.reset()
	memo.newgame()
	if network.hasPlayer(memo._plcnt):
		surface.set_dice_sens(True,memo.act_pl)
	else:
		surface.set_dice_sens(False,memo.act_pl)
	#rules.reset()
