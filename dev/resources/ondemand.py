import os

def missing_pyrobot_envs(missing):
    print '(pyrobot|ondemand) failed to receive all required env variables from pyrobot initiation script: ' + missing
    exit(1)
    
# default is to run locally
envname_pyrobot_usesauce = "SAUCE"
envname_pyrobot_browser = "PYROBOT_BROWSER"
envname_pyrobot_remote_url = "PYROBOT_REMOTE_URL"
envname_pyrobot_caps = "PYROBOT_CAPS"

env_pyro_browser = ""
env_sauce_mode = ""

#print '(pyrobot|ondemand) %s %s %s' % (os.environ[envname_pyrobot_browser], os.environ[envname_pyrobot_remote_url], os.environ[envname_pyrobot_caps])

if not os.environ.get(envname_pyrobot_browser):
    missing_pyrobot_envs()
else:
    BROWSER = '%s' % os.environ[envname_pyrobot_browser]

if not (os.environ.get(envname_pyrobot_remote_url), os.environ.get(envname_pyrobot_caps)):
    missing_pyrobot_envs("%s %s" % (envname_pyrobot_remote_url, envname_pyrobot_caps))
#BROWSER += '    remote_url=%s     desired_capabilities=%s' % (os.environ[envname_pyrobot_remote_url], os.environ[envname_pyrobot_caps])
REMOTE = os.environ[envname_pyrobot_remote_url]
CAPS = os.environ[envname_pyrobot_caps]

#LIST__BROWSER = ["http://www.google.ca", "chrome remote_url=http://talliskane:6c3ed64b-e065-4df4-b921-75336e2cb9cf@ondemand.saucelabs.com:80/wd/hub", "desired_capabilities=name:chrome_Linux_4.0,platform:Linux,version:32,browserName:chrome,javascriptEnabled:True"]
#BROWSER += "remote_url=%s       desired_capabilities=%s" % (os.environ[envname_pyrobot_remote_url], os.environ[envname_pyrobot_caps])
#print '(pyrobot|ondemand) BROWSER : ' + BROWSER
#print '(pyrobot|ondemand) REMOTE : ' + REMOTE
#print '(pyrobot|ondemand) CAPS : ' + REMOTE
# if os.environ.get('SAUCE'):
    # env_sauce_mode = os.environ['SAUCE']
# if os.environ.get('PYRO_BROWSER'):
    # env_pyro_browser = os.environ['PYRO_BROWSER']

# use_sauce = 0
# if env_sauce_mode == 'true' or env_sauce_mode == '1':
	# use_sauce = 1 
	# if not env_pyro_browser:
		# print 'error: using sauce mode requires PRYO_BROWSER to be set'
		# exit(1)

# if use_sauce:	
	# print '-- USEDSAUCE'		
	# REMOTE_URL = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (sauce_user, sauce_api)
	# TEST_NAME = 'Testing RobotFramework Selenium2Library'
	# PLATFORM = 'Windows 2008'
	# VERSION = '14'
	# BROWSER_NAME = 'firefox'	
	# BROWSER = '%s    remote_url=%s    desired_capabilities=%s' % (BROWSER_NAME, REMOTE_URL, BROWSER_STR)
# else:
    # BROWSER = 'firefox'
    
# print 'Sauce CI (TeamCity) - Browser determined:'
# print BROWSER


