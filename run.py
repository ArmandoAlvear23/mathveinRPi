from pulsesensor import Pulsesensor
import requests
import json
import time
import datetime

p = Pulsesensor()
p.startAsyncBPM()
url = "https://aa1191.000webhostapp.com/scripts/monitor_mode_rpi.php"
sr1 = "==========Server Response at "
sr2 = "=========="
sr3 = "++++++++++Server Request Successful!++++++++++"
statusMessage = "Monitor Mode Status: "
mmStart = "Starting Monitor Mode..."
mmEnd = "Ending Monitor Mode..."

try:
	while True:
		func = 1
		userID = 1
		data={'user_id': userID,'func': func}
		res = requests.post(url, json=data)
		r = res.json()

		ts = datetime.datetime.now()
		print sr1+ str(ts) + sr2
		error = r['error']	
		mmStatus = r['monitor_mode']
		print error
		print statusMessage + mmStatus

		if (error == 0):
			print sr3
			print statusMessage + mmStatus

			if (mmStatus == 1):
				print mmStart
				func = 2
				data={'user_id': userID, 'func': func}
				res = requests.post(url, json=data)
				r = res.json()

				ts = datetime.datetime.now()
				print sr1 + str(ts) + sr2
				error = r['error']

				if error == 0:
					bpmCount = r['bpm_counter']
					bpm1 = r['bpm1']
					bpm2 = r['bpm2']
					bpm3 = r['bpm3']
					nif = r['no_input_flag']

					if nif == 0:
						if bpmCount == 1:
							func=3
							bpm = p.BPM
							if bpm > 0:
								print("BPM: %d" %bpm)
							else:
								print("No Heartbeat found")
							bpm1 = bpm
							bpmCount = 2
							if bpm2==0 and bpm3==0:
								bpmAvg = bpm1
							else:
								bpmAvg = (bpm1+ bpm2 + bpm3)/3
							data={'user_id': userID,'func': func,'bpm_counter': bpmCount,'bpm1': bpm1,'bpm_average': bpmAvg}
							res = requests.post(url, json=data)
							r = res.json()
							#time.sleep(5)
						elif bpmCount == 2:
							func=4
							bpm = p.BPM
							if bpm > 0:
								print("BPM: %d" %bpm)
							else:
								print("No Heartbeat found")
							bpm2 = bpm
							bpmCount = 3
							if bpm3 == 0:
								bpmAvg = (bpm1 + bpm2)/2
							else:
								bpmAvg = (bpm1 + bpm2 + bpm3)/3
							data={'user_id': userID,'func': func,'bpm_counter': bpmCount,'bpm2': bpm2,'bpm_average': bpmAvg}
							res = requests.post(url, json=data)
							r = res.json()
							#time.sleep(5)
						elif bpmCount == 3:
							func=5
							bpm = p.BPM
							if bpm > 0:
								print("BPM: %d" %bpm)
							else:
								print("No Heartbeat found")
							bpm3 = bpm
							bpmCount = 1
							bpmAvg = (bpm1 + bpm2 + bpm3)/3
							data={'user_id': userID,'func': func, 'bpm_counter': bpmCount, 'bpm3': bpm3, 'bpm_average': bpmAvg}	
							res = requests.post(url, json=data)
							r = res.json()
							#time.sleep(5)
					else:
						print "Error: no-input flag detected %d " %nif						
				else:
					print "Error: %d" %error
			else:
				print statusMessage + mmStatus
				print mmEnd 
		else:
			print "Error: %d" %error
	time.sleep(5)
	print("sleeping for 5 seconds...")


except:
p.stopAsyncBPM()

