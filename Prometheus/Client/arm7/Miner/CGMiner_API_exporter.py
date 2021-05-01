# Copyright 2013 Setkeh Mkfr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.  See COPYING for more details.

#Short Python Example for connecting to The Cgminer API
#Written By: setkeh <https://github.com/setkeh>
#Thanks to Jezzz for all his Support.
#NOTE: When adding a param with a pipe | in bash or ZSH you must wrap the arg in quotes
#E.G "pga|0"

#Sript furhter modified by jostholm to export information from multiple ASIC USB miners
#Remember to add <"api-listen" : true> at the end of the cgminer .conf file

import socket
import json
import sys
import prometheus_client
import time

UPDATE_PERIOD = 15
lastWellPrevious=0
##__SUMMARY__#

FoundBlocks=prometheus_client.Gauge('miner_Found_Blocks','Indication if a block was found')
totalMHS5s=prometheus_client.Gauge('miner_tot_MHS_5s','Total MH/s')
totalTimeElapsed=prometheus_client.Gauge('miner_tot_time_elapsed','Total Uptime')
totalaccpted=prometheus_client.Gauge('miner_tot_accepted_shares','Total Accepted Shares')
totalRejected=prometheus_client.Gauge('miner_tot_Rejected_shares','Total Rejected Shares')
totalHardwareErrors=prometheus_client.Gauge('miner_tot_HrdWare_Errors','Total Miner Hardware Errors')
totalPoolsStalePct=prometheus_client.Gauge('miner_tot_Pool_Stale','Pool Stale indication')
totalGetWorks=prometheus_client.Gauge('miner_tot_GetWorks','Amount of GetWorks done')
totalBestShare=prometheus_client.Gauge('miner_tot_BestShare','Best Share since Start')
totalLastGetWork=prometheus_client.Gauge('miner_tot_LastGetWork','Timestamp of last Get Work')

#__NOTIFY__#




LastWell = prometheus_client.Gauge('miner_notify_lastWell','Timestamp of Last Well',['id'])
LastNotWell = prometheus_client.Gauge('miner_notify_lastNotWell','Timestamp of Last not Well',['id'])
ThreadFailInit = prometheus_client.Gauge('miner_notify_threadFailInit','Thread Failing Initialization',['id'])
DevSickIdle= prometheus_client.Gauge('miner_notify_devSickIdle','Device Sick Idle',['id'])
DevSickThermalCutoff = prometheus_client.Gauge('miner_notify_DevScikThermalCutoff','Sick Thermal Cutoff',['id'])
ThreadZeroHash = prometheus_client.Gauge('miner_notify_ThreadZeroHash','Thread Zero Hash',['id'])
ThreadFailQueue= prometheus_client.Gauge('miner_notify_threadFailQueue','Thread Fail Queue',['id'])
DevNoStart= prometheus_client.Gauge('miner_notify_noStart','Device not Starting',['id'])
DevDeadIdle60s= prometheus_client.Gauge('miner_notify_DeviceDeadIdle600s','Device dead Idling more than 600s',['id'])
DevOverHeat= prometheus_client.Gauge('miner_notify_DevOverheat','Device Over Heating',['id'])
DevComsError= prometheus_client.Gauge('miner_notify_DeviceComsError','Device Coms Error',['id'])






#__DEVS__#
asc_hashrate = prometheus_client.Gauge('miner_hshrte','current hashrate of the asc',['id'])
accepted_difficulty = prometheus_client.Gauge('miner_accDiff','Accepted Difficulty of this miner',['id'])
status = prometheus_client.Gauge('miner_stat','current status of the asc',['id'])
accepted = prometheus_client.Gauge('miner_accptd','accepted shares from this asc',['id'])
rejected = prometheus_client.Gauge('miner_rjectd','rejected shares of the asc',['id'])
upTime  = prometheus_client.Gauge('up_Time','Time passed since start',['id'])


if __name__ == '__main__':
    prometheus_client.start_http_server(9989)

