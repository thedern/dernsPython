"""
Author:  Darren Smith

Purpose: Deploys commerce application, restarts servers, and executes static content sync.  
         It can differentiate between prod and non-prod as well as between clustered and 
	 standalone environments.

Date:    7/9/2018

Notes:
cluster states 
'websphere.cluster.partial.start'
'websphere.cluster.partial.stop'
'websphere.cluster.running'
'websphere.cluster.stopped'

wsadmin evironment cannot utilize the python 'subprocess' module even if added to:
'/optware/IBM/WebSphere/V7/AppServer/optionalLibraries/jython/Lib' Perhaps a more modern version can.
Instead, 'os.system' is used to execute scripts versus running shell commands from this program.

"""
##################
#### MODULES #####
##################

import time
#WAS JYTHON CANNOT IMPORT datetime
#import datetime
import os
import sys

#dt = datetime.datetime.now().strftime("%m/%d/%y")

#CAPTURE SCRIPT START TIME
start_time = time.time()

#SCRIPT ARGUMENTS ARE BUILD DIR AND DEPLOY ENVIRONMENT
#BUILD DIR MUST BE ABSOLUTE PATH
from sys import argv
#'script' IS REMOVED FROM ARGV WHEN RUNNING VIA WSADMIN
#script, buildDir, targetEnv = argv
buildDir, targetEnv = argv

###################
#### FUNCTIONS ####
###################
#--------------------------------------------------------------------------------------#
#LOGGER

def logger(x):
	logfile = open('/home/wasuser2/b2c_CVWEB_restart.log', 'a')
	logfile.write(x)
	logfile.close()


#--------------------------------------------------------------------------------------#
#GET SERVER STATE
#TAKES SERVER MBEAN AS ARGUMENT

def getState(s1):
	#print "DEBUG Getting server state" 
	return AdminControl.getAttribute(s1, 'state')


#--------------------------------------------------------------------------------------#
#SHUTDOWN CLUSTER

def shutdownCluster(clusterBean):
	x = None
	#print "DEBUG Stopping Cluster"
	AdminControl.invoke(clusterBean, 'stop')
	#CHECK TO SEE CLUSTER HAS STOPPED
	while x != "websphere.cluster.stopped":
		time.sleep(10)
		x = AdminControl.getAttribute(clusterBean, 'state')
        	

#--------------------------------------------------------------------------------------#
#STARTUP CLUSTER 

def startupCluster(clusterBean):
	x = None
        #print "DEBUG Starting Cluster"
	AdminControl.invoke(clusterBean, 'start')
	#CHECK TO SEE IF CLUSTER HAS STARTED
	while x != "websphere.cluster.running":
		time.sleep(10)
		x = AdminControl.getAttribute(clusterBean, 'state')


#--------------------------------------------------------------------------------------#
#START PROD SERVERS
#ONLY SPECIFIC SERVERS ARE TO BE STARTED, CANNOT START WHOLE CLUSTER IN PROD

def startProdServers():
	prdServers1 = { 'WC_cve_node_nd' : 'server1', 'WC_cve_node' : 'server1',
		'WC_cve_node_02' : 'server1', 'WC_cve_node_03': 'server1',
		'WC_cve_node_04' : 'server1', 'WC_cve_node_05' : 'server1',
		'WC_cve_mode_06' : 'server1' } 
	
	prdServers2 = { 'WC_cve_mode_06' : 'server2' }

	#ITERATE THROUGH DICTIONARIES AND START SERVERS
	for key in prdServers1:
		AdminControl.startServer(key, prdServers1[key])

	for key in prdServers2:
		AdminControl.startServer(key, prdServers2[key])

	#time.sleep(600)


#--------------------------------------------------------------------------------------#
#START SERVER1 ON NODE1 ONLY

def startPrd04():
	prd04Servers1 = { 'WC_cve_node' : 'server1' }
	#ITERATE THROUGH DICTIONARIES AND START SERVERS
        for key in prd04Servers1:
                AdminControl.startServer(key, prd04Servers1[key])


#--------------------------------------------------------------------------------------#
#START NODE1 SERVER ONLY

def startLiveStage():
	LS_Servers1 = { 'WC_cve_node' : 'server1' }
	
	#LS_Servers2 = { 'WC_cve_node_02' : 'server1' }

	#ITERATE THROUGH DICTIONARIES AND START SERVERS
        for key in LS_Servers1:
                AdminControl.startServer(key, LS_Servers1[key])


#--------------------------------------------------------------------------------------#
#STARTUP STANDALONE SERVER
#TAKES SERVER AND NODE NAME AS ARGUMENT, MBEAN NOT REQUIRED

def startup(server, node):
        #print "DEBUG Starting server"
        AdminControl.startServer(server, node)


#--------------------------------------------------------------------------------------#
#SHUTDOWN STANDALONE SERVER
#TAKES SERVER NAME AS ARGUMENT, MBEAN NOT REQUIRED

def shutdown(server):
        #print "DEBUG Stopping server"
        AdminControl.stopServer(server,'immediate')


#--------------------------------------------------------------------------------------#
#GET APPLICAION STATUS

def appStatus():
	return AdminControl.completeObjectName('type=Application,name=WC_cve,*')


#--------------------------------------------------------------------------------------#
#DEPLOY APPLICATION

def deployApp(buildDir, targetEnv):
	buildDir = '/optware/IBM/WebSphere/V7/CommerceServer70/wcbd/dist/server/'+buildDir
	#print "DEBUG dir and target are %s %s" % (buildDir, targetEnv)
	#deployString = "'%s/wcbd-ant -buildfile wcbd-deploy.xml -Dtarget.env=%s'" % (buildDir, targetEnv)
        #os.system(deployString)
        os.system('%s/wcbd-ant -buildfile wcbd-deploy.xml -Dtarget.env=%s') % (buildDir, targetEnv)
	retCode = os.system('echo $?')
	#print "DEBUG return code is ", retCode

