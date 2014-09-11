from random import randint #for random
import socket   #for sockets
import sys  #for exit
 
#The user must change these two variables to his own parameters
totalJobs = 2 #quantity of jobs that will be executed or sent, 
timeLimit = 5 #time limit that the job will be using the CPU
#--------------------------------------------------------------

mobileID = str(sys.argv[1]) 
jobs = [0]*totalJobs #creating the array to hold the time limit for each job

#host and port of the server
host = sys.argv[2] 
port = int(sys.argv[3])

for i in range(totalJobs):
    jobs[i] = randint(1,timeLimit)

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

#sending the messages with the mobileID and the time of each job
for i in range(totalJobs):
    msg = mobileID + ":" + str(jobs[i])
    try:

        s.sendto(msg, (host, port))
        d = s.recvfrom(port)
        reply = d[0]
        addr = d[1]

        print 'Server reply : ' + reply

    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()