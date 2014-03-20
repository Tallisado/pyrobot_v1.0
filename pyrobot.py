# -*- coding: utf-8 -*-
#
 
# imports
from robot.running import TestSuite
from robot import utils
from robot.conf import settings
import os, glob
import subprocess
import time
from datetime import datetime
import sys
import getopt
import fileinput
import random
import PyrobotConfig as config
import string
import random
import shutil
 
from BrowserData import *
from SauceRest import *
 
class Jybot():
    """ Helper class to interact with RobotFrameworks pybot script to execute tests / test suites.    
    """
    name = ""
    tests = []
    suite = ""
    args = []
    output = ""
    process = -1
    running = False
    jyLogLoc = ""
   
    def __init__(self, name):
        """ Constructor, creates the object and assigns the given 'name'.
        """
        self.name = name
   
    def start(self, args=[]):
        """ Starts the pybot script from RobotFramework executing the given 'suite'.
        'args' (optional) is a list of additional parameters passed to pybot
        """
        self.suite = payload
        self.output_file = '%s_Output.xml' % self.name
        self.log_file = '%s_Log.html' % self.name 
        self.report_file = '%s_Report.html' % self.name

        self.jyLogLoc = os.path.join(workspace_home, ("%s_Stdout.txt" % self.name))
        jyLog = open(self.jyLogLoc, "w")        
        jybotCommand = "pybot --name %s --outputdir %s --output %s --log %s --report %s %s" % (self.name, workspace_home, self.output_file, self.log_file, self.report_file, payload)
        
        print "Executing :        %s ..." % jybotCommand
        self.running = True
        #self.process = subprocess.Popen(["pybot", "-o", "%s" % os.path.join(log_folder, self.output_file), "%s" % self.suite], cwd=client_cwd, stdout=jyLog, stderr=jyLog)
        self.process = subprocess.Popen(jybotCommand.split(' '), cwd=client_cwd, stdout=jyLog, stderr=jyLog)
   
    def isRunning(self):
        """ Polls the pybot subprocess to check if it's running. Will return true if the process is running.
        Returns false if the process hasn't been started or has finished already.
        """
        if not self.running:
            return False
        elif self.process.poll() == 0 or self.process.returncode >= 0:
            return False
        else:
            return True
   
    def stop(self):
        """ Kills the pybot subprocess.
        """
        os.system("taskkill /T /F /PID %s" % self.process.pid)
        self.running = False
        
# Methods #####################################################################################################
def startJybot(name, args=[]):
    """ Creates a pybot object, starts it and returns the object
    'name' is the name for the pybot (will be used for log outputs)
    'tests' is a list of tests to be executed by the pybot
    'suite' is the filename of the test suite containing the 'tests'
    'args' (optional) is a list of additional parameters passed to pybot
    """
    jybot = Jybot(name)
    jybot.start(args)
    return jybot
 
def generateReportAndLog(xmlFiles, reportFile, logFile):
    """ Calls RobotFrameworks rebot tool to generate Report and Log files from output.xml files
    'xmlFiles' is a list of output.xml files from jybot / pybot
    'reportFile' is the path+name of the report.html file to be written
    'logFile' is the path+name of the log.html file to be written
    the global variable 'payload' will be used a report title
    """    
    rebotCommand = "rebot --log %s --report %s --reporttitle \"%s\" --name ' ' %s/*.xml" % (logFile, reportFile, suite_name, workspace_home)
    print 'rebotCommand: ' +  rebotCommand
    rc = os.system(rebotCommand)
    return rc
 
# def parseArgs(argv):
    # """ Parses command line arguments like the testsuite name and additonal parameters
    # Expects the command line args without the python class as parameter argv (sys.argv[1:])
    # Fails and aborts script if args don't match the expected format
    # """
    # global payload, client_cwd, base_dir, log_folder, testsToRun, suiteToRun, testDirectory

 
def getDynArgs(index):
    """ Reads the DYN_ARGS variable from the config file and parses it into a list of argument strings
    like --variable name:"value".
    This list can be passed to the Pybot start() method as args[] list.
    """
    arglist = []
    for row in config.DYN_ARGS:
        valueIndex = index
        if len(row) < 2:
            print "Error reading DYN_ARGS: Row is invalid: %s. Row will be skipped!" % row
        else:
            varName = row[0]
            values = []
            i = 1
            while i < len(row):
                values.append(row[i])
                i = i+1
            if valueIndex >= len(values):
                valueIndex = (len(values)-1) % valueIndex
            varValue = values[valueIndex]
            arglist.append("--variable %s:\"%s\"" % (varName, varValue))
    return arglist
 
