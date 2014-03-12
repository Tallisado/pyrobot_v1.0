import os

# default is to run locally
use_ondemand = "false"
sauce_user = "talliskane"
sauce_api = "6c3ed64b-e065-4df4-b921-75336e2cb9cf"

BROWSER_STR = 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True'

env_pyro_browser = ""
env_sauce_mode = ""

if os.environ.get('SAUCE'):
    env_sauce_mode = os.environ['SAUCE']
if os.environ.get('PYRO_BROWSER'):
    env_pyro_browser = os.environ['PYRO_BROWSER']

use_sauce = 0
if env_sauce_mode == 'true' or env_sauce_mode == '1':
	use_sauce = 1 
	if env_pyro_browser:
		print 'error: using sauce mode requires PRYO_BROWSER to be set'
		exit(1)

if use_sauce:	
	print '-- USEDSAUCE'		
	REMOTE_URL = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (sauce_user, sauce_api)
	TEST_NAME = 'Testing RobotFramework Selenium2Library'
	PLATFORM = 'Windows 2008'
	VERSION = '14'
	BROWSER_NAME = 'firefox'
	
	BROWSER = '%s    remote_url=%s    desired_capabilities=%s' % (TARGET_BROWSER, REMOTE_URL, BROWSER_CAPS)
else:
    REMOTE_URL = ''
    BROWSER_CAPS = ''
    BROWSER = 'firefox'

