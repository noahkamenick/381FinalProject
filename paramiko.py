import paramiko
import time
import getpass

# creating an ssh client object
ssh_client = paramiko.SSHClient()
# print(type(ssh_client))
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Saves SSH key for first time if needed
###password = getpass.getpass('Enter Password:')
router = {'hostname': '192.168.122.10', 'port': '22', 'username': 'cisco', 'password': 'passwd'}

print(f'Connecting to {router["hostname"]}')

#error occurs here, grabing from the router
ssh_client.connect(**router, look_for_keys=False, allow_agent=False) # Grabs keys and values from router dictionary (double asterisk is key and value)


# checking if the connection is active
if ssh_client.get_transport().is_active():
    print(router['hostname'], 'is connected')

shell = ssh_client.invoke_shell() #Create Shell object
shell.send('enable\n')
shell.send(password)
shell.send('\n')
shell.send('terminal length 0\n')
shell.send('show int br\n')


time.sleep(3)
output = shell.recv(10000)
output = output.decode('utf-8')
print(output)

if print(ssh_client.get_transport().is_active()) == True:
    print('Closing connection')
    ssh_client.close()
