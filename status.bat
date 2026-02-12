@echo off  

REM read value from recent.default.port file
for /f "usebackq delims=" %%A in ("storage/recent.default.port") do (
    echo [INFO] Apache2D running in DEFAULT port : %%A    
)

REM read value from recent.ssl.port file
for /f "usebackq delims=" %%B in ("storage/recent.ssl.port") do (
    echo [INFO] Apache2D running in SSL port : %%B 
)

echo [INFO] Checking Apache2D status.. 
sc query Apache2D
echo [INFO] Here all the list. hope you know what the status of the service right now. 
echo [WARN] this program will exit after timeout
timeout /t 44

