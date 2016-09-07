
#Author:  Darren Smith
#Date:  04/12/2012
#Purpose:  Selectively restarts application servers in a cluster, skipping servers specfied.  Must be executed as wasuser2.


import time
#LIST OF NODES TO SKIP
skippedNodeList = [ 'cvas_node2', 'WC_cve_node_05' ]

#--------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
	logfile = open('/backup/ecomm/sysadm/jython/b2c_CVWEB_restart.log', 'a')
	logfile.write(x)
	logfile.close()


#--------------------------------------------------------------------------------------#
#GET SERVER MBEAN

def getMBean(x,y,z):
	return AdminControl.completeObjectName('cell='+ x +',node='+ y +',name='+ z +',type=Server,*') 


#--------------------------------------------------------------------------------------#
#GET SERVER STATUS

def getStatus(x):
	status = AdminControl.getAttribute(s1, "state")
        while status !='STARTED':
        	status = AdminControl.getAttribute(s1, "state")
	return status

#--------------------------------------------------------------------------------------#
#RESTART SERVER

def restartServer(x):
	AdminControl.invoke(x, 'restart', '[]', '[]')
	msg1 = "Waiting... " + "\n"
	print msg1
	logger(msg1)
	time.sleep(200)
        result = getStatus(x)		
	print "result is " + result + "\n"
	logger(result)
	
#--------------------------------------------------------------------------------------#
#MAIN

from time import strftime
now = strftime("%Y-%m-%d %H:%M:%S") 
formatNow = now + "\n"
logger("---------------------------")
logger(formatNow)

#SET CONSTANT OF CLUSTER NAME
cluster="WC_cve_cluster"

#GET CELL NAME
cell = AdminControl.getCell()
#print "cell is " + cell

#GET CLUSTER ID
clusterId = AdminConfig.getid('/Cell:'+ cell +'/ServerCluster:'+ cluster + '/')
#print "clusterId is " + clusterId

#GET CLUSTER MEMBERS - WILL BE APP SERVERS ONLY
memberList = AdminConfig.showAttribute(clusterId, "members")
#print "memberList is " + memberList

#PARSE MEMBERS
members = memberList[1:len(memberList)-1]
#print "members are " + members

#GET NODE NAME, SERVER NAME, AND SERVER ID
for member in members.split():
	node = AdminConfig.showAttribute(member, "nodeName")
	server = AdminConfig.showAttribute(member, "memberName")
	#serverId = AdminConfig.getid('/Cell:'+ cell +'/Node:'+ node +'/Server:'+ server +'/') 
	#print "node is " + node
	#print "server is " + server

	#SKIP NODE
	if node in skippedNodeList:
		print "Skipping " + node	
	else:

		#GET MBEAN FOR SERVER OBJECT - THERE WILL BE MBEAN FOR RUNNING SERVERS ONLY
		s1 = getMBean(cell, node, server) 

		if len(s1)>0:
			curState = getStatus(s1)

			if curState == 'STARTED':
				msg = "The current state of " + node + " " + server + " is " + curState + " , Restarting..." + "\n"
				print msg
				logger(msg) 
				restartServer(s1)


