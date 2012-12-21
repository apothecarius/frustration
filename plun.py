import game
class unit:
	def __init__(self, num,pl):
		self.nr = num
		self.player = pl
		self.pos = pl.nr*4+num
		self.cond = 0
		#cond == 0: dead
		#cond == 1: alive
		#cond == 2: safe
		self.threatened = [False,False]

	def spawn(self):
		if not self.free_for_me(self.player.nr*10,1) or self.cond != 0:#spawn is not free or unit is not dead
			return False
		self.cond = 1
		self.pos = (self.player.nr)*10
		
		for i in range(0,4):#delete the threats for all mates
			self.player.units[i].threatened = [False,False]
		return True
    
	def die(self):
		self.cond = 0
		self.pos = self.player.nr*4+self.nr
		return


	def move(self, dice,richtung):	#returns [nr of blocking unit][4] if move is not possible 
					#due to block, simple false, if it isn't possible else returns new position, does NOT move the unit
		if self.cond == 0:#unit is dead
			return False

		posi = self.pos
		condi = self.cond
		if richtung == True: #moves forward
			while dice != 0:
				if condi == 2 and posi == (self.player.nr*4)+3:#at the end of the safe
					return False
				
				dice -= 1
				if self.cond == 1:
					a = self.bec_safe(posi)#entering safe
					if a == 1:
						posi = self.player.nr*4
						condi = 2
						continue
					elif a >= 2:
						return [a-2,4]
					#further blocking objects on the road are tested here
				if self.cond == 2:#blocks in the safe
					if posi == (self.player.nr*4)+3:#blocking at the end of safe
						return False
					for i in range(0,4):
						if i == self.nr:
							continue
						if self.player.units[i].is_there(posi+1, 2):#blocks
							return [i,4]

				#nothing blocks, so move
				posi += 1
				posi %= 40#jump over the edge of the world
				
			#blocking things on the endpos of a movement are inserted here
			for i in range(0,4):
				if i == self.nr:
					continue
				if self.player.units[i].pos == posi and self.player.units[i].cond == condi:
					return [i,4]
			return [posi,condi]
		else: #moves backward
			if self.cond == 2:#unit is safe
				return False
			while dice != 0:
				dice -= 1
				posi -= 1
				#insert move_animation here
			posi %= 40#jump to the other edge of the world
			return [posi,condi]


        
	def bec_safe(self, posi):
		if self.player.nr == 0 and posi == 39 or self.player.nr != 0 and posi == (self.player.nr*10)-1:#at the place to become safe
			for i in range(0,4):
				if self.player.units[i].is_there((self.player.nr)*4,2):
					return 2+i#at the entrance, but is blocked by i-2
			return 1#could go inside
		else:
			return 0#not at the entrance
        

	def jump(self):
		if not game.rules.jumps:#check if jumps are disabled
			return False
		if self.cond != 1:
			return False
		if self.pos != 4 and self.pos != 14 and self.pos != 24 and self.pos != 34:#not on a jump position
			return False
		new = (self.pos +20)%40
		for i in range(0,4):#somebody blocking?
			if i == self.nr:#himself
				continue
			if self.player.units[i].pos == new and self.player.units[i].cond == 1:
				return False
		#else:no prob
		self.pos = new
		return True


	def is_there(self, posi, zus):
		if self.pos == posi and self.cond == zus:
			return True
		else:
			return False

	def check_pos(self, position):
		if self.cond != 1:
			return position
		position %= 40
		return position

	def free_for_me(self,posi,zus):
		for i in range(0,4):
			if self.player.units[i].is_there(posi, zus) and i != self.nr:
				return False
		return True

	def is_threatened(self,dice, forward):#returns True if threatened else false, does not overwrite self.threatened
		if self.cond != 1:
			return False
		dist = self.move(dice,forward)
		if (not dist) or dist[1] != 1:
			return False
		for i in range(0,4):
			if type(game.players[i]) == int or i == self.player.nr:
				continue
			for j in range(0,4):
				if game.players[i].units[j].cond == 1 and game.players[i].units[j].pos == dist[0]:
					return True
		return False


	def blocked_by(self,dice):#returns 4 if blocked by nobody, else returns nr
		new_pos = self.move(dice,True)
		if new_pos[1] == 4:
			return new_pos[0]
		for i in range(0,4):
			if i == self.nr:
				continue
			if self.player.units[i].pos == new_pos[0] and self.player.units[i].cond == new_pos[1]:
				#check if can attack backwards
				if True in self.threatened:
					return 4
				return i
		return 4
	
	def can_do(self,dice):
		if self.is_threatened(dice,False):
			return True
		if self.cond == 0 and dice == 6:
			return True
		new = self.move(dice,True)
		if new == False:
			return False
		if new[1] == 4:
			return False
		return True


