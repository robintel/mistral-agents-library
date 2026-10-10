---
type: platform
family: industrial
---

# Schneider Electric Modicon PLC

**The heart of Schneider's industrial automation**: Modicon PLCs offer
**scalable, flexible, and secure** solutions for discrete and process
applications. From the compact **M221** to the high-availability **M580**,
Modicon controllers integrate seamlessly with **EcoStruxure** and
support **open standards** like Modbus, Ethernet, and OPC UA.

## Eras

The era is declared by the **controller family** and **firmware version**.

**Modicon M221 (2010)**: Compact micro PLC. Integrated IO, Ethernet.
24-64 IO points. Unity Pro XL. Logic + motion + PID.

**Modicon M241 (2013)**: Enhanced micro PLC. Ethernet, serial, CANopen.
48-80 IO points. Unity Pro XL. Enhanced motion.

**Modicon M251 (2013)**: High-performance micro PLC. Ethernet, serial.
80-160 IO points. Unity Pro XL. High-speed counters.

**Modicon M262 (2016)**: Modular micro PLC. Ethernet, Modbus, CANopen.
Up to 1024 IO points. Unity Pro XL. Distributed IO.

**Modicon M340 (2005)**: Mid-range modular PLC. Ethernet, Modbus, Fipway.
Unity Pro. Hot-standby redundancy.

**Modicon M580 (2014)**: High-end Ethernet PLC. Native Ethernet backbone.
Unity Pro XL. Hot-standby, I/O redundancy.

**Modicon Quantum (1994)**: Large-scale PLC. 140CPUxxx series.
Ethernet, Fipway, Modbus. Unity Pro. High availability.

**Modicon Premium (1994)**: High-end modular PLC. TSX57/67 series.
Ethernet, Fipway, Modbus. Unity Pro. Hot-standby.

**Modicon Momentum (2000)**: Distributed IO. 170 series.
Modbus TCP/RTU, Ethernet. Unity Pro.

## Programming Model

### Project Structure

**Application**: Contains all programs, data types, and configurations.

**Program (PRG)**: Container for sections (POUs).

**POU (Program Organization Unit)**: Program sections.
- **Main**: Main program (continuous execution)
- **Routine**: Subroutine
- **Function**: Function with return value
- **Function Block**: Reusable block with memory

**Tasks**: Execution contexts with priorities.
- **MAIN**: Continuous cyclic task (default)
- **FAST**: Fast cyclic task (higher priority)
- **PERIODIC**: Periodic task (fixed interval)
- **EVENT**: Event-triggered task
- **FREE**: Free-running task (manual execution)

### Tags

**Tag Types**:
- **Variable**: Named memory location with data type
- **Alias**: Reference to another variable
- **Array**: Array of variables
- **Structure**: Structured data type
- **Function Block Instance**: Instance of a function block

**Tag Scope**:
- **Global**: Accessible throughout the application
- **Local**: Accessible within POU
- **Application**: Accessible within application

**Memory Areas**:
| Area | Description | Access | Persistence |
|------|-------------|--------|-------------|
| %M | Internal memory | R/W | Retentive |
| %I | Input image | R | Volatile |
| %Q | Output image | R/W | Volatile |
| %R | Remanent memory | R/W | Retentive (battery) |
| %S | System memory | R/W | Volatile |
| %G | Global data | R/W | Persistent |

### Data Types

**Elementary**:
- BOOL, INT (16-bit), DINT (32-bit), LINT (64-bit)
- UINT, UDINT, ULINT (unsigned)
- REAL (32-bit float), LREAL (64-bit float)
- TIME, DATE, TOD (Time of Day), DT (Date & Time)
- STRING, CHAR, WCHAR
- BYTE, WORD, DWORD, LWORD

**Derived**:
- TIMER, COUNTER
- R_TRIG (Rising edge), F_TRIG (Falling edge)
- RSEL (Rising edge selector), FSEL (Falling edge selector)

**User-Defined**:
- STRUCT (Structure)
- ENUM (Enumerated)
- ARRAY (Array)
- FUNCTION_BLOCK (Function Block Type)

### Programming Languages (IEC 61131-3)

