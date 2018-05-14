import platform


if "Windows" in platform.system():
    host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
elif "Darwin" in platform.system():
    host_file_path = r"/etc/hosts"


def add_multiple_hostnames(list_of_hostnames):
    # Receives a list of tuples, each tuple consist an ip and hostname:
    # [("192.168.2.1", "domain1.com"), ("10.0.0.2", "domain2.com")]

    lines = open(host_file_path, "r").readlines()
    for entry in list_of_hostnames:
        for line in lines:
            if entry[1] in line:
                lines.pop(lines.index(line))

    for entry in list_of_hostnames:
        lines.append(entry[0] + "\t" + entry[1] + "\n")

    with open(host_file_path, "w") as file:
        for line in lines:
            file.write(line)

def add_hostname(ip, hostname):
    # remove old entry if exists
    remove_hostname(hostname)

    with open(host_file_path, "a") as file:
        file.write(ip + "\t" + hostname)

def remove_hostname(hostname):
    host_file = ""

    with open(host_file_path, "r") as file:
        for line in file:
            if hostname not in line:
                host_file = host_file + line

    with open(host_file_path, "w") as file:
        file.write(host_file)

def revert_to_default():
    default = """# Copyright (c) 1993-2006 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
# localhost name resolution is handle within DNS itself.
#       127.0.0.1       localhost
#       ::1             localhost 

127.0.0.1	localhost
255.255.255.255	broadcasthost
"""

    with open(host_file_path, "w") as file:
        file.write(default)
