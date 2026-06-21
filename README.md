# Custom Activation Servers for Old Rovio Games

## How it works

The script emulates Rovio's original activation server and redirects any traffic from Rovio's servers[^1] to the host machine[^2].

When the script receives a request, it always returns that the key is valid. That tricks the game into activating.

- [Latest x64 Download](https://github.com/nikolan123/rovio-drm-servers/releases/download/nightly/Rovio.CAS-win-x64.exe)
- [Latest x86 Download](https://github.com/nikolan123/rovio-drm-servers/releases/download/nightly/Rovio.CAS-win-x86.exe)
- [Decompilation Info](https://github.com/nikolan123/rovio-drm-servers/tree/main/decompilation)

[^1]: Rovio's activation servers are cloud.rovio.com/drm and drm-pc.angrybirdsgame.com

[^2]: Does this by editing the hosts file, which may trigger detections from some anti-virus programs

## Tested on

|Series|Version|Platform|Installer Name|Status|
|------|-------|--------|--------------|------|
|Angry Birds Seasons|4.1.0|Windows|AngryBirdsSeasonsInstaller_4.1.0.exe|1|
|Angry Birds|3.3.0|Windows|AngryBirdsInstaller_3.3.0.exe|1|
|Angry Birds|4.0.0|Windows|AngryBirdsInstaller_4.0.0.exe|1|
|Angry Birds Star Wars|1.5.0|Windows|AngryBirdsStarWarsInstaller_1.5.0.exe|1|
|Angry Birds Star Wars II|1.5.1|Windows|AngryBirdsStarWarsIIInstaller_1.5.1.exe|1|
|Angry Birds Rio|1.1.0|Windows|AngryBirdsRioInstaller_1.1.0.exe|2,3,5|
|Angry Birds Rio|1.2.2|Windows|AngryBirdsRioInstaller_1.2.2.exe|2,5|
|Angry Birds Rio|1.3.2|Windows|AngryBirdsRioInstaller_1.3.2.exe|2,5|
|Angry Birds Rio|1.4.0|Windows|AngryBirdsRioInstaller_1.4.0.exe|2,5|
|Angry Birds Rio|1.4.2|Windows|AngryBirdsRioInstaller_1.4.2.exe|2,5|
|Angry Birds Rio|1.4.4|Windows|AngryBirdsRioInstaller_1.4.4.exe|2,5|
|Angry Birds Rio|1.7.0|Windows|AngryBirdsRioInstaller_1.7.0.exe|2|
|Angry Birds Rio|1.8.0|Windows|AngryBirdsRioInstaller_1.8.0.exe|2|
|Angry Birds Rio|2.0.0|Windows|AngryBirdsRioInstaller_2.0.0.exe|2|
|Angry Birds Rio|2.1.0|Windows|AngryBirdsRioInstaller_2.1.0.exe|2|
|Angry Birds Rio|2.2.0|Windows|AngryBirdsRioInstaller_2.2.0.exe|2|

1 - Accepts anything<br>
2 - Accepts anything in format XXXX-XXXX-XXXX-XXXX<br>
3 - The activation server needs to be run on another device in the network<br>
4 - Not tested yet<br>
5 - Uses the old activator (separate window)

## Supported Code Rewards

In Classic, Star Wars, and Star Wars II, you can redeem codes for prizes. While this server includes handling for SW1 and Classic, only SW2 has been tested since only it has this functionality supported on Windows. Below is a list of all of the codes supported for each game:

<details>
<summary>Angry Birds v3.3.0</summary>

- `SUPERSEEDXX` → `rovio-ad-codes-2` — awards 30 Super Seeds.

</details>

<details>
<summary>Angry Birds Star Wars v1.5.0</summary>

- `BONUSLEVELX` → `bonus` — awards 10 Mighty Falcons, or 30 when Dagobah content is unavailable.
- `PATHOFJEDIX` → `dagobah` — unlocks Path of the Jedi. Awards 30 Mighty Falcons if already unlocked.
- `ONEFALCONXX` → `falcon` — awards 1 Mighty Falcon.
- `BOBAFETTXXX` → `bobafett` — unlocks the Boba Fett Missions. Awards 30 Mighty Falcons if already unlocked.

</details>

<details>
<summary>Angry Birds Star Wars II v1.5.1</summary>

- `CREDITTIERA` → `cred-tier1` — awards 100 credits.
- `HASBROCODEA` → `hasbro-toy-codes-10` — awards 100 credits.
- `CREDITTIERB` → `cred-tier2` — awards 300 credits.
- `HASBROCODEB` → `hasbro-toy-codes-11` — awards 300 credits.

</details>

> [!NOTE]
> The EXE files are built using PyInstaller

![Works on my machine](https://blog.codinghorror.com/content/images/uploads/2007/03/6a0120a85dcdae970b0128776ff992970c-pi.png)

**by nikolan and tom1212.**
