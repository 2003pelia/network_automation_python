#!/usr/bin/env python3
"""
Network Automation with Python
------------------------------
Automates network device backups and configuration changes using Netmiko.
Includes multi-threading for performance and structured logging.

Author: Preston Elia
"""

from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
import yaml
import datetime
import logging
import os
import sys

# -----------------------------
# Setup folders
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# -----------------------------
# Logging setup
# -----------------------------
today = datetime.date.today().strftime("%Y-%m-%d")
log_file = os.path.join(LOG_DIR, f"automation_log_{today}.txt")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------------
# Load device list
# -----------------------------
DEVICE_FILE = os.path.join(BASE_DIR, "devices.yaml")
try:
    with open(DEVICE_FILE) as f:
        devices = yaml.safe_load(f)
        if not devices:
            raise ValueError("Device list is empty or invalid.")
except Exception as e:
    print(f" Error loading {DEVICE_FILE}: {e}")
    sys.exit(1)

# -----------------------------
# Configuration to push
# -----------------------------
CONFIG_COMMANDS = [
    "banner motd ^Authorized Access Only!^",
    "service timestamps log datetime",
    "logging buffered 32000",
    "no ip http server"
]

# -----------------------------
# Backup and config push logic
# -----------------------------
def backup_and_push(device):
    host = device.get("host", "Unknown")
    try:
        print(f" Connecting to {host}...")
        net_connect = ConnectHandler(**device)

        # Backup current configuration
        running_config = net_connect.send_command("show running-config")
        backup_file = os.path.join(BACKUP_DIR, f"{host}_backup_{today}.txt")
        with open(backup_file, "w") as f:
            f.write(running_config)
        logging.info(f" Backup successful for {host}")
        print(f" Backup complete for {host}")

        # Push configuration commands
        print(f"  Pushing configuration updates to {host}...")
        output = net_connect.send_config_set(CONFIG_COMMANDS)
        save_output = net_connect.save_config()

        # Log configuration output
        log_entry = f"--- CONFIG PUSH OUTPUT ({host}) ---\n{output}\n{save_output}\n"
        logging.info(log_entry)
        print(f" Configuration updated for {host}")

        net_connect.disconnect()

    except Exception as e:
        logging.error(f" Error on {host}: {e}")
        print(f" Failed on {host}: {e}")

# -----------------------------
# Run multi-threaded automation
# -----------------------------
def main():
    print(f" Starting automation for {len(devices)} devices...\n")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(backup_and_push, device) for device in devices]
        for future in as_completed(futures):
            future.result()

    print("\n All tasks complete. Check the 'backups' and 'logs' folders for results.")
    logging.info("All device automation tasks complete.")

if __name__ == "__main__":
    main()

