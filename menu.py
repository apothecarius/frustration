#!/usr/bin/python
#author:Jonas Bollgruen
#mail:apothecarius@web.de
#version: 2.3

#TODO netzwerknachrichten ueber optionsaenderungen nutzen
#BUG 
#frisch gespawnt, mit 6 weglaufen, nach hinten bedroht, nach vorn gelaufen, konnte nicht geopfert werden

import gtk
import gobject
gobject.threads_init()

import surface
import game
import plun
import network
import language




class start_win(gtk.Window):
	def __init__(self):
		super(start_win,self).__init__()
		self.destro_a = self.connect("destroy", gtk.main_quit)
		#self.resize(250,250)
		self.set_resizable(False)
		self.set_position(gtk.WIN_POS_CENTER)
		self.pl = [1,0,1,0] #list for what player is controlled by what(bot,user,LAN)
		self.grid = gtk.Table(5,4,False)
		self.loaded = False#required for start_game not to overwrite the players
		self.tex = [gtk.Label("Red")]
		self.tex.append(gtk.Label("Blue"))
		self.tex.append(gtk.Label("Yellow"))
		self.tex.append(gtk.Label("Green"))

		self.sel_but = [gtk.combo_box_new_text(),gtk.combo_box_new_text(),gtk.combo_box_new_text(),gtk.combo_box_new_text()]
		for i in range(0,4):#selectors or control
			self.sel_but[i].append_text("Server")
			self.sel_but[i].append_text("Closed")
			#self.sel_but[i].append_text("Computer")
			self.sel_but[i].append_text("Network")
		self.sel_but[0].set_active(0)
		self.sel_but[1].set_active(1)
		self.sel_but[2].set_active(0)
		self.sel_but[3].set_active(1)
		for i in range(0,4):#connect the playercontrolswitches to the function
			self.sel_but[i].connect("changed", self.switch_player)
		self.names = []
		for i in range(0,4):#entries for name
			self.names.append(gtk.Entry(max = 24))
			self.names[-1].set_text("Player "+str(i+1))
			self.names[-1].connect("changed",self.name_change,i)

		self.joinwindow = joinWindow()
		self.optwindow = optionwindow()

		self.opt_but = gtk.Button("Options",None,False)
		self.opt_but.connect("clicked",self.optwindow.showwrap)
		self.but = gtk.Button("Start Game", None, False)
		self.but.connect("clicked", game_start, self.pl)
		self.join = gtk.Button("Join Game",None, False)
		self.join.connect("clicked",self.joinwindow.show_all_wrap)
		self.leave = gtk.Button("Exit",None,False)
		self.destro_b = self.leave.connect("clicked", self.quit_startgame)
		#self.hostbut = gtk.ToggleButton(label="Host")#not necessary since opening player to network activates NW too
		#self.hostbut.connect("toggled",self.switch_network)

		for i in range(0,4):
			self.grid.attach(self.tex[i],0,1,i,i+1)
			self.grid.attach(self.sel_but[i],1,2,i,i+1)
			self.grid.attach(self.names[i],2,3,i,i+1)

		self.grid.attach(self.opt_but,2,3,4,5)
		#self.grid.attach(self.hostbut,0,1,4,5)

		self.grid.attach(self.but,0,1,5,6)
		self.grid.attach(self.join,1,2,5,6)#todo: complete network
		self.grid.attach(self.leave,2,3,5,6)
		self.add(self.grid)
		self.show_all()
		gobject.timeout_add(int(1000*network.poll_intervall), self.networkPoll)

	def networkPoll(self):
		data = network.getInput()
		for e in data:
			a = e[0]#adress
			e = e[1]#message
			#print e
			if e[0] == "g":#gamestart
				game_start("lan",self.pl)
			elif e[0] == "d":
				if network.hosting:
					network.send(e,a,True)
				game.throw_the_dice("butter",inp=int(e[1]))
			elif e[0] == "z":
				if network.hosting:
					print("MUHAHAHA")#this is called repeatedly
					network.send(e,a,True)
				game.actio(int(e[2]),None,int(e[1]),fr=True)#actio(doing,player,unit)
			elif e[0] == "o":#optionsaenderung #TODO might not work, hasnt been tested
				if e[1] == "c":#change chessmod
					self.optwindow.chessmod.set_active(int(e[1]))
					#self.optwindow.chessmod.toggled()
				elif e[1] == "j":#change jumps
					self.optwindow.check_jumps.set_active(int(e[1]))#TODO geht nicht, und nur host darf das aendern
				else:
					continue
			elif e[0] == "s":#spieleraenderung
				try:
					num = int(e[1])#which player
				except:
					continue
				if e[2] == "n":#name
					self.names[num].set_text(e[3:])
				elif e[2] == "c":#controlled how
					t = {"h":0,"n":3,"b":2,"c":1}[e[3]]
					self.sel_but[num].set_active(t)
				else:
					continue
			elif e[0] == "e":#end of turn
				if network.hosting:#send it to everyone else
					network.send("e",adress=a,n=True)
				game.next_pl("nw")

			else:#nix
				continue
		return 1

	def name_change(self,but,i):
		#TODO prohibit empty name #= ""
		if but.get_sensitive():
			network.gamedetails.pn[i] = but.get_text()
		

	def quit_startgame(self, but):#might have to do some stuff for network
		gtk.main_quit()
		exit()

	#def switch_network(self,but):
	#	if self.hostbut.get_active():
	#		network.enable()
	#	else:
	#		network.disable()
	#	return


	def switch_player(self, which):#reacts on changing the entry of a player
		if not network.hosting:
			return
		if which == self.sel_but[0]:
			order = 0
		elif which == self.sel_but[1]:
			order = 1
		elif which == self.sel_but[2]:
			order = 2
		elif which == self.sel_but[3]:
			order = 3
		

		if "Closed" == which.get_active_text():
			self.pl[order] = 0
			tag = "c"
			self.names[order].set_sensitive(True)
		elif "Server" == which.get_active_text():
			self.pl[order] = 1
			tag = "h"
			self.names[order].set_sensitive(True)

		elif "Computer" == which.get_active_text():
			self.pl[order] = 2
			tag = "b"
			self.names[order].set_sensitive(True)
		elif "Network" == which.get_active_text():
			self.pl[order] = 4
			self.names[order].set_sensitive(False)
			self.names[order].set_text("")
				
			tag = "n"
			if not network.enabled and self.but.get_sensitive():
				network.enable()
			#eig nicht noetig TO DO activate network if first
		else:#network player player was assigned
			pass



		network.gamedetails.setType(order,tag)###bug ist hier
		if network.enabled:
			f = True
			for but in self.sel_but:#suche nach offenen netzwerkslots
				if but.get_active_text() == "Network":
					f = False
			#keiner mehr offen also netzwerk abschalten
			if f:
				network.enabled = False
		#FALLS HIER NOCH WAS KOMMT DIE OBIGE STRUKTUR ERSETZEN
		return

	def leavegame(self,butt):
		start_window.but.set_sensitive(True)
		start_window.join.set_label("Join Game") #umbenennen
		start_window.join.connect("clicked",self.joinwindow.join_game)
		start_window.opt_but.set_sensitive(True)

		
	def resetMenu(self):
		butt.set_label("Join Game")
		self.but.set_sensitive(True)
		
		for i in range(4):
			self.names[i].set_text("Player "+str(i+1))
		


