
#Author:  Darren Smith
#Date:  04/12/2012
#Purpose:  Dump threads for clustered JVMs.  Must be executed as wasuser.


#LIST OF NODES TO SKIP
skippedNodeList = [ "WC_cve_node_05", "WC_cve_node_nd" ]

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
#GENERATE THREAD DUMP

def dumpThreads(x,y):
	serverJVM = AdminControl.queryNames("type=JVM,process="+x+",node="+y+",*")

	print "Producing thread dump."
	AdminControl.invoke(serverJVM,"dumpThreads")

	print "Producing heap dump."
        AdminControl.invoke(serverJVM,"generateHeapDump")

	print "Thread and Heap dumps complete, check profile home for resulting file."
		

#--------------------------------------------------------------------------------------#
#MAIN

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
	print "node is " + node
	print "server is " + server

	#SKIP NODE
	if node in skippedNodeList:
		print "Skipping " + node + "\n"	
	else:

		#GET MBEAN FOR SERVER OBJECT - THERE WILL BE MBEAN FOR RUNNING SERVERS ONLY
		s1 = getMBean(cell, node, server) 

		if len(s1)>0:
			curState = getStatus(s1)
			print "curstate is " + curState

			if curState == 'STARTED':
				dumpThreads(server, node)



