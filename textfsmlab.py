from netmiko import ConnectHandler

privatekey = "G:/IPA/admin"
username = "admin"

def createdevice(ip):
    return {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }
def config_gen(cdpnei):
    config = []
    for neighbor in cdpnei:
        local_interface = neighbor['local_interface'].replace(" ", "")
        remote_interface = neighbor['platform'] + " " + neighbor['neighbor_interface']
        neighbor_name = neighbor['neighbor_name'].replace(".ipa.com", "")
        config.append(f'int {local_interface}')
        config.append(f'description Connect to {remote_interface} of {neighbor_name}')
        config.append('exit')
    return config

# R1 - has 3 interfaces:
# Gi0/0: Connect to S0 Gi0/1
# Gi0/1: Connect to PC
# Gi0/2: Connect to R2 Gi0/1
def R1Config():
    device = createdevice("172.31.13.4")
    conn = ConnectHandler(**device)
    cdp_neighbors = conn.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(cdp_neighbors)
    config.extend([
        'int Gig0/1',
        'description Connect to PC',
        'exit'
    ])
    conn.send_config_set(config)
    conn.disconnect()

# R2 - has 4 interfaces:
# Gi0/0: Connect to S0 Gi0/2
# Gi0/1: Connect to R1 Gi0/2
# Gi0/2: Connect to S1 Gi0/1
# Gi0/3: DHCP client — Connect to WAN
def R2Config():
    device = createdevice("172.31.13.5")
    conn = ConnectHandler(**device)
    cdp_neighbors = conn.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(cdp_neighbors)
    config.extend([
        'int Gig0/3',
        'description Connect to WAN',
        'exit'
    ])
    conn.send_config_set(config)
    conn.disconnect()

# S1 - has 3 interfaces:
# Gi0/0: Connect to S0 Gi0/3
# Gi0/1: Connect to R2 Gi0/2
# Gi1/1: Connect to PC
def S1Config():
    device = createdevice("172.31.13.3")
    conn = ConnectHandler(**device)
    cdp_neighbors = conn.send_command("show cdp neighbors", use_textfsm=True)
    config = config_gen(cdp_neighbors)
    config.extend([
        'int Gig1/1',
        'description Connect to PC',
        'exit'
    ])
    conn.send_config_set(config)
    conn.disconnect()
