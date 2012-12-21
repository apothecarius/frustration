import gtk
import gobject

import game
#import menu

#TODO
#click auf eigene einheit, selektion schon gesetzt -> neue selektion

class brett(gtk.Window):
	def __init__(self):
		super(brett, self).__init__()
		self.connect("destroy", gtk.main_quit)
		self.set_title("Frustration")
		self.set_resizable(False)
		self.big_gui = True
		self.chessmod = False
		self.animation_freq = 75
		self.note = gtk.Label("")
		self.note.set_justify(gtk.JUSTIFY_CENTER)
		if not self.chessmod:
			self.dice = gtk.Image()
			self.dice_button = gtk.Button()
			self.dice_button.set_image(self.dice)
			self.dice_button.connect("clicked", game.throw_the_dice)
		else:
			self.dice = [gtk.Image()]
			for i in range(1,7):
				self.dice.append(gtk.Image())
			self.dice_button = []
			for i in range(0,6):
				self.dice_button.append(gtk.Button())
				self.dice_button[i].set_image(self.dice[i+1])
				self.dice_button[i].connect("clicked", game.throw_the_dice)
			self.dice_button_frame = gtk.Table(3, 2, True)
			self.dice_button_frame.attach(self.dice_button[0], 0,1,0,1)
			self.dice_button_frame.attach(self.dice_button[1], 1,2,0,1)
			self.dice_button_frame.attach(self.dice_button[2], 0,1,1,2)
			self.dice_button_frame.attach(self.dice_button[3], 1,2,1,2)
			self.dice_button_frame.attach(self.dice_button[4], 0,1,2,3)
			self.dice_button_frame.attach(self.dice_button[5], 1,2,2,3)
		self.next = gtk.Button("Runde beenden", None, False)
		self.next.connect("clicked",game.next_pl)
		self.next.set_sensitive(False)
		
		self.table = gtk.Table(4,2,False)#includes self.tab, dice,nextpl,tools and note
		self.tab = gtk.Table(11,11,True)#playingfield
		
		#boxes:
		#[0]:home
		#[1]:field
		#[2]:safe
		self.buttons = [[gtk.Button()],[gtk.Button()],[gtk.Button()]]
		self.images = [[gtk.Image()],[gtk.Image()],[gtk.Image()]]
		self.buttons[0][0].set_image(self.images[0][0])
		self.buttons[0][0].connect("clicked",self.click, 0,0)
		self.buttons[1][0].set_image(self.images[1][0])
		self.buttons[1][0].connect("clicked",self.click, 1,0)
		self.buttons[2][0].set_image(self.images[2][0])
		self.buttons[2][0].connect("clicked",self.click, 2,0)
		for i in range(1, 16):
			self.buttons[0].append(gtk.Button())#homes
			self.images[0].append(gtk.Image())
			self.buttons[0][i].set_image(self.images[0][i])
			self.buttons[0][i].connect("clicked",self.click, 0,i)

			self.buttons[2].append(gtk.Button())#safes
			self.images[2].append(gtk.Image())
			self.buttons[2][i].set_image(self.images[2][i])
			self.buttons[2][i].connect("clicked",self.click, 2,i)
			
		for i in range(1,40):
			self.buttons[1].append(gtk.Button())#field
			self.images[1].append(gtk.Image())
			self.buttons[1][i].set_image(self.images[1][i])
			self.buttons[1][i].connect("clicked",self.click, 1,i)

		#attach boxes to tableslots
		self.tab.attach(self.buttons[0][0],8,9,1,2)#spawns of player red
		self.tab.attach(self.buttons[0][1],9,10,1,2)
		self.tab.attach(self.buttons[0][2],8,9,2,3)
		self.tab.attach(self.buttons[0][3],9,10,2,3)
		self.tab.attach(self.buttons[0][4],8,9,8,9)#spawns of player blue
		self.tab.attach(self.buttons[0][5],9,10,8,9)
		self.tab.attach(self.buttons[0][6],8,9,9,10)
		self.tab.attach(self.buttons[0][7],9,10,9,10)
		self.tab.attach(self.buttons[0][8],1,2,8,9)#spawns of player yellow
		self.tab.attach(self.buttons[0][9],2,3,8,9)
		self.tab.attach(self.buttons[0][10],1,2,9,10)
		self.tab.attach(self.buttons[0][11],2,3,9,10)
		self.tab.attach(self.buttons[0][12],1,2,1,2)#spawns of player green
		self.tab.attach(self.buttons[0][13],2,3,1,2)
		self.tab.attach(self.buttons[0][14],1,2,2,3)
		self.tab.attach(self.buttons[0][15],2,3,2,3)
		#fields
		self.tab.attach(self.buttons[1][0],6,7,0,1)#spawn of red
		self.tab.attach(self.buttons[1][1],6,7,1,2)
		self.tab.attach(self.buttons[1][2],6,7,2,3)
		self.tab.attach(self.buttons[1][3],6,7,3,4)
		self.tab.attach(self.buttons[1][4],6,7,4,5)#jump
		self.tab.attach(self.buttons[1][5],7,8,4,5)
		self.tab.attach(self.buttons[1][6],8,9,4,5)
		self.tab.attach(self.buttons[1][7],9,10,4,5)
		self.tab.attach(self.buttons[1][8],10,11,4,5)
		self.tab.attach(self.buttons[1][9],10,11,5,6)
		self.tab.attach(self.buttons[1][10],10,11,6,7)#spawn of blue
		self.tab.attach(self.buttons[1][11],9,10,6,7)
		self.tab.attach(self.buttons[1][12],8,9,6,7)
		self.tab.attach(self.buttons[1][13],7,8,6,7)
		self.tab.attach(self.buttons[1][14],6,7,6,7)#jump
		self.tab.attach(self.buttons[1][15],6,7,7,8)
		self.tab.attach(self.buttons[1][16],6,7,8,9)
		self.tab.attach(self.buttons[1][17],6,7,9,10)
		self.tab.attach(self.buttons[1][18],6,7,10,11)
		self.tab.attach(self.buttons[1][19],5,6,10,11)
		self.tab.attach(self.buttons[1][20],4,5,10,11)#spawn of yellow
		self.tab.attach(self.buttons[1][21],4,5,9,10)
		self.tab.attach(self.buttons[1][22],4,5,8,9)
		self.tab.attach(self.buttons[1][23],4,5,7,8)
		self.tab.attach(self.buttons[1][24],4,5,6,7)#jump
		self.tab.attach(self.buttons[1][25],3,4,6,7)
		self.tab.attach(self.buttons[1][26],2,3,6,7)
		self.tab.attach(self.buttons[1][27],1,2,6,7)
		self.tab.attach(self.buttons[1][28],0,1,6,7)
		self.tab.attach(self.buttons[1][29],0,1,5,6)
		self.tab.attach(self.buttons[1][30],0,1,4,5)#spawn of green
		self.tab.attach(self.buttons[1][31],1,2,4,5)
		self.tab.attach(self.buttons[1][32],2,3,4,5)
		self.tab.attach(self.buttons[1][33],3,4,4,5)
		self.tab.attach(self.buttons[1][34],4,5,4,5)#jump
		self.tab.attach(self.buttons[1][35],4,5,3,4)
		self.tab.attach(self.buttons[1][36],4,5,2,3)
		self.tab.attach(self.buttons[1][37],4,5,1,2)
		self.tab.attach(self.buttons[1][38],4,5,0,1)
		self.tab.attach(self.buttons[1][39],5,6,0,1)
		#safes
		self.tab.attach(self.buttons[2][0],5,6,1,2)#red
		self.tab.attach(self.buttons[2][1],5,6,2,3)
		self.tab.attach(self.buttons[2][2],5,6,3,4)
		self.tab.attach(self.buttons[2][3],5,6,4,5)
		self.tab.attach(self.buttons[2][4],9,10,5,6)#blue
		self.tab.attach(self.buttons[2][5],8,9,5,6)
		self.tab.attach(self.buttons[2][6],7,8,5,6)
		self.tab.attach(self.buttons[2][7],6,7,5,6)
		self.tab.attach(self.buttons[2][8],5,6,9,10)#yellow
		self.tab.attach(self.buttons[2][9],5,6,8,9)
		self.tab.attach(self.buttons[2][10],5,6,7,8)
		self.tab.attach(self.buttons[2][11],5,6,6,7)
		self.tab.attach(self.buttons[2][12],1,2,5,6)#green
		self.tab.attach(self.buttons[2][13],2,3,5,6)
		self.tab.attach(self.buttons[2][14],3,4,5,6)
		self.tab.attach(self.buttons[2][15],4,5,5,6)
		
		self.tools = gtk.Toolbar()
		self.tools.set_show_arrow(True)

		#buttons
		self.tool_newgame = gtk.ToolButton(label="New Game")
		self.tool_newgame_pic = gtk.Image()
		self.tool_newgame.set_icon_widget(self.tool_newgame_pic)

		self.tool_save = gtk.ToolButton(label="Save Game")
		self.tool_save_pic = gtk.Image()
		self.tool_save.set_icon_widget(self.tool_save_pic)

		self.tool_load = gtk.ToolButton(label="Load Game")
		self.tool_load_pic = gtk.Image()
		self.tool_load.set_icon_widget(self.tool_load_pic)

		self.tool_config = gtk.ToolButton(label="Options")
		self.tool_config_pic = gtk.Image()
		self.tool_config.set_icon_widget(self.tool_config_pic)

		self.tool_help = gtk.ToolButton(label="Help")
		self.tool_help_pic = gtk.Image()
		self.tool_help.set_icon_widget(self.tool_help_pic)

		self.tool_quit = gtk.ToolButton(label="Quit Game")
		self.tool_quit_pic = gtk.Image()
		self.tool_quit.set_icon_widget(self.tool_quit_pic)

		self.set_imgs()


