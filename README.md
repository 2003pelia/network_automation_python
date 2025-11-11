# Network Automation with Python

**Automated Configuration and Backup System for Cisco Routers and Switches**

This project demonstrates how to automate network device management using **Python** and **Netmiko** — no hardware required.  
It securely connects to simulated routers or switches, performs **parallel configuration backups**, and **pushes new configuration commands** using **multi-threading** for speed and efficiency.

---

## Features

-  **Multi-threaded** SSH connections to multiple devices  
-  Automatic **configuration backups** with timestamps  
-  Pushes common configuration updates (banner, logging, disable HTTP)  
-  Supports **Cisco IOS devices** (works in GNS3 or Packet Tracer)  
-  Organized folder structure (`/backups`, `/logs`)  
-  Easy to expand for additional commands or integrations  

---

## Tools & Technologies

| Tool | Purpose |
|------|----------|
| **Python 3** | Scripting and automation |
| **Netmiko** | SSH connection library for network devices |
| **PyYAML** | Device inventory file parsing |
| **ThreadPoolExecutor** | Multi-threading for performance |
| **Cisco Packet Tracer** | Network simulation environment |

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/<yourusername>/network-automation-python.git
cd network-automation-python
