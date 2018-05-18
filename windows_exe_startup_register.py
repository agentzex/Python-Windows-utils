from ntpath import basename
import os
import _winreg


def register_on_registry(exec_path, registry_name, exec_args=None):
    registry_path = "Software\Microsoft\Windows\CurrentVersion\Run"
    exec_path = '"' + exec_path + '"'
    if exec_args:
        exec_path = exec_path + " " + exec_args
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, registry_path, 0, _winreg.KEY_ALL_ACCESS)
        _winreg.SetValueEx(key, registry_name, 0, _winreg.REG_SZ, exec_path)
        _winreg.CloseKey(key)
        print "Executable registered on registry successfully"
    except Exception, e:
        print "Error writing this executable on the registry. Error was: " + str(e.args)


def remove_exec_from_registry(registry_name):
    registry_path = "Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, registry_path, 0, _winreg.KEY_ALL_ACCESS)
        _winreg.DeleteValue(key, registry_name)
        _winreg.CloseKey(key)
        print "Executable removed from registry successfully"
    except Exception, e:
        print "Error removing this executable from the registry. Error was: " + str(e.args)


windows_startup_directory = os.getenv('APPDATA') + '\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\'


def register_on_startup_directory(exec_path, exec_args=None):
    exec_name = basename(exec_path) + ".bat"
    startup_script = write_batch_script(exec_path, exec_args)
    with open(windows_startup_directory + exec_name, "w") as file:
        file.write(startup_script)


def remove_startup_directory_exec_file(exec_file_path_to_remove):
    exec_name = basename(exec_file_path_to_remove) + ".bat"
    try:
        os.remove(windows_startup_directory + exec_name)
    except Exception, e:
        print "Couldn't remove " + exec_name + "\nError was: " + str(e.args)


def remove_all_startup_directory_files():
    for startup_file in os.listdir(windows_startup_directory):
        try:
            os.remove(windows_startup_directory + startup_file)
        except Exception, e:
            print "Couldn't remove " + startup_file + "\nError was: " + str(e.args)


def get_startup_directory_files():
    """ Returns a list of all the current startup scripts located in the startup dir"""
    return os.listdir(windows_startup_directory)


def write_batch_script(exec_path, exec_args):
    if exec_args:
        start_script = "echo off\n" + exec_path + " " + exec_args
    else:
        start_script = "echo off\n " + exec_path
    return start_script



if __name__ == "__main__":
    # These function can help you register or delete an executable on the windows startup directory or on windows registry (under
    # HKCU\Software\Microsoft\Windows\CurrentVersion\Run)

    # If you are registering a python script and wish to run it silently (i.e. - so no console window will appear on screen),
    # then simply save it as .pyw instead of .py

    #Examples:
    #register_on_startup_directory("C:\Users\\" + os.getenv("USERNAME") + "\Desktop\\foo.py", "-p param1")
    #remove_startup_directory_exec_file("C:\Users\\" + os.getenv("USERNAME") + "\Desktop\\foo.py")
    #remove_all_startup_directory_files()

    register_on_registry("C:\Users\\" + os.getenv("USERNAME") + "\Desktop\\foo.py", "myscript", "-p param1")
    #remove_exec_from_registry("myscript")
