import paramiko

def vpn_command(prev_ip, new_ip):

    ssh_client = paramiko.SSHClient()

    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    router = {'hostname': '192.168.56.110', 'port': '22', 'username': 'cisco', 'password': 'cisco123!'}

    ssh_client.connect(**router, look_for_keys=False, allow_agent=False) # Grabs keys and values from router dictionary (double asterisk is key and value)
    
    print(f'Connecting to {router["hostname"]}')

    if ssh_client.get_transport().is_active():
        print(router['hostname'], 'is connected')
    
    shell = ssh_client.invoke_shell() #Create Shell object

    shell.send('enable\n')
    shell.send('terminal length 0\n')
    shell.send('configure terminal\n')

    shell.send('crypto isakmp key cisco address {}\n'.format(new_ip))     # Remove and replace VPN commands with new IP
    shell.send('no crypto isakmp key cisco address {}\n'.format(prev_ip))
    
    shell.send('crypto map Crypt 10 ipsec-isakmp\n')
    shell.send('no set peer {}\n'.format(prev_ip))
    shell.send('set peer {}\n'.format(new_ip))
    shell.send('exit\n')

    

    if print(ssh_client.get_transport().is_active()) == True:
        print('Closing connection')
        ssh_client.close()

    return str("\nExecuted VPN Peer IP Change") #