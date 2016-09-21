
# Author:  Darren Smith
# Date:  04/10/2012
# Purpose:  Restarts the B2B Production cluster via the ripplestart
# command.  Must be executed as wasuser2.

import sys
import time
from time import strftime
# -----------------------------------


def logger(x):
    logfile = open('/backup/ecomm/sysadm/jython/b2b_ripplestart.log', 'a')
    logfile.write(x)
    logfile.close()

# -----------------------------------

# timestamp


now = strftime("%Y-%m-%d %H:%M:%S")
formatNow = now + "\n"
logger(formatNow)

startMsg = "B2B Ripplestart Initiated" + "\n"
errorMsg = "B2B Ripplestart Failed" + "\n" + "\n"
completeMsg = "B2B Ripplestart Completed" + "\n" + "\n"


logger(startMsg)

try:
    AdminControl.invoke(
        'WebSphere:name=WC_cve_cluster,process=dmgr,platform=common,node=prd1CellManager01,version=7.0.0.13,type=Cluster,mbeanIdentifier=WC_cve_cluster,cell=prd1Cell01,spec=1.0', 'rippleStart')
    logger(completeMsg)
except RuntimeError:
    logger(errorMsg)
