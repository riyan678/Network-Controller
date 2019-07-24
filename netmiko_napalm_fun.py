from netmiko import ConnectHandler
from napalm import get_network_driver


def send_config(ipAddress_list, username, password, enable, command_list):
    '''
    This function is used to send like commands to one
    or more devices. Arguments are ipAddress_list,
    username, password, enable, and command_list.
    '''
    device_profile =[]
    for ip  in ipAddress_list:
        device = { "device_type": "cisco_xe",
                   "ip": ip,
                   "username": username,
                   "password": password,
                   "secret": enable
                  }
        device_profile.append(device)

    for profile in device_profile:
        connect = ConnectHandler(**profile)
        connect.enable()
        connect.send_config_set(command_list)
