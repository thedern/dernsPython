
# Author:  Darren Smith
# Date:  04/12/2012
# Purpose:  Selectively restarts application servers in a cluster,
# skipping servers specfied.  Must be executed as wasuser2.

import sys
import smtplib
import time

#--------------------------------------------------------------------------------------#
# LIST OF NODES TO SKIP

skippedNodeList = ['WC_cve_node_02']

#--------------------------------------------------------------------------------------#
# EMAIL CONSTANTS

MSERVER = "mailrelay.corp.advancestores.com"
FROM = "WCAPPSTG01@advancestores.com"
TO = ["ecomm_infra@advance-auto.com"]
SUBJECT = "RESTARTING WCAPPSTG01"
TEXT = "Logged output: /backup/ecomm/sysadm/jython/b2c_wcappstg01_restart.log"

#--------------------------------------------------------------------------------------#
# LOGGER


def logger(x):
    logfile = open(
        '/backup/ecomm/sysadm/jython/b2c_wcappstg01_restart.log', 'a')
    logfile.write(x)
    logfile.close()


#--------------------------------------------------------------------------------------#
# GET SERVER MBEAN

def getMBean(x, y, z):
    return AdminControl.completeObjectName('cell=' + x + ',node=' + y + ',name=' + z + ',type=Server,*')


#--------------------------------------------------------------------------------------#
# GET SERVER STATUS

def getStatus(x):
    status = AdminControl.getAttribute(s1, "state")
    while status != 'STARTED':
        status = AdminControl.getAttribute(s1, "state")
    return status

#--------------------------------------------------------------------------------------#
# RESTART SERVER


def restartServer(x):
    AdminControl.invoke(x, 'restart', '[]', '[]')
    msg1 = "Waiting... " + "\n"
    logger(msg1)
    time.sleep(200)
    result = getStatus(x)
    logger(result)
    return result

#--------------------------------------------------------------------------------------#
# MAIN

from time import strftime
now = strftime("%Y-%m-%d %H:%M:%S")
formatNow = now + "\n"
logger("---------------------------")
logger(formatNow)

message =  """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
mserver = smtplib.SMTP(MSERVER)
mserver.sendmail(FROM, TO, message)
mserver.quit()
sys.exit


# SET CONSTANT OF CLUSTER NAME
cluster = "WC_cve_cluster"

# GET CELL NAME
cell = AdminControl.getCell()
# print "cell is " + cell

# GET CLUSTER ID
clusterId = AdminConfig.getid(
    '/Cell:' + cell + '/ServerCluster:' + cluster + '/')
# print "clusterId is " + clusterId

# GET CLUSTER MEMBERS - WILL BE APP SERVERS ONLY
memberList = AdminConfig.showAttribute(clusterId, "members")
# print "memberList is " + memberList

# PARSE MEMBERS
members = memberList[1:len(memberList) - 1]
# print "members are " + members

# GET NODE NAME, SERVER NAME, AND SERVER ID
for member in members.split():
    node = AdminConfig.showAttribute(member, "nodeName")
    server = AdminConfig.showAttribute(member, "memberName")
    #serverId = AdminConfig.getid('/Cell:'+ cell +'/Node:'+ node +'/Server:'+ server +'/')
    # print "node is " + node
    # print "server is " + server

    # SKIP NODE
    if node in skippedNodeList:
        # print "Skipping " + node
        pass
    else:

        # GET MBEAN FOR SERVER OBJECT - THERE WILL BE MBEAN FOR RUNNING SERVERS
        # ONLY
        s1 = getMBean(cell, node, server)

        if len(s1) > 0:
            curState = getStatus(s1)

            if curState == 'STARTED':
                msg = "The current state of " + node + " " + server + \
                    " is " + curState + " , Restarting..." + "\n"
                logger(msg)
                restartServer(s1)
