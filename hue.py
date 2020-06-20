from os import path
from qhue import Bridge, QhueException, create_new_username
import discoverhue,csv,json,os,random,time

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
        
        with open(CRED_FILE_PATH, "a") as csv_file:
            fieldnames = ['ip','username']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'ip': ip, 'username': username})

        return username

def Get_LightInfo():
    lights = {}
    lights = bridge.lights
    with open('lights.json', 'w') as outfile:
        json_lights = json.dumps(lights(), indent=4)
        json.dump(lights(), outfile)
    print(json_lights)

def Start_Rave(light):
    print("Press Ctrl-C to terminate the rave!")
    try:
        while True:
            bridge.lights[random.randint(1,light)].state(on=True, sat=random.randint(0,254), bri=254,hue=random.randint(0,65535))
            time.sleep(.1)
    except KeyboardInterrupt:
        os.system('clear')
        pass   

def Turn_Off(lights):
    for x in range(lights):
        light = x + 1
        bridge.lights[light].state(on=False)

def Turn_On(lights):
    for x in range(lights):
        light = x + 1
        bridge.lights[light].state(on=True)

def menu():
    os.system('clear')
    ans=True
    while ans:
        print('Bridge IP {ip} and Username {UN}'.format(ip=BRIDGE_IP, UN=username))
        print ("""
1. View Light Info
2. Start Rave
3. Turn Off All Lights
4. Turn On All Lights
5. View Creds File
6. Exit Program
        """)
        ans=input("What would you like to do? ") 
        if ans=="1": 
            Get_LightInfo()
            input("Press Enter to continue...")
            menu()
        elif ans=="2":
            num_lights = int(input("Enter the number of hue lights:"))
            Start_Rave(num_lights)
            input("Press Enter to continue...")
            menu()
        elif ans=="3":
            num_lights = int(input("Enter the number of hue lights:"))
            Turn_Off(num_lights)
            input("Press Enter to continue...")
            menu()
        elif ans=="4":
            num_lights = int(input("Enter the number of hue lights:"))
            Turn_On(num_lights)
            input("Press Enter to continue...")
            menu()
        elif ans=="5":
            Creds = open(CRED_FILE_PATH, "r")
            for line in Creds:
                print(line)
            input("Press Enter to continue...")
            menu()
        elif ans=="6":
            exit()   
        elif ans !="":
            print("\n Not Valid Choice Try again")
            input("Press Enter to continue...")
            menu() 


#Gets Bridge IP
BRIDGE_IP = Get_Bridge_IP()
#Get Bridge Username
username = Get_Username(BRIDGE_IP)
#Creates Bridge Connection
bridge = Bridge(BRIDGE_IP, username)

menu()
