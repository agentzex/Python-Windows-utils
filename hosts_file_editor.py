import platform


if "Windows" in platform.system():
    host_file_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    host_file_path = r"/etc/hosts"


def remove_multiple_hostnames(list_of_hostnames):
    # Receives a list of hostnames to remove from the hosts file:
    # ["domain.com", "domain2.com"]

    lines = open(host_file_path, "r").readlines()
    for entry in list_of_hostnames:
        for line in lines:
            if entry in line:
                lines.pop(lines.index(line))

    with open(host_file_path, "w") as file:
        for line in lines:
            file.write(line)

def add_multiple_hostnames(list_of_hostnames):
    # Receives a list of tuples, each tuple consist an ip and hostname, to add to the hosts file:
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

def restore_to_defualt():
    default = ""

    if "Windows" in platform.system():
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
    ::1    localhost 
    """
    elif "Linux" in platform.system():
        default = """# Do not remove the following line, or various programs
        # that require network functionality will fail.
        127.0.0.1 localhost
        # The following lines are desirable for IPv6 capable hosts
        ::1 ip6-localhost ip6-loopback
        fe00::0 ip6-localnet
        ff00::0 ip6-mcastprefix
        ff02::1 ip6-allnodes
        ff02::2 ip6-allrouters
        ff02::3 ip6-allhosts"""

    elif "Darwin" in platform.system():
        default = """##
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting. Do not change this entry.
##
127.0.0.1 localhost
255.255.255.255 broadcasthost
::1 localhost
fe80::1%lo0 localhost"""

    with open(host_file_path, "w") as file:
        file.write(default)

