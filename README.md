OT Security Lab – Modbus, HMI, Firewall

This project is a small OT (Operational Technology) lab running entirely in Docker.  
It simulates two PLCs, an HMI, an OT firewall and an IT workstation, focusing on:

- secure Modbus TCP communication in an OT network,
- basic process and alarm logic,
- BESS (Battery Energy Storage System) behaviour,
- logging of alarm events in a format ready for SIEM / SOC.

Architecture

Containers:

- PLC1 (plc) – generic process controller (e.g. temperature / level), exposed via Modbus TCP.
- PLC2 (plc2) – BESS controller (SoC and minimum SoC limit), also Modbus TCP.
- HMI (hmi) – Node-RED instance:
  - acts as an HMI / mini-SCADA,
  - reads and writes Modbus registers,
  - implements alarm logic and logging.
- Firewall (fw) – Linux container with `iptables`
  - enforces OT firewall rules,
  - allows only HMI → PLC1/PLC2 Modbus TCP,
  - logs and drops IT → PLC traffic.
- IT workstation (it_test) – simulates an IT-side host / potential attacker.

Example addressing (inside the Docker network):

- `plc`   → 10.0.0.10 (Modbus TCP server)
- `plc2`  → 10.0.0.11 (Modbus TCP server – BESS)
- `fw`    → 10.0.0.5  (router + firewall between IT and OT)
- `hmi`   → 10.0.0.30 (Node-RED / HMI)
- `it_test` → 10.0.0.2 (IT host)

System Architecture:


        IT Zone                           OT Zone
  ┌─────────────────┐              ┌──────────────────────┐
  │  it_test        │              │  HMI (Node-RED)      │
  │  10.0.0.2       │              │  10.0.0.30           │
  └────────┬────────┘              └─────────┬────────────┘
           │  (routed via fw)                │  Modbus TCP
           ▼                                  ▼
     ┌────────────┐                    ┌────────────┬──────────────┐
     │  fw        │                    │  PLC1      │   PLC2       │
     │ 10.0.0.5   │                    │10.0.0.10   │10.0.0.11     │
     │ iptables   │                    │ PROCESS    │ BESS         │
     └────────────┘                    └────────────┴──────────────┘

OT Zones Example
- Zone 1 – PLCs (Critical Process Controllers)
- Zone 2 – HMI (Monitoring only)
- Zone 3 – IT Network (Restricted – blocked access to PLC)

Security concepts implemented:
Zone & Conduit architecture (IEC 62443)  
Modbus traffic control (TCP/502)  
Segmentation and communication filtering  
Alarm logic & threshold monitoring  
Prevention of write commands from HMI to PLC unless explicitly allowed  
Basic logging mechanism with JSON logs  
Example of cyberattack simulation (unauthorised write attempt)

Technologies Used

ICS Simulation | Docker / Docker Compose 
PLC Logic | Python (`pymodbus`) 
HMI | Node-RED 
Network Control | `iptables`, Linux 
Protocol | Modbus TCP 
Dashboard | Node-RED UI 
Logging | JSON → file (`/data/alarm-log.txt`) 


How to Run
Build and start containers:
docker compose up --build

Access Node-RED HMI:
http://localhost:1880/ui

Enter firewall container to check rules:
docker exec -it fw sh
iptables -L -v -n
