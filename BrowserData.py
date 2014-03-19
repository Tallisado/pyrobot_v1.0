import json
import os
import platform
#'[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

class BrowserData:
    def __init__(self, config):
        self.url_list = []
        self.browser_holder = []
        self.teamcity_intersect = False
        self.override_username = False
        self.browser_override = config.DEFAULT_SOLO_BROWSER
        
        self.envname_pyrobot_usesauce = "SAUCE"
        self.envname_pyrobot_browser = "PYROBOT_BROWSER"
        self.envname_pyrobot_default_browser = "PYROBOT_DEFAULT_BROWSER"
        self.envname_pyrobot_remote_url = "PYROBOT_REMOTE_URL"
        self.envname_pyrobot_caps = "PYROBOT_CAPS"
        
        
        if os.environ.get('SAUCE_ONDEMAND_BROWSERS'):
            print '(SauceTeamCityBrowserData) : Multiple browsers'
            self.teamcity_intersect = True
            self.raw_json = json.loads(os.environ.get('SAUCE_ONDEMAND_BROWSERS')) 
            for browser_item in self.raw_json:            
                if 'url' in browser_item:
                    self.url_list.append(browser_item['url'])
                    
        elif os.environ.get('SELENIUM_DRIVER'):
            print '(SauceTeamCityBrowserData) : Single browser'
            self.teamcity_intersect = True
            self.url_list.append(os.environ.get('SELENIUM_DRIVER'))
            
        # elif os.environ.get('BROWSER'):
            # print '(SauceTeamCityBrowserData) : SOLO Browser (Override)'
            # browser = {}
            # for browser_item in os.environ.get('BROWSER'):
                # [key, value] = field.split('=')    
                # browser[key] = value
        else:
            print '(SauceTeamCityBrowserData) : SOLO Browser (Default)'           
            browser_url = config.DEFAULT_SAUCEURL % (os.getenv('SAUCE_USERNAME', config.SAUCE_USERNAME), os.getenv('SAUCE_ACCESSKEY', config.SAUCE_ACCESSKEY), config.DEFAULT_SOLO_BROWSER)
            self.url_list.append(browser_url)
                
                
        if self.teamcity_intersect:
            for browser_item in self.browser_holder:
                #print browser_item
                if os.environ.get('SAUCE_USERNAME'):
                    browser_item['username'] = os.environ.get('SAUCE_USERNAME')
                elif os.environ.get('SAUCE_ACCESSKEY'):
                    browser_item['access-key'] = os.environ.get('SAUCE_ACCESSKEY')                        
        
            
    # def getBrowsersString(self):
        # if self.url_list:
            # return self.url_list
        # else 
            # getDefaultUrl()
    def setPyrobotEnvForTest(self, i, config, test_name):
        os.environ[self.envname_pyrobot_default_browser] = config.DEFAULT_SOLO_BROWSER
        os.environ[self.envname_pyrobot_browser] = self.getValue("browser", i)
        os.environ[self.envname_pyrobot_remote_url] = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (self.getUserName(i), self.getAccessKey(i))
        os.environ[self.envname_pyrobot_caps] = 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True' % (test_name, self.getOS(i), self.getBrowserVersion(i), self.getBrowser(i))
        # if os.environ.get(self.envname_pyrobot_browser):
            # os.environ[self.envname_pyrobot_browser] = self.browser_override 
            # os.environ[self.envname_pyrobot_remote_url] = 'http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (getUserName(index), getAccessKey(index))
               # # eg : 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True'
            # os.environ[self.envname_pyrobot_caps] = config.BROWSER_CAPABILITIES % ('test_name', )
        # else
            # os.environ[self.envname_pyrobot_browser] = getBrowser(index)   
        
        
    
    def getUrlCount(self):
        return len(self.url_list)
        
    def getUrlString(self, index):
        return self.url_list[index]
    
    def getParsedUrl(self, index):
        self.fields = {}
        fields = self.getUrlString(index).split(':')[1][1:].split('&')
        for field in fields:
            [key, value] = field.split('=')   
            self.fields[key] = value
        return self.fields
        
    def getValue(self, target_key, index):   
        fields = self.getParsedUrl(index)
        if target_key in fields:
            return fields[target_key]
        else:
            return ""

    def getBrowser(self, index):
        if self.teamcity_intersect:
            return self.getValue("browser", index)
        else:
            return 'local'
            
    def getUserName(self, index):
        return self.getValue("username", index)

    def getAccessKey(self, index):
        return self.getValue("access-key", index)

    def getJobName(self, index):
        return self.getValue("job-name", index)

    def getOS(self, index):
        if self.teamcity_intersect:
            return self.getValue("os", index)
        else:
            return platform.system()        

    def getBrowserVersion(self, index):        
        if self.teamcity_intersect:
            return self.getValue('browser-version', index)
        else:
            return 'any' 
            
    def getFirefoxProfileURL(self, index):
        return self.getValue('firefox-profile-url', index)

    def getMaxDuration(self, index):
        try:
            return int(self.getValue('max-duration', index))
        except:
            return 0

    def getIdleTimeout(self, index):
        try:
            return int(self.getValue('idle-timeout', index))
        except:
            return 0

    def getUserExtensionsURL(self, index):
        return self.getValue('user-extensions-url', index)    
    # def getDefaultUrl(self, username=, accesskey):
        # return 'sauce-ondemand:?username=%s&access-key=%s&os=Windows 2012 R2&browser=internet explorer&browser-version=11&max-duration=null&idle-timeout=null' % (SAUCE_USERNAME, SAUCE_ACCESSKEY)
        # #sauce-ondemand:?username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf&os=Windows 2012 R2&browser=internet explorer&browser-version=11&max-duration=null&idle-timeout=null
            
        
class ParseSauceJson:
    def __init__(self, json_raw):
        self.browser_holder = []
        
        self.json_raw = json_raw
        self.data = json.loads(json_raw) 
        
        for url in self.data:
            browser = {}
            for attribute, value in url.iteritems():
                browser[attribute] = value
                
            self.browser_holder.append(browser.copy())
        print self.browser_holder       
        
    def getBrowserCount(self):
        return len(self.data)
        
    # def getUrlList(self):
        # url_list = []
        # for browsers in data:
            # for attribute, value in browsers.iteritems():
                # print attribute, value # example usage
                # #if attribute == 'url'
                    # #url_list.append(attribute)
        # return url_list
            
    def getValue(self, key):
        if key in self.fields:
            return self.fields[key]
        else:
            return ""

    def getUserName(self):
        return self.getValue("username")

    def getAccessKey(self):
        return self.getValue("access-key")

    def getJobName(self):
        return self.getValue("job-name")

    def getOS(self):
        return self.getValue("os")
    
    def getBrowser(self):
        return self.getValue('browser')

    def getBrowserVersion(self):
        return self.getValue('browser-version')
    
    def getFirefoxProfilejson_raw(self):
        return self.getValue('firefox-profile-json_raw')

    def getMaxDuration(self):
        try:
            return int(self.getValue('max-duration'))
        except:
            return 0

    def getIdleTimeout(self):
        try:
            return int(self.getValue('idle-timeout'))
        except:
            return 0

    def getUserExtensionsjson_raw(self):
        return self.getValue('user-extensions-json_raw')

    def tojson_raw(self):
        return json_raw.dumps(self.fields, sort_keys=False)