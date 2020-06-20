from os import path
from qhue import Bridge, QhueException, create_new_username
import discoverhue,csv,json,os,random,time,os

#https://pypi.org/project/discoverhue/
#https://github.com/studioimaginaire/phue

# the path for the username credentials file
CRED_FILE_PATH = "qhue_username.txt"

def Get_Bridge_IP():
    # the IP address of your bridge
    found = discoverhue.find_bridges()
    for bridge in found: 
        ip = found[bridge]
    ip = ip.replace("http://","")
    ip = ip.replace(":80/","")
    return ip

def Get_Username(ip):
    if not path.exists(CRED_FILE_PATH):
        with open(CRED_FILE_PATH, "w") as csv_file:
            fieldnames = ['ip','username']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    # check for a credential file
    found = False  
    cred_file = open(CRED_FILE_PATH)
    csv_file = csv.reader(cred_file)  
    for row in csv_file:
        if ip in row:
            username = row[1]   
            found = True
            break
    
    if found == True:
        return username
    else:
        try:
            username = create_new_username(ip)
        except QhueException as err:
            print("Error occurred while creating a new username: {}".format(err))
            os.system("LED M SOLID")
        
        with open(CRED_FILE_PATH, "a") as csv_file:
            fieldnames = ['ip','username']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'ip': ip, 'username': username})

        os.system("LED G SUCCESS")
        return username

def Get_LightInfo():
    lights = {}
    lights = bridge.lights
    with open('lights.json', 'w') as outfile:
        json_lights = json.dumps(lights(), indent=4)
        json.dump(lights(), outfile)
    
    json_item = json.loads(json_lights)
    os.system("LED FINISH")
    return len(json_item)
    

def Start_Rave(light):
    print("Press Ctrl-C to terminate the rave!")
    try:
        while True:
            bridge.lights[random.randint(1,light)].state(on=True, sat=random.randint(0,254), bri=254,hue=random.randint(0,65535))
            time.sleep(.1)
    except KeyboardInterrupt:
        os.system('clear')
        pass   
    

#Gets Bridge IP
BRIDGE_IP = Get_Bridge_IP()
#Get Bridge Username
username = Get_Username(BRIDGE_IP)
#Creates Bridge Connection
bridge = Bridge(BRIDGE_IP, username)
#Gets Number of Lights
num_lights = Get_LightInfo()

Start_Rave(num_lights)