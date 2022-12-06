import os

devices = []
for device in os.popen('arp -a'): 
    devices.append(device)
    print(device)

