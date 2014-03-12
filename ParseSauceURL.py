import json
import os
#'[{"platform":"LINUX","os":"Linux","browser":"chrome","url":"sauce-ondemand:?os=Linux&browser=chrome&browser-version=32&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"32"},{"platform":"LINUX","os":"Linux","browser":"android","url":"sauce-ondemand:?os=Linux&browser=android&browser-version=4.0&username=talliskane&access-key=6c3ed64b-e065-4df4-b921-75336e2cb9cf","browser-version":"4.0"}]'

class SauceTeamCityBrowserData:
    def __init__(self):
        self.browser_holder = []        
        
        if os.environ.get('SAUCE_ONDEMAND_BROWSERS'):
            print 'mult'
            self.raw_json = json.loads(os.environ.get('SAUCE_ONDEMAND_BROWSERS')) 
            for browser_item in self.raw_json:            
                browser = {}
                for attribute, value in browser_item.iteritems():
                    browser[attribute] = value
                self.browser_holder.append(browser.copy())
            #print self.browser_holder 
        elif os.environ.get('SELENIUM_DRIVER'):
            print 'single'
            browser = os.environ.get('SELENIUM_DRIVER').split(':')[1][1:].split('&')
            for field in browser:
                [key, value] = field.split('=')    
                browser[key] = value
            self.browser_holder.append(browser.copy())
        
        self.url_list = []
        for browser_item in self.browser_holder:
            #print browser_item
            if 'url' in browser_item:
                self.url_list.append(browser_item['url'])
                
    def getBrowsersString(self):
        if self.url_list:
            return self.url_list
        # else 
            # getDefaultUrl()
    
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
        return self.getValue("browser", index)

    def getUserName(self, index):
        return self.getValue("username", index)

    def getAccessKey(self, index):
        return self.getValue("access-key", index)

    def getJobName(self, index):
        return self.getValue("job-name", index)

    def getOS(self, index):
        return self.getValue("os", index)
    
    def getBrowser(self, index):
        return self.getValue('browser', index)

    def getBrowserVersion(self, index):
        return self.getValue('browser-version', index)
    
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