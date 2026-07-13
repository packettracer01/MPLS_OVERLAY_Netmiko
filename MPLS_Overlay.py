from netmiko import ConnectHandler
from getpass import getpass

# Prompt user for credentials
username = input("Enter SSH Username: ")
password = getpass("Enter SSH Password: ")

routers = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "hostname": "R1",
        "system_id": "0000.0000.0001"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.2",
        "hostname": "R2",
        "system_id": "0000.0000.0002"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.3",
        "hostname": "R3",
        "system_id": "0000.0000.0003"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.4",
        "hostname": "R4",
        "system_id": "0000.0000.0004"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.5",
        "hostname": "R5",
        "system_id": "0000.0000.0005"
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.100.6",
        "hostname": "R6",
        "system_id": "0000.0000.0006"
    }
]

for router in routers:

    device = {
        "device_type": router["device_type"],
        "host": router["host"],
        "username": username,
        "password": password,
    }

    connection = ConnectHandler(**device)

    config = [
        f"hostname {router['hostname']}",
        "router isis CORE",
        f"net 49.0001.{router['system_id']}.00",
        "is-type level-2-only",
        "metric-style wide",
        "mpls ldp sync",
        "interface Loopback0",
        "ip router isis CORE",
        "isis circuit-type level-2",
        "interface GigabitEthernet1",
        "ip router isis CORE",
        "isis network point-to-point",
        "mpls ip",
        "interface GigabitEthernet2",
        "ip router isis CORE",
        "isis network point-to-point",
        "mpls ip",
        "mpls label protocol ldp",
        "mpls ldp router-id Loopback0 force"
    ]

    print(f"\nConfiguring {router['hostname']} ({router['host']})...")

    output = connection.send_config_set(config)
    print(output)

    connection.save_config()
    connection.disconnect()

print("\nAll routers configured successfully.")
