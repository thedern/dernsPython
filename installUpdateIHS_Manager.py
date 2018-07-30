
import subprocess
import time
import os
#import sys

#########################################################################################

#Darren, 4/25/2016

""" Using preconfigured responsefiles, this python program does the following:
1. checks for install manager and install it if not present.
2. installs IHS, Plugin, and WebSphere Configuration tool from the universal installers
3. updates the IHS and Plugin to FP7
4. updates the WCT to FP7
5. verifies the installation using the IBM versionInfo.sh script """

#########################################################################################

#Functions

def checkVersions():
    "Allows user to verify installs after FP"

    print "\n Verifying install and update."

    subprocess.call(["/optware/IBM/HTTPServer/V8/bin/versionInfo.sh"])
    time.sleep(2)
    subprocess.call(["/optware/IBM/Plugins/V8/bin/versionInfo.sh"])

def install85Components(responsefile, logfile):
    "installs IHS, PLG, WCT, and updates to FP7 in order"

    subprocess.call(["/opt/IBM/InstallationManager/eclipse/tools/imcl", "-acceptLicense", "-showProgress", "-input", responsefile, "-log", logfile])

def callCommand(hostOS):

    if hostOS == "LINUX": 
        print "\n Installing IHS, PLG, and WCT"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/install_IHS_response_file_LINUX.xml", "/var/temp/install_IHS_PLG_Tools.log")
        time.sleep(5)
        print "\n Updating IHS and PLG to FP7"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/update_IHS_PLG_FP7_response_file_LINUX.xml", "/var/temp/update_IHS_PLG_FP7.log")
        time.sleep(5)
        print "\n Updating WCT to FP7"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/update_WCT_FP7_response_file_LINUX.xml", "/var/temp/update_WCT_FP7.log")
        checkVersions()

    elif hostOS == "AIX":
        print "\n Installing IHS, PLG, and WCT"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/install_IHS_response_file_AIX.xml", "/var/temp/install_IHS_PLG_Tools.log")
        time.sleep(5)
        print "\n Updating IHS and PLG to FP7"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/update_IHS_PLG_FP7_response_file_AIX.xml", "/var/temp/update_IHS_PLG_FP7.log")
        time.sleep(5)
        print "\n Updating WCT to FP7"
        install85Components("/backup/ecomm/sysadm/was8_repo/responsefiles/update_WCT_FP7_response_file_AIX.xml", "/var/temp/update_WCT_FP7.log")
        checkVersions() 

def installManager(hostOS):
    """ The Install Manager was not deteted, installing.
        Then, proceed with IHS, PLG, and WCT install and upgrade."""

    print "\n Installing IBM Install Manager"

    if hostOS == "LINUX":
        subprocess.call(["/backup/ecomm/sysadm/was8_repo/WAS_V855_InstallManager_LINUX_V1.6.2/installc", "-acceptLicense", "-showProgress", "-log", "/var/temp/InstallManager.log"])
        callCommand(os)
    elif hostOS == "AIX":
        subprocess.call(["/backup/ecomm/sysadm/was8_repo/WAS_V855_InstallManager_AIX_V1.6.2/installc", "-acceptLicense", "-showProgress", "-log", "/var/temp/InstallManager.log"])
        callCommand(os)

def checkManager(hostOS):
    """ Check if the InstallManager is present """

    if os.path.isfile('/opt/IBM/InstallationManager/eclipse/tools/imcl') == True:
        print "IBM Install Manager found."
        return
    else:
        print "\n IBM Install Manager not detected"
        installManager(hostOS)

def verifyOS(hostOS):
    if hostOS == "LINUX" or hostOS == "AIX":
        print "\n OS is valid: ", hostOS
        return
    else:
        print "\n please enter either LINUX or AIX"
        userInput()

def userInput():

    opSystem = raw_input("Enter OS as LINUX or AIX:  " )

    #check user input as valid
    verifyOS(opSystem)

    #check for installManager
    print "\n Checking for IBM Install Manager"
    checkManager(opSystem)

    #Install Manager detected, install and upgrade IHS and related components.
    callCommand(opSystem)

#################################################################################################

#MAIN
    
print "installing 64bit v8.5.5 of IHS, PLG, WCT, and updating all to FP7 \n press [Enter] to continue; press [Ctrl-C] to quit" 
raw_input()

#gather user input
userInput()



