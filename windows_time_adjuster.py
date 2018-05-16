import win32api
import ntsecuritycon
import win32security


def adujst_time_privilege(privilege):
    flags = ntsecuritycon.TOKEN_ADJUST_PRIVILEGES | ntsecuritycon.TOKEN_QUERY
    htoken = win32security.OpenProcessToken(win32api.GetCurrentProcess(), flags)
    id = win32security.LookupPrivilegeValue(None, privilege)
    newPrivileges = [(id, ntsecuritycon.SE_PRIVILEGE_ENABLED)]
    win32security.AdjustTokenPrivileges(htoken, 0, newPrivileges)


def adjust_system_time(year, month, dayOfWeek, day, hour, minute, second, millseconds):
    try:
        win32api.SetSystemTime(year, month, dayOfWeek, day, hour, minute, second, millseconds)
    except Exception, e:
        print "error adjusting the system time: " + str(e)


def adjust_system_timezone(time_zone_tuple):
    # Enable the privilege for SetTimeZoneInformation
    try:
        adujst_time_privilege(win32security.SE_TIME_ZONE_NAME)
    except Exception, e:
        print "error getting the privilege token: " + str(e)

    try:
        win32api.SetTimeZoneInformation(time_zone_tuple)
    except Exception, e:
        print "error setting the new timezone: " + str(e)

if __name__ == "__main__":
    # Install win32api lib before using these functions!

    # Use this function for changing the windows system time.
    # All attributes should be an int
    # This only change the system time, so pay attention to the set timezone on the system too with the function below
    adjust_system_time(2018, 5, 0, 16, 12, 0, 0, 0)

    # Use this function for changing the windows system timezone.
    # Should receive a tuple of the following format:
    # [0]
    # int: Bias
    #
    # [1]
    # string: StandardName
    #
    # [2]
    # SYSTEMTIME
    # tuple: StandardDate
    #
    # [3]
    # int: StandardBias
    #
    # [4]
    # string: DaylightName
    #
    # [5]
    # daylightTime
    # tuple: DaylightDate
    #
    # [6]
    # int: DaylightBias
    adjust_system_timezone((-60, u'', (0, 0, 0, 0, 0, 0, 0, 0), 0,
                                 u'', (0, 0, 0, 0, 0, 0, 0, 0), 0))
