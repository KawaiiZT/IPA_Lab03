from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader

privatekey = "G:/IPA/admin"
username = 'admin'

env = Environment(loader=FileSystemLoader('.'))

template = env.get_template('config_template.j2')

# --------------------
# DEVICE CONFIGURATION
# --------------------
devices = {
    'R1': {
        'ip': '172.31.13.4',
        'config': {
            'loopback': {'ip': '1.1.1.1', 'mask': '255.255.255.255'},
            'ospf': {
                'process_id': 10,
                'vrf': 'control-data',
                'router_id': '1.1.1.1',
                'networks': [
                    {'ip': '1.1.1.1', 'wildcard': '0.0.0.0', 'area': 0},
                    {'ip': '172.31.13.0', 'wildcard': '0.0.0.255', 'area': 0},
                    {'ip': '10.13.0.0', 'wildcard': '0.0.255.255', 'area': 0}
                ]
            }
        }
    },
    'R2': {
        'ip': '172.31.13.5',
        'config': {
            'loopback': {'ip': '2.2.2.2', 'mask': '255.255.255.255'},
            'ospf': {
                'process_id': 10,
                'vrf': 'control-data',
                'router_id': '2.2.2.2',
                'networks': [
                    {'ip': '2.2.2.2', 'wildcard': '0.0.0.0', 'area': 0},
                    {'ip': '172.31.13.0', 'wildcard': '0.0.0.255', 'area': 0},
                    {'ip': '10.13.0.0', 'wildcard': '0.0.255.255', 'area': 0}
                ],
                'default_originate': True
            },
            'interfaces': [
                {'name': 'range g0/1-2', 'vrf': 'control-data', 'nat': 'inside'},
                {'name': 'g0/3', 'vrf': 'control-data', 'dhcp': True, 'nat': 'outside'}
            ],
            'acls': [
                {'number': 1, 'network': '172.31.13.0', 'wildcard': '0.0.0.255'},
                {'number': 1, 'network': '10.13.0.0', 'wildcard': '0.0.255.255'}
            ],
            'nat_config': {
                'acl': 1,
                'interface': 'GigabitEthernet0/3',
                'vrf': 'control-data'
            }
        }
    },
    'S1': {
        'ip': '172.31.13.3',
        'config': {
            'vlans': [{'id': 101, 'name': 'control-data'}],
            'switchports': [
                {'name': 'gi 0/1', 'vlan': 101},
                {'name': 'gi 1/1', 'vlan': 101}
            ]
        }
    }
}

# ------------------------
# DEPLOY CONFIGS TO DEVICES
# ------------------------
for hostname, data in devices.items():
    ip = data['ip']
    rendered_config = template.render(**data['config'])

    device_params = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }

    print(f"\n--- Connecting to {hostname} ({ip}) ---")
    with ConnectHandler(**device_params) as ssh:
        result = ssh.send_config_set(rendered_config.splitlines())
        print(result)
