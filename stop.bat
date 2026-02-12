@echo off
echo "bitch Apache2D stopping.........."
REM configure apache random port
cd /d "%~dp0"

net stop apache2D

netsh interface portproxy delete v4tov4 listenport=80 listenaddress=0.0.0.0
netsh interface portproxy delete v4tov4 listenport=443 listenaddress=0.0.0.0

echo [INFO] Port forwarding deleted successfully.

REM read value from recent.default.port file
for /f "usebackq delims=" %%A in ("storage/recent.default.port") do (
    netsh advfirewall firewall delete rule name="Apache2D Port %%A"
    echo [INFO] Deleted Rule Apache Port %%A
)
REM read value from recent.ssl.port file
for /f "usebackq delims=" %%B in ("storage/recent.ssl.port") do (
    netsh advfirewall firewall delete rule name="Apache2D Port %%B"   
    echo [INFO] Deleted Rule Apache Port %%B
)

echo "yeah dude, Apache2D cumming......." 
pause

REM make if else with error level for stoping service