def usage():
    """ Prints usage information for Parabot """
    print ""
    print "Usage: python parabot.py [options] <testsuite.tsv>"
    print ""
    print "<testsuite.tsv> can be absolute or relative path + filename of a testsuite."
    print "The containing folder will be used as working directory"
    print ""
    print "Options:"
    print "-h\t--help\t\tThis screen"
    print "-i\t--include\tInclude a tag"
    print "-e\t--exclude\tExclude a tag"
    print "-f\t--forceserial\tForces serial test execution"
    print "-b\t--basedir\tSet parabots base dir"
    print ""
 
# helper classes ##############################################################################################
 

 
# MAIN SCRIPT #################################################################################################


print "";
print "-- PYROSUITE --";
print "";

# save current time to calculate execution time at the end of the script
startTime = datetime.now()
 
# global vars
payload = "No suite defined yet" # specified via args
argumentFiles = []
listeners = [] 
jybots = []
 
client_cwd = "No cwd defined" # specified via testsuite from args
base_dir = "./"

 
# reading variables from ParabotConfig
time_between_test_start_up = config.time_between_test_start_up
log_folder = config.LOG_DIR

# Example of multiple browsers (TeamCity)
#os.environ['SAUCE_ONDEMAND_BROWSERS'] =  '[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

# Example of Single Browser (TeamCity)
#os.environ['SELENIUM_DRIVER'] = "sauce-ondemand:?username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf&os=Windows 2012 R2&browser=internet explorer&browser-version=11&max-duration=null&idle-timeout=null"

if not os.environ.get('SAUCE_ONDEMAND_BROWSERS') and not os.environ.get('SELENIUM_DRIVER'):
    print 'WARNING: Pyrobot was unable to intersect the sauce environment variables'
    print '  -> SAUCE_ONDEMAND_BROWSERS SELENIUM_DRIVER'
    print '  Entering test mode by overriding SELENIUM_DRIVER with a fake value'
    print ''
    os.environ['SELENIUM_DRIVER'] = "sauce-ondemand:?username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf&os=Windows 2012 R2&browser=internet explorer&browser-version=11&max-duration=null&idle-timeout=null"

# parsing command line arguments
#parseArgs(sys.argv[1:])  
 
# if len(arglist)<1:
    # usage()
    # sys.exit(2)

os.environ['DISPLAY'] = config.DEFAULT_BROWSER_DISPLAY

arglist = sys.argv[1:]
if os.environ.get('PAYLOAD'):
    payload = os.environ['PAYLOAD']
else:
    try:
        payload = arglist[len(arglist)-1]
    except:
        usage()
        sys.exit(2)
            
suite_name = os.path.basename(os.path.normpath(payload))
client_cwd = os.path.realpath(base_dir)
workspace_home = os.path.join("/mnt/wt/pyrobot/workspace/", ''.join(random.choice(string.ascii_uppercase) for i in range(12)))
os.mkdir(workspace_home, 0755)

payload = os.path.join(os.path.realpath(base_dir), payload)
if not os.path.exists(payload):
    print "FATAL - Pyro must be given a payload that exists: %s\n" % payload
    sys.exit(2)
   
    
#####
####  log_folder = os.path.abspath(log_folder)
log_folder = payload

print "Base dir:         %s" % base_dir  
print "Client dir:       %s" % client_cwd
print "Log dir:          %s" % log_folder
print "Payload:          %s" % payload
print "Workspace Home:   %s" % workspace_home
print "Display:          %s" % os.environ['DISPLAY']
print ""


# Browser information 
construct = BrowserData(config)


print "Starting suite:   \"%s\" ...\n" % suite_name

for x in range(0, construct.getUrlCount()):
    test_name = ("%s_%s_%s" % (construct.getBrowser(x), construct.getOS(x), construct.getBrowserVersion(x))).replace(' ', '_')
    construct.setPyrobotEnvForTest(x, config, test_name)
    print ""   
    print "Starting browser tests for %s ..." % test_name
    jybot = startJybot(test_name, getDynArgs(0))
    while jybot.isRunning():
        time.sleep(time_between_test_start_up)
    jybots.append(jybot)
    with open(jybot.jyLogLoc, 'r') as fin:
        print fin.read()
    
print "Serial tests finished"
print ""

 
# merging outputs to one report and log
print "Generating report and log"

report = os.path.join(workspace_home, "%s_Report.html" % suite_name)
log = os.path.join(workspace_home, "%s_Log.html" % suite_name)

print 'final log and report' 
print report
print log

outputXmls = []
for jybot in jybots:
    outputXmls.append(os.path.join(log_folder, jybot.output))
 
reportRC = generateReportAndLog(outputXmls, report, log)
 
 
# delete XML output files after generating the report / log (if report generation
# returned zero)
#if reportRC == 0:
#    for outXML in outputXmls:
#        os.remove(outXML)
 
# calculating test execution time
endTime = datetime.now()
executionTime = endTime - startTime
print ""
print "Execution time: %s" % executionTime