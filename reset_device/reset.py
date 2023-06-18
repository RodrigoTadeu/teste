import os
import fileinput
import subprocess

def reset_to_host_mode():
    os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')

    if(os.path.exists('/etc/default/bb-wl18xx.original')):
            os.system('rm -f /etc/default/bb-wl18xx')
            os.system('mv /etc/default/bb-wl18xx.original /etc/default/bb-wl18xx')

    if(os.path.exists('/etc/network/interfaces.original')):
            os.system('rm -f /etc/network/interfaces')
            os.system('mv /etc/network/interfaces.original /etc/network/interfaces')
    os.system('reboot')