#TODO:connect toolbarfunctions
		self.tools.insert(self.tool_newgame, 0)
		#self.tool_newgame.connect("clicked", new_game_pressed)
		self.tools.insert(self.tool_save, 1)
		self.tool_save.connect("clicked", save_game)
		self.tools.insert(self.tool_load, 2)
		self.tool_load.connect("clicked", load_game)
		self.tools.insert(self.tool_config, 3)
		#self.tool_config.connect("clicked", configure)
		self.tools.insert(self.tool_help, 4)
		#self.tool_help.connect("clicked", show_help)
		self.tools.insert(self.tool_quit,5)
		self.tool_quit.connect("clicked", quit)

		self.table.attach(self.tools, 0,2,0,1)
		self.table.attach(self.tab, 1,2,1,4)
		self.table.attach(self.note, 0,1,1,2)

		if self.chessmod:
			self.table.attach(self.dice_button_frame,0,1,2,3)
		else:
			self.table.attach(self.dice_button,0,1,2,3)

		self.table.attach(self.next,0,1,3,4)

		self.add(self.table)

		#self.show_all()
		#self.set_position(gtk.WIN_POS_CENTER)
		return


	def set_imgs(self):
		#felder
		self.pixes = [[0],[0],[0],[0],[0]]#import image files
		for i in range(0,4):
			for j in range(0,5):
				self.pixes[j].append(0)
		cola = {0:"re_",1:"bl_",2:"ye_",3:"gr_",4:"nu_"} #ring
		colb = {0:"re.svg",1:"bl.svg",2:"ye.svg",3:"gr.svg",4:"nu.svg"} #inner
		#0:rot
		#1:blau
		#2:gelb
		#3:gruen
		#4:leer
		for i in range(0,5):
			for j in range(0,5):
				if self.big_gui:
					self.pixes[i][j] = gtk.gdk.pixbuf_new_from_file("pic/"+cola[i]+colb[j])
				else:
					self.pixes[i][j] = gtk.gdk.pixbuf_new_from_file("pic/"+cola[i]+colb[j]).scale_simple(25,25, gtk.gdk.INTERP_BILINEAR)
		del cola
		del colb

		#tools
		self.tool_pics = [gtk.gdk.pixbuf_new_from_file("pic/new.svg")
				,gtk.gdk.pixbuf_new_from_file("pic/save.svg")
				,gtk.gdk.pixbuf_new_from_file("pic/load.svg")
				,gtk.gdk.pixbuf_new_from_file("pic/config.svg")
				,gtk.gdk.pixbuf_new_from_file("pic/help.svg")
				,gtk.gdk.pixbuf_new_from_file("pic/close.svg")
				]
		if self.big_gui:
			for i in range(0,6):
				self.tool_pics[i] = self.tool_pics[i].scale_simple(50,50, gtk.gdk.INTERP_BILINEAR)
		else:
			for i in range(0,6):
				self.tool_pics[i] = self.tool_pics[i].scale_simple(25,25, gtk.gdk.INTERP_BILINEAR)

		self.tool_newgame_pic.set_from_pixbuf(self.tool_pics[0])
		self.tool_save_pic.set_from_pixbuf(self.tool_pics[1])
		self.tool_load_pic.set_from_pixbuf(self.tool_pics[2])
		self.tool_config_pic.set_from_pixbuf(self.tool_pics[3])
		self.tool_help_pic.set_from_pixbuf(self.tool_pics[4])
		self.tool_quit_pic.set_from_pixbuf(self.tool_pics[5])


		#dice
		self.dices = [gtk.gdk.pixbuf_new_from_file("pic/empty_throw.svg")]
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/one.svg"))
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/two.svg"))
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/three.svg"))
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/four.svg"))
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/five.svg"))
		self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/six.svg"))
		if not self.chessmod:
			if not self.big_gui:
				for i in range(0, 7):
					self.dices[i] = self.dices[i].scale_simple(125,125, gtk.gdk.INTERP_BILINEAR)
			self.dice.set_from_pixbuf(self.dices[0])
		else:
				for i in range(0,7):
					d = self.dices[i]
					if not self.big_gui:
						self.dices[i] = d.scale_simple(55, 55, gtk.gdk.INTERP_BILINEAR)
					else:
						self.dices[i] = d.scale_simple(125,125,gtk.gdk.INTERP_BILINEAR)

					self.dice[i].set_from_pixbuf(self.dices[i])
		return


	def set_chessmod(self,yes):
		if yes:#activate chessmod
			if self.chessmod:
				return
			self.chessmod = True
			game.rules.chessmod = True
			self.dice = [gtk.Image()]
			for i in range(1,7):
				self.dice.append(gtk.Image())
			self.table.remove(self.dice_button)
			self.dice_button = []
			for i in range(0,6):
				self.dice_button.append(gtk.Button())
				self.dice_button[-1].set_image(self.dice[i+1])
				self.dice_button[-1].connect("clicked", game.throw_the_dice)
			self.dice_button_frame = gtk.Table(3, 2, True)
			self.dice_button_frame.attach(self.dice_button[0], 0,1,0,1)
			self.dice_button_frame.attach(self.dice_button[1], 1,2,0,1)
			self.dice_button_frame.attach(self.dice_button[2], 0,1,1,2)
			self.dice_button_frame.attach(self.dice_button[3], 1,2,1,2)
			self.dice_button_frame.attach(self.dice_button[4], 0,1,2,3)
			self.dice_button_frame.attach(self.dice_button[5], 1,2,2,3)

			for i in range(0,7):
				d = self.dices[i]
				if not self.big_gui:
					self.dices[i] = d.scale_simple(55, 55, gtk.gdk.INTERP_BILINEAR)
				else:
					self.dices[i] = d.scale_simple(125,125,gtk.gdk.INTERP_BILINEAR)
				self.dice[i].set_from_pixbuf(self.dices[i])
			self.table.attach(self.dice_button_frame,0,1,2,3)

		else:#disable chessmod
			if not self.chessmod:
				return
			self.chessmod = False
			game.rules.chessmod = False
			self.dice = gtk.Image()
			self.dice_button = gtk.Button()
			self.dice_button.set_image(self.dice)
			self.dice_button.connect("clicked", game.throw_the_dice)

			#reload images
			self.dices = [gtk.gdk.pixbuf_new_from_file("pic/empty_throw.svg")]
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/one.svg"))
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/two.svg"))
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/three.svg"))
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/four.svg"))
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/five.svg"))
			self.dices.append(gtk.gdk.pixbuf_new_from_file("pic/six.svg"))

			if not self.big_gui:
				for i in range(0, 7):
					self.dices[i] = self.dices[i].scale_simple(125,125, gtk.gdk.INTERP_BILINEAR)
			self.dice.set_from_pixbuf(self.dices[0])
			self.table.remove(self.dice_button_frame)
			self.table.attach(self.dice_button,0,1,2,3)

	def show_all(self, yes):
		if yes:
			super(brett,self).show_all()
		else:
			super(brett,self).hide()
		memo.board_visible = yes

	
	def set_dice_sens(self, show, pl): #dice(s) clickable or not?
		#pl is either the current player or whether the number on the dice is to be shown
		if self.chessmod:
			if show:
				#allow all dices that make sense
				for d in range(0,6):
					self.dice_button[d].set_sensitive(False)
					for u in range(0,4):
						if pl.units[u].can_do(d+1):
							
							self.dice_button[d].set_sensitive(True)
							break

			else:
				for i in range(0,6):
					self.dice_button[i].set_sensitive(False)
				
		else:
			self.dice_button.set_sensitive(show)
			if not pl:
				self.dice.set_from_pixbuf(self.dices[0])
				
		return

	def show_dice_throw(self, x):#zeigt an was der wuerfel gekriegt hat(1-6), oder leert ihn (0)
		if not self.chessmod:
			self.dice.set_from_pixbuf(self.dices[x])
		else:
			if x == 0:
				for i in range(0,6):
					self.dice_button[i].set_image(self.dice[i+1])
			else:
				#only show clicked button and disable all buttons
				for i in range(0,6):
					if i+1 != x:
						self.dice_button[i].set_image(self.dice[0])

	
	def pre_render(self, players): #players: contains all player objects in the game
		self.set_imgs()
	#first render the empty field
		#normal fields
		for x in range(0,40):
			if x in [0,10,20,30]:
				continue
			self.images[1][x].set_from_pixbuf(self.pixes[4][4])

		#safes, homes and spawns
		for x in range(0,4):#players
			self.images[1][x*10].set_from_pixbuf(self.pixes[x][4])
			for y in range(0,4):#fieldindex
				self.images[0][x*4 + y].set_from_pixbuf(self.pixes[x][4])
				self.images[2][x*4 + y].set_from_pixbuf(self.pixes[x][4])
				
	#then render the units on it
		for p in players:
			if type(p) == int:
				continue
			for u in p.units:
				cond = u.cond 
				pos = u.pos
				# rc: ringcolor
				if cond in [0,2]: #unit is dead or safe
					rc = p.nr
				elif pos in [0,10,20,30]: #unit is on a spawn
					rc = pos % 10
				else: #unit is on a normal field
					rc = 0
				self.images[cond][pos].set_from_pixbuf(self.pixes[rc][p.nr])
		return


	def render(self, pos,zus,col):#returns True if worked, else False
		if (col not in range(0,6) #inexistent color
			or (pos not in range(0,40)) #beyond any measurement
			or (zus in [0,2] and pos not in range(0,16)) #in safe/home but beyond safe/home
			or (zus in [0,2] and col not in [4, pos/4])): #/in safe/home but wrong color(-> A SPY)
			return False
		if zus != 1:#spawns or safes must have same color (except empty)
			if col == 4:#empty
				if pos in range(0,4):#red
					self.images[zus][pos].set_from_pixbuf(self.pixes[0][4])
					return True
				if pos in range(4,8):#blue
					self.images[zus][pos].set_from_pixbuf(self.pixes[1][4])
					return True
				if pos in range(8,12):#yellow
					self.images[zus][pos].set_from_pixbuf(self.pixes[2][4])
					return True
				if pos in range(12,16):#green
					self.images[zus][pos].set_from_pixbuf(self.pixes[3][4])
					return True
			else:#fill
				self.images[zus][pos].set_from_pixbuf(self.pixes[col][col])
				return True

		else:#field
			if pos == 0:#red spawnpoint
				self.images[1][0].set_from_pixbuf(self.pixes[0][col])
				return True
			elif pos == 10:#blue spawnpoint
				self.images[1][10].set_from_pixbuf(self.pixes[1][col])
				return True
			elif pos == 20:#yellow spawnpoint
				self.images[1][20].set_from_pixbuf(self.pixes[2][col])
				return True
			elif pos == 30:#green spawnpoint
				self.images[1][30].set_from_pixbuf(self.pixes[3][col])
				return True
			else:#normal field
				self.images[1][pos].set_from_pixbuf(self.pixes[4][col])
				return True
		return False

	def get_ring_coords(self,pos,cond):#returns 0,4 on 2,1
		if (cond in [0,2] and pos in range(0,4)) or (pos == 0 and cond == 1):#red ring
			return [0,4]
		elif (cond in [0,2] and pos in range(4,8)) or (pos == 10 and cond == 1):#blue ring
			return [1,4]
		elif( cond in [0,2] and pos in range(8,12)) or (pos == 20 and cond == 1):#yello ring
			return [2,4]
		elif (cond in [0,2] and pos in range(12,16)) or (pos == 30 and cond == 1):#green ring
			return [3,4]
		else:#black ring
			return [4,4]



	def moving_render(self,unit,player,doing):#TODO gets a black ring for spawnpoints, instead of colored ring 
		memo.wait = True
		self.show_dice_throw(0)
		places = [[unit.pos,unit.cond]]
		if doing[0] == 1:
			for i in range(0,doing[1]):
				if places[-1][1] == 1 and places[-1][0] == player.safe_entrance:#at entrance
					places.append([player.nr*4,2])
				else:
					p = [(places[-1][0]+1)%40, places[-1][1]]
					places.append(p)
		elif doing[0] == 2:
			for i in range(0,doing[1]):
				places.append( [(places[-1][0] -1)%40 , 1] )

		#get first ring
		if places[0][0] == 0:#red
			r = 0
		elif places[0][0] == 10:#blue
			r = 1
		elif places[0][0] == 20:#yellow
			r = 2
		elif places[0][0] == 30:#green
			r = 3
		else: #black
			r = 4
		if places[0][1] == 2:#in safe so get the playercolor
			r = player.nr
		gobject.timeout_add(self.animation_freq, self.moving_render_loop, unit, player, doing, places, self.pixes[r][4])
		#fyi self.pixes[ring][filling]
		#fyi self.images[cond][pos]
		#fyi places[i][0:pos,1:cond]
			#places[start...end]
		return

	def moving_render_loop(self, unit,player,doing,places,colbu):
		#TODO use render funktion
		#BUG bug : rings are black 
		#fill place with colbu
		#render(self, pos,zus,col)
		prefi = places[0]#previous field
		nefi = places[1]#next field
		self.images[prefi[1]][prefi[0]].set_from_pixbuf(colbu)
		#backup next_place if there will be another call
		if len(places) > 2:
			colbux = self.images[nefi[1]] [nefi[0]].get_pixbuf()
		#fill next_place with unit
		i = self.get_ring_coords(nefi[0],nefi[1])#mistake
		i = i[0]
		# bug somewhere around here
		# player red spawned, went 2 ahead, field 2 got red ring
		img = self.pixes[i][unit.player.nr]#[ringcolor][playercolor]
		self.images[nefi[1]][nefi[0]].set_from_pixbuf(img)
		#delete entry in places
		if len(places) == 2:#animation done -> return to after_actio
			memo.wait = False
			game.after_actio(doing,unit,player)
		else:#remaining anim-steps ->set new timer
			gobject.timeout_add(	self.animation_freq,
						self.moving_render_loop,
						unit,player,doing, places[1:] 
						,colbux)

		#kill this timer
		return False

	def click(self,button,cond, pos):
		if memo.wait:
			return

		if game.memo.selection != 4:#unit selected?
			#TODO einheiten selektion ueberschreiben muss angepasst werden
			u = game.memo.selection
			doing = [0,0]
			pf = u.move(game.memo.dice,True)
			pb = u.move(game.memo.dice,False)
			#valid order?
			#doing[0] =
			if cond == u.cond and pos == u.pos:#clicked himself
				if game.memo.may_spawn:#may spawn
					doing[0] = 3
					doing.pop(-1)
				elif game.memo.suicide:#has_to_die
					doing[0] = 4
					doing.pop(-1)
				else:#fail
					game.select_unit(4)
					self.note.set_text("\nInvalid Command\n")
					return
				result = game.actio(doing, game.memo.act_pl,u)
				game.select_unit(4)
				return
			#valid order?
			#move forward
			elif pf != False and pos == pf[0] and cond == pf[1]:
				doing[0] = 1
			#move backward
			elif pb != False and pos == pb[0] and cond == pb[1]:
				doing[0] = 2 
			#move forth over corner
			elif pf != False and pf[0] in [4,14,24,34] and pf[0]%20 == pos%20:#expecting jump over corner
				doing[0] = 1
			#move back over corner
			elif pf != False and pb[0] in [4,14,24,34] and pb[0]%20 == pos%20:#expecting jump over corner
				doing[0] = 2
			#version 2.5
			elif (game.memo.may_spawn and 
			pos == game.memo.act_pl.nr*10 and cond == 1 and
			u.cond == 0):#spawn by spawnpointclick
				doing[0] = 3
				doing.pop(-1)
				result = game.actio(doing, game.memo.act_pl,u)
				game.select_unit(4)
				return
			elif (game.memo.suicide and cond == 0 and
				u.cond != 0):#suicide by graveclick
				doing[0] = 4
				doing.pop(-1)
				result = game.actio(doing, game.memo.act_pl,u)
				game.select_unit(4)
				return

			else:#no valid order
				self.note.set_text("\nInvalid Command\n")
				game.select_unit(4)
				return
		else:
			#select
			game.select_unit(game.get_unit_bypos(pos,cond))
			return

		doing[1] = game.memo.dice
		if doing[1] == 0:
			self.note.set_text(game.memo.act_pl.name+"\n("+game.memo.act_pl.get_color()+")Please throw \n the dice first!")

		game.actio(doing, game.memo.act_pl,game.memo.selection)
		game.memo.selection = 4
			


