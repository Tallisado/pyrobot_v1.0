import os
from robot.libraries.BuiltIn import BuiltIn

envname_pyrobot_browser = 'PYROBOT_BROWSER'
envname_pyrobot_default_browser = "PYROBOT_DEFAULT_BROWSER"

SELENIUM2LIB_BROWSERS = [   'ff',
                            'firefox',
                            'ie',
                            'internetexplorer',
                            'googlechrome',
                            'gc',
                            'chrome',
                            'opera',
                            'phantomjs',
                            'htmlunit',
                            'htmlunitwithjs',
                            'android',
                            'iphone',
                            'safari'
                        ]

def open_pyrobot(arglist, opt_arg=""):
    seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    if hasattr(arglist, 'lower'):
        print '(open_pybot) solo' 
        if opt_arg == "":
            target_browser = os.environ[envname_pyrobot_default_browser]
        else:
            if not opt_arg in SELENIUM2LIB_BROWSERS:
                raise ValueError(opt_arg + " is not a supported browser.")
            target_browser = opt_arg
        print '%s (%s)' % (arglist, opt_arg)
        seleniumlib.open_browser(arglist, browser=target_browser)
    else:
        print '(open_pybot) sauce'
        if opt_arg == "":
            url = arglist[0]
        elif "http" in opt_arg:
            url = opt_arg
        else:
            raise ValueError(opt_arg + " is not a valid url.")
            
        print '[%s] url(%s)' % (', '.join(map(str, arglist)), url)        
        seleniumlib.open_browser(url, browser=os.environ[envname_pyrobot_default_browser], remote_url=arglist[2], desired_capabilities=arglist[3])
        
# def open_browser(url, browser=None, remote=None, caps=None):
    # seleniumlib = BuiltIn().get_library_instance('Selenium2Library')
    # seleniumlib.open_browser(url, remote_url=remote, desired_capabilities=caps)