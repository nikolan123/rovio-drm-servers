# Scripts for game updates

These scripts allow you to publish an exe (possibly other files too) to the game and make it detect an update.

## Configuring hosts file

In your OS's hosts file, add the lines:
- `127.0.0.1 cloud.rovio.com`
- `127.0.0.1 drm-pc.angrybirdsgame.com`

(Only replace 127.0.0.1 with the IP of the computer hosting the server.py file if it isn't the same computer you're going to play the game on)

## Configuring server.py file

In the server.py file, find your game's name/names and remove the # from all the lines used by it.
Next, put your file onto a web server that doesn't force the client to use HTTPS. Then run: 


```
$filepath = Read-Host "Input file path pls: "
$file = Get-Item -Path "$filepath"
$fileSize = $file.Length
Write-Host "$fileSize bytes."
Get-FileHash $filepath -Algorithm MD5`
```

in PowerShell, supplying the path to the file.

You should see a number with "bytes" after it and a hash. Take them to the server.py file and replace:
- `yourfilesize` with the number before "bytes"
- `yourfilemd5` with the hash string
- Replace all `yourfilename`'s with the name of the file and `yourip` with the IP of the webserver.

Example below:

```
[Update]
Name=Angry Birds
URL=http://192.168.1.30/Angrybirdsver4.3.0.exe
Size=1605331
MD5=3D950D76A80A9812E92F124AE5BAB36E
ServerFileName=Angrybirdsver4.3.0.exe
FilePath=[APPDIR]Angrybirdsver4.3.0.exe
Version=4.3.0
```


You should now be able to start the server.py file and launch a game. It should say there's an update available as long as the version tag is higher than the current version.

If you get an error about a missing Flask module, run `pip install flask`.