| Language | M221 | M241 | M251 | M262 | M340 | M580 | Quantum | Premium |
|----------|------|------|------|------|------|------|--------|---------|
| LD (Ladder) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| ST (Structured Text) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| FBD (Function Block) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SFC (Sequential Function Chart) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| IL (Instruction List) | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |

**LD (Ladder Diagram)**: Graphical, rung-based. Best for logic, interlocks.
**ST (Structured Text)**: Textual, Pascal-like. Best for complex math, algorithms.
**FBD (Function Block Diagram)**: Graphical, block-based. Best for continuous control.
**SFC (Sequential Function Chart)**: Graphical, step-based. Best for sequential control.
**IL (Instruction List)**: Textual, assembly-like. Best for low-level control.

## Communication

### Networks

**Ethernet TCP/IP**: Standard Ethernet. 10/100/1000 Mbps.
- **Modbus TCP**: Port 502. Standard Modbus over TCP.
- **Ethernet/IP**: CIP protocol. Compatible with Rockwell.
- **OPC UA**: Unified Architecture. Secure, platform-independent.
- **DNP3**: SCADA protocol. Common in utilities.
- **IEC 61850**: Power utility protocol.

**Modbus**: Serial communication.
- **Modbus RTU**: RS-485. Standard Modbus RTU.
- **Modbus ASCII**: RS-232/485. ASCII-based Modbus.
- **Baud Rates**: 1200-115200.

**Fipway**: Schneider's proprietary fieldbus.
- **Fipway IO**: For IO modules.
- **Fipway P2P**: Peer-to-peer communication.
- **Speed**: 1 Mbps, 2.5 Mbps, 5 Mbps.

**CANopen**: CAN-based fieldbus.
- **Speed**: 10 Kbps - 1 Mbps.
- **Use**: Drives, sensors, distributed IO.

**Uni-Telway**: Legacy fieldbus. Token-passing.

**S-Bus**: Legacy. For older Modicon controllers.

### Protocols

**Modbus**: Standard Modbus protocol for all Ethernet/Serial networks.
- **Function Codes**: 0x01-0x17 (standard Modbus)
- **Addressing**: Modbus addressing (1-247 for slaves)
- **Data Types**: Coils, Discrete Inputs, Holding Registers, Input Registers

**Unity Protocol**: Schneider's proprietary protocol.
- **Ethernet**: Over TCP/IP
- **Serial**: Over RS-485/422
- **Features**: Tag-based access, file transfer, diagnostics

**OPC UA**: Standard OPC UA server.
- **Security**: Username/password, certificates
- **Transport**: TCP/IP (port 4840)
- **Features**: Information model, services, historical access

**Ethernet/IP (CIP)**: Compatible with Rockwell Automation.
- **CIP**: Common Industrial Protocol
- **Features**: Tag-based, explicit/implicit messaging

### Communication Instructions

**Modbus Instructions**:
- **MBUS_AQ**: Modbus Asynchronous Query
- **MBUS_RD**: Modbus Read
- **MBUS_WR**: Modbus Write
- **MBUS_DIAG**: Modbus Diagnostic

**Ethernet Instructions**:
- **ETH_RD**: Ethernet Read
- **ETH_WR**: Ethernet Write
- **ETH_DIAG**: Ethernet Diagnostic

**OPC UA Instructions**:
- **OPC_RD**: OPC UA Read
- **OPC_WR**: OPC UA Write
- **OPC_BROWSE**: OPC UA Browse

## Technology Functions

### Motion Control

**Integrated Motion (M251/M580)**:
- **Lexium Drives**: Schneider's servo drives.
- **Motion Instructions**:
  - **MC_Power**: Power on/off
  - **MC_Reset**: Reset
  - **MC_Stop**: Stop
  - **MC_Halt**: Controlled stop
  - **MC_MoveAbsolute**: Absolute positioning
  - **MC_MoveRelative**: Relative positioning
  - **MC_MoveVelocity**: Velocity control
  - **MC_Home**: Homing
  - **MC_Jog**: Jogging
  - **MC_GearIn**: Gear in
  - **MC_GearOut**: Gear out

**CANopen Motion**:
- **CiA 402**: Standard CANopen motion profile.
- **Drives**: Altivar, Lexium, other CANopen drives.

