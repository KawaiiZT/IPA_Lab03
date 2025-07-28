import paramiko
import os
privatekey = "G:/IPA/admin"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

network = [
    "172.31.13.1",
    "172.31.13.2",
    "172.31.13.3",
    "172.31.13.4",
    "172.31.13.5"
]

for index, ip in enumerate(network):
    try:
        ssh.connect(
            hostname=ip,
            username='admin',
            key_filename=privatekey,
            allow_agent=False,
            look_for_keys=False,
            disabled_algorithms=dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])
        )
        if 0 <= index <= 2:
            print(f"Connecting to {ip} or Router{index}")
        elif 3 <= index <= 4:
            print(f"Connecting to {ip} or Switch{index - 2}")

        if index == 0:
            stdin, stdout, stderr = ssh.exec_command("show running-config")
            with open('R0_running_config', 'w') as file:
                file.write(stdout.read().decode())
            print("Saving R0 running config")

        ssh.close()

    except Exception as e:
        print(f"Failed to connect to {ip}: {e}")
