import argparse
import time
import receiver
from sys import argv
import socket
import select



#First we use the argparse package to parse the aruments
parser=argparse.ArgumentParser(description="""This is a very basic client program""")
parser.add_argument('-f', type=str, help='This is the source file for the strings to reverse', default='source_strings.txt',action='store', dest='in_file')
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
    tmp = 'temp'
    backup = ""
    lost = False
    off_set = False

    while tmp:
        start = time.time()
        if not lost and not off_set:
            line = f.read(488)
        elif lost:
            line = backup
        elif off_set:
            f.seek(header_info['ack_number'], 0)
            line = f.read(488)

        # if no more line to read, stop
        if not line:
            break
        
        # send packet
        header = receiver.make_TCP_PACK(sequence_number, 0)
        sender_sock.sendto(header + line, server_addr)

        # to check if socket received a reponse (ack)
        rlist, wlist, xlist = select.select([sender_sock], [], [], 0.3)
        
        if len(rlist) > 0:
            ack = sender_sock.recv(512)
            header_info = receiver.make_TCP_UNPACK(ack)        
            
            if header_info['ack_number'] - sequence_number == 488:
                sequence_number += len(line)
            else:
                offset = abs(header_info['ack_number'] - sequence_number)
                sequence_number = header_info['ack_number']
                off_set = True
            lost = False
            continue
        else:
            lost = True
            backup = line
        
header = receiver.make_TCP_PACK(0,0, FIN=1)
sender_sock.sendto(header, server_addr)

sender_sock.close()
