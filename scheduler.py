#############################################
#    Author: Julio de la Cruz Natera        #
#    Course: CCOM 4017 - Operating Systems  #
#    Assignment 02: Threads and Scheduling  #
#############################################

from threading import Thread, Semaphore
import time
import sys
import socket
from Queue import Queue

#The user should change this variable to his own parameter
totalMsg = 10 #total of messages that the server will allow
#-------------------------------------------------------------

schedulerQ = Queue() #shared queue 
table = {} #table to hold the CPU time that used each Mobile

lock = Semaphore() #semaphore to avoid race condition when accesing the queue
lockFull = Semaphore(0) #semaphore that will block the consumer when there is not data in the queue

host = 'localhost'   # Symbolic name meaning all available interfaces
port = int(sys.argv[1]) # Arbitrary non-privileged port
 
# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((host, port))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'

#function that will use the producer thread to put a message in the queue
def producerWork():
	global totalMsg
	global schedulerQ
	while(totalMsg):
		d = s.recvfrom(port)
		data = d[0]
		addr = d[1]

		if not data:
			break

		reply = "The message has been received"
		s.sendto(reply , addr)
   	 	print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

   	 	#-----------Critial Region begins-----------
   	 	# lockEmpty.acquire()
		lock.acquire() #acquire the semaphore to avoid other threads of putting a message in the queue at the same time
		schedulerQ.put(data) #putting the message in the shared queue
		totalMsg-=1
		lock.release() #releasing the semaphore to be used by another thread
		lockFull.release()
		#------------Critial Region ends------------

def consumerWork():
	global schedulerQ
	global table

	while totalMsg or not schedulerQ.empty():
		#-----------Critial Region begins-----------
		lockFull.acquire()
		lock.acquire() #acquire the semaphore to avoid other threads of getting a message from the queue at the same time
		msg = schedulerQ.get() #getting a message from the shared queue
		lock.release() #releasing the semaphore to be used by another thread
		# lockEmpty.release()
		#------------Critial Region ends------------

		mobileID = msg.split(":")[0] #taking the mobileID from the message 
		jobTimer = int(msg.split(":")[1]) #taking the time that the job will be using the CPU from the message

		#checking if the mobileID is already in the table
		if(mobileID in table): #if it's so, then we have to add the new time of the job
			table[mobileID] = table[mobileID] + jobTimer
		else: #if it's not, then we have to add the mobileID to the table and the time of the job
			table[mobileID] = jobTimer
		time.sleep(jobTimer)#the thread will sleep until the job finished using the CPU
	for key, value in table.items():
		print "Mobile %s consumed %s seconds of CPU time"%(key, value)

 
producer = Thread(target=producerWork) #Thread that will put the messages in the queue
consumer = Thread(target=consumerWork) #Thread that will take the messages from the queue, one by one, and will execute them

producer.start() #starting the producer thread
consumer.start() #starting the consumer thread

#waiting for the threads to finish
producer.join() 
consumer.join()

s.close() #closing the socket