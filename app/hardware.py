import os
import psutil

KEY_FORMAT = ".bin"


def get_available_usb_sticks()->list[str]:
    usb_sticks_paths = []
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts:
            usb_sticks_paths.append(partition.mountpoint)

    return usb_sticks_paths

def scan_for_key_files(usb_path: str)->list[str]:
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


    