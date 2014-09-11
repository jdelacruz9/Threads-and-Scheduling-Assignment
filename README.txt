README

Description:

	For this project we are making a server (scheduler.py) that will receive messages from mobile devices (mobile.py) and will "execute" them. These messages contain the ID of the mobile that is sending the message and the time that a certain "job"
	will be using the CPU (i.e. 3:4). Once the message is sent, the server receives it and send a reply to the mobile saying that the message was received. 

	Now the server puts the message in a shared queue using a thread (receiver), that is desing to wait for the message and put it in the queue. Later in the program the server will pick a message from the queue, using another thread (producer), and will add the time of the "job" to the corresponging mobile in a table. Then it will put the producer thread in sleep mode until the "job" time has passed. 

	Once the server receives certain quantity of messages, the program will end and will "print the mobile IDs with the time consumed by its jobs."

How to use the program:

	1) Open the file mobile.py and set the global variables totalJobs (how many jobs do you want to run with a mobile) and
		timeLimit (the time limit that a job can be using the CPU).
	2) Open the file scheduler.py and set the totalMsg variable to specify how many messages the server is allowed to receive
	3) Run the scheduler.py, specifying the port in which the server will be running
		syntax: python scheduler.py <server port> (i.e python scheduler.py 4017)
	4) Run the mobile.py, specifying the mobile ID, server address and port
		syntax: python mobile.py <mobile ID> <server address> <server port> (i.e python mobile.py 1 localhost 4017)
	5) Repeat instruction number 4 until you reach the limit of messages that the server allows

People that helped me in the process:

	- Luis Albertorio
	- José de la Vega