### PID Control

**PID Function Block**:
- **PID**: Standard PID controller
- **PID_ADV**: Advanced PID with auto-tuning
- **Features**: Manual/auto mode, bumpless transfer, anti-windup

### High-Speed IO

**High-Speed Counters**:
- **HSC**: High-speed counting (up to 1 MHz)
- **HSC_PLS**: Pulse counting
- **HSC_AB**: A/B quadrature counting

**Pulse Output**:
- **PTO**: Pulse train output
- **PWM**: Pulse width modulation

### Process Control

**Analog IO**:
- **Scaling**: Analog input/output scaling
- **Filtering**: Signal filtering
- **Alarm Detection**: Analog alarm detection

**Temperature Control**:
- **RTD**: Resistance Temperature Detector
- **TC**: Thermocouple
- **Linearization**: Temperature linearization

## Engineering Tools

### Unity Pro

**Unity Pro XL**: Current engineering software for Modicon PLCs.
- **Project**: Contains all applications, devices, libraries
- **Application**: PLC program (POUs, tags, data types)
- **Device**: Hardware configuration
- **Library**: Reusable components (POUs, data types, function blocks)

**Unity Pro Versions**:
- **Unity Pro**: Basic version
- **Unity Pro XL**: Full-featured version (includes SFC, IL)
- **Unity Pro S**: Simplified version for small controllers

**Features**:
- **Online Monitoring**: Monitor tags, variables, programs
- **Trend Chart**: Real-time trend charting
- **Oscilloscope**: Signal oscilloscope
- **Diagnostics**: Comprehensive diagnostics
- **Simulation**: PLC simulation (Software PLC)
- **Version Control**: Project comparison, merge

### EcoStruxure

**EcoStruxure Control Expert**: Successor to Unity Pro (based on CODESYS).
- **IEC 61131-3**: Full compliance
- **Multi-vendor**: Support for multiple PLC brands
- **Cloud Integration**: EcoStruxure Cloud
- **Digital Twin**: Virtual representation of the system

**EcoStruxure System Platform**: SCADA and visualization.

**EcoStruxure Power**: Power monitoring and management.

**EcoStruxure Machine**: Machine-level optimization.

**EcoStruxure Plant**: Plant-level optimization.

### Simulation

**Software PLC**: PLC emulation within Unity Pro.
- **Features**: Full PLC functionality simulation
- **Use**: Logic testing without hardware
- **Limitations**: No real IO, limited timing accuracy

**Factory I/O**: 3D factory simulation. Integration with Unity Pro.

## Diagnostics

### Diagnostic Tools

**Unity Pro Diagnostics**:
- **Online Diagnostics**: Real-time diagnostics while online
- **Historical Diagnostics**: Access to historical diagnostic data
- **Diagnostic View**: Dedicated diagnostic view
- **Alarm View**: Active alarms and warnings

**System Tags**:
- **%S0**: System status
- **%S1**: Last error code
- **%S2**: Last error parameter
- **%S3**: Scan time
- **%S4**: Task execution time
- **%S5**: Memory usage

**Diagnostic Instructions**:
- **DIAG**: Diagnostic instruction
- **ERR**: Error code
- **ERP**: Error parameter

### Fault Codes

**Common Fault Codes**:
| Code | Description | Severity |
|------|-------------|----------|
| 0x0001 | Watchdog timeout | Major |
| 0x0002 | Memory error | Major |
| 0x0003 | IO error | Major |
| 0x0004 | Communication error | Major |
| 0x0005 | Program error | Major |
| 0x0101 | Scan time exceeded | Minor |
| 0x0102 | Task timeout | Minor |
| 0x0103 | Tag not found | Minor |
| 0x0104 | Data type mismatch | Minor |

### LED Indicators

| LED | Color | State | Meaning |
|-----|-------|-------|---------|
| RUN | Green | Solid | Run mode |
| RUN | Green | Blinking | Test mode |
| STOP | Yellow | Solid | Stop mode |
| FAULT | Red | Solid | Major fault |
| FAULT | Red | Blinking | Minor fault/Warning |
| COMM | Green | Blinking | Communication active |
| BATT | Red | Solid | Battery low |
| PWR | Green | Solid | Power OK |

