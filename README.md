# Custom Activation Servers for Old Rovio Games
## How it works:
The script emulates Rovio's original activation server and redirects any traffic from Rovio's servers[^1] to the host machine[^2].
When the script recieves a request, it always returns that the key is valid. That tricks the game into activating.
[^1]: Rovio's activation servers are cloud.rovio.com/drm and drm-pc.angrybirdsgame.com
[^2]: Does this by editing the hosts file which may trigger detections from some anti-virus programs
## Tested on:
|Series|Version|Platform|Installer Name|Status|
|------|-------|--------|--------------|------|
|Angry Birds Seasons|4.1.0|Windows|AngryBirdsSeasonsInstaller_4.1.0.exe|1|
|Angry Birds|4.0.0|Windows|AngryBirdsSeasonsInstaller_4.1.0.exe|1|
|Angry Birds Star Wars III|1.5.1|Windows|AngryBirdsStarWarsIIInstaller_1.5.1.exe|1|
|Angry Birds Rio|1.1.0|Windows|AngryBirdsRioInstaller_1.1.0.exe|2,3,5|
|Angry Birds Rio|1.2.2|Windows|AngryBirdsRioInstaller_1.2.2.exe|2,5|
|Angry Birds Rio|1.3.2|Windows|AngryBirdsRioInstaller_1.3.2.exe|2,5|
|Angry Birds Rio|1.4.0|Windows|AngryBirdsRioInstaller_1.4.0.exe|2,5|
|Angry Birds Rio|1.4.2|Windows|AngryBirdsRioInstaller_1.4.2.exe|2,5|
|Angry Birds Rio|1.4.4|Windows|AngryBirdsRioInstaller_1.4.4.exe|2,5|

|Angry Birds Rio|1.7.0|Windows|AngryBirdsRioInstaller_1.7.0.exe|4|
|Angry Birds Rio|1.8.0|Windows|AngryBirdsRioInstaller_1.8.0.exe|4|
|Angry Birds Rio|2.0.0|Windows|AngryBirdsRioInstaller_2.0.0.exe|4|
|Angry Birds Rio|2.1.0|Windows|AngryBirdsRioInstaller_2.1.0.exe|4|
|Angry Birds Rio|2.2.0|Windows|AngryBirdsRioInstaller_2.2.0.exe|2|

1 - Accepts anything<br>
2 - Accepts anything in format XXXX-XXXX-XXXX-XXXX<br>
3 - The activation server needs to be ran on another device in the network<br>
4 - Not tested yet
5 - Uses the old activator (separate window)
> [!NOTE]
> The EXE files are built using PyInstaller

![Works on my machine](https://blog.codinghorror.com/content/images/uploads/2007/03/6a0120a85dcdae970b0128776ff992970c-pi.png)

**by nikolan and tom1212.**