class optionwindow(gtk.Window):#TODO closing destroys the window
	def __init__(self):
		super(optionwindow,self).__init__()
		self.opt_win_grid = gtk.Table()
		self.add(self.opt_win_grid)
		
		self.check_jumps = gtk.CheckButton(label ="Jumping")
		self.check_jumps.set_active(jumbs)
		self.check_jumps.connect("toggled",self.tog_jump)

		self.small_gui = gtk.CheckButton(label = "Small GUI")
		self.small_gui.set_active(not bigui)
		self.small_gui.connect("toggled", self.toggle_guisize)

		self.chessmod = gtk.CheckButton(label="Chessmod")
		self.chessmod.set_active(cheese)
		self.chessmod.connect("toggled", self.toggle_chessmod)

		self.opt_win_grid.attach(self.chessmod, 0,1,4,5)
		self.opt_win_grid.attach(self.small_gui, 1,2,4,5)
		self.opt_win_grid.attach(self.check_jumps, 2,3,4,5)

	def showwrap(self,a):
		self.show_all()
	def tog_jump(self,but):
		if self.check_jumps.get_active():#activated
			game.rules.jumps = True
		else:#deactivated
			game.rules.jumps = False
		return
	def toggle_guisize(self,but):
		if self.small_gui.get_active():#activated
			surface.board.big_gui = False
		else:
			surface.board.big_gui = True
		return

	def toggle_chessmod(self,but):
		if self.chessmod.get_active():#activated
			game.rules.chessmod = True
		else:#deactivated
			game.rules.chessmod = False
		surface.set_chessmod(game.rules.chessmod)
		return



class joinWindow(gtk.Window):
	def __init__(self):
		#network join window
		#currently not being used
		super(joinWindow,self).__init__()
		self.join_win_grid = gtk.Table(5,3,False)
		self.add(self.join_win_grid)
		self.con_win_name_note = gtk.Label("Name")
		self.con_win_name = gtk.Entry(max = 24)
		self.join_one = gtk.CheckButton(label = "Rot")
		self.join_two = gtk.CheckButton(label ="Blau")
		self.join_three = gtk.CheckButton(label = "Gelb")
		self.join_four = gtk.CheckButton(label ="Gruen")
		self.aipi_note = gtk.Label("IP")
		self.aipi = gtk.Entry(max = 15)
		self.but_connect = gtk.Button("Beitreten",None,False)
		self.but_connect.connect("clicked",self.join_game)
		self.join_win_grid.attach(self.con_win_name_note,0,1,0,1)
		self.join_win_grid.attach(self.con_win_name,1,3,0,1)
		self.join_win_grid.attach(self.join_one,0,2,1,2)
		self.join_win_grid.attach(self.join_two,2,3,1,2)
		self.join_win_grid.attach(self.join_three,0,2,2,3)
		self.join_win_grid.attach(self.join_four,2,3,2,3)
		self.join_win_grid.attach(self.aipi_note,0,1,3,4)
		self.join_win_grid.attach(self.aipi,1,3,3,4)
		self.join_win_grid.attach(self.but_connect,0,3,4,5)
	def show_all_wrap(self,but):
		self.show_all()
	def join_game(self,a):
		ip = self.aipi.get_text()
		name = self.con_win_name.get_text()
		if ";" in name or name == "":
			self.errormsgwin = gtk.MessageDialog(message_format="Fehlerhafter Name")
			self.errormsgwin.show_all()
			return
		players = 0
		plist = []
		if self.join_one.get_active():
			players += 1
			plist.append(0)
		if self.join_two.get_active():
			players += 2
			plist.append(1)
		if self.join_three.get_active():
			players += 4
			plist.append(2)
		if self.join_four.get_active():
			players += 8
			plist.append(3)
		self.hide()
		result = network.connect(ip,name,players)
		#1 : ip/port nicht richtig
		#2 : verlangte spieler nicht frei
		#else 
		if result == 1:
			ermsg = "Konnte keine Verbindung erstellen"
		elif result == 2:
			ermsg = "Diese Spieler sind nicht mehr verfuegbar"

		else:
			#print plist
			#passe menue an result an
			#start_window.hostbut.set_sensitive(False)
			start_window.but.set_sensitive(False)
			start_window.join.set_label("Leave Game") #umbenennen
			start_window.join.connect("clicked",start_window.leavegame)
			network.hosting = False
			#start_window.opt_but.set_sensitive(False)voruebergehend
			for i in range(4):
				typ = result[i][0]
				name = result[i][1]
				
				start_window.sel_but[i].set_sensitive(False)
				
				if typ == "h":#server
					start_window.sel_but[i].set_active(0)
					start_window.pl[i] = 1
				elif typ == "n":#network
					start_window.sel_but[i].set_active(3)
					start_window.pl[i] = 4
				elif typ == "b":#bot
					start_window.sel_but[i].set_active(2)
					start_window.pl[i] = 2
				elif typ == "c":#closed
					start_window.sel_but[i].set_active(1)
					start_window.pl[i] = 0
				
				start_window.names[i].set_sensitive(0)
				start_window.names[i].set_text(name)
				network.gamedetails.pna[0]= name
				network.gamedetails.pn[0] = name
				
			for i in plist:
				start_window.names[i].set_sensitive(1)
			print("clientmenu set")
			return

		self.errormsgwin = gtk.MessageDialog(message_format=ermsg)
		self.errormsgwin.show_all()
		return
	
	


def game_start(asd,gamers):
	#schnelles durchprobieren, ob genug spieler da sind
	amount_players = 0
	for i in range(0,4):#enough players or bots
		if gamers[i] in [1,2,4]:#human, bot or networkplayer
			amount_players += 1
	if amount_players in [0,1]:
		return
	del amount_players
	for i in range(4):#players with no names
		if start_window.names[i].get_text() == "" and start_window.sel_but.get_active_text() != "Closed":
			start_window.bgohg = gtk.MessageDialog(message_format="Ein Spieler hat keinen Namen")
			start_window.bgohg.show_all()
			return
	#game can begin

	if network.hosting:
		network.send("g")
		for i in range(4):
			if start_window.sel_but[i].get_active_text() != "Network":
				network.gamedetails.op.append(i)
	#set players
	print (network.gamedetails.op)
	for i in range(0,4):
		if start_window.loaded:
			break
		if gamers[i]:
			game.players[i] = plun.player(i,"balubel")
			game.players[i].name = start_window.names[i].get_text()
			
		else:
			game.players[i] = 0
		
	start_window.optwindow.hide()
	start_window.joinwindow.hide()
	start_window.hide()
	surface.set_visi(True)
	#todo: network stuff
	#send msg to clients that the game has started
	#send playernames to the server and otherway round
	#send rules of the game
	
	surface.pre_render(game.players)
	game.newgame()
	surface.set_msg(game.memo.get_plstr()+"\nstarts the game")	

game.rules = game.rule()
game.memo = game.memory()

surface.board = surface.brett()
#these values are some starting values for the startmenu
bigui = False
jumbs = True
cheese = False
surface.set_chessmod(cheese)
surface.set_size(bigui)
#surface.board.set_imgs()#done in set_size()

start_window = start_win()
start_window.show_all()
gtk.main()
