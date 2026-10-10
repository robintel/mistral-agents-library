---
type: platform
family: industrial
---

# Siemens S7 PLC

**The workhorse of industrial automation**: Siemens' SIMATIC S7 family
of Programmable Logic Controllers, powering factories worldwide for
decades. From the compact S7-200 to the high-performance S7-1500, the
S7 platform offers deterministic control, extensive IO, and seamless
integration with the Totally Integrated Automation (TIA) ecosystem.

## Eras

The era is declared by the **controller family** and **firmware version**.

**S7-200 (1996)**: Entry-level micro PLC. PPI/MPI/Freeport comms.
CPU 21x/22x. 4-16 KB program. STEP 7 Micro/WIN.

**S7-200 Smart (2014)**: Successor. Ethernet built-in. 50-250 KB program.
TIA Portal V13+.

**S7-300 (1994)**: Modular mid-range. MPI, PROFIBUS DP, Ethernet.
CPU 31xC/31x/31x-2 PN/DP. 128 KB-1 MB. STEP 7 V5.x.

**S7-400 (1994)**: High-end for large applications. Multi-rack.
CPU 41x/41x-3 PN/DP/41x-5H. 1-8 MB. Redundancy, hot standby.

**S7-1200 (2009)**: Compact modular with integrated IO. PROFINET.
CPU 121xC/121x/121x-3 PN. 125 KB-4 MB. TIA Portal.

**S7-1500 (2013)**: High-performance. Multi-port PROFINET.
CPU 151x/151x-3 PN/DP/151xT. 1-10 MB. Integrated safety, motion.

**ET200**: Distributed IO stations (S, M, SP, MP variants).
PROFIBUS DP and PROFINET.

## Programming Model

### Organization Blocks (OBs)
Entry points triggered by events. Priority classes 1-6.

| OB | Trigger | Description |
|----|---------|-------------|
| OB1 | Cyclic | Main program |
| OB80 | Startup | Cold/warm start |
| OB87 | Communication error | Comm fault handling |
| OB60 | Diagnostic | Cyclic OB error |
| OB35 | Cyclic interrupt | Time-controlled |
| OB40-47 | Hardware interrupt | External events |

### Code Blocks

**FC (Function)**: Reusable code without local data.
**FB (Function Block)**: Reusable code with instance data (DB).
**DB (Data Block)**: Structured data storage (standard, optimized, symbolic).

### Memory Areas

| Area | Range | Access | Persistence |
|------|-------|--------|-------------|
| V | V0.0-V65535.7 | R/W | Volatile (per scan) |
| I | I0.0-I65535.7 | R | Input image |
| Q | Q0.0-Q65535.7 | R/W | Output image |
| M | M0.0-M65535.7 | R/W | Retentive |
| DB | DB0-DB65535 | R/W | Persistent |
| T | T0-T255 | R/W | Timers |
| C | C0-C255 | R/W | Counters |

**Access Types**: Bit (X0.0), Byte (XB0), Word (XW0), DWord (XDW0), Real (IEEE 754).

### Data Types

**Elementary**: BOOL, BYTE, WORD, DWORD, INT, DINT, REAL, LREAL, CHAR, STRING, DATE, TIME, TOD.
**Complex**: TIMER, COUNTER, RTC.
**User-Defined**: UDT, Enum, Array.

### Programming Languages

| Language | S7-200 | S7-300 | S7-400 | S7-1200 | S7-1500 |
|----------|--------|--------|--------|---------|---------|
| LAD | ✓ | ✓ | ✓ | ✓ | ✓ |
| FBD | ✓ | ✓ | ✓ | ✓ | ✓ |
| STL | ✓ | ✓ | ✓ | ✓ | ✓ |
| SCL | ✗ | ✗ | ✓ | ✓ | ✓ |
| GRAPH | ✗ | ✓ | ✓ | ✓ | ✓ |
| CFC | ✗ | ✓ | ✓ | ✓ | ✓ |

## Communication

### Interfaces

**MPI**: RS-485, 187.5 Kbps-12 Mbps, multi-drop up to 32 nodes, 50m max.
**PROFIBUS DP**: RS-485, 9.6 Kbps-12 Mbps, up to 126 nodes, 100m+ with repeaters.
**PROFINET**: Industrial Ethernet, 100/1000 Mbps, line/star/ring topology.
**Industrial Ethernet**: 10/100/1000 Mbps, TCP/IP, OPC UA, MQTT.

### Protocols

**S7 Protocol (ISO-on-TCP)**: Port 102. Read/write memory, block operations.
**PUT/GET**: Transfer DBs between PLCs.
**BSend/BReceive**: Custom communication via comm blocks.
**TCON/TDISCON/TSend/TReceive/TUse**: S7-1200/1500 communication functions.

### Communication Blocks

**TSend_C, TReceive_C, TConnect, TDiscon, TUse**: For BSend/BReceive.

## Technology Functions

### Integrated (S7-1200/1500)

**PID Control**: FB41 (Compact), FB42 (3-Step), FB43 (Continuous).
Auto-tuning, manual tuning, bumpless transfer.