while True:
	def linesplit(socket):
	        buffer = socket.recv(4096)
	        done = False
	        while not done:
	                more = socket.recv(4096)
	                if not more:
	                        done = True
	                else:
	                        buffer = buffer+more
	        if buffer:
	                return buffer

	api_command = 'devs+summary+notify'


	api_ip = '127.0.0.1'
	api_port = 4028


	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((api_ip,int(api_port)))

	s.send(json.dumps({"command":api_command}))

	response = linesplit(s)
	response = response.replace('\x00','')
	response = json.loads(response)
	#print response
	#print "this is the api_command place 0:",api_command[0]
	#print "this is the api command: ", api_command

	for dev in response['summary'][0]['SUMMARY']:
		fndBlocks=dev['Found Blocks']
		totMHS5s=dev['MHS 5s']
		totTimeElapsed=dev['Elapsed']
		totaccpted=dev['Accepted']
		totRejected=dev['Rejected']
		totHardwareErrors=dev['Hardware Errors']
		totPoolsStalePct=dev['Pool Stale%']
		totGetWorks=dev['Getworks']
		totBestShare=dev['Best Share']
		totLastGetWork=dev['Last getwork']

		FoundBlocks.set(fndBlocks)
		totalMHS5s.set(totMHS5s)
		totalTimeElapsed.set(totTimeElapsed)
		totalaccpted.set(totaccpted)
		totalRejected.set(totRejected)
		totalHardwareErrors.set(totHardwareErrors)
		totalPoolsStalePct.set(totPoolsStalePct)
		totalGetWorks.set(totGetWorks)
		totalBestShare.set(totBestShare)
		totalLastGetWork.set(totLastGetWork)

	#id2=response['notify'][0]['NOTIFY'][0]['ID']
	#print "ID2 : ", id2
	for dev in response['notify'][0]['NOTIFY']:
		id=dev['ID']
		lastWell=dev['Last Well']
		if (lastWell > lastWellPrevious):
			lastWellNew=lastWell
			lastWellPrevious=lastWell
		else:
			lastWellNew=lastWellPrevious

		lastNotWell=dev['Last Not Well']
		threadFailInit=dev['*Thread Fail Init']
		devSickIdle=dev['*Dev Sick Idle 60s']
		devSickThermalCutoff=dev['*Dev Thermal Cutoff']
		threadZeroHash=dev['*Thread Zero Hash']
		threadFailQueue=dev['*Thread Fail Queue']
		devNoStart=dev['*Dev Nostart']
		devDeadIdle60s=dev['*Dev Dead Idle 600s']
		devOverHeat=dev['*Dev Over Heat']
		devComsError=dev['*Dev Comms Error']

		LastWell.labels(id).set(lastWellNew)
		LastNotWell.labels(id).set(lastNotWell)
		ThreadFailInit.labels(id).set(threadFailInit)
		DevSickIdle.labels(id).set(devSickIdle)
		DevSickThermalCutoff.labels(id).set(devSickThermalCutoff)
		ThreadZeroHash.labels(id).set(threadZeroHash)
		ThreadFailQueue.labels(id).set(threadFailQueue)
		DevNoStart.labels(id).set(devNoStart)
		DevDeadIdle60s.labels(id).set(devDeadIdle60s)
		DevOverHeat.labels(id).set(devOverHeat)
		DevComsError.labels(id).set(devComsError)




	for dev in response['devs'][0]['DEVS']:
		id=dev['ID']
		hshrte=dev['MHS 5s']
		accDiff=dev['Difficulty Accepted']
		stat=dev['Status']
		up_Time=dev['Device Elapsed']
		if(stat=='Alive'):
			statInt=1
		else:
			statInt=0
		accptd=dev['Accepted']
		rjectd=dev['Rejected']

		asc_hashrate.labels(id).set(hshrte)
		accepted_difficulty.labels(id).set(accDiff)
		status.labels(id).set(statInt)
		accepted.labels(id).set(accptd)
		rejected.labels(id).set(rjectd)
		upTime.labels(id).set(up_Time)
	s.close()
	time.sleep(UPDATE_PERIOD)