class player:
	def __init__(self, num, ipee=None):
		self.nr = num
		self.units = [unit(0,self),unit(1,self),unit(2,self),unit(3,self)]
		self.safe_entrance = (num*10-1)%40
		self.control = ipee
		self.name = str(num)
		self.roll_log = []
		
	def prep_for_turn(self):
		self.roll_log = []
		for i in range(0,4):
			self.units[i].threatened = [False, False]

	def isa_bot(self):
		return self.control == "bot"

	def reset(self):
		self.units = (unit(0,self),unit(1,self),unit(2,self),unit(3,self))
		self.name = ""

	def all_out(self): #tells, whether all own units are alive and on the field
		for u in self.units:
			if u.cond == 0:
				return False
		return True

	def spawn_is_free(self):
		for u in self.units:
			if u.pos == self.nr*10 and u.cond == 1:
				return False
		return True

	def has_roll_flush(self):#returns True if the player rolled the same 3 times
		return len(self.roll_log) == 3 and self.roll_log[0] == self.roll_log[1] and self.roll_log[2] == self.roll_log[0] and 6 not in self.roll_log and self.has_tripleroll()

	def has_tripleroll(self):#returns whether the player may roll the dice three times
		if game.rules.chessmod:
			return False
		for i in range(0,4):#anybody in the field
			if self.units[i].cond == 1:
				return False
		b = []#list with the positions of the units in the safe
		for i in range(0,4):#is the safe in order
			if self.units[i].cond == 2:
				b.append(self.units[i].pos)
		if len(b) == 0:#nobody safe
			return True
		#for i in range(self.nr*4+3, self.nr*4-1,-1):
		if len(b) == 1:
			if self.nr*4+3 not in b:
				return False
		elif len(b) == 2:
			if self.nr*4+2 not in b or self.nr*4+3 not in b:
				return False
		elif len(b) == 3:
			if self.nr*4+1 not in b or self.nr*4+2 not in b or self.nr*4+3 not in b:
				return False
		return True

	
	def get_color(self):
		if self.nr == 0:
			return "Red"
		elif self.nr == 1:
			return "Blue"
		elif self.nr == 2:
			return "Yellow"
		elif self.nr == 3:
			return "Green"

	def set_threats(self, dice):
		for i in range(0,4):
			u = self.units[i]
			if dice == 0:#new round
				u.threatened = [False, False]
			elif dice == 7:#chessmod
				u.threatened[0] = False
				u.threatened[1] = False
				for d in range(1,7):
					if u.is_threatened(d,True):
						u.threatened[0] = True
						break
				for d in range(1,7):
					if u.is_threatened(d,False):
						u.threatened[1] = True
						break
			else:
				#TODO sonderfall wenn die figur gar nicht gehen darf weil zB anderer auf spawn
				if not self.spawn_is_free() and not self.all_out(): #spawn blockiert und jn im friedhof
					if u.pos == self.nr*10 and u.cond == 1:
						u.threatened[0] = u.is_threatened(dice,True)
						u.threatened[1] = u.is_threatened(dice,False)
					else:
						u.threatened = [False,False]
				else:
					u.threatened[0] = u.is_threatened(dice,True)
					u.threatened[1] = u.is_threatened(dice,False)


	def must_spawn(self):
		for i in range(0,4):
			if self.units[i].cond == 0:
				return True
		return False

	def done(self):
		for u in self.units:
			if u.cond != 2:
				return False
		return True
