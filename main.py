import os 
import subprocess
import random

def saved_port(file_path):
    """ get old configured port. """
    ordp = open(file_path,"r")
    port = ordp.read()
    ordp.close()

    return port

def random_port(file_path, start, stop, step):
    """ get new default random port, and save into storage file."""
    random_port = random.randrange(start, stop, step)

    # save random default port into file.
    rdp = open(file_path,"w")
    rdp.write(str(random_port))

    return random_port

def replace_string_in_file(file_path, old_str, new_str):
    """ Reads file and replace old string with the new one """
    # Validate file existence
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exists.")
        return False

    try: 
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace content
        updated_content = content.replace(str(old_str), str(new_str))

        # write if changes are made
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Replaced all '{old_str}' with '{new_str}'.")
        else:
            print(f"No '{old_str}' found.")

        return True

    except (OSError, IOError) as e:
        print(f"File Error: {e}")
        return False

def add_windows_firewall_rule(port, action="allow", protocol="TCP", direction="in"):
    """
    Adds an inbound firewall rule to the Windows Firewall.
    If not add, windows will not allow custom port to be access.
    """
    command = [
        "netsh",
        "advfirewall",
        "firewall",
        "add",
        "rule",
        f"name=Apache2D Port {port}",
        f"dir={direction}",
        f"action={action}",
        f"protocol={protocol}",
        f"localport={port}"
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to add rule Apache2D Port {port}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

def port_forwarding(port, listenport):
    """
    port forwarding for default and ssl port
    forwarding 80 and 443 into custom port.
    """
    command = [
        "netsh",
        "interface",
        "portproxy",
        "add",
        "v4tov4",
        f"listenport={listenport}",
        "listenaddress=0.0.0.0",
        f"connectport={port}",
        "connectaddress=127.0.0.1"
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except Exception as e:
        print(f"An unexcepted error occured: {e}")

def check_folder_existance(path):
    """ Validate folder path """
    if not os.path.exists(path):
        print(f"[WARN] Folder does not found")
        return False
    else:
        return True

def init():
    """ 
    create storage folder and init file with 
    default value port 80 and 443 if not existed
    """
    if os.path.isdir("storage"):
        pass
    else:
        os.makedirs("storage", exist_ok=True)


# This is from my POV using Apache24, All developments config will be on conf/extra/developments folder, which will set by 
# include <example.conf> in conf/extra/httpd-vhosts.conf file. We need to change every port listed in the vhost file.
# in my perpective in learning Apache24 , we also need to change to custom used port in httpd.conf and httpd-ssl.conf
#
# Example usage

# in init, create storage folder if not exists
init()
# i will configure random default and ssl port using exmaple below
pts = ["default","ssl"]
for pt in pts:
    # make file path string
    fp = f"storage/recent.{pt}.port"

    # Validate file existence. else will get recent configured port.
    if not os.path.isfile(fp):
        print(f"[ERROR] File '{fp}' does not exists. Creating '{fp}' with default port...")
        old_port = "80" if pt == "default" else "443"
        with open(fp, "w") as file:
            file.write(old_port)
        print(f"[INFO] '{fp}' file successfully create.")
    else:
        old_port = saved_port(fp)
    
    # get random custom new port
    new_port = random_port(fp, 80 if pt == "default" else 443, 65536, 1)

    # file or directory that need to change custom port
    # this is my directory that need to change port in Apache24
    conf_files = [
        "D:/Project/Apache/Apache24/conf/httpd.conf",
        "D:/Project/Apache/Apache24/conf/extra/httpd-ssl.conf",
        "D:/Project/Apache/Apache24/conf/extra/httpd-vhosts.conf",
        "D:/Project/Apache/Apache24/conf/extra/developments/"
    ]

    for cf in conf_files:
        # check if path is file or directory
        if not os.path.isfile(cf):
            for fn in os.listdir(cf):
                cfp = os.path.join(cf, fn)
                if os.path.isdir(cfp):
                    continue
                replace_string_in_file(cfp, old_port, new_port)
        else:
            replace_string_in_file(cf, old_port, new_port)

    # add firewall rile to allow custom port to be access
    add_windows_firewall_rule(new_port)
    #port forwarding default and ssl into new custom
    port_forwarding(new_port, 80 if pt == "default" else 443)