class Game_Over_Window(gtk.Window):
	def __init__(self):
		super(Game_Over_Window, self).__init__()
		self.table = gtk.Table()
		self.head = gtk.Label("Game Over")
		self.content = gtk.Label()
		self.table
		#TODO finish



#this is pressed by the surface
def new_game_pressed(junk):
	surface.set_visi(False)
	game.newgame()()
	surface.pre_render()
	start_window.show()
	return

def save_game(junk):
	#show a window with a textbar for the title
	savwin = gtk.Window()
	savwin.set_title("Save as...")
	savwin.text = gtk.Entry(max=16)
	savwin.text.set_text("LastGame")
	savwin.ok = gtk.Button()
	savwin.ok.set_label("Ok")
	savwin.ok.connect("clicked", save_game_ok,savwin)
	savwin.tab = gtk.Table(rows=1, columns=2)
	savwin.tab.attach(savwin.text, 0,1,0,1)
	savwin.tab.attach(savwin.ok, 1,2,0,1)
	savwin.add(savwin.tab)
	savwin.show_all()

def save_game_ok(junk, savwin):
	text = savwin.text.get_text()
	if text == "":
		return
	else:
		save(text)
		savwin.hide()
		return
	
def load_game(junk):
	loadwin = gtk.Window()
	loadwin.set_title("Load...")
	loadwin.text = gtk.Entry(max=16)
	loadwin.text.set_text("Last Game")
	loadwin.ok = gtk.Button()
	loadwin.ok.set_label("Ok")
	loadwin.ok.connect("clicked", load_game_ok,loadwin)
	loadwin.tab = gtk.Table(rows=1, columns=2)
	loadwin.tab.attach(loadwin.text, 0,1,0,1)
	loadwin.tab.attach(loadwin.ok, 1,2,0,1)
	loadwin.add(loadwin.tab)
	loadwin.show_all()

