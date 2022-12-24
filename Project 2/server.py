
import socket
import binascii
import argparse
from sys import argv

#receiving input from command line
parser=argparse.ArgumentParser(description="""This is a very basic server program""")
parser.add_argument('port', type=int, help='This is the port to connect to the client with',action='store')
args = parser.parse_args(argv[1:])

#client connection
HOST = ''
PORT = args.port
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.bind(('', PORT))
sock_client.listen(1)
conn, address = sock_client.accept()


# dns server socket
dns_host = "8.8.8.8"
dns_port = 53
dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns_server_addr = (dns_host, dns_port)
dns_sock.connect(('8.8.8.8', 53))

# revceiving the URL from client and preparing the message 
question_count = 0
complete_question_string = ''
message = ''
x = 'temp' 
while x:
    # receive the string from the client and decode it
    x = conn.recv(512)
    x = x.decode('utf-8')
    length = len(x)
    #print(length)
    char_count = 0
    label_string = ''
    complete_question_string = ''
    for i in range(length):
        #print(i)
        if x[i] == '.':
            #char_count = str(chr(char_count))
            label_string = '0' + hex(char_count)[2:] + label_string
            char_count = 0
            complete_question_string = complete_question_string + ' ' + label_string
            question_count += 1
            label_string = ''
        elif i == length-1:
            char_count += 1  
            label_string = '0' + hex(char_count)[2:] + label_string + ' ' + hex(ord(x[i]))[2:]
            #label_string = hex(char_count) + ' ' + label_string
            char_count = 0
            complete_question_string = complete_question_string + ' ' + label_string
            question_count += 1
        else:
            char_count += 1    
            label_string = label_string + ' ' + hex(ord(x[i]))[2:]
            

    if (complete_question_string != '') :       # if there is a question, add it into a message and send to dns server
        message = "AA AA 01 00 00 01 00 00 00 00 00 00" + complete_question_string + " 00 00 01 00 01"
        message = message.replace(" ", "").replace("\n", "")   
        dns_sock.sendto(binascii.unhexlify(message), dns_server_addr)
        res_rec, _ = dns_sock.recvfrom(512)
        res_rec = binascii.hexlify(res_rec).decode("utf-8")

        #print('resource record: ')
        response = res_rec[len(message):]               # removing query from response record
        ans_cnt = int(res_rec[12:16], base=16)
        result_data = ''
        for i in range(ans_cnt) :           #checking each answer of the response message
            #print('answer ' + str(i+1))
            resp_block = response[:(24 + (2*int(response[20:24], base=16)))]        # dividing each answer into its own block for parsing
            response = response[len(resp_block):]
            #print('response block: ' + resp_block)
            if (int(resp_block[4:8], base=16) == 1 and ans_cnt - i == 1) :          # if its the only answer, or the last answer of a response
                ip_hex = resp_block[24:]
                ip1 = int(ip_hex[:2], base=16)
                ip2 = int(ip_hex[2:4], base=16)
                ip3 = int(ip_hex[4:6], base=16)
                ip4 = int(ip_hex[6:], base=16)
                result_data = result_data + str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
                conn.sendall(result_data.encode('utf-8'))
                #print(result_data + '\n')
            elif (int(resp_block[4:8], base=16) == 1 and ans_cnt - i > 1) :         # if there are multiple answers, and this one is not the last
                ip_hex = resp_block[24:]
                ip1 = int(ip_hex[:2], base=16)
                ip2 = int(ip_hex[2:4], base=16)
                ip3 = int(ip_hex[4:6], base=16)
                ip4 = int(ip_hex[6:], base=16)
                result_data = result_data + str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4) + ','
                #print(result_data + '\n')


dns_sock.close()
conn.close()
sock_client.close()