## Best Practices

### Programming
- **Use ST for complex logic**: Structured Text is best for algorithms, math, data processing
- **Use LD for simple logic**: Ladder Diagram is best for logic, interlocks
- **Use FBD for continuous control**: Function Block Diagram is best for analog, continuous control
- **Use SFC for sequential control**: Sequential Function Chart is best for state machines
- **Use meaningful names**: Descriptive tag and variable names
- **Use comments**: Document complex logic, rungs, POUs
- **Use UDTs**: User-defined types for structured data
- **Use arrays**: For similar data (motor speeds, temperatures, etc.)
- **Use function blocks**: For reusable functionality with memory
- **Handle errors**: Check error codes after communication instructions

### Memory
- **Use %M for internal memory**: Fast, retentive memory
- **Use %R for retentive data**: Battery-backed memory
- **Use %G for global data**: Shared between applications
- **Avoid %S for data**: System memory is for system use only
- **Monitor memory usage**: Leave room for growth
- **Use appropriate data types**: Match data types to values (DINT for counters, REAL for analog)

### Communication
- **Use Modbus TCP for new installations**: Standard, widely supported
- **Use Ethernet/IP for Rockwell integration**: Compatible with Allen-Bradley
- **Use OPC UA for modern integration**: Secure, platform-independent
- **Configure timeouts**: Appropriate for communication
- **Handle communication errors**: Check error codes, use retry logic
- **Use Quality/Status**: Always check tag quality and status

### Motion Control
- **Use integrated motion for M251/M580**: Best performance, integration
- **Use CANopen for distributed motion**: Flexible, multi-vendor
- **Configure axes properly**: Match drive configuration
- **Use gearing for synchronized motion**: Coordinate multiple axes
- **Monitor motion status**: Check for faults, warnings, status

### Security
- **Use password protection**: Set PLC password
- **Use OPC UA security**: Username/password, certificates
- **Disable unused ports**: Close unused communication ports
- **Use firewalls**: Protect network from unauthorized access
- **Update firmware**: Keep PLCs up to date
- **Use secure protocols**: Use TLS for sensitive data

## Migration Paths

### M221 → M241/M251
- New hardware with enhanced features
- Reuse logic with adjustments
- Add Ethernet, CANopen, high-speed IO
- Benefits: More IO, better performance, enhanced motion

### M241/M251 → M262
- Modular design with distributed IO
- Reuse logic with adjustments
- Add Modbus, CANopen, Fipway
- Benefits: More IO, distributed architecture

### M262 → M340
- Mid-range PLC with high availability
- Reuse logic with adjustments
- Add Fipway, hot-standby
- Benefits: More processing power, high availability

### M340 → M580
- Ethernet-native architecture
- Reuse logic with significant adjustments
- Native Ethernet backbone
- Benefits: Better performance, integrated safety, native Ethernet

### Quantum → M580
- Modern architecture with Ethernet
- Reuse logic with adjustments
- Native Ethernet, OPC UA
- Benefits: Modern platform, long-term support

### Unity Pro → EcoStruxure Control Expert
- New engineering environment
- CODESYS-based
- Multi-vendor support
- Benefits: Modern tools, cloud integration

## Integration

### HMI
- **Vijeo Designer**: Schneider's HMI development software
- **Vijeo Citect**: SCADA development software
- **Magelis HMI**: Schneider's HMI terminals
- **Panel PC**: Industrial PCs with HMI software

### SCADA
- **EcoStruxure System Platform**: Site-wide SCADA
- **Citect SCADA**: Comprehensive SCADA solution
- **Vijeo Citect**: SCADA with advanced visualization
- **Third-party SCADA**: OPC, OPC UA, Modbus TCP

### MES/ERP
- **EcoStruxure MES**: Manufacturing Execution System
- **Wonderware MES**: MES solution
- **SAP Integration**: Via OPC UA, web services

