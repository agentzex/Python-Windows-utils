"""
This module helps finding details about services hosted in svchost.exe processes on Windows.

How to use:

processes_list = get_svchost_processes()
found_services = get_services_of_pid(processes_list, 876) - returns all services hosted by a running svchosts.exe pid
found_pids = get_pid_of_service(processes_list, "lanmanworkstation") - returns pids found of a searched service name
print_process(processes_list) - prints all svchosts processes currently running, their hosted services and pids

"""

import subprocess



class ServiceHost(object):
    def __init__(self, pid, services):
        self.pid = pid
        self.services = services

    @staticmethod
    def add_services_to_pid(services_to_add, service_instance):
        for service in services_to_add:
            service_instance.services.append(service)


def get_svchost_processes():
    processes_list = []
    buf = subprocess.check_output("""tasklist /svc /fi "imagename eq svchost.exe""")
    buf = buf.split("\r\n")
    for line in buf[3:]:
        line = line.split()
        if line and line[0] == "svchost.exe":
            new_line = []
            for item in line:
                if item.endswith(','):
                    item = item[:-1]
                new_line.append(item)
            p = ServiceHost(line[1], new_line[2:])
            processes_list.append(p)
        else:
            ServiceHost.add_services_to_pid(line, processes_list[-1])
    return processes_list


def print_process(processes_list):
    print "PID\t\t\tServices"
    print "========\t============================================"
    for process in processes_list:
        print process.pid + "\t\t\t" + ", ".join(process.services)


def get_services_of_pid(processes_list, pid):
    for process in processes_list:
        if process.pid == str(pid):
            return process.services


def get_pid_of_service(processes_list, service_name):
    found_pids = []
    for process in processes_list:
        for service in process.services:
            if service.lower() == service_name.lower():
                found_pids.append(process.pid)
                break
    return found_pids


