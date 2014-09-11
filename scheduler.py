from threading import Thread, BoundedSemaphore
import time
import sys
import socket
from Queue import Queue

totalMsg = 10 #total of messages that the server will allow
schedulerQ = Queue() #shared queue 
table = {} #table to hold the CPU time that used each Mobile

mutex = BoundedSemaphore() #semaphore to avoid race condition when accesing the queue

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

#function that will use the receiver thread to put a message in the queue
def receiverWork(msg):
	global totalMsg
	global schedulerQ
	mutex.acquire() #acquire the semaphore to avoid other threads of putting a message in the queue at the same time
	schedulerQ.put(msg) #putting the message in the shared queue
	totalMsg-=1
	mutex.release() #releasing the semaphore to be used by another thread

def producerWork():
	global schedulerQ
	mutex.acquire() #acquire the semaphore to avoid other threads of getting a message from the queue at the same time
	msg = schedulerQ.get() #getting a message from the shared queue
	mutex.release() #releasing the semaphore to be used by another thread
	mobileID = msg.split(":")[0] #taking the mobileID from the message 
	jobTimer = int(msg.split(":")[1]) #taking the time that the job will be using the CPU from the message

	#checking if the mobileID is already in the table
	if(mobileID in table): #if it's so, then we have to add the new time of the job
		table[mobileID] = table[mobileID] + jobTimer
	else: #if it's not, then we have to add the mobileID to the table and the time of the job
		table[mobileID] = jobTimer

	time.sleep(jobTimer)#the thread will sleep until the job finished using the CPU
	

 
#now keep talking with the client
while totalMsg:
    # receive data from client (data, addr)
    d = s.recvfrom(port)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    receiver = Thread(target=receiverWork, args=(data,)) #Thread that will put the messages in the queue
    producer = Thread(target=producerWork) #Thread that will take the messages from the queue, one by one, and will execute them

    receiver.start() #starting the receiver thread
    producer.start() #starting the producer thread

    reply = "The message has been received"
     
    s.sendto(reply , addr)
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()
     


#waiting for the threads to finish
receiver.join() 
producer.join()

s.close() #closing the socket

for key, value in table.items():
		print "Mobile %s consumed %s seconds of CPU time"%(key, value)