### Cloud
- **EcoStruxure Cloud**: Schneider's cloud platform
- **AWS/Azure**: Via OPC UA, MQTT, REST APIs
- **AVEVA Cloud**: Via OPC UA, historical data

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Watchdog timeout | Controller fault | Optimize program, reduce task complexity |
| Memory overflow | Controller fault | Use appropriate data types, monitor usage |
| Tag not found | Message error | Verify tag names, check scope |
| Data type mismatch | Message error | Use matching data types |
| Communication error | Data loss | Check wiring, verify config, use diagnostics |
| IO error | IO data loss | Check IO modules, wiring, configuration |
| Message timeout | Slow communication | Increase timeout, check network |
| Motion fault | Motion stop | Check axis configuration, drive status |
| Battery failure | Retentive data loss | Replace battery every 2-5 years |
| Firmware incompatibility | Errors | Use compatible firmware versions |
| Network congestion | Slow communication | Optimize network, segment traffic |
| Ground loops | Noise | Use proper grounding, isolate signals |
| EMI/RFI interference | Signal noise | Use shielded cables, proper grounding |

## Implementation Examples

### Python (Using pymodbus)
```python
from pymodbus.client import ModbusTcpClient

# Connect
client = ModbusTcpClient('192.168.0.1')
client.connect()

# Read holding register (Modbus address 40001 = 0)
response = client.read_holding_registers(address=0, count=1, slave=1)
if not response.isError():
    value = response.registers[0]
    print(f"Register 40001: {value}")

# Write holding register
client.write_register(address=0, value=1234, slave=1)

# Close
client.close()
```

### Node.js (Using modbus-serial)
```javascript
const ModbusRTU = require("modbus-serial");

// Modbus TCP
const client = new ModbusRTU();
client.connectTCP("192.168.0.1", { port: 502 });
client.setID(1);

// Read holding register
client.readHoldingRegisters(0, 1)
    .then(data => {
        console.log(data.data[0]);
    })
    .catch(err => {
        console.error(err);
    });

// Write holding register
client.writeRegister(0, 1234)
    .then(() => {
        console.log("Write successful");
    });

// Close
setTimeout(() => { client.close(); }, 1000);
```

### C# (Using EasyModbus)
```csharp
using EasyModbus;

ModbusClient client = new ModbusClient();
client.IPAddress = "192.168.0.1";
client.Port = 502;
client.UnitIdentifier = 1;
client.Connect();

// Read holding register
int[] registers = client.ReadHoldingRegisters(0, 1);
int value = registers[0];
Console.WriteLine($- **AWS/Azure**: Via OPC UA, MQTT, REST APIs

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Watchdog timeout | Controller fault | Optimize program, reduce task complexity |
| Memory overflow | Controller fault | Use appropriate data types, monitor usage |
| Tag not found | Message error | Verify tag names, check scope |
| Data type mismatch | Message error | Use matching data types |
| Communication error | Data loss | Check wiring, verify config, use diagnostics |
| IO error | IO data loss | Check IO modules, wiring, configuration |
| Message timeout | Slow communication | Increase timeout, check network |
| Motion fault | Motion stop | Check axis configuration, drive status |
| Battery failure | Retentive data loss | Replace battery every 2-5 years |
| Firmware incompatibility | Errors | Use compatible firmware versions |

## Implementation Examples

### Python (Using pymodbus)
```python
from pymodbus.client import ModbusTcpClient

# Connect
client = ModbusTcpClient('192.168.0.1')
client.connect()

# Read holding register (Modbus address 40001 = 0)
response = client.read_holding_registers(address=0, count=1, slave=1)
if not response.isError():
    value = response.registers[0]
    print(f"Register 40001: {value}")

# Write holding register
client.write_register(address=0, value=1234, slave=1)

# Close
client.close()
```

### Node.js (Using modbus-serial)
```javascript
const ModbusRTU = require("modbus-serial");

// Modbus TCP
const client = new ModbusRTU();
client.connectTCP("192.168.0.1", { port: 502 });
client.setID(1);

// Read holding register
client.readHoldingRegisters(0, 1)
    .then(data => {
        console.log(data.data[0]);
    })
    .catch(err => {
        console.error(err);
    });

// Write holding register
client.writeRegister(0, 1234)
    .then(() => {
        console.log("Write successful");
    });

// Close
setTimeout(() => { client.close(); }, 1000);
```

### C# (Using EasyModbus)
```csharp
using EasyModbus;

ModbusClient client = new ModbusClient();
client.IPAddress = "192.168.0.1";
client.Port = 502;
client.UnitIdentifier = 1;
client.Connect();

