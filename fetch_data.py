import time
import requests
import json
import csv
import os
import socket
controller_ip_address = socket.gethostbyname(socket.gethostname())
#controller_ip_address = "10.0.0.3"
# Number of attached plugs 
l = requests.post("http://"+controller_ip_address+":8083/ZWaveAPI/CallForAllNIF",auth=("admin","password"))
nodes = len(l.json()['result'])
node_ids =[]
for i in range(nodes):
	node_ids.append(l.json()["result"][i]["nodeId"])
# For each appliance create separte csv file
#filename = "data_file.csv"
fileheader = ['plug_timestamp','value','controller_timestamp']
for filename in range(len(node_ids)):
	if os.path.exists(node_ids[filename]+".csv"):
		mode = 'a'
	else:
		with open(node_ids[filename]+".csv",'w') as f:
			writer = csv.writer(f)
			writer.writerow(fileheader)	
			mode = "w"
end_time = time.time() + 1*2*60 # collect data for for one hour
set_time = time.time()
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
while (set_time <= end_time):
	for plug  in range(len(node_ids)):
		plug_no = node_ids[plug]
		url1 = "http://"+controller_ip_address+":8083/ZWaveAPI/Run/devices["+plug_no+"].instances[0].commandClasses[50].Get()"
		
		r = requests.post(url1, headers = headers, auth = ("admin","password"))
		url2 = "http://"+controller_ip_address+":8083/ZWaveAPI/Run/devices["+plug_no+"].instances[0].commandClasses[50].data"
		r = requests.post(url2, headers = headers, auth = ("admin","password"))
		#rows: device timestamp, device value, units, my timestamp
		plug_timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(r.json()['2']['val']['updateTime']))
		controller_timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		#my_row = [r.json()['2']['val']['updateTime'],r.json()['2']['val']['value'],r.json()['2']['scaleString']['value'], int(time.time()) ]
		my_row = [plug_timestamp,r.json()['2']['val']['value'], controller_timestamp]
		val2 = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(r.json()['2']['val']['updateTime']))
		print(r.json()['2']['val']['value'])
		print(val2)
		with open(plug_no+".csv", 'a') as f:
			writer = csv.writer(f)
			writer.writerow(my_row)
	time.sleep(60) # delay of 1 minute
	set_time = time.time()