pyrobot
=======

"PYROBOT" is a python wrapper to integrate Sauce and Robot Framework

## Feature Set

### TeamCity Sauce Plugin interpretation
- Intersects TeamCity Sauce CI plugin parameters to determine which browsers are targeted. 
- SAUCE_ONDEMAND_BROWSERS or BROWSER, depending on if single or multiple
- Also runs in standalone mode

### Pybot serial execution
- Spawns pybot processes in serial
- Stages each pybot test suite with the target browser
- Browser information is embedded into log

### Rebot file management
- Concat  pybot's resulting output and reports


## How it works:
1. A Teamcity build is started, and as such invokes; [Sauce CI - Plugin](http://saucelabs.com/teamcity/1 "SauceLabs Teamcity plugin") and Pyrobot, the build feature and build step respectively.
  * __Example Build__ Feature ![Build Feature](docs/teamcitybuildfeature_sauce.JPG?raw=true)
  * __Example Pyrobot__ ![Pyrobot](docs/teamcitybuild_sauce.JPG?raw=true)
2. Teamcity will start OnConnect (if selected)
3. Pyrobot executes the payload, either a single file or entire directory
  * If a directory is provided, the directory contents can be enumerated to allow the files to be ordered.
4. The results are placed into __pyrobot/workspace__ under a unique folder, after which the files are consolidated into a single report if multiple browsers were selected in build features
5. __TODO__ Sauce REST API integration to show results under 'Sauce Results' tab in teamcity build

## Feature Explanation:
### TeamCity Sauce Plugin interpretation
  * The SauceCI plugin provides either SAUCE_ONDEMAND_BROWSERS or BROWSER, when multiple or single browser selection within the build feature respectively
  * These environment vaiables are intersected and intrepreted to provide a remote webdriver instantiation to robot framework

### Execute standalone
  * Pyrobot can be executed from the commandline, using ant, or directly with the python script itself. When in standalone mode, the browser object is created based on the default values in __./PyrobotConfig__
  * ``` vncserver :60 -geometry 1280x1024 ``` or ``` Xvfb ... ```
  * ```BASE_URL=http://10.10.9.129/Login/index.php python pyrobot.py dev/spec/01__sauce_browser.txt ```

### Pybot wrapper
  * Pybot is executed for each payload specified, and all selected browsers in the Build Feature in Sauce CI.
  * The Selenium2Library is augmented to provided integration to the Sauce service (see Pyrobot Robot Framework)

#### Pybot configuration
  * ``` SAUCE_USERNAME = "yourname" ```
  * ``` SAUCE_ACCESSKEY = "yourkey" ```
  * ``` DEFAULT_SAUCEURL = "sauce-ondemand:?username=%s&access-key=%s&os=Windows 2012 R2&browser=%s&browser-version=11&max-duration=null&idle-timeout=null" ```
    1. when executed in standalone, this remote webdriver is instanciated if using sauce
  * ``` DEFAULT_SOLO_BROWSER = 'firefox' ```
    1. when executed in standalone, this remote webdriver is instanciated if using local browser
  * ``` DEFAULT_BROWSER_DISPLAY = ":60" ```
  * ``` BASE_URL = "http://www.google.ca" ```
    1. when not provided through ant/python, base_url default here
  
#### Pyrobot Robot Framework
1. Reference the resource file: 
  * ``` Resource       ../resources/resource.txt ```
2. Various Invocations:
  1. 	``` Open Pyrobot	  http://www.google.ca                              __Local Default Browser TestLevel URL__ ```
  2. 	``` Open Pyrobot 	  http://www.google.ca      chrome                  __Local Non-Default Browser TestLevel URL__ ```
  3. 	``` Open Pyrobot 	  ${PYRO_BROWSER}           http://www.google.ca    __Sauce Browser TestLevel URL__ ```
  4. 	``` Open Pyrobot	  ${PYRO_BROWSER}                                   __Sauce Browser BaseUrl URL OnConnect__ ```
    * base_url is OnConnect only