def load_game_ok(junk,loadwin):
	text = loadwin.text.get_text()
	if text == "":
		return
	else:
		load(text)
		loadwin.hide()
		start_window.loaded = True
		return

def configure(junk):
	return
def show_help(junk):
	return


def save(filename):
	code = ""
	playercode = 0#code for which player is in the game (binary)
	if game.players[0]:
		playercode += 1
	if game.players[1]:
		playercode += 2
	if game.players[2]:
		playercode += 4
	if game.players[3]:
		playercode += 8
	if playercode < 10:
		code += "0"
	code += (str(playercode))

	for pl in game.players:#players
		if not pl:
			code += "            " #12 digits per player doesnt save playername or controls
			continue
		#else: #save
		for u in pl.units: #positions and states of his units
			if u.pos < 10:
				code += "0"#position must have two digits
			code += (str(u.pos))
			code += (str(u.cond))

	#general options
	if game.rules.jumps:
		code += "1"
	else:
		code += "0"
	if game.rules.chessmod:
		code += "1"
	else:
		code += "0"

	savegame = open("./saves/"+filename , "w")
	savegame.write(code)
	savegame.close()
	return



def load(filename):
	sav = open("./saves/"+filename, "r")
	data = sav.read()
	sav.close()
	#todo: set game after data
	players = [	data[2:14],
			data[14:26],
			data[26:38],
			data[38:50]]
	
	for i in range(0,4):
		if players[i][0] == " ":#player empty
			game.players[i] = 0
		else:
			units = [players[i][0:3],
				players[i][3:6],
				players[i][6:9],
				players[i][9:12]]
			for j in range(0,4):
				game.players[i].units[j].pos = int(units[j][0:2])
				game.players[i].units[j].cond = int(units[j][2])

	game.rules.jumps = data[50] == "1"
	game.rules.chessmod = data[51] == "1"

	#after setting data, open a gamestartwindow
	#and set the combo_box(who controls what) according to data[0:1]
	players = int(data[0:1])
	if players >= 8:#player 4 active
		start_window.sel_but[3].set_active(0)
		players -= 8
	else:
		start_window.sel_but[3].set_active(1)
	if players >= 4:#player 3 active
		start_window.sel_but[2].set_active(0)
		players -= 4
	else:
		start_window.sel_but[2].set_active(1)
	if players >= 2:#player 2 active
		start_window.sel_but[1].set_active(0)
		players -= 2
	else:
		start_window.sel_but[1].set_active(1)
	if players == 1:#player 1 active
		start_window.sel_but[0].set_active(0)
	else:
		start_window.sel_but[0].set_active(1)

	start_window.show()
	return

#fyi self.images[cond][pos]
def jump_render(pos):
	if pos not in [4,14,24,34]:
		return False
	
	c = board.images[1][(pos+20)%40].get_pixbuf()
	board.images[1][pos].set_from_pixbuf(c)
	board.render((pos+20)%40,1,4)


def allow_nextpl(yes):
	board.next.set_sensitive(yes)
def render(pos,zus,col):
	board.render(pos,zus,col)
def moving_render(unit,player,doing):
	board.moving_render(unit,player,doing)
def set_msg(txt):
	board.note.set_text(txt)
def show_dice_throw(x):
	board.show_dice_throw(x)
def set_dice_sens(yes,pl):
	board.set_dice_sens(yes,pl)
def identify_roll(but):
	if type(but) == int:
		return but
	if not board.chessmod:#only necessary when chessmod is on
		return False
	for i in range(0,6):
		if but == board.dice_button[i]:
				return i+1
def kill(unit):#shows the unit in its home
	board.render(unit.player.nr*4+unit.nr, 0, unit.player.nr)
def set_chessmod(yes):
	board.set_chessmod(yes)
def set_size(big):
	board.big_gui = big
	board.set_imgs()
def set_visi(yes):
	board.show_all(yes)
def get_visi():
	return memo.board_visible
def pre_render(p):
	board.pre_render(p)

class memory:
	def __init__(self):
		self.selection = 4#deprecated
		self.wait = False
		self.board_visible = False

memo = memory()
game_over_win = Game_Over_Window()
