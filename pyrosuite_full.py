#! /usr/bin/env python

from ParseSauceURL import *
from SauceRest import *


import os
import sys
from tempfile import TemporaryFile
from subprocess import Popen, call, STDOUT

for arg in sys.argv:
    if arg.startswith("--usesauce"):
        parts = arg.split("=")
        use_sauce = 1
    if arg.startswith("--sauceusername"):
        parts = arg.split("=")
        sauce_username = parts[1].lower()      
    if arg.startswith("--sauceaccesskey"):
        parts = arg.split("=")
        sauce_accesskey = parts[1].lower()       
    if arg.startswith("--typology"):
        parts = arg.split("=")
        typology = parts[1].lower()     
    if arg.startswith("--payload"):
        parts = arg.split("=")
        payload = parts[1].lower() 

class Pybot():
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
        print "Created pybot %s." %name
    
    def start(self, tests, suite, args=[]):
        """ Starts the pybot script from RobotFramework executing the defined 'tests' from the given 'suite'.
        'tests' is a list of tests to be executed by the pybot
        'suite' is the filename of the test suite containing the 'tests'
        'args' (optional) is a list of additional parameters passed to pybot
        """
        self.tests = tests
        self.suite = suite
        self.args = args
        temp, suiteName = os.path.split(suite_name)
        self.output = "%s_%s_Output.xml" % (suiteName, self.name)
        pybotCommand = "pybot.bat "
        for test in self.tests:
            pybotCommand = pybotCommand + "-t \"%s\" " % test
        for arg in self.args:
            pybotCommand = pybotCommand + arg + " "
        pybotCommand = pybotCommand + "-o %s " % os.path.join(logFolder, self.output)
        pybotCommand = pybotCommand + "-l NONE "
        pybotCommand = pybotCommand + "-r NONE "
        pybotCommand = pybotCommand + "-N \"%s %s\" " % (suiteName, self.name)
        pybotCommand = pybotCommand + suite
        #print pybotCommand
        pyLog = open(os.path.join(logFolder, ("Pybot_%s_Log.txt" % self.name)), "w")
        print "Starting pybot %s ..." % self.name
        self.running = True
        self.process = subprocess.Popen(pybotCommand, cwd=clientCwd, stdout=pyLog, stderr=pyLog)
    
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

def startPybot(name, tests, suite, args=[]):
    """ Creates a pybot object, starts it and returns the object
    'name' is the name for the pybot (will be used for log outputs)
    'tests' is a list of tests to be executed by the pybot
    'suite' is the filename of the test suite containing the 'tests'
    'args' (optional) is a list of additional parameters passed to pybot
    """
    pybot = Pybot(name)
    pybot.start(tests, suite, args)
    return pybot


### MAIN

		
os.environ['SAUCE_ONDEMAND_BROWSERS'] =  '[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

construct = SauceTeamCityBrowserData()
#print construct.getBrowsersString(sauce_username,sauce_accesskey)
print construct.getBrowsersString()


# parsing command line arguments
parseArgs(sys.argv[1:])

# generating two lists containing parallel and serial tests
para_tests = []
seri_tests = []
try:
    # RobotFramework 2.0.4
    suite = TestSuite(os.path.join(clientCwd, suite_name), process_curdir=False)
except Exception:
    # RobotFramework 2.5
    suiteOps = settings.RobotSettings()
    suite = TestSuite([os.path.join(clientCwd, suite_name)], suiteOps)

for test in suite.tests:
    # special treatment for tests without tags:
    # include them into serial execution as long as no include tags are defined
    if not test.tags and len(includeTags)==0:
        seri_tests.append(test.name)
    # tests with tags:
    # filter excluded tests (if any), then filter included tests (if any), then scan for
    # parallel keyword and assign to parallel / serial block
    elif len(excludeTags)==0 or not test._contains_any_tag(excludeTags):
        if len(includeTags)==0 or test._contains_any_tag(includeTags):
            if test._contains_tag(para_tag) and not forceSerialExecution:
                para_tests.append(test.name)
            else:
                seri_tests.append(test.name)

# output serial test list
print ""
print "Serial tests:"
if len(seri_tests) == 0:
    print "NONE"
else:
    for test in seri_tests:
        print test               