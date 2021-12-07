# 381FinalProject
This is where our CNIT381 Network Programmability and Automation Final is going to be
Everything in this project will be completed using several virtual machines running on virtual box.

GUI Ubuntu virtual machine with 4MB of memory allocated

Virtual router allocated 4MB of memory

Starting the bot…

a.	In a new terminal on your GUI virtual machine enter the command “ngrok http 5000” Copy the https address for later use. 

   ![ngroksc](images/ngrok.png)

b. Open GenieRobot.py in virtual studio and paste the https address here:

   ![ngroksc2](images/ngrok2.png)

c. Initial connectivity tests:

Check that R1 can ping 172.16.0.2 this should work

Check that R1 can ping 2.2.2.2 this should work

d. Start up the bot: 

Interact with the bot and receive a greeting message by sending the bot a message like “hey”

![botsc](images/bot1.png)

Use the /help command to see what skills the bot has.

###NEED SCREENSHOT###

Now on R1 issue the ping command ping 2.2.2.2 repeat 10000

Finally change the IP address of Gi2 on CSR2 and we should see that the pings on CSR1 stop and then continue after the vpn tunnel is reestablished.