**Motion Control**: MC_Power, MC_Reset, MC_Stop, MC_Halt, MC_MoveAbsolute,
MC_MoveRelative, MC_MoveVelocity, MC_Home, MC_ReadAxisStatus. S7-1500T.

**Counting/Measuring**: CTUD, CTU, CTD, HSC, FM, PTO, PWM.

**Positioning**: MC_MoveToPosition, MC_MoveToReference, MC_ChangeDynamic.

### CAM
Computer Aided Manufacturing. Table of positions with automatic interpolation. S7-1500T.

## Engineering Tools

### STEP 7 V5.x
For S7-300, S7-400. Project/Station/S7 Program hierarchy. PLCSIM Classic.

### TIA Portal
Unified engineering for all S7 PLCs. Project/Portal/Device/Network/PLC/HMI/Drives views.
PLCSIM Advanced. Versions V13-V17.

### GSDML
Generic Station Description Markup Language. Device description files for PROFINET.

## Diagnostics

### Diagnostic Buffer
Stores 100-500 events. System faults, comm faults, program errors, IO faults, time errors.

### SFBs (System Function Blocks)

| SFB | Function | Description |
|-----|----------|-------------|
| SFB0 | RDREC | Read record |
| SFB1 | WRREC | Write record |
| SFB2 | ALARM_S | Alarm trigger |
| SFB33 | DPNRM_DG | PROFIBUS DP diagnostic |
| SFB35 | PNRM_DG | PROFINET diagnostic |

### SFCs (System Function Calls)
SFC1 (READ_SINFO), SFC51 (RDSYSST), SFC59 (WR_USMSG), SFC86-89 (X_SEND/X_RCV/X_GET/X_PUT).

### LED Indicators

| LED | Color | Meaning |
|-----|-------|---------|
| SF | Red | System fault |
| BF | Red | Bus fault |
| RUN | Green | RUN mode |
| STOP | Yellow | STOP mode |
| MRES | Red | Memory reset |
| BATT | Red | Battery low |
| DC5V | Green | 5V supply OK |

## Best Practices

### Programming
- Use structured programming: Break into reusable FCs/FBs
- Use meaningful names: Descriptive variable/block names
- Use comments: Document complex logic and assumptions
- Use UDTs: User-defined data types for structured data
- Avoid deep nesting: Limit to 8 levels max
- Handle errors: Use OB60/61/80/81/82
- Use watchdog: Enable watchdog timer
- Optimize cycle time: Keep OB1 < 100ms
- Use symbolic addressing: Avoid absolute when possible

### Memory
- Use DBs for data: Store process data in DBs, not V/M
- Size DBs appropriately: Leave room for growth
- Use optimized DB access: For S7-1200/1500
- Avoid large arrays: Impact on memory
- Use data types wisely: REAL uses more memory than INT/DINT

### Communication
- Use PROFINET for new installations: Future-proof
- Use PROFIBUS for distributed IO: Cost-effective
- Use MPI for PLC-to-PLC: Simple, reliable
- Configure timeouts: Appropriate for communication
- Handle comm errors: Use OB87
- Use PUT/GET for simple data transfer
- Use TSend/TReceive for custom protocols

### Security
- Protect against unauthorized access: Passwords, network segmentation
- Disable unused interfaces: Close unused ports
- Use secure passwords: Strong PLC access passwords
- Update firmware: Keep up to date
- Use OPC UA for modern integration: Better security

## Migration Paths

### S7-200 → S7-200 Smart
New hardware, Ethernet, TIA Portal. Reuse code with adjustments.

### S7-200 → S7-1200
Complete redesign, PROFINET, modular IO. Rewrite in TIA Portal.

### S7-300 → S7-1500
Similar modular design, PROFINET optional. Reuse code with adjustments.

### STEP 7 V5.x → TIA Portal
Different project structure, same concepts. Unified engineering.

## Integration

### HMI
- SIMATIC WinCC: Direct integration, OPC, alarms, trends
- WinCC Unified: Web-based, PROFINET, OPC UA
- SIMATIC HMI Panels: Basic/Comfort/Mobile Panels

### SCADA
- SIMATIC PCS 7: Process control, PROFIBUS DP, PROFINET
- Third-party: OPC, OPC UA, Modbus TCP

### MES/ERP
- SIMATIC IT: Manufacturing Execution System
- SAP: OPC UA, web services, IDoc

### Cloud
- SIMATIC IOT2020/2040/2050: PROFINET, OPC UA, MQTT, REST
- MindSphere, AWS, Azure

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Cycle time too long | Watchdog timeout | Optimize program, reduce OB1 complexity |
| Communication errors | Data loss | Check wiring, verify config, use diagnostics |
| Memory overflow | Crashes | Use DBs, monitor memory |
| Addressing errors | Incorrect access | Use symbolic addressing, validate |
| Power supply issues | Shutdown | Use UPS, monitor supply |
| Module failures | IO loss | Use redundant modules |
| Battery failure | Retentive data loss | Replace battery every 2-5 years |
| Firmware incompatibility | Errors | Use compatible versions |
| Network congestion | Slow comms | Optimize network, use appropriate RT class |
| Ground loops | Noise | Use proper grounding |
| EMI/RFI interference | Signal noise | Use shielded cables, proper grounding |

