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
    BROWSER = os.environ[envname_pyrobot_browser]

BASE_URL = os.environ['BASE_URL']
    
if not (os.environ.get(envname_pyrobot_remote_url), os.environ.get(envname_pyrobot_caps)):
    missing_pyrobot_envs("%s %s" % (envname_pyrobot_remote_url, envname_pyrobot_caps))
#BROWSER += '    remote_url=%s     desired_capabilities=%s' % (os.environ[envname_pyrobot_remote_url], os.environ[envname_pyrobot_caps])
REMOTE = os.environ[envname_pyrobot_remote_url]
CAPS = os.environ[envname_pyrobot_caps]
