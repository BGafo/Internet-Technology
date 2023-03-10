This is a medium difficulty project. I suggest you get started early and make use of the provided resources (especially the homework).
This will be worth 12 points. A working reciever code is given to you in reciever.py;  Your job is to write the corresponding sender code.
The goal of the sender is to send a file successfully and quickly using first stop and wait, then cumulative ack.
For the main part of the project, you may not change the reciever code at all.

To simplify the project for you, we are using a fixed window size that is manually entered into both the sender and receiver.


Any code that is copied from anywhere without citation INCLUDING POSTED RESOURCES or fellow classmates will be considered a violation of the academic integrity policy and dealt with appropriately. To clarify, you may use code from the posted resources, but you must cite the resource you used.
PART 1: Stop and wait. (3 pts.)
Step 1: Write a sender that sends 1 packet at a time then waits for an ack, hint: this is very similar to the clients we have been dealing with until now.
you may have to use the select function here (and you will definitely want it later)
https://docs.python.org/3/library/select.html
first test:
set all the dropping constants at the top of receiver.py to zero and run both sender and receiver.
you should run both the same way, first the file name then the local port, then the foregn ip the the foreign port.
for example:


(on cd.cs.rutgers.edu)
python receiver.py 5032 ls.cs.rutgers.edu 4021 --stop_and_wait
(on ls.cs.rutgers.edu)
python sender.py 4021 cd.cs.rutgers.edu 5032

If everything works, this should produce a correct results file. I suggest a file of around 10,000 bytes for this test

second test:
now run the same test but with some probability of dropping the ACK_DROP and PACK_DROP. I suggest 0.5 each for this test.
the code is run the same way and should still work.

This concludes the Stop and wait section, rename the sender to stopandwait.py and save the code separately.

Part 2 (9 pts.) windowed cumulative ack.
You next need to make your sender work with a window. This allows for the sending of large files much faster.
The main goal is to send a window of packets, where a window is defined by the window size field, then increase the window as you get acks.
for example, if you get ack with ack_number 1024, and window size is 5000, then your window includes bytes between 1024 and 6024.

as before, first get it to work without dropping, then introduce dropping.

With dropping I recommend setting all three dropping values like this:
ACK_DROP = 0.1
PACK_DROP = 0.1
HALF_DROP = 0.1

Here is what an example run might look like:

(on cd.cs.rutgers.edu)
python receiver.py 5032 ls.cs.rutgers.edu 4021 --window 10000
(on ls.cs.rutgers.edu)
python sender.py 4021 cd.cs.rutgers.edu 5032 10000


TIPS:
To get large files to send, I recommend txt books from project gutenberg. You should also test with some smaller files, these can be the first few thousand bytes of these books.
If no acks are sent, you send an entire window of packets, then wait for acks before sending anything else.
for large files (~2,700,000 bytes) with recommended dropping (all three dropping variables set to 0.1) it should still send in less than 3 minutes with a window size of 10,000 (my implementation takes 1 minute 20 seconds, compared to 12 minutes for stop and wait)
To make things simpler, the only thing I require in terms of timeout, is that if you have not gotton any kind of ack
for 0.1 seconds, you must consider it a timeout and resend from the beginning of the current window.
You can use the select function mentioned earlier, along with setting the socket to non-blocking (you can use settimeout), to check for acks while sending
you can create a simple timer using time.time() and storing the value
without wasting time.
Note that there is a maximum packet size that the receiver can get, and that this size includes a header.


Part 3. extra credit (+ 3 pts.)
In the reciever you should see two sections labled extra credit part 1 and 2.
For extra credit make and ADDTIONAL sender and reciever files called reciever_extra.py and sender_extra.py.
These must be extra files (total of 4 python files) to get credit for the regular part too.

In this part you should fill in the two sections to correctly preform the 3 way handshake and the double fin close
you may assume no packets are dropped during this section. You need to fill in the sequence_number, ack_number SYN and FIN and ACK sections
to generate random Initial sequence numbers and exchange them, the rest of the code should still work (with the new numbers).

How we will test your programs
------------------------------


As part of your submission, you will turn in 2 program:Server.py and one README file (more on this below). We will be running the two programs on the ilab machines with Python 3.8.


Please do not assume that all programs will run on the same machine or that all
connections are made to the local host.  We reserve the right to test your
programs with local and remote socket connections. You are welcome to
simplify the initial development and debugging of your project, and get off the
ground by running all programs on one machine first. However, you must
eventually ensure that the programs can work across multiple machines.


The programs must work with the following command lines:


python stopandwait.py LOCALPORT OTHERADDRESS OTHERPORT
python sender.py LOCALPORT OTHERADDRESS OTHERPORT WINDOWSIZE

For examples look above.

By default the receiver writes to a file called results.txt.