## Implementation Examples

### Python (snap7)
```python
import snap7
from snap7.util import *

client = snap7.client.Client()
client.connect('192.168.0.1', 0, 1)

data = client.db_read(1, 0, 4)
value = get_int(data, 0)

buffer = set_int(buffer, 0, 1234)
client.db_write(1, 0, buffer)

client.disconnect()
```

### Node.js (node-s7)
```javascript
const S7 = require('node-s7');
const client = new S7();

client.connect('192.168.0.1', () => {
    client.readDB(1, 0, 4, (err, data) => {
        console.log(data.readInt32LE(0));
    });
});
```

### C# (S7.NET)
```csharp
using S7.Net;

Plc client = new Plc(CpuType.S71200, "192.168.0.1", 0, 1);
client.Open();

var db1 = client.DB1;
var value = (short)db1.DBW0;
db1.DBW0 = 1234;
client.Write("DB1.DBW0", 1234);

client.Close();
```

## Vendor Ecosystem

**PLCs**: S7-200, S7-200 Smart, S7-300, S7-400, S7-1200, S7-1500, ET200
**Tools**: STEP 7 V5.x, TIA Portal, PLCSIM Classic/Advanced, PRONETA
**HMI**: WinCC, WinCC Unified, SIMATIC HMI Panels
**SCADA**: PCS 7
**Cloud**: IOT2020/2040/2050, MindSphere

## Resources

- **PI (PROFIBUS International)**: [profibus.com](https://www.profibus.com)
- **Siemens Support**: [support.industry.siemens.com](https://support.industry.siemens.com)
- **TIA Portal**: [siemens.com/tia-portal](https://new.siemens.com/global/en/products/automation/industry-software/automation-systems/tia-portal.html)
- **STEP 7**: [siemens.com/step7](https://new.siemens.com/global/en/products/automation/industry-software/automation-systems/step7.html)

## Standing Rules

- **OB1 is the heartbeat** — main cyclic OB runs continuously; watchdog faults CPU if too long.
- **Memory areas have contracts** — V is volatile (per scan), M is retentive, DB is persistent; never store process data in V if needed across scans.
- **The address is absolute until it isn't** — absolute addressing (DB1.DBW0) is fast but brittle; symbolic (MyDB.Temperature) survives changes but is slower; choose based on need.
- **A timer that isn't running is a timer to distrust** — S7 timers are pulse-catchers: must see 0→1 transition to start; signal already 1 when enabled is ignored.
- **The counter accumulates in the direction of the last edge** — CTU counts up on rising edge, CTD on falling edge, CTUD both; direction set by last edge.
- **OBs are the only entry points** — runtime never calls FC/FB directly; must be called from OB or it won't run.
- **Data blocks are the only retainers** — when PLC goes to STOP, only DBs marked retentive survive; V, M, T, C all volatile unless configured.
- **The scan cycle is atomic from the outside** — external devices see outputs freeze for OB1 duration; use process image partitioning or distributed IO for tight coupling.
- **A PLC without a watchdog is a PLC that can hang forever** — always enable watchdog; default usually sufficient, adjust slightly longer than longest scan.
- **Communication must be bounded** — always set timeouts; unanswered PUT/GET can lock CPU indefinitely.
- **Diagnostics are free** — diagnostic buffer and SFBs cost no scan time; use to detect and log errors.
- **The hardware configuration is the source of truth** — configured but not present = fault; present but not configured = ignored; must match.
- **Firmware updates require downtime** — S7 cannot update online; plan stop, download, restart.
- **PROFINET requires managed switches** — unmanaged switches break real-time; use certified switches for IRT.
- **Symbolic names are case-insensitive** — MyVariable == myvariable; can cause subtle bugs.
- **Arrays are 0-based** — unlike some PLCs, S7 arrays start at index 0; Array[1] is second element.
- **REAL has limited precision** — 32-bit float has ~7 decimal digits; use DINT with fixed-point for financial calculations.
- **The PLC clock is not battery-backed by default** — without battery or external RTC, clock resets on power cycle.
- **Retentive memory is configured, not automatic** — DBs, Ms, Ts, Cs must be explicitly marked retentive for warm start; cold start clears all.
- **A cold start erases everything** — program, data, configuration; only firmware survives; always have backup.
- **The SD card is a backup, not primary storage** — for S7-1200/1500, SD card stores backup; primary is internal memory.
- **Network changes require a restart** — changing IP or network config typically requires PLC restart.
- **Security is physical by default** — no built-in authentication; control physical access to network and PLC.
- **OPC UA is the modern integration path** — prefer OPC UA over OPC Classic for security and platform independence.
- **TIA Portal is the future** — STEP 7 V5.x supported but TIA Portal is strategic; migrate for new projects.
- **Always test with PLCSIM first** — PLCSIM catches most logic errors before hardware; reserve hardware for IO and timing.
- **Document the OB priority classes** — know which OBs interrupt which; high-priority OB can interrupt OB1.
- **Use SFBs for system functions** — System Function Blocks provide access to system services; well-tested and efficient.
