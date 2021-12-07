### teams Bot ###
from typing import List
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
### Utilities Libraries
import inventory as routers
# Test Skills
import useful_skills as useful
import useless_skills as useless
# Monitor interfac
from Monitor_Interfaces import MonitorInterfaces
#import paramiko_netmiko_skills as pn_skill
#import netconf_resconf_skills as nr_skill
#import ansible_skills as a_skill
import threading as threads
import time
from myparamiko import paramik

# Create  thread list
threads = []
# Exit flag for threads
exit_flag = False

# Router Info 
device_address = routers.router['host']
device_username = routers.router['username']
device_password = routers.router['password']

# RESTCONF Setup
port = '443'
url_base = "https://{h}/restconf".format(h=device_address)
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

# Bot Details
bot_email = '381-Final@webex.bot' #Fill in your Teams Bot email#
teams_token = 'ZDE2MGRlMDMtYjViYi00ZmY4LTkxMmYtODY0MTE2Y2Q1YWM5OGE4NWViNGYtNGFl_P0A1_529b5ae9-ae34-46f8-9993-5c34c3d90856' #Fill in your Teams Bot Token#
bot_url = "https://409e-12-206-249-123.ngrok.io" #Fill in the ngrok forwarding address#
bot_app_name = 'CNIT-381 Network Final Auto Chat Bot'

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=True,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Create a function to respond to messages that lack any specific command
# The greeting will be friendly and suggest how folks can get started.
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I'm a friendly CSR1100v assistant .  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response

def arp_list(incoming_msg):
    """Return the arp table from device
    """
    response = Response()
    arps = useful.get_arp(url_base, headers,device_username,device_password)

    if len(arps) == 0:
        response.markdown = "I don't have any entries in my ARP table."
    else:
        response.markdown = "Here is the ARP information I know. \n\n"
        for arp in arps:
            response.markdown += "* A device with IP {} and MAC {} are available on interface {}.\n".format(
               arp['address'], arp["hardware"], arp["interface"]
            )

    return response

def sys_info(incoming_msg):
    """Return the system info
    """
    response = Response()
    info = useful.get_sys_info(url_base, headers,device_username,device_password)

    if len(info) == 0:
        response.markdown = "I don't have any information of this device"
    else:
        response.markdown = "Here is the device system information I know. \n\n"
        response.markdown += "Device type: {}.\nSerial-number: {}.\nCPU Type:{}\n\nSoftware Version:{}\n" .format(
            info['device-inventory'][0]['hw-description'], info['device-inventory'][0]["serial-number"], 
            info['device-inventory'][4]["hw-description"],info['device-system-data']['software-version'])

    return response

def get_int_ips(incoming_msg):
    response = Response()
    intf_list = useful.get_configured_interfaces(url_base, headers,device_username,device_password)

    if len(intf_list) == 0:
        response.markdown = "I don't have any information of this device"
    else:
        response.markdown = "Here is the list of interfaces with IPs I know. \n\n"
    for intf in intf_list:
        response.markdown +="*Name:{}\n" .format(intf["name"])
        try:
            response.markdown +="IP Address:{}\{}\n".format(intf["ietf-ip:ipv4"]["address"][0]["ip"],
                                intf["ietf-ip:ipv4"]["address"][0]["netmask"])
        except KeyError:
            response.markdown +="IP Address: UNCONFIGURED\n"
    return response
"""
def Monitor_ips(ignition):

    response = Response()
    active = True
    if(ignition == "on"):
        response.markdown = "Running Monitor...\nType /stopmon to abort"
        while(active==True):
            learn = MonitorInterfaces()
            learn.setup('routers.yml')
            response.markdown += learn.learn_interface_ip()
            continue
            
    if(ignition == "off"):
        active == False
        response.markdown = "Stopped Monitor..."
        return
"""
        
def check_int(incoming_msg):
   
    response = Response()
    response.text = "Gathering  Information...\n\n"

    mon = MonitorInterfaces()
    status = mon.setup('routers.yml')
    if status != "":
        response.text += status
        return response

    status = mon.learn_interface_ip()
    if status == "":
        response.text += "Nothing has changed"
    else:
        response.text += status

    return response

def monitor_int(incoming_msg):
    """Monitor interfaces in a thread
    """
    response = Response()
    response.text = "Monitoring interfaces...\n\n"
    monitor_int_job(incoming_msg)
    th = threads.Thread(target=monitor_int_job, args=(incoming_msg,))
    threads.append(th)

    # starting the threads
    for th in threads:
        th.start()

    # waiting for the threads to finish
    for th in threads:
        th.join()

    return response

def monitor_int_job(incoming_msg):
    response = Response()
    msgtxt_old=""
   
    global exit_flag
    while exit_flag == False:
        msgtxt = check_int(incoming_msg)
        print(msgtxt.text)
        w = str(msgtxt.text)
        useless.create_message(incoming_msg.roomId, w)
        time.sleep(10)
        #return response
        
    print("exited thread")
    exit_flag = False

    

def stop_monitor(incoming_msg):
    """Monitor interfaces in a thread
    """
    response = Response()
    response.text = "Stopping all Monitors...\n\n"
    global exit_flag
    exit_flag = True
    time.sleep(5)
    response.text += "Done!..\n\n"

    return response

def paramik_skill(incoming_msg):
    """
    Spit out "sh ip int br" output
    """

    response = Response()
    response.text = "Show IP interface brief with Paramiko\n"
    response.text = paramik()
    
    return response 
    
    


        




# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
bot.add_command(
    "arp list", "See what ARP entries I have in my table.", arp_list)
bot.add_command(
    "system info", "Checkout the device system info.", sys_info)
bot.add_command(
    "show interfaces", "List all interfaces and their IP addresses", get_int_ips)
bot.add_command("attachmentActions", "*", useless.handle_cards)
bot.add_command("showcard", "show an adaptive card", useless.show_card)
bot.add_command("dosomething", "help for do something", useless.do_something)
bot.add_command("time", "Look up the current time", useless.current_time)
bot.add_command("monitor interfaces", "This job will monitor interface status in back ground", monitor_int)
bot.add_command("stop monitoring", "This job will stop all monitor job", stop_monitor)
bot.add_command("sh int br", "View Router 2 'sh ip int br' output using Paramiko", paramik_skill)
# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)