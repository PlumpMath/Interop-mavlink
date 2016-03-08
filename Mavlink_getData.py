import time
from pymavlink import mavutil

def getMavlinkData():
	data = mavutil.mavlink_connection('udp:localhost:14551', planner_format=False,
                                  notimestamps=True,
                                  robust_parsing=True)
	msg = data.recv_match();
	#If we have a valid message
	if msg is not None:
		#print msg.get_type()
		if msg.get_type() is "VFR_HUD":
			altitude_msl = msg.alt * 3.28084		# convert from meter to feet
		elif msg.get_type() is "GLOBAL_POSITION_INT":
			latitude = msg.lat / 10000000.0			# Latitude, expressed as degrees * 1E7
			longitude = msg.lon / 10000000.0		# Longitude, expressed as degrees * 1E7
			uas_heading = msg.hdg / 100.0			# Vehicle heading (yaw angle) in degrees * 100
	
	return {'latitude':latitude, 'longitude':longitude ,'altitude_msl':altitude_msl, 'uas_heading':uas_heading }