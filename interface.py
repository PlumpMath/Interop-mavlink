import argparse
import requests
from dronekit import connect, VehicleMode
import time

parser = argparse.ArgumentParser()
parser.add_argument("server", help="interop server address ex: 192.168.1.2:8080")
parser.add_argument("user", help="username")
parser.add_argument("pas", help="password")
args = parser.parse_args()

cookie = ""

def login():
	global cookie
	print "Logging in..."
	while True:
		try:
			r = requests.post('http://'+args.server+'/api/login',data={'username': args.user, 'password': args.pas}, timeout=5)
			if r.status_code == 200:
				print "Login Sucessfull!\n"
				#print r.cookies['sessionid']
				cookie = r.cookies
				break
			print r
		except requests.exceptions.ConnectionError:
			print "ConnectionError: Invalid url?"
		print "Login failed tring again...\n"

def server_info():
	print "Server info:"
	try:
		r = requests.get('http://'+args.server+'/api/server_info',cookies=cookie, timeout=5)
		if r.status_code == 200:
			for item in r.json():
				print item+": "+r.json()[item] 
			print ""
	except requests.exceptions.ConnectionError:
		print "ConnectionError: Invalid url?"

def send_telemetry(lat, lon, alt, head):
	#print "Send packet"
	try:
		r = requests.post('http://'+args.server+'/api/telemetry',data={'latitude': lat, 'longitude': lon, 'altitude_msl':alt ,'uas_heading':head}, timeout=5, cookies=cookie)
		if r.status_code == 200:
			pass
			#print "Sucessfull\n"
		elif r.status_code == 400:
			print "Invalid Telem Data\n"
	except requests.exceptions.ConnectionError:
			print "ConnectionError: Invalid url?\n"

if __name__ == '__main__':
	login()
	server_info()
	vehicle = connect('0.0.0.0:14450', wait_ready=True, rate=10)
	print "Sending Telemetry Data"
	while True:
		send_telemetry(vehicle.location.global_frame.lat,vehicle.location.global_frame.lon,vehicle.location.global_relative_frame.alt,vehicle.heading)