def addrovio(urlto):
    #rovio urls
    hostsentrys = [
        f"{urlto} drm-pc.angrybirdsgame.com",
        f"{urlto} cloud.rovio.com"
    ]
    #read hosts file
    try:
        with open("c:\windows\system32\drivers\etc\hosts", "r") as dahosts:
            lines = dahosts.readlines()
            allhosts = ""
            for line in lines:
                allhosts += line
    except Exception as e:
        return f"Error reading hosts file: {e}"
    #add stuffs if not found
    try:
        with open("c:\windows\system32\drivers\etc\hosts", "a") as dahosts:
            for entry in hostsentrys:
                if not entry in allhosts:
                    dahosts.write("\n")
                    dahosts.write(entry)
                    print(f"Wrote {entry} to the hosts file")
                else:
                    print(f"Skipping {entry} as its already there")
    except Exception as e:
        return f"Error writing to hosts file: {e}"
    return "Success"
