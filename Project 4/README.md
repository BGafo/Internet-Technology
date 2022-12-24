The goal of this project is to modify the HTTP server given to correctly use cookies.
First step is to make the login functions work. Throughout this project I suggest you use the provided tester to test whether or not your project works.
If it works, all the tests should succeed. There is a guide attached from a previous semester to help you figure out what to do.

I have also given you a tester program to test your code easily with a few test cases.

How we will test your programs
------------------------------

We will test your project in two ways. First we will run the provided testing script. Then we will make sure a simple login and logout work on a normal web browser (we will use the firefox on ilabs).
Please note that when testing on a webbrowser, you should clear your cookies between tests to make sure that previos cookies don't interfere.
If you don't want to clear all the cookies, you can run the tests in private mode, closing the browser between tests.

As part of your submission, you will turn in 2 program:server.py and one README file (more on this below). We will be running the two programs on the ilab machines with Python 3.8.

For the project_3_tester.py program, you should assume that everything happens on one machine.
You should test multiple machines using a browser for example:
if you server is running on cd.cs.rutgers.edu port 8081, then go to

http://cd.cs.rutgers.edu:8081/

in your browser and you should be able to use the form. This should not require any extra work on your part, since the given code does this for you
(assuming it passes the tests)

Please do not assume that all programs will run on the same machine or that all
connections are made to the local host.  We reserve the right to test your
programs with local and remote socket connections. You are welcome to
simplify the initial development and debugging of your project, and get off the
ground by running all programs on one machine first. However, you must
eventually ensure that the programs can work across multiple machines.
Note that the tester only works on the same machine as the server.
Also note that the tests can be commented out while developing to make it easier to read, if you only want to run test 1, then comment out the other tests.
you can also enable verbose mode by adding a v after the portnumber on the command line
e.g.

python project_3_tester.py 8081 v

The programs must work with the default command lines:

For examples, see the guide.





