import os
import getpass

username = getpass.getuser()
autoexec_path = "C:\\Users\\" + username + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
os.system("taskkill /F /im fsociety.exe")
try:
    os.remove(autoexec_path + "\\fsociety.exe")
except:
    print("nie ma chuja")