// Read holding register
int[] registers = client.ReadHoldingRegisters(0, 1);
int value = registers[0];
Console.WriteLine($"Register 40001: {value}");

// Write holding register
client.WriteSingleRegister(0, 1234);

// Close
client.Disconnect();
```

## Vendor Ecosystem

**PLCs**: Modicon M221, M241, M251, M262, M340, M580, Quantum, Premium, Momentum
**HMI**: Vijeo Designer, Vijeo Citect, Magelis, Panel PC
**SCADA**: EcoStruxure System Platform, Citect SCADA, Vijeo Citect
**Networks**: Ethernet TCP/IP, Modbus, Fipway, CANopen, Uni-Telway, S-Bus
**Drives**: Altivar, Lexium, TeSys
**Safety**: Preventa, Safety relays

## Resources

- **Schneider Electric**: [se.com](https://www.se.com)
- **EcoStruxure**: [ecostruxure.se.com](https://www.ecostruxure.se.com)
- **Modicon**: [modicon.se.com](https://www.se.com/ww/en/work/s/brand/modicon/)
- **Unity Pro**: [schneider-electric.com/unity-pro](https://www.schneider-electric.com/en/work/s/software/unity-pro/)
- **EcoStruxure Control Expert**: [schneider-electric.com/control-expert](https://www.schneider-electric.com/en/work/s/software/ecostruxure-control-expert/)
- **Exchange**: [exchange.se.com](https://exchange.se.com)

## Standing Rules

- **Tags are the contract** — a tag is a typed, named memory location; a program without tags is unmaintainable; always use symbolic tags.
- **The Main task is the heartbeat** — the continuous cyclic task runs continuously; if it takes too long, the watchdog will fault the CPU.
- **Tasks have priorities** — use different tasks for different priorities; a high-priority task can interrupt lower-priority tasks.
- **POUs are reusable** — Program Organization Units (Programs, Functions, Function Blocks) can be reused; design for reusability.
- **UDTs are your friends** — User-Defined Types make programs more readable and maintainable; use them for structured data.
- **A message without error checking is a message that will fail silently** — always check error codes after communication instructions.
- **Ethernet is the preferred network** — while Modbus and Fipway are still supported, Ethernet offers better performance and future-proofing.
- **OPC UA is the modern integration path** — for new installations, prefer OPC UA for better security and platform independence.
- **A tag without a description is a tag that will be misunderstood** — always add descriptions to tags; future maintainers will thank you.
- **Retentive memory is configured** — %M and %R memory can be configured as retentive; %M is volatile by default, %R is retentive by default.
- **The scan time is the sum of all task times** — monitor individual task times to identify bottlenecks.
- **Unity Pro is the single source of truth** — keep the project file in source control; it contains the entire configuration.
- **Firmware versions matter** — different firmware versions have different features and bugs; keep a compatibility matrix.
- **The IO configuration must match the hardware** — if a module is configured but not present, or present but not configured, IO will not work.
- **Watchdog timeout is a design decision** — set it slightly longer than the longest possible scan; too short causes nuisance faults, too long misses real hangs.
- **Memory is not infinite** — controller memory is limited; monitor usage and leave room for future expansion.
- **Use the right data type for the job** — BOOL for digital, INT/DINT for counting, REAL for analog, TIME for durations.
- **Always validate inputs** — validate inputs from external sources to ensure they are within expected ranges.
- **Use quality codes** — check tag quality before using consumed tags; bad quality means the value cannot be trusted.
- **Use structured error handling** — handle errors at the appropriate level and provide meaningful error messages.
- **Document motion configuration** — motion axes, groups, and CAM tables must be documented; motion faults are hard to troubleshoot without it.
- **Test in simulate first** — Software PLC can catch most logic errors before hardware; reserve hardware testing for IO and timing validation.
- **Monitor scan time** — use system tags to monitor performance; log warnings if it exceeds thresholds.
- **Use multiple tasks for different priorities** — use continuous tasks for always-running logic, periodic tasks for time-based execution.
- **EcoStruxure is the future** — while Unity Pro is still supported, EcoStruxure Control Expert is the strategic direction.
