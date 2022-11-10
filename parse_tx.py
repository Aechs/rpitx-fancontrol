# Python rpitx fan control (sendook needs root permissions to run)
import RPi.GPIO as GPIO
import time
import os
import sys

# This program takes 2 arguments, the fan ID and control code, and sends remote commands over 304.2MHz using rpitx/sendook -> https://github.com/F5OEO/rpitx
# The command "python parse_tx.py K 1" would set the fan marked 'K' to speed 1
# More info about the fan here -> https://yourceilingfan.com/harbor-breeze-ceiling-fan-parts/harbor-breeze-ceiling-fan-remotes/
# The fan codes were obtained by using a sdr (tv tuner) set to record buttons of a fan remote and decoding the results to binary data after removing carrier of '10_'

def add_carrier(cxs): #Adds '10_' carrier to input
	outData = ""
	for i in range(0, len(cxs)):
		outData = outData +"10"+cxs[i]
	return(outData)

def sendrpitx(tid, tdat):
	TXid = ""
	TXdat = ""
	msgLen = 6
	# Fan IDs (first 16 bits) - Place all fan IDs here with a letter
	if tid.find("H") == 0: #Hallway fan 
		TXid = "00000110001111100" 
	if tid.find("K") == 0: #Kitchen Fan
		TXid = "0011010000110000" 
	if tid.find("F") == 0: #Bedroom 1 fan
		TXid = "0111010101100001"
	if tid.find("S") == 0: #Bedroom 2 fan
		TXid = "1001010100110001"

	# Fan Control codes (last 8 bits)
	if tdat.find("L") == 0: #Light
		TXdat = "010111110"
	if tdat.find("D") == 0: #Dimm Light
		TXdat = "010111110"	
		msgLen = 50
	if tdat.find("0") == 0: #Fan Speeds 0->3
		TXdat = "110111110"
	if tdat.find("1") == 0:
		TXdat = "101111110"  
	if tdat.find("2") == 0:
		TXdat = "011111110" 
	if tdat.find("3") == 0:
		TXdat = "001111110" 
	
	#print(TXdat+" "+TXid))
	if TXdat == "" or TXid == "":
		print("Improper keycode specfied for TX")
	else:
		# Send 304.2MHz on/off keyed message with 400us timings repeated 6 times with 10ms pause
		os.system('sudo /home/user/rpitx/sendook -f 304200000 -0 400 -1 400 -p 10000 -r '+str(msgLen)+" "+add_carrier(TXid) +add_carrier(TXdat))
	print(add_carrier(TXid)+" "+add_carrier(TXdat))

#if __name__ == "__main__":
#	sendrpitx(str(sys.argv[1]), str(sys.argv[2]))

sendrpitx(str(sys.argv[1]), str(sys.argv[2]))
