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
