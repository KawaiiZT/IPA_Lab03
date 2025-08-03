from netmiko import ConnectHandler
import re

privatekey = "G:/IPA/admin"
username = "admin"

routers = {
    "R1": "172.31.13.4",
    "R2": "172.31.13.5"
}

interface_pattern = re.compile(
    r"^(?P<iface>\S+)\s+(?P<ip>\S+)\s+\S+\s+\S+\s+up\s+up",
    re.MULTILINE
)

uptime_pattern = re.compile(r"(\S+) uptime is (.+)")

for hostname, ip in routers.items():
    device_params = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'use_keys': True,
        'key_file': privatekey,
        "disabled_algorithms": dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
    }

    print(f"\n[Connecting to {hostname} - {ip}]")
    with ConnectHandler(**device_params) as ssh:
        output = ssh.send_command("show ip interface brief")
        matches = interface_pattern.finditer(output)

        version_output = ssh.send_command("show version")
        uptime_match = uptime_pattern.search(version_output)
        if uptime_match:
            uptime_text = uptime_match.group(2)
            print(f"{hostname} Uptime: {uptime_text}")
        else:
            print("Uptime not found.")
        found = False
        for match in matches:
            if not found:
                print(f"\nActive interfaces on {hostname}:")
                found = True
            iface = match.group("iface")
            ip_addr = match.group("ip")
            print(f"  - {iface} (IP: {ip_addr})")
        if not found:
            print("No active interfaces found.")