return retCode	
	

#--------------------------------------------------------------------------------------#
#GET HOSTNAME

def getHostname():
	return socket.gethostname()


#--------------------------------------------------------------------------------------#
#DEPLOY STATIC LOWER ENV

def deployStaticLower():
	os.system('/optware/scripts/static_contents/copy2web.sh')
	resultStatic = os.system('echo $?') 
        if resultStatic == 0:
                staticMessage = "static content push success \n"
                logger(staticMessage)
        else:
                staticMessage = "static push failed, please check \n"
                logger(staticMessage)


#--------------------------------------------------------------------------------------#
#DEPLOY STATIC PROD ENV

def deployStaticProd(Logger):
        os.system('/optware/scripts/static_contents_v7/prd2static_rsync.sh')
        resultStatic = os.system('echo $?')
	if resultStatic == 0:
        	staticMessage = "static content push success \n"
                logger(staticMessage)
        else:
        	staticMessage = "static push failed, please check \n"
                logger(staticMessage)

#--------------------------------------------------------------------------------------#
#######################
#### END FUNCTIONS ####
#######################


##############
#### MAIN ####
##############

logger("---------------------------")
#logger(dt)

#GET CELL NAME
cell = AdminControl.getCell()
#print "DEBUG cell is " + cell

#TEST TO SEE IF CLUSTER EXISTS BY OBTAINING CLUSTER_ID
clusterID = AdminConfig.list('ServerCluster', AdminConfig.getid( '/Cell:' + cell))
#print "DEBUG cluster name is " + clusterID

#CHECK IF CLUSTER EXISTS
if len(clusterID) > 0:
	#GET CLUSTERNAME ONLY - USES CLUSTERID
	clusterName =  AdminConfig.showAttribute(clusterID, 'name')
	#GET CLUSTER MBEAN - USES CELL AND CLUSTERNAME
	clusterBean = AdminControl.completeObjectName('cell='+cell+',type=Cluster,name='+clusterName+',*')
	#GET CLUSTER STATE - USES CLUSTERMBEAN
	clusterState  = AdminControl.getAttribute(clusterBean, 'state')

	if clusterState != 'websphere.cluster.stopped':
		#STOP CLUSTER BEFORE DEPLOY
		shutdownCluster(clusterBean)
		msgDown =  "cluster is down, deploying application \n"
		#print "DEBUG ", msgDown
		logger(msgDown)
		retCode = deployApp(buildDir, targetEnv)

		if retCode == 0:
			msgDeploySuccess =  "deploy successful \n"
			#print "DEBUG", msgDeploySuccess
			logger(msgDeploySuccess)
			#GET APPLICAION STATUS
			appCheck = appStatus()

			if len(appCheck) > 0:
				#CONDITIONAL STATEMENTS BASED ON HOSTNAME
				serverName =  getHostname()

				if serverName == "wcndprd01":
					startProdServers()
					deployStaticProd(Logger)
`
				elif serverName == "ecomdev04":
					startPrd04()
					deployStaticProd(Logger)

			 	elif serverName == "wcappstg01":		
					startLivStage()
					deployStaticProd(Logger)
				else:
					startupCluster(clusterBean)
					deployStaticLower(Logger)
				
			else:
				msgDeployFailed = "Length of appCheck is '0', deploy failed/application not running. Please check the logs \n"
				#print "DEBUG", msgDeployFailed
				logger(msgDeployFailed)
				sys.exit()
	else:
	#STANDALONE SERVER, NO CLUSTER

		#GET MBEAN FOR RUNNING SERVER
		s1 = AdminControl.completeObjectName('type=Server,*')
		if len(s1) < 0:
			#GET NODE NAME, NEEDED FOR STARTING SERVER ONLY
			node = AdminControl.getAttribute(s1, 'nodeName')
			#GET SERVER NAME, NEEED FOR STARTING AND STOPPING SERVER
			server1 =  AdminControl.getAttribute(s1, 'name')
			#GET SERVER STATE
			status1 = getState(s1)

			if status1  == 'STARTED':
				#DEPLOY APP
				retCode = deployApp(buildDir, targetEnv)

				if retCode == 0:
                        		msgDeploySuccess =  "deploy successful \n"
                        		logger(msgDeploySuccess)
      					msgStandAlone = "The current state of " + node + " " + server1 + " is " + status1 + " , Restarting..." + "\n"
                			#print "DEBUG", msgStandAlone
                			logger(msgStandAlone)
					#GET APPLICATION STATUS
					status2 = getState(s1)					

					if status2  == 'STARTED':
						#DEPLOY STATIC
						deployStaticLower(Logger)
                				#shutdown WILL WAIT FOR SERVER PROCESS TO DIE AND MBEAN DESTROYED
                				shutdownServer(server1)
                				#startup REQUIRES BOTH SERVER AND NODEdminControl.getAttribute(server, 'state')
                				startupServer(server1, node)
				else:
					msgDeployFailed = "deploy failed, please check the logs \n"
					#print "DEBUG", msgDeployFailed
                        		logger(msgDeployFailed)
                        		sys.exit()
		else:
			msgStandaloneNotRunning = "standalone applications server is not running, please start and redeploy \n"
			#print "DEBUG", msgStandaloneNotRunning
			logger(msgStandaloneNotRunning)
			sys.exit()
				
msgTime = ("EXECUTION TIME: \n --- %s seconds ---" % (time.time() - start_time))
#print "DEBUG", msgTime
logger(msgTime)
