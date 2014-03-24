pyrobot
=======
pyrobot is a wrapper that does the following:

TeamCity Sauce Plugin interpretation
- intersects TeamCity Sauce CI plugin parameters to determine which browsers are targeted. 
- SAUCE_ONDEMAND_BROWSERS or BROWSER, depending on if single or multiple

Pybot serial execution
- spawns pybot processes in serial
- stages each pybot test suite with the target browser
- browser information is embedded into log

Rebot file management
- concat  pybot's resulting output and reports


How to run:
-start vnc for local firefox to run in (if necessary)
	#> vncserver :60 -geometry 1280x1024
-execute pybot
	#> BASE_URL=http://<IP REMOVED>/Login/index.php python pyrobot.py dev/spec/01__sauce_browser.txt