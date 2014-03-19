import os
from robot.libraries.BuiltIn import BuiltIn

envname_pyrobot_browser = 'PYROBOT_BROWSER'
envname_pyrobot_default_browser = "PYROBOT_DEFAULT_BROWSER"

def open_pyrobot(arglist, url='http://www.google.ca', default_browser=os.environ[envname_pyrobot_browser]):
    is_sauce = False
    if hasattr(arglist, 'lower'):
        if default_browser:
            print '%s (%s)' % (arglist, default_browser)
        else:    
            print '%s' % arglist
    else:
        is_sauce = True
        print '[%s]' % ', '.join(map(str, arglist))

    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
        
    if is_sauce and (len(arglist) == 3):
        print '(open_pybot) sauce'
        seleniumlib.open_browser(url, browser=default_browser, remote_url=arglist[1], desired_capabilities=arglist[2])
    else:
        print '(open_pybot) solo'
        seleniumlib.open_browser(url, arglist, browser=os.environ[envname_pyrobot_default_browser])
        
# def open_browser(url, browser=None, remote=None, caps=None):
    # seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    # seleniumlib.open_browser(url, remote_url=remote, desired_capabilities=caps)