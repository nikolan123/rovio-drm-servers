# Scripts for game updates

These scripts allow you to publish a exe (Possibly other files too) to the game and make it detect a update

Configuring hosts file:

In your OSs hosts file add the line
`127.0.0.1 cloud.rovio.com` (only replace 127.0.0.1 with the ip of the computer hosting the server.py file if it isnt the same computer as your going to play the game on)

Configuring server.py file:

Find your games name/names and remove the # from all the lines used by it.
Next put your file onto a web server that doesnt force the client to use https now run 

`$filepath = Read-Host "Input file path pls: "
$file = Get-Item -Path "$filepath"
$fileSize = $file.Length
Write-Host "$fileSize bytes."
Get-FileHash $filepath -Algorithm MD5` 

in powershell supplying the path to the file
You should see a number with bytes after it and a hash take them to the server.py file and replace yourfilesize with the number before bytes and yourfilemd5 with the hash string and replace all yourfilename's with the name of the file and yourip with the ip of the webserver
Example below:

`
[Update]
Name=Angry Birds
URL=http://192.168.1.30/Angrybirdsver4.3.0.exe
Size=1605331
MD5=3D950D76A80A9812E92F124AE5BAB36E
ServerFileName=Angrybirdsver4.3.0.exe
FilePath=[APPDIR]Angrybirdsver4.3.0.exe
Version=4.3.0
    """`

You now should be able to start the server.py file and launch a game and it should say theres an update avalble as long as the version tag is higher then the current version

If you get an error about missing a module about flask run `pip install flask`

