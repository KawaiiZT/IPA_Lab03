from textfsmlab import R1Config, R2Config, S1Config
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

network = {
    "S1": "172.31.13.3",
    "R1": "172.31.13.4",
    "R2": "172.31.13.5"
}

def get_int_descriptions(ip):
    device = createdevice(ip)
    with ConnectHandler(**device) as conn:
        return conn.send_command("show interfaces description", use_textfsm=True)

def test_S1():
    S1Config()
    descriptions = get_int_descriptions(network["S1"])
    intf = {d['port']: d['description'] for d in descriptions}
    assert intf["Gi0/0"] == "Connect to Gig 0/3 of S0"
    assert intf["Gi0/1"] == "Connect to Gig 0/2 of R2"
    assert intf["Gi1/1"] == "Connect to PC"

def test_R1():
    R1Config()
    descriptions = get_int_descriptions(network["R1"])
    intf = {d['port']: d['description'] for d in descriptions}
    assert intf["Gi0/0"] == "Connect to Gig 0/1 of S0"
    assert intf["Gi0/1"] == "Connect to PC"
    assert intf["Gi0/2"] == "Connect to Gig 0/1 of R2"

def test_R2():
    R2Config()
    descriptions = get_int_descriptions(network["R2"])
    intf = {d['port']: d['description'] for d in descriptions}
    assert intf["Gi0/0"] == "Connect to Gig 0/2 of S0"
    assert intf["Gi0/1"] == "Connect to Gig 0/2 of R1"
    assert intf["Gi0/2"] == "Connect to Gig 0/1 of S1"
    assert intf["Gi0/3"] == "Connect to WAN"
