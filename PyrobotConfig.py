###############################################################################################################
# Configure Logging:
# A directory to place log files in
LOG_DIR = "./logs/"
WORKSPACE_ = "./workspace/"
###############################################################################################################
# Dynamic pybot variables:
# Specifies an 3D-array with variables passed to the single pybot instances
# Each row contains a variablename - value(s) combination (array, name at index 0, values at 1++)
# One variable value will be passed to each python instance using --variable name:value
# If multiple values are defined parabot will iterate over the values and assign one to each pybot
DYN_ARGS =  [
    # specify different users
    ["USER", "Hans", "Klaus", "Peter", "Martin", "Eric"],
    # passwords
    ["PASS", "HansPassword", "KlausPassword", "PetersPassword", "MartinsPassword", "EricsPassword"]
]


time_between_test_start_up = 0


####
# NEW
#
#######

SAUCE_USERNAME = 'talliskane'
SAUCE_ACCESSKEY = "6c3ed64b-e065-4df4-b921-75336e2cb9cf"
DEFAULT_SAUCEURL = "sauce-ondemand:?username=%s&access-key=%s&os=Windows 2012 R2&browser=%s&browser-version=11&max-duration=null&idle-timeout=null"
DEFAULT_SOLO_BROWSER = 'firefox'
DEFAULT_SINGLE_BROWSER = "sauce-ondemand:?username=%s&access-key=%s&os=Windows 2012 R2&browser=internet explorer&browser-version=11&max-duration=null&idle-timeout=null"


DEFAULT_BROWSER_DISPLAY = ":60"

BROWSER_CAPABILITIES = 'name:%s,platform:%s,version:%s,browserName:%s,javascriptEnabled:True'

BASE_URL = "http://www.google.ca"