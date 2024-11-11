# GetGrass Crooter
## Installation
#### Install python3
- For windows: https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe 
- For linux distros: https://dev.to/ivayloiv/install-latest-python-version-on-any-linux-distro-5gc3
#### Python3 module Installation
- Install from requirements.txt
```pip install -r requirements.txt```
### REGISTER: https://app.getgrass.io/register/?referralCode=03XXIyiaeCGb9Vh ( Please use this link instead! xD )
## HOW TO USE
#### How to get your grass userid
- Login to https://app.getgrass.io
- Press f12 go to console, then type ```allow pasting``` insert to console
![pasting](https://github.com/user-attachments/assets/80d2e2ae-fde7-49cb-8e99-9746e2e01de7)
- Then insert this code to console
```localStorage.getItem('userId')```
![userid](https://github.com/user-attachments/assets/7b8cbb77-5371-41c9-821f-cb30b7706797)
#### Usage command
- Open file ```proxy_list.txt``` and insert your proxies
- Open file ```run.py``` via notepad or notepad++ or Visual Studio Code and insert your userid in line 81

- Example at Line 81 here:
- 
    tasks = [asyncio.ensure_future(connect_to_wss(i, 'enter your userid')) for i in local_proxies]
 => tasks = [asyncio.ensure_future(connect_to_wss(i, 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')) for i in local_proxies]
- 
- Run ```python run.py```




