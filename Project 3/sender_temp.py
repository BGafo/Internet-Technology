import argparse
import receiver
from sys import argv
import socket



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings1.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('local_port', type=int, help='This is the local port',action='store')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])


#next we create a client socket
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.server_location, args.port)
sender_sock.bind(('', args.local_port))
sender_sock.connect(server_addr)



with open(args.in_file, "rb") as f:
    sequence_number = 0
    sender_sock.settimeout(2)
    acked = False

    while not acked:
        line = f.read(488)
        #print(len(line))

        if not line:
            break
        header = receiver.make_TCP_PACK(sequence_number, 0)
        sender_sock.sendto(header + line, server_addr)
        sequence_number += len(line)

        print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))


header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

#close the socket (note this will be visible to the other side)
sender_sock.close()













import argparse
import time
import receiver
from sys import argv
import socket



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings1.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('local_port', type=int, help='This is the local port',action='store')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])


#next we create a client socket
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.server_location, args.port)
sender_sock.bind(('', args.local_port))
sender_sock.connect(server_addr)




# I think the problemis with the logic of timer. I think I am setting the timer at the beginning of the loop, then sending the packet but it needs to be in the reverse order. I mean we should check the timer
# after sending the packet.

with open(args.in_file, "rb") as f:
    # time out value
    max_time = 3.0
    # last sequence number in the case of a drop packet or ack or half packet
    last_seq_num = 0
    sequence_number = 0
    #sender_sock.settimeout(2)
    tmp = 'temp'
    # number of packets that are sent
    packet_num = 1

    while tmp:
        # start time
        start = time.time()
        #print(start)
        line = f.read(488)
        #print(last_seq_num)
        #print(len(line))

        # if no more line to read, stop
        if not line:
            break

        
        
        packet_num += 1
        header = receiver.make_TCP_PACK(sequence_number, 0)
        sender_sock.sendto(header + line, server_addr)
        print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))
        print(start, time.time())
        print(str(packet_num) + "packet sent")
        if time.time() - start > max_time:
            print('YOLO')
            print(last_seq_num)
            header = receiver.make_TCP_PACK(last_seq_num, 0)
            sender_sock.sendto(header + line, server_addr)
            sequence_number += len(line)
            print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))

            # i am not sure if this works but I am trying to reset the timer by equalling to 0
            #start = 0
            #continue
        else:    
            sequence_number += len(line)
            last_seq_num = sequence_number
            print(sequence_number)
            print("last seq number :"  + str(last_seq_num))
            #start = 0

        # if a packet or ack drops, sent the packet from the last sequence number
        #if max_time - start < 0:
        

        # normal case: last sequence number only updated to sequence number when a packet successfully sent
        
            

header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

#close the socket (note this will be visible to the other side)
sender_sock.close()








import argparse
import time
import receiver
from sys import argv
import socket
import select



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings1.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('local_port', type=int, help='This is the local port',action='store')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])


#next we create a client socket
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.server_location, args.port)
sender_sock.bind(('', args.local_port))
sender_sock.connect(server_addr)




# I think the problemis with the logic of timer. I think I am setting the timer at the beginning of the loop, then sending the packet but it needs to be in the reverse order. I mean we should check the timer
# after sending the packet.

with open(args.in_file, "rb") as f:
    # time out value
    max_time = 3.0
    # last sequence number in the case of a drop packet or ack or half packet
    last_seq_num = 0
    sequence_number = 0
    #sender_sock.settimeout(2)
    tmp = 'temp'
    # number of packets that are sent
    packet_num = 1

    while tmp:
        # start time
        start = time.time()
        #print(start)
        line = f.read(488)
        #print(last_seq_num)
        #print(len(line))

        # if no more line to read, stop
        if not line:
            break

        
        # send packet
        packet_num += 1
        header = receiver.make_TCP_PACK(sequence_number, 0)
        sender_sock.sendto(header + line, server_addr)
        # check if the socket has any response from receiver
        rlist, wlist, xlist = select.select([sender_sock], [], [], 0.3)
        #print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))
        print(start, time.time())
        
        if len(rlist) == 0:
            print('YOLO')
            print(last_seq_num)
            header = receiver.make_TCP_PACK(last_seq_num, 0)
            sender_sock.sendto(header + line, server_addr)
            sequence_number += len(line)
            print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))

            # i am not sure if this works but I am trying to reset the timer by equalling to 0
            #start = 0
            #continue
        else:    
            sequence_number += len(line)
            last_seq_num = sequence_number
            print(sequence_number)
            print("last seq number :"  + str(last_seq_num))
            print(str(packet_num) + "packet sent")
            #start = 0

        # if a packet or ack drops, sent the packet from the last sequence number
        #if max_time - start < 0:
        

        # normal case: last sequence number only updated to sequence number when a packet successfully sent
        
            

