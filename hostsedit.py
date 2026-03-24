def addrovio(urlto):
    """Add Rovio server redirects to the hosts file."""
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    
    # Rovio URLs
    host_entries = [
        f"{urlto} drm-pc.angrybirdsgame.com",
        f"{urlto} cloud.rovio.com"
    ]
    
    # Read hosts file
    try:
        with open(hosts_path, "r") as dahosts:
            lines = dahosts.readlines()
            allhosts = "".join(lines)
    except PermissionError:
        return "Error: Permission denied. Please run this script as administrator."
    except FileNotFoundError:
        return f"Error: Hosts file not found at {hosts_path}"
    except Exception as e:
        return f"Error reading hosts file: {e}"
    
    # Check what needs to be added
    entries_to_add = []
    entries_existing = []
    
    for entry in host_entries:
        if entry not in allhosts:
            entries_to_add.append(entry)
        else:
            entries_existing.append(entry)
    
    # Report existing entries
    if entries_existing:
        print("Already in hosts file:")
        for entry in entries_existing:
            print(f"  - {entry}")
    
    # Add new entries if needed
    if entries_to_add:
        try:
            with open(hosts_path, "a") as dahosts:
                for entry in entries_to_add:
                    dahosts.write(f"\n{entry}")
                    print(f"  + Added: {entry}")
        except PermissionError:
            return "Error: Permission denied. Please run this script as administrator."
        except Exception as e:
            return f"Error writing to hosts file: {e}"
        return "Success: Hosts file updated"
    else:
        return "Success: All entries already present"
