from netmiko import ConnectHandler

privatekey = "G:/IPA/admin"
username = 'admin'

devices = {
    'R1': ('172.31.13.4', [
        "int Loopback0", 
        "ip add 1.1.1.1 255.255.255.255",
        "no shut", 
        "exit",
        "router ospf 10 vrf control-data","router-id 1.1.1.1","network 1.1.1.1 0.0.0.0 area 0", 
        "network 172.31.13.0 0.0.0.255 area 0",
        "network 10.13.0.0 0.0.255.255 area 0",
        "exit"
    ]),
    'R2': ('172.31.13.5', [
        "int Loopback0", 
        "ip add 2.2.2.2 255.255.255.255", "no shut", "exit", 
        "router ospf 10 vrf control-data", "router-id 2.2.2.2", "network 2.2.2.2 0.0.0.0 area 0", 
        "network 172.31.13.0 0.0.0.255 area 0",
        "network 10.13.0.0 0.0.255.255 area 0", "default-information originate always",
        "exit", 
        "int range g0/1-2","vrf forwarding control-data","ip nat inside","no shut" 
        "exit", 
        "int g0/3", "vrf forwarding control-data", "ip add dhcp", "ip nat outside", 
        "no shut",
        "exit", 
        "access-list 1 permit 172.31.13.0 0.0.0.255",
        "access-list 1 permit 10.13.0.0 0.0.255.255",
        "ip nat inside source list 1 interface GigabitEthernet0/3 vrf control-data overload"
    ]),
    'S1': ('172.31.13.3', [
        "vlan 101", 
        "name control-data", 
        "exit", 
        "int gi 0/1", "switchport mode access", "switchport access vlan 101", 
        "no shut",
        "exit",
        "int gi 1/1", "switchport mode access", "switchport access vlan 101",
        "no shut",
        "exit"
    ])
}

for hostname, (ip, commands) in devices.items():
    device_params = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }

    print(f"Connecting to {hostname} ({ip})...")
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_config_set(commands)
        print(result)
