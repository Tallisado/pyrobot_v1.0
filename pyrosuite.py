# -*- coding: utf-8 -*-
#
# Script to execute test cases from one suite in parallel
# by thomas klein / 2009
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
import PyroConfig as config
 
from ParseSauceURL import *
from SauceRest import *
 
# Methods #####################################################################################################
def startJybot(name, suite, args=[]):
    """ Creates a pybot object, starts it and returns the object
    'name' is the name for the pybot (will be used for log outputs)
    'tests' is a list of tests to be executed by the pybot
    'suite' is the filename of the test suite containing the 'tests'
    'args' (optional) is a list of additional parameters passed to pybot
    """
    jybot = Jybot(name)
    jybot.start(suite, args)
    return jybot
 
def generateReportAndLog(xmlFiles, reportFile, logFile):
    """ Calls RobotFrameworks rebot tool to generate Report and Log files from output.xml files
    'xmlFiles' is a list of output.xml files from jybot / pybot
    'reportFile' is the path+name of the report.html file to be written
    'logFile' is the path+name of the log.html file to be written
    the global variable 'payload' will be used a report title
    """    
    rebotCommand = "rebot --log %s --report %s --reporttitle \"%s\" --name ' ' %s*.xml" % (logFile, reportFile, suiteName, payload)
    print 'rebotCommand: ' +  rebotCommand
    rc = os.system(rebotCommand)
    return rc
 
def parseArgs(argv):
    """ Parses command line arguments like the testsuite name and additonal parameters
    Expects the command line args without the python class as parameter argv (sys.argv[1:])
    Fails and aborts script if args don't match the expected format
    """
    global payload, clientCwd, baseDir, logFolder, testsToRun, suiteToRun, testDirectory
    if len(argv)<1:
        usage()
        sys.exit(2)
   
    # last argument is test suite name
    suiteToRun = payload = argv[len(argv)-1]
    #args_file = argv[len(argv)-4]
    #print "args_file: %s" % args_file
     
    if len(os.path.split(payload)) == 0:
        clientCwd = "./"
    else:
        clientCwd = os.path.realpath(baseDir)
    
    #last commented line
    payload = os.path.join(os.path.realpath(baseDir), payload)
   #####
 ####  logFolder = os.path.abspath(logFolder)
    logFolder = payload
    
    print "Base dir:         %s" % baseDir;
    print "Real Base dir:    %s" % os.path.realpath(baseDir);    
    print "Client dir:       %s" % clientCwd
    print "Real Client Dir:  %s" % os.path.realpath(clientCwd)
    print "Log dir:          %s" % logFolder
    print "Payload:          %s" % payload
 
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
   
    def __init__(self, name):
        """ Constructor, creates the object and assigns the given 'name'.
        """
        self.name = name
   
    def start(self, suite, args=[]):
        """ Starts the pybot script from RobotFramework executing the defined 'tests' from the given 'suite'.
        'suite' is the filename of the test suite containing the 'tests'
        'args' (optional) is a list of additional parameters passed to pybot
        """
        self.suite = suite
        self.output_file = "%s_Output.xml" % (self.name)
        temp, suiteName = os.path.split(payload) 
        jyLog = open(os.path.join(logFolder, ("%s_Log.txt" % self.name)), "w")        
        jybotCommand = "pybot -o %s %s" % (os.path.join(logFolder, self.output_file), self.suite)
        
        print "Executing :        %s ..." % jybotCommand
        self.running = True
        self.process = subprocess.Popen(["pybot", "-o", "%s" % os.path.join(logFolder, self.output_file), "%s" % self.suite], cwd=clientCwd, stdout=jyLog, stderr=jyLog)
   
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
 
clientCwd = "No cwd defined" # specified via testsuite from args
baseDir = "./"

 
# reading variables from ParabotConfig
time_between_test_start_up = config.time_between_test_start_up
logFolder = config.LOG_DIR
#antBatch = os.path.abspath(config.ANT_BATCH_FILE)
#seCwd = os.path.abspath(config.SELENIUM_GRID_DIR)
#startSelenium = config.AUTOSTART_SELENIUM
#browser = config.SELENIUM_BROWSER

os.environ['SAUCE_ONDEMAND_BROWSERS'] =  '[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

construct = SauceTeamCityBrowserData()
#print construct.getBrowsersString(sauce_username,sauce_accesskey)
browser_list = construct.getBrowsersString()
#print browser_list
#print construct.getBrowser(0)
#print construct.getUserName(0)

# parsing command line arguments
parseArgs(sys.argv[1:])        


suiteName = os.path.basename(os.path.normpath(payload))
print "Starting suite \"%s\" ...\n" % suiteName

for (i, browser_list) in enumerate(browser_list):
    testName = "%s_%s_%s" % (construct.getBrowser(i), construct.getOS(i), construct.getBrowserVersion(i))
    print ""   
    print "Starting browser tests for %s ..." % testName
    
    jybot = startJybot(testName, payload, getDynArgs(0))
    while jybot.isRunning():
        time.sleep(time_between_test_start_up)
    jybots.append(jybot)
    print "Serial tests finished"
    print ""
 
 
# merging outputs to one report and log
print "Generating report and log"

report = "%s_Report.html" % os.path.join(logFolder, suiteName)
log = "%s_Log.html" % os.path.join(logFolder, suiteName)
outputXmls = []
for jybot in jybots:
    outputXmls.append(os.path.join(logFolder, jybot.output))
 
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