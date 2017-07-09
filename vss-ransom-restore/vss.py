#!/usr/bin/env python
import win32com.client


class ShadowCopy:
    def __init__(self):
        """
        Creates shadow copies for each local drive in the set drive_letters.
        """
        self.__shadow_paths = self.__vss_list()

    def shadow_path(self, path):
        """
        Takes a regular file system path and transforms it into an
        equivalent path in a shadow copy
        """
        # TODO: validate path starts with a drive letter
        drive_letter = path[0]
        for shadow_path in self.__shadow_paths:
            new_path = path.replace(drive_letter + u':',
                                    shadow_path,
                                    1)
            # TODO: handle exact exception
            try:
                with open(new_path, 'rb'):
                    return new_path
            except:
                pass
        return None

    def __vss_list(self):
        wcd = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        wmi = wcd.ConnectServer(".", "root\cimv2")
        query = "SELECT * FROM Win32_ShadowCopy ORDER BY InstallDate DESC"
        obj = wmi.ExecQuery(query)
        return [o.DeviceObject for o in obj]