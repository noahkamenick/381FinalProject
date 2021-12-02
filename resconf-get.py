# This is for getting the ip address of CSR2 VPN interface.
import json
import requests
requests.packages.urllib3.disable_warnings()

api_url = "https://192.168.56.120/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface=GigabitEthernet2?fields=ipv4"
headers = { "Accept": "application/yang-data+json",
"Content-type":"application/yang-data+json"
}
basicauth = ("cisco", "cisco123!")
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
# print(resp)
# The following block formats output to give just the ipv4 address
response_json = resp.json()
json_object = json.loads(json.dumps(response_json, indent=4))
ipv4List = (json_object["Cisco-IOS-XE-interfaces-oper:interface"])

def Gi2_address():
    print(ipv4List["ipv4"])

Gi2_address()
#end of file