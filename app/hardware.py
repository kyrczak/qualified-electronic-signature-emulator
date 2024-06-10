import os
import psutil

KEY_FORMAT = ".bin"


def get_available_usb_sticks()->list[str]:
    """ 
    This function returns the available USB sticks.

    :return: A list of the available USB sticks.
    """
    usb_sticks_paths = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            usb_sticks_paths.append(partition.mountpoint)

    return usb_sticks_paths

def scan_for_key_files(usb_path: str)->list[str]:
    """
    This function scans the USB stick for key files.

    :param usb_path: The path to the USB stick.

    :return: A list of the key files found on the USB stick.
    """
    key_files = []
    try:
        for root, dir, files in os.walk(usb_path):
            for file in files:
                
                if file.endswith(KEY_FORMAT):
                    print(file)
                    key_files.append(os.path.join(root, file))
        
        return key_files
    except Exception as e:
        print(f"exception {e}")


    