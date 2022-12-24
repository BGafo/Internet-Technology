This is a medium difficulty project. I suggest you get started early and make use of the provided resources (Start by reading the routly blog post). This will be worth 12 points. A working client code is given to you in Client.py; this is the same client as project 0.  Your job is again to write the corresponding server code. The goal of the server is to reply to any client with a list of the IP address corresponding to any domain name sent to it. 



The server is not allowed to use gethostbyname or any function designed for DNS. Instead, the server must send a UDP (SOCK_DGRAM) message to the Google DNS server at 8.8.8.8 and ask it for the IP address. This means the server will need two sockets, one server socket to talk to the client and one client socket to talk to the Google DNS server. You must construct this DNS message according to your knowledge of the protocol and the provided resources. Lastly, it should then close gracefully when the client is done sending domain names. Sample output and input files have also been provided. Note that due to certain aspects of the way DNS works, your output may not exactly match the sample; you can check if it worked by typing the IP address into your browser and making sure you get the right webpage (or in some cases an error page)


If the DNS server at 8.8.8.8 sends many answers, send all of them back to the client separated by a ‘,’ character in the order that they were sent to you. If the answer is not an A record, you should skip that record.


Any code that is copied from anywhere without citation INCLUDING POSTED RESOURCES or fellow classmates will be considered a violation of the academic integrity policy and dealt with appropriately. To clarify, you may use code from the posted resources, but you must cite the resource you used.
