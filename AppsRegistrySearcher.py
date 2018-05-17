from _winreg import *
import re
"""
Module used for searching apps' path strings in the windows registry
"""


class AppRegistrySearcher:

    def __init__(self):
        self._last_error = None

    def find_program_uninstall_path(self, program_name):
        """
        find_program_uninstall_path - Searching the uninstall string of a given app name in all the known uninstall
        registry paths.
        :param program_name - program name to search.
        """
        app_to_search = program_name.lower()
        registry_paths = {
            HKEY_CURRENT_USER: "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            HKEY_LOCAL_MACHINE: ["SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                                 "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall"]
        }
        apps_registry_paths = []
        # Checking if it's HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE path, sending each key to _open_key in order to get
        # the found values
        for root_key, sub_key in registry_paths.iteritems():
            try:
                if isinstance(sub_key, list):
                    for item in sub_key:
                        apps_registry_paths = self.__open_key(root_key, item, apps_registry_paths,
                                                              "UninstallString", app_to_search)
                else:
                    apps_registry_paths = self.__open_key(root_key, sub_key, apps_registry_paths,
                                                          "UninstallString", app_to_search)
            except Exception as error:
                self._last_error = error.args
                continue
        return apps_registry_paths

    def find_program_install_path(self, program_name):
        """
        find_program_install_path - Searching for install path of a given program name in all the known install
        registry paths
        :param program_name - program name to search.
        """
        app_to_search = program_name.lower()
        registry_paths = {
            HKEY_CURRENT_USER: "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
            HKEY_LOCAL_MACHINE: ["SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                                 "SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall",
                                 "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths"]
        }

        apps_registry_paths = []
        # Checking if it's HKEY_CURRENT_USER or HKEY_LOCAL_MACHINE path, sending each key to _open_key in order to get
        # the found values
        for root_key, sub_key in registry_paths.iteritems():
            try:
                if isinstance(sub_key, list):
                    for item in sub_key:
                        apps_registry_paths = self.__open_key(root_key, item, apps_registry_paths,
                                                              "InstallLocation", app_to_search)
                else:
                    apps_registry_paths = self.__open_key(root_key, sub_key, apps_registry_paths,
                                                          "InstallLocation", app_to_search)
            except Exception as error:
                self._last_error = error.args
                continue
        return apps_registry_paths

    def delete_registry(self, root_key, sub_key):
        try:
            key_handle = OpenKey(root_key, sub_key, 0, KEY_WOW64_64KEY + KEY_ALL_ACCESS)
            num_subkeys, num_values, l_modified = QueryInfoKey(key_handle)
            for i in range(0, num_subkeys):
                sub_sub_key = EnumKey(key_handle, 0)
                try:
                    DeleteKey(key_handle, sub_sub_key)
                except Exception, error:
                    self._last_error = error.args
                    self.delete_registry(root_key, sub_key + "\\" + sub_sub_key)
            DeleteKey(key_handle, "")
            key_handle.Close()
        except Exception as error:
            self._last_error = error.args

    def __open_key(self, root_key, sub_key, apps_registry_paths, requested_path, app_to_search):
        """
        find_program_install_path - # Finding a given registry key, returning a list of found uninstall/install paths
        registry paths
        :param root_key - Registry root_key.
        :param sub_key - Registry sub_key.
        :param apps_registry_paths - a list to store all the found app's paths.
        :param requested_path - sub_key value to query its value.
        :param app_to_search - program name to search.
        """
        try:
            key_handle = OpenKey(root_key, sub_key, 0, KEY_WOW64_64KEY + KEY_ALL_ACCESS)
            num_subkeys, num_values, l_modified = QueryInfoKey(key_handle)
            for i in range(num_subkeys):
                sub_sub_key = EnumKey(key_handle, i)
                sub_sub_key_handle = OpenKey(root_key, sub_key + "\\" + sub_sub_key, 0,
                                             KEY_WOW64_64KEY + KEY_ALL_ACCESS)
                try:
                    if sub_key == "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths":
                        app_name = QueryValueEx(sub_sub_key_handle, "Path")[0].lower()
                        path = app_name
                    else:
                        app_name = QueryValueEx(sub_sub_key_handle, "DisplayName")[0].lower()
                        path = QueryValueEx(sub_sub_key_handle, requested_path)[0]
                    found = re.findall(".*" + app_to_search + ".*", app_name)
                    if found:
                        apps_registry_paths.append(path)
                except WindowsError:
                    pass
            key_handle.Close()
        except WindowsError, error:
            self._last_error = error.args
        return apps_registry_paths
