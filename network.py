import socket
import thread
from time import sleep
import copy
#one socket to recv and send
#the host will always send a message which is immediately replied to by one from the client
#
#muss implementieren
#enabled : ein boolean der angibt ob das netzwerk an ist
#enable()
#disable() : jeweils zum aktivieren und deaktivieren
#connect(ip,name,players) : funktion mit der sich ein client verbindet
#send(player,


class gd:
	def elaborate(self):
		retu = ""
		for i in range(4):
				retu += self.pt[i]+"\\"+self.pn[i]+"\\\\"
		return retu
	def getNameChange(self):#puffer fuers namen-aendern

		retu = []
		for i in range(4):
			if self.pna[i] != self.pn[i]:#change
				retu.append("s"+str(i)+"n"+self.pn[i])
				self.pna[i] = self.pn[i]
		return retu
	def setType(self,num,tag):
		self.pt[num] = tag
		send("s"+str(num)+"c"+tag)

	#def update(self,num,was,cont):
		#if was =="name":
		#	self.pn[num] = cont
		#else:
		#	self.pt[num] = cont
gamedetails = gd()#supposed to be kept uptodate by module:menu
gamedetails.pn = []
gamedetails.pt = []
gamedetails.pn.append("Spieler 1")
gamedetails.pn.append("Spieler 2")
gamedetails.pn.append("Spieler 3")
gamedetails.pn.append("Spieler 4")
gamedetails.pna = copy.deepcopy(gamedetails.pn)
gamedetails.pt.append("h")
gamedetails.pt.append("c")
gamedetails.pt.append("h")
gamedetails.pt.append("c")
gamedetails.op = []#owned players

def hasPlayer(i):
	return i in gamedetails.op


poll_intervall= 0.1
backlog = 5
host = ''
port = 1338
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
answersize = 100#being sent on answer TODO adjust
packagesize = 128#being sent all the time TODO adjust
socket.setdefaulttimeout(poll_intervall)
hosting = True

output_stack = []
input_stack = []

enabled = False#these two handle aborting the hosting process
_running = False

adresses = []
lock = thread.allocate_lock()
######################### client ######################################
def connect(ip,name,players):
	global hosting,s
	
	hosting = False
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print("trying to connect")
	try:
		s.connect((ip,port))
	except:
		return 1#connection failed
	print("connected")
	s.send(str(players)+"\n"+name)
	print("info sent")
	answ = s.recv(answersize)
	if answ == "fail":
		#players are not free
		s.close()
		return 2
	else:#players are free
		
		retu = []#what the players are
		answ = answ.split("\\\\")#split by players
		for i in range(0,4):
			retu.append([])
			typ = answ[i].split("\\")[0]
			retu[-1].append(typ)#kontrolltyp
			retu[-1].append(answ[i].split("\\")[1])#spielername
		lock.acquire()
		global enabled,gamedetails
		gamedetails.op = itol(players)
		enabled = False
		while 1:
			global _running
			if not _running:
				break
			lock.release()
			sleep(0.11)
			lock.acquire()
		lock.release()
		s.settimeout(0.1)
		
		thread.start_new_thread(client_nwloop,tuple([s]))
		return retu

		
def disconnect_client(con):#vom menu aufgerufen
	#todo: socket schliessen
	con.close()
	#threads killen
	pass


def client_nwloop(con):
	while 1:
		#empfangen
		try:
			data = con.recv(packagesize)
		except:
			data = 1
		#verarbeiten
		if not data:
			disconnect_client(con)
			return
		if data != 1:
			#TODO falls sich nachrichten ueberschneiden muessen sie hier auseinander genommen werden (mit trennzeichen versehen)
			#lock.acquire()
			global input_stack
			input_stack.append(("host",data))
			#lock.release()
		#auslesen
		#lock.acquire()
		global output_stack
		output_stack.extend(gamedetails.getNameChange())
		if len(output_stack) == 0:
			pass
			#lock.release()
		else:
			data = output_stack.pop()
			#lock.release()
			con.send(data)########
		sleep(0.1)



############################################################### host ########################################################################
def await():
	lock.acquire()
	global _running,enabled,hosting
	hosting = True
	if _running:#already listening
		lock.release()
		return
	_running = True
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((host,port))
	s.listen(backlog)
	s.settimeout(poll_intervall)
	while enabled:
		lock.release()
		try:
			#sleep(0.1)
			thread.start_new_thread(listen,s.accept())
			
		except:
			pass
		lock.acquire()
		if not enabled:
			s.close()
			print "closed"
			break
								
		#print("neue connection")
	_running = False
	print("shutting down")
	lock.release()
	thread.exit()



def listen(client, adress):
	lock.acquire()
	global adresses
	adresses.append(adress)
	global gamedetails
	lock.release()
	data = client.recv(128)#code for which players to use
	name = data.split("\n")[1]
	data = int(data.split("\n")[0])

	pl = itol(data)#all players that he wants to use
	for i in pl:
		if gamedetails.pt[i] != "n":#player not available for networkplayers
			client.send("fail")
			return
	#just connected, so send game details
	for i in pl:#namechange
		gamedetails.pn[i] = name
		gamedetails.pna[i] = name
		send("s"+str(i)+"n"+name,adress,True)
		input_stack.append(("me","s"+str(i)+"n"+name))
	client.send(gamedetails.elaborate())		
		
	while 1:
		if not enabled:
			return

		#receive
		try:
			data = client.recv(packagesize)############
		except:
			data = 1
		if not data:#disconnect
			disconnect(adress)
			return
		if data != 1:
			#work on input
			###if a name- or controlchange is received send it to everyone else
			if data[0] == "s":
				send(data,adress,True)

			lock.acquire()
			input_stack.append((adress,data))
			lock.release()

		#send
		lock.acquire()
		newname = gamedetails.getNameChange()
		lock.release()
		for t in newname:
			send(t)
		lock.acquire()
		data = getOutput(adress)
		lock.release()
		if data:
			client.send(data[1])###########
		sleep(0.1)
		

	

def enable():
	lock.acquire()
	global enabled,_running
	enabled = True
	if not _running:
		lock.release()
		thread.start_new_thread(await,())
	else:
		lock.release()
	
	
def disable():
	lock.acquire()
	global enabled
	enabled = False
	print "disabled"
	lock.release()
	
	
def disconnect(adress="me"):
	global adresses
	
	adresses.remove(adress)#remove the adress from the adresses list


def send(data, adress = "all", n = False):
	if adress=="all" and n:
		#nonsense
		return
	lock.acquire()
	global output_stack
	if hosting:
		if adress == "all":#brotkast
			global adresses
			for a in adresses:
				output_stack.append((a,data))
		elif n: #send to everyone except one
			global adresses
			for a in adresses:
				if a != adress:
					output_stack.append((a,data))
		else:#send to adress
			output_stack.append((adress,data))
		
	else:
		output_stack.append(data)
	lock.release()

def getOutput(adress):
	#print output_stack
	i = 0
	retu = []
	while i != len(output_stack):
		if output_stack[i][0]==adress:
			return output_stack.pop(i)
		else:
			i+=1
	return False

def getInput():
	lock.acquire()
	global input_stack
	retu = input_stack
	input_stack = []
	lock.release()
	return retu

def itol(data):
	pl = []
	#print data
	if data >= 8:
		pl.append(3)
		data -= 8
	if data >= 4:
		pl.append(2)
		data -= 4
	if data >= 2:
		pl.append(1)
		data -= 2
	if data >= 1:
		pl.append(0)
	return pl	
