need to run the server and also the clients on the same device

for example:

powershell -NoExit -command "cd C:\Tamir\simpleMessaging\server;.\serverenv\Scripts\Activate.ps1;python .\clientfastapi.py"

powershell -NoExit -command "cd C:\Tamir\simpleMessaging\client;.\clientenv\Scripts\Activate.ps1;python .\clientfastapi.py"