header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

#close the socket (note this will be visible to the other side)
sender_sock.close()









08/06 4:26pm



import argparse
import time
import receiver
from sys import argv
import socket
import select



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings1.txt',action='store', dest='in_file')
parser.add_argument('-o', type=str, help='This is the destination file for the reversed strings', default='results.txt',action='store', dest='out_file')
parser.add_argument('local_port', type=int, help='This is the local port',action='store')
parser.add_argument('server_location', type=str, help='This is the domain name or ip address of the server',action='store')
parser.add_argument('port', type=int, help='This is the port to connect to the server on',action='store')
args = parser.parse_args(argv[1:])


#next we create a client socket
sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_addr = (args.server_location, args.port)
sender_sock.bind(('', args.local_port))
sender_sock.connect(server_addr)




# I think the problemis with the logic of timer. I think I am setting the timer at the beginning of the loop, then sending the packet but it needs to be in the reverse order. I mean we should check the timer
# after sending the packet.

with open(args.in_file, "rb") as f:
    # time out value
    #max_time = 3.0
    # last sequence number in the case of a drop packet or ack or half packet
    #last_seq_num = 0
    sequence_number = 0
    #sender_sock.settimeout(2)
    tmp = 'temp'
    # number of packets that are sent
    packet_num = 0
    backup = ""
    lost = False

    while tmp:
        # start time
        start = time.time()
        #print(start)
        if not lost:
            line = f.read(488)
        else:
            line = backup
        #print(last_seq_num)
        #print(len(line))

        # if no more line to read, stop
        if not line:
            break
        
        # send packet
        #print('here is the seq num' + str(sequence_number))
        header = receiver.make_TCP_PACK(sequence_number, 0)
        sender_sock.sendto(header + line, server_addr)

        # to check if socket received a reponse (ack)
        rlist, wlist, xlist = select.select([sender_sock], [], [], 0.3)
        #print(receiver.make_TCP_UNPACK(sender_sock.recv(512)))
        #print(start, time.time())
        
        if len(rlist) > 0:
            #packet_num += 1
            ack = sender_sock.recv(512)
            header_info = receiver.make_TCP_UNPACK(ack)
            print('seq_num_1= ' + str(sequence_number))
            print('ack_number: ',header_info['ack_number'])
            #if header_info['ack_number'] - sequence_number == 488:
            #print('even')
            sequence_number += len(line)
            print('seq_num_2= ' + str(sequence_number))
            #elif header_info['ack_number'] - sequence_number < 488:
            #else:
                #sequence_number += packet_num*488 - sequence_number
                
                #offset = header_info['ack_number'] - sequence_number
                #print(offset)
                #f.seek(offset, 1)
                #print('half_drop')
                #print('seq num= ' + str(sequence_number))
                #print('ack num= ' + str(header_info['ack_number']))

            #packet_num += 1
            
            #last_seq_num = sequence_number
            #print("last seq number :"  + str(last_seq_num))
            #print(str(packet_num) + "packet sent")
            lost = False
            #print('hey')
            #start = 0
        else:
            lost = True
            backup = line
            

        # if a packet or ack drops, sent the packet from the last sequence number
        #if max_time - start < 0:
        

        # normal case: last sequence number only updated to sequence number when a packet successfully sent
        
            

header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

#close the socket (note this will be visible to the other side)
sender_sock.close()
