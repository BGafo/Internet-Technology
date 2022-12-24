import argparse
import time
import receiver
from sys import argv
import socket
import select



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings2.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('local_port', type=int, help='This is the local port',action='store')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
parser.add_argument('window_size', type=int, help='This is the size of the window being used to send bytes',action='store')
args = parser.parse_args(argv[1:])


#next we create a client socket
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.server_location, args.port)
sender_sock.bind(('', args.local_port))
sender_sock.connect(server_addr)




# I think the problemis with the logic of timer. I think I am setting the timer at the beginning of the loop, then sending the packet but it needs to be in the reverse order. I mean we should check the timer
# after sending the packet.

with open(args.in_file, "rb") as f:
	sequence_number = 0
	bytes_read = 0
	tmp = 'temp'
	# number of packets that are sent
	packet_num = 1
	window_num = 1
	backup = ""
	lost = False
	run=True
	retransmit= list()
	retransmitting = False
	handshake_case = 0

	while tmp:
		if handshake_case == 0:
			handshake_case = 1
			handshake = receiver.make_TCP_PACK(sequence_number, 0, SYN=1)
			sender_sock.sendto(handshake, server_addr)
			response = sender_sock.recv(512)
			handshake_info = receiver.make_TCP_UNPACK(response)
			syn = handshake_info['flags']['SYN']
			ack = handshake_info['flags']['ACK']
			#print(str(syn) + ' ' +  str(ack))
			if syn == 1 and ack == 1:
				sequence_number = handshake_info['ack_number']
				handshake = receiver.make_TCP_PACK(sequence_number, handshake_info['sequence_number'] + 1,  ACK=1)
				sender_sock.sendto(handshake, server_addr)
				# try
			sequence_number = 0
		print('retransmitting:',len(retransmit),retransmitting)
		bytes_read = 0
		while (bytes_read+488<=args.window_size):

			# If were are retransmitting packets
			if retransmitting:
				if len(retransmit)==0:
					retransmitting = False
					break
				# pop packets from the retransmission list in sequential order, and set them to be the new packet to get sent
				pack = retransmit.pop(0)
			else:
				line = f.read(488)
				if not line:
					run = False
					break
				header = receiver.make_TCP_PACK(sequence_number, 0)
				pack = header + line
			
			if retransmitting:
				pass
			sender_sock.sendto(pack, server_addr)
			rlist, wlist, xlist = select.select([sender_sock], [], [], 0.01)
			if len(rlist)>0:
				ack = sender_sock.recv(512)
				header_info = receiver.make_TCP_UNPACK(ack)
				if retransmitting:
					print('retransmitted success')
				else:
					print('seq number:',header_info['ack_number'])
					
			else:
				if retransmitting:
					print('retransmit fail')
				retransmit.append(pack)

			if not retransmitting:
				bytes_read+=len(line)
				sequence_number += len(line)
				#print('next seq:',sequence_number)
			
		if (len(retransmit)>0):
			retransmitting = True

		if not retransmitting:
			print("window num:",window_num)
			window_num+=1

		if not run:
			break
           

header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

#close the socket (note this will be visible to the other side)
sender_sock.close()
