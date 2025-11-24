OT Security Lab – PLC, Modbus, HMI, Firewall

IN PROGRESS

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

Addressing (inside the Docker network):

- `plc`   → 10.0.0.10 (Modbus TCP server)
- `plc2`  → 10.0.0.11 (Modbus TCP server – BESS)
- `fw`    → 10.0.0.5  (router + firewall between IT and OT)
- `hmi`   → 10.0.0.30 (Node-RED / HMI)
- `it_test` → 10.0.0.2 (IT host)

System Architecture Diagram

![OT DIAGRAM](screenshots/OT.jpg)



       

OT Zones:

- Zone 1 – PLCs (Critical Process Controllers)
- Zone 2 – HMI (Monitoring only)
- Zone 3 - Firewall
- Zone 4 – IT Network (Restricted – blocked access to PLC)

Security concepts implemented:

- Zone & Conduit architecture (IEC 62443)  
- Modbus traffic control (TCP/502)  
- Segmentation and communication filtering  
- Alarm logic & threshold monitoring  
- Prevention of write commands from HMI to PLC unless explicitly allowed  
- Basic logging mechanism with JSON logs  


Technologies Used

- ICS Simulation | Docker / Docker Compose 
- PLC Logic | Python (`pymodbus`) 
- HMI | Node-RED 
- Network Control | `iptables`, Linux 
- Protocol | Modbus TCP 
- Dashboard | Node-RED UI 
- Logging | JSON → file (`/data/alarm-log.txt`)
  
What this lab demonstrates

- Basic OT network segmentation using Docker networking + firewall
- Secure Modbus TCP communication patterns
- HMI to PLC interaction and alarm logic
- Logging strategy ready for SIEM/SOC integration
- BESS-style control logic (SoC monitoring and threshold management)
  
Screenshots:

HMI DASHBOARD - real-time OT process monitoring

![HMI Dashboard](screenshots/hmi_dashboard.jpeg)

This dashboard is designed to displays real-time monitoring of two industrial PLCs similar to HMI/SCADA interface.

 PLC1 – Process Monitoring (e.g., temperature):
 
- Live chart using Modbus TCP (HR0 read).
- Alarm threshold dynamically adjustable via UI slider (written to PLC using Modbus).
- Status logic with conditional display: OK, Elevated, or Alarm, based on threshold.
- Gauge visualization for fast operator situational awareness.

 PLC2 – BESS (Battery Energy Storage System):
 
- Displays current State of Charge (SoC).
- Operator can define minimum allowed SoC level.
- Alarm logic alerts when SoC < limit.

Flow 1 - PLC1 Process Logic Alarm Simulation

![PLC1 Flow 1](screenshots/plc1_flow.jpeg)

This flow simulates a critical industrial process controlled by PLC1:

- Modbus READ (HR0): Retrieves process value at fixed intervals.
- Function node (“extract HR0”): Converts raw register value for processing.
- Alarm logic: Determines severity level (OK / Elevated / High Alarm).
- UI Slider (“SETPOINT”): Operator dynamically adjusts alarm threshold.
- Modbus WRITE (HR1): Writes new threshold to PLC.
- Alarm event logging: Persisted to /data/alarm-log.txt for audit/security analysis.

Flow 2 - PLC2 BESS Simulation

![PLC2 Flow 2](screenshots/plc2_flow.jpeg)

This flow represents a basic Battery Energy Storage System (BESS) control simulation:

- Modbus READ (HR0): Reads current State of Charge (%).
- Modbus READ (HR1): Retrieves minimum allowed SoC value.
- Alarm logic: If current SoC drops below limit → Alarm triggered.
- UI Slider (“Set Min SoC”): Operator can change minimum SoC threshold.
- Modbus WRITE: Updates new threshold in PLC memory.
- Event Logging: Alarm conditions are written to the same log for centralized tracking.

Future Improvements:

To further evolve this lab into a more realistic OT security simulation, I plan to implement:

- **Network-level segmentation (VLANs) simulated**
  
- **SIEM / Security Monitoring Integration**
  - Send alarm logs (from HMI) to a mock SOC using Elasticsearch / Wazuh.
  
- **Add Intrusion Detection**
  - Integrate Suricata to monitor ICS traffic (Modbus anomalies, Lateral movement detection).
  
- **Introduce authentication & encrypted ICS protocols**
  - Replace Modbus TCP with OPC UA
  
- **Multiple user access levels**
  - Add role-based access in HMI (operator vs. engineer vs. attacker simulation).
  
- **Simulate common cyber attack vectors**
  
- **More complex PLC logic**
  - Add interlock logic or emergency shutdown.
  
- **Include external services**
  - An industrial cloud API connection.
  

How to Run from Scratch

1. Make sure you have Docker installed and updated.

2. Clone the project.

git clone https://github.com/edyta9/ot-security-lab-docker.git
cd ot-security-lab-docker

3. Build and start containers:

docker compose up --build

4. Access Node-RED HMI:

http://localhost:1880/ui

5. Enter firewall container to check rules:

docker exec -it fw sh

iptables -L -v -n

6. Attempt simulated intrusion ( expected to fail):

docker exec -it it_test sh

nc -zv 10.0.0.10 502

> Disclaimer: This lab is for educational and training purposes only.  
> Do not connect it directly to production networks or real industrial systems.
