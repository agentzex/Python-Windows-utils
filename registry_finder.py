from _winreg import *
import re


def find_program_uninstall_path(program_to_search):
    # Use this to search for the uninstall paths of a given program name in all the known uninstall
    # registry paths, like Windows "add or remove program" does.
    found_paths = []
    program_to_search = program_to_search.lower()
    registry_paths = {
        HKEY_CURRENT_USER: "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        HKEY_LOCAL_MACHINE: ["SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                             "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"]
    }

    # Checking if it's HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE path, sending each key to check_key in order to get
    # the found values
    for key, sub_key in registry_paths.iteritems():
        try:
            if isinstance(sub_key, list):
                for item in sub_key:
                    apps_registry_paths = check_key(key, item, found_paths,
                                                          "UninstallString", program_to_search)
            else:
                apps_registry_paths = check_key(key, sub_key, found_paths,
                                                      "UninstallString", program_to_search)
        except Exception as e:
            print str(e.args)
    return found_paths


def find_program_install_path(program_to_search):
    # Use this to search for the installation paths of a given program name in all the known installation registry paths.

    program_to_search = program_to_search.lower()
    registry_paths = {
        HKEY_CURRENT_USER: "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
        HKEY_LOCAL_MACHINE: ["SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                             "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                             "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"]
    }

    apps_registry_paths = []
    # Checking if it's HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE path, sending each key to check_key in order to get
    # the found values
    for root_key, sub_key in registry_paths.iteritems():
        try:
            if isinstance(sub_key, list):
                for item in sub_key:
                    apps_registry_paths = check_key(root_key, item, apps_registry_paths,
                                                          "InstallLocation", program_to_search)
            else:
                apps_registry_paths = check_key(root_key, sub_key, apps_registry_paths,
                                                      "InstallLocation", program_to_search)
        except Exception, e:
            print str(e)
    return apps_registry_paths


def check_key(key, sub_key, found_paths, registry_value_name, program_to_search):
    try:
        opened_key = OpenKey(key, sub_key, 0, KEY_WOW64_64KEY + KEY_ALL_ACCESS)
        subkeys_found, values_found, last_modified = QueryInfoKey(opened_key)
        for i in range(subkeys_found):
            sub_sub_key = EnumKey(opened_key, i)
            opened_sub_sub_key = OpenKey(key, sub_key + "\\" + sub_sub_key, 0,
                                         KEY_WOW64_64KEY + KEY_ALL_ACCESS)
            try:
                if sub_key == "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths":
                    found_program_path = QueryValueEx(opened_sub_sub_key, "Path")[0].lower()
                    path = found_program_path
                else:
                    found_program_path = QueryValueEx(opened_sub_sub_key, "DisplayName")[0].lower()
                    path = QueryValueEx(opened_sub_sub_key, registry_value_name)[0]
                found = re.findall(".*" + program_to_search + ".*", found_program_path)
                if found:
                    found_paths.append(path)
            except WindowsError, e:
                pass
        opened_key.Close()
    except WindowsError, e:
        print str(e.args)
    return found_paths

if __name__ == "__main__":

    # Use these functions to search for programs install and uninstall path strings in the windows registry

    for found in find_program_uninstall_path("Winrar"):
        print found

    # for found in find_program_install_path("chrome"):
    #     print found