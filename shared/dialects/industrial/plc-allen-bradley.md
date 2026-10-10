---
type: platform
family: industrial
---

# Allen-Bradley PLC (Rockwell Automation)

**The foundation of Rockwell's industrial automation**: Allen-Bradley PLCs
dominate process and discrete manufacturing in North America and beyond.
From the versatile **ControlLogix/CompactLogix** to the compact **Micro800**,
these controllers excel at **high-speed IO, motion control, and seamless
integration** with Rockwell's Studio 5000 ecosystem.

## Eras

The era is declared by the **controller family** and **firmware revision**.

**PLC-5 (1985)**: Legacy high-end PLC. DH+/DH485/RIONet comms.
16K-64K words memory. RSLogix 5. Sequential scan, no tag-based addressing.

**SLC 500 (1991)**: Small to medium applications. DH485/DeviceNet/EtherNet.
4K-64K words. RSLogix 500. First with peer-to-peer messaging.

**MicroLogix (1994)**: Micro PLCs. 1000/1100/1200/1400/1500 series.
Built-in IO, DH485/DeviceNet/EtherNet. RSLogix 500. Battery-backed RAM.

**Micro800 (2006)**: Ultra-compact. 20-80 IO points. Ethernet, USB, RS-485.
Connected Components Workbench. Tag-based, Micro800 instruction set.

**CompactLogix (2000)**: Mid-range modular. 1768/1769/5370/5380/5480.
EtherNet/IP, DeviceNet, ControlNet. Studio 5000. Tag-based addressing.

**ControlLogix (2000)**: High-performance. 1756/1789/5580/5730.
Multi-processor, redundant control. EtherNet/IP, ControlNet, DeviceNet.
Studio 5000. Motion control, process control.

**GuardLogix (2005)**: Safety-rated. 1756/5580S. SIL 3/PLe certified.
Integrated safety logic. Studio 5000.

**DriveLogix (2010)**: Drive-integrated. 1794/525/5730. Motion + logic in drives.

## Programming Model

### Project Organization

**Controller Project**: Contains controller configuration, tags, programs, routines.

**Program**: Container for routines, tags, and data types. Can have multiple programs per controller.

**Routine**: Reusable code (Main, Continuous, Periodic, Event).
- **Main Routine**: Executes continuously (like OB1 in S7)
- **Continuous Task**: Always running, configurable priority
- **Periodic Task**: Runs at fixed interval
- **Event Task**: Triggered by events (IO change, alarm, etc.)

**Tags**: Named memory locations with data types. Two types:
- **Controller Tags**: Global, accessible to all programs
- **Program Tags**: Local, accessible only within program

### Tag Addressing

**Symbolic**: Preferred. `MyTag`, `Motor1.Speed`, `Tank.Level`

**Absolute**: Legacy. `N7:0` (N=integer, 16-bit), `N10:0` (32-bit), `F8:0` (float)

**Memory Types**:
| Prefix | Data Type | Size | Description |
|--------|-----------|------|-------------|
| N | Integer | 16-bit | N file (integer data) |
| F | Float | 32-bit | F file (floating point) |
| B | Binary | 1 bit | B file (bit data) |
| T | Timer | 3 words | Timer data |
| C | Counter | 3 words | Counter data |
| R | Control | 3 words | R file (control data) |
| O | Output | 1 bit | Output image |
| I | Input | 1 bit | Input image |

### Data Types

**Elementary**: BOOL, SINT (8-bit), INT (16-bit), DINT (32-bit), LINT (64-bit),
REAL (32-bit float), LREAL (64-bit float), STRING, TIME, DATE, TOD.

**Complex**: TIMER, COUNTER, CONTROL, MESSAGE, PID.

**User-Defined**: UDT (User-Defined Type), Enum, Array, Structure.

**Special**:
- **PID**: PID controller structure
- **MOTION**: Motion group structure
- **AXIS**: Axis configuration structure
- **Cam**: CAM table structure

### Programming Languages

| Language | PLC-5 | SLC 500 | MicroLogix | CompactLogix | ControlLogix |
|----------|-------|----------|------------|--------------|--------------|
| Relay Ladder | ✓ | ✓ | ✓ | ✓ | ✓ |
| Structured Text | ✗ | ✗ | ✗ | ✓ | ✓ |
| Function Block | ✗ | ✓ | ✗ | ✓ | ✓ |
| Sequential Function Chart | ✗ | ✗ | ✗ | ✓ | ✓ |

**Relay Ladder Logic (RLL)**: Graphical, rung-based. Industry standard for logic.
**Structured Text (ST)**: High-level, Pascal-like. Best for complex math, algorithms.
**Function Block Diagram (FBD)**: Graphical, block-based. Good for analog, continuous control.
**Sequential Function Chart (SFC)**: Graphical, step-based. Best for sequential control, state machines.

## Communication

### Networks

**EtherNet/IP**: Industrial Ethernet. 100/1000 Mbps. TCP/IP + CIP protocol.
**ControlNet**: High-speed control network. 5 Mbps. Deterministic, scheduled.
**DeviceNet**: Device-level network. CAN-based. 125/250/500 Kbps.
**DH485**: Legacy serial. RS-485. 19.2 Kbps.
**DH+**: Legacy token-passing. 57.6/115.2/230.4 Kbps.

### Protocols

**CIP (Common Industrial Protocol)**: Application layer protocol for all Rockwell networks.
- **EtherNet/IP**: CIP over Ethernet/IP
- **ControlNet**: CIP over ControlNet
- **DeviceNet**: CIP over DeviceNet

**Message Instructions**:
- **MSG**: Generic messaging. Read/Write to other controllers, IO devices.
- **CIP Generic**: Read/Write CIP tags on EtherNet/IP.
- **CIP Data**: Read/Write CIP data on EtherNet/IP.
- **DeviceNet Generic**: Read/Write DeviceNet devices.
- **ControlNet Generic**: Read/Write ControlNet devices.

**Produced/Consumed Tags**: Tag-based communication between controllers.
- **Produced Tags**: Tags published by this controller
- **Consumed Tags**: Tags subscribed from other controllers
- **Connection**: Explicit or Implicit (for IO)

### Message Types

**Explicit Messaging**: Request/response. Used for non-time-critical communication.
- **CIP Explicit**: EtherNet/IP, ControlNet, DeviceNet
- **CIP Class 3**: Unconnected messages
- **CIP Class 1**: Connected messages

**Implicit Messaging**: IO scanning. Used for time-critical IO communication.
- **CIP Implicit**: EtherNet/IP IO, ControlNet IO, DeviceNet IO

## Motion Control

### Integrated Motion

**CompactLogix/ControlLogix**: Built-in motion control via Kinetix drives.

**Motion Groups**: Collection of axes that move together.

**Motion Instructions**:
- **MCR**: Motion Control Reset
- **MCC**: Motion Control Configure
- **MCD**: Motion Control Download
- **MCI**: Motion Control Initialize
- **MCM**: Motion Control Move
- **MCG**: Motion Control Gear
- **MCS**: Motion Control Stop
- **MCH**: Motion Control Halt
- **MCJ**: Motion Control Jog

**CAM Tables**: Coordinate motion via CAM profiles.

### Drive Integration

**Kinetix Drives**: Integrated with Logix controllers.
**PowerFlex Drives**: AC drives with EtherNet/IP.
**Servo Drives**: Motion control via SERCOS or EtherNet/IP.

## Engineering Tools

### RSLogix 5000

**Studio 5000**: Unified engineering environment. Successor to RSLogix 5000.
- **Logix Designer**: PLC programming
- **View Designer**: HMI development (View SE/ME)
- **FactoryTalk Linx**: Communication configuration
- **FactoryTalk Directory**: User management

**RSLogix 5000**: Original programming software for ControlLogix/CompactLogix.

**RSLogix 500**: Programming software for SLC 500/MicroLogix 1000/1100/1200/1500.

**RSLogix Micro**: Programming software for Micro800/MicroLogix 1400.

**Connected Components Workbench**: Programming for Micro800 and PanelView 800.

### FactoryTalk Suite

**FactoryTalk View**: HMI/SCADA development. SE (site edition), ME (machine edition).
**FactoryTalk Metrics**: Data collection and reporting.
**FactoryTalk Analytics**: Advanced analytics and machine learning.
**FactoryTalk AssetCentre**: Asset management and version control.
**FactoryTalk Historian**: Historical data collection.
**FactoryTalk VantagePoint**: Web-based visualization.

### Simulation

**Studio 5000 Logix Emulate**: PLC emulation software.
- Emulates ControlLogix/CompactLogix controllers
- Supports most instructions
- Can connect to FactoryTalk View for HMI testing

**RSLogix Emulate 5000**: Standalone emulation (older).

## Diagnostics

### Controller Diagnostics

**Controller Faults**: Major errors that cause controller to go to fault state.
- **Watchdog timeout**: Program execution too long
- **Memory error**: Memory access violation
- **Communication error**: Network failure
- **IO error**: IO module failure

**Controller Warnings**: Non-fatal issues that don't stop execution.

**Major/Minor Faults**: Severity levels for diagnostic events.

### Diagnostic Tools

**Controller Tags**: System tags for diagnostics.
- `ControllerFault`: Current fault code
- `ControllerFaultString`: Fault description
- `ControllerOperatingMode`: Current mode (Program, Run, Test, etc.)
- `ControllerScanTime`: Current scan time
- `ControllerScanTimeMax`: Maximum scan time

**Message Instructions Diagnostics**:
- `.ERROR`: Error code from last message
- `.DONE`: Message complete
- `.BUSY`: Message in progress

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
| 0x0102 | Message timeout | Minor |
| 0x0103 | Tag not found | Minor |
| 0x0104 | Data type mismatch | Minor |

### LED Indicators

| LED | Color | State | Meaning |
|-----|-------|-------|---------|
| OK | Green | Solid | Normal operation |
| OK | Green | Blinking | Booting/Initializing |
| OK | Green | Off | Power off/Fault |
| FAULT | Red | Solid | Major fault |
| FAULT | Red | Blinking | Minor fault/Warning |
| RUN | Green | Solid | Run mode |
| RUN | Green | Blinking | Test mode |
| REM | Yellow | Solid | Remote operation |
| IO | Green | Blinking | IO communication active |
| NET | Green | Blinking | Network communication active |

## Best Practices

### Programming
- **Use tags**: Always use symbolic tag names, never absolute addresses
- **Use UDTs**: Create user-defined types for structured data
- **Use arrays**: For similar data (motor speeds, temperatures, etc.)
- **Use meaningful names**: Descriptive tag names (Motor1_Speed vs N7:0)
- **Use comments**: Document complex logic, rungs, and routines
- **Use routines**: Break code into reusable routines
- **Handle errors**: Check .ERROR after MSG instructions
- **Use tasks**: Use continuous/periodic tasks for different priorities
- **Avoid large programs**: Keep programs manageable (< 1000 rungs)
- **Use add-on instructions**: For complex functions (PID, motion, etc.)

### Memory
- **Use appropriate data types**: DINT for counters, REAL for analog, BOOL for digital
- **Avoid REAL for counting**: Use DINT/LINT for precise counting
- **Use controller tags for global data**: Accessible to all programs
- **Use program tags for local data**: Accessible only within program
- **Monitor memory usage**: Leave room for growth

### Communication
- **Use produced/consumed tags**: For controller-to-controller communication
- **Use MSG for explicit messaging**: For non-time-critical data transfer
- **Use EtherNet/IP for new installations**: Future-proof, high performance
- **Configure timeouts**: Appropriate for message instructions
- **Handle communication errors**: Check .ERROR, use retry logic
- **Use Quality/Status**: Always check tag quality and status

### Motion Control
- **Use motion groups**: For coordinated multi-axis motion
- **Use CAM tables**: For complex motion profiles
- **Configure axes properly**: Match drive configuration
- **Use gearing**: For synchronized motion
- **Monitor motion status**: Check for faults, warnings, status

### Security
- **Use password protection**: Set controller password
- **Use FactoryTalk Security**: Centralized user management
- **Disable unused ports**: Close unused communication ports
- **Use firewalls**: Protect network from unauthorized access
- **Update firmware**: Keep controllers up to date
- **Use secure protocols**: Use TLS for sensitive data

## Migration Paths

### MicroLogix → CompactLogix
- New hardware design with modular IO
- Reuse logic with adjustments
- Use tag-based addressing
- Benefits: More IO, better performance, EtherNet/IP

### SLC 500 → ControlLogix
- Complete redesign with modular architecture
- Reuse logic with adjustments
- Use Studio 5000
- Benefits: More memory, better performance, modern features

### PLC-5 → ControlLogix
- Complete redesign with new architecture
- Reuse logic with significant adjustments
- Use Studio 5000
- Benefits: Modern platform, long-term support

### CompactLogix → ControlLogix
- Similar architecture, higher performance
- Reuse logic with minimal adjustments
- Use same Studio 5000 environment
- Benefits: More processing power, more IO

### ControlLogix Classic → ControlLogix 5580
- New hardware with same architecture
- Reuse logic with minimal adjustments
- Use Studio 5000 v28+
- Benefits: Faster processing, more memory, integrated safety

## Integration

### HMI
- **FactoryTalk View SE/ME**: Full-featured HMI. Tags, alarms, trends, recipes.
- **PanelView Plus**: Standalone HMI terminals. FactoryTalk View ME.
- **PanelView 800**: Compact HMI. Connected Components Workbench.
- **ViewPoint**: Web-based HMI. Browser access.

### SCADA
- **FactoryTalk View SE**: Site-wide SCADA. Distributed architecture.
- **FactoryTalk Metrics**: Data collection, reporting, OEE.
- **FactoryTalk Historian**: Historical data collection.
- **Third-party SCADA**: OPC, OPC UA, Modbus TCP via gateways.

### MES/ERP
- **FactoryTalk ProductionCentre**: Manufacturing operations management.
- **FactoryTalk Analytics**: Advanced analytics, machine learning.
- **SAP Integration**: Via FactoryTalk middleware or custom integration.

### Cloud
- **FactoryTalk Analytics for Devices**: Cloud-based analytics.
- **FactoryTalk Cloud Gateway**: Secure cloud connectivity.
- **AWS/Azure**: Via OPC UA, MQTT, REST APIs.

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Watchdog timeout | Controller fault | Optimize program, reduce scan time |
| Memory overflow | Controller fault | Use appropriate data types, monitor usage |
| Tag not found | Message error | Verify tag names, check scope |
| Data type mismatch | Message error | Use matching data types |
| Communication error | Data loss | Check wiring, verify config, use diagnostics |
| IO error | IO data loss | Check IO modules, wiring, configuration |
| Message timeout | Slow communication | Increase timeout, check network |
| Motion fault | Motion stop | Check axis configuration, drive status |
| CAM table error | Motion error | Verify CAM table configuration |
| Battery failure | Retentive data loss | Replace battery every 2-5 years |
| Firmware incompatibility | Errors | Use compatible firmware versions |
| Network congestion | Slow communication | Optimize network, segment traffic |
| Ground loops | Noise | Use proper grounding, isolate signals |
| EMI/RFI interference | Signal noise | Use shielded cables, proper grounding |

## Implementation Examples

### Python (Using pylogix)
```python
from pylogix import PLC

# Connect
plc = PLC()
plc.IPAddress = '192.168.0.1'
plc.ProcessorSlot = 0
plc.Connect()

# Read tag
tag_name = 'MyTag'
tag = plc.Read(tag_name)
print(f"{tag_name}: {tag.Value}")

# Write tag
plc.Write(tag_name, 1234)

# Read multiple tags
tags = plc.Read(['Tag1', 'Tag2', 'Tag3'])
for tag in tags:
    print(f"{tag.TagName}: {tag.Value}")

# Disconnect
plc.Close()
```

### Node.js (Using node-logix)
```javascript
const { PLC } = require('node-logix');

const plc = new PLC('192.168.0.1');
plc.connect((err) => {
    if (err) {
        console.error('Error:', err);
        return;
    }

    // Read tag
    plc.readTag('MyTag', (err, value) => {
        console.log('MyTag:', value);
    });

    // Write tag
    plc.writeTag('MyTag', 1234, (err) => {
        if (err) console.error('Error:', err);
    });

    // Disconnect after 5 seconds
    setTimeout(() => plc.disconnect(), 5000);
});
```

### C# (Using LibPlc)
```csharp
using LibPlc;
using LibPlc.Communication;

var driver = new CipDriver(new IpAddress("192.168.0.1"));
driver.Open();

// Read tag
var tag = driver.ReadTag("MyTag");
Console.WriteLine($"MyTag: {tag.Value}");

// Write tag
driver.WriteTag("MyTag", 1234);

// Read multiple tags
var tags = driver.ReadTags(new[] { "Tag1", "Tag2", "Tag3" });
foreach (var t in tags)
    Console.WriteLine($"{t.Name}: {t.Value}");

driver.Close();
```

## Vendor Ecosystem

**PLCs**: PLC-5, SLC 500, MicroLogix, Micro800, CompactLogix, ControlLogix, GuardLogix, DriveLogix
**HMI**: PanelView, PanelView Plus, FactoryTalk View SE/ME
**SCADA**: FactoryTalk View SE, FactoryTalk Metrics, FactoryTalk Historian
**Networks**: EtherNet/IP, ControlNet, DeviceNet, DH485, DH+
**Drives**: Kinetix, PowerFlex, Servo
**Motion**: Kinetix, MP-Series, Servo
**Safety**: GuardLogix, Guard I/O, Safety relays

## Resources

- **Rockwell Automation**: [rockwellautomation.com](https://www.rockwellautomation.com)
- **Literature Library**: [literature.rockwellautomation.com](https://literature.rockwellautomation.com)
- **Knowledgebase**: [rockwellautomation.custhelp.com](https://rockwellautomation.custhelp.com)
- **Studio 5000**: [rockwellautomation.com/studio5000](https://www.rockwellautomation.com/en-us/products/software/studio-5000.html)
- **FactoryTalk**: [rockwellautomation.com/factorytalk](https://www.rockwellautomation.com/en-us/products/software/factorytalk-analytics.html)
- **EtherNet/IP**: [odva.org](https://www.odva.org)

## Standing Rules

- **Tags are the contract** — a tag is a typed, named memory location; a program without tags is unmaintainable; always use symbolic tags.
- **The Main routine is not the only routine** — a controller can have multiple programs with multiple routines; use periodic and event routines for different execution patterns.
- **A message without error checking is a message that will fail silently** — always check `.ERROR` after MSG instructions and implement retry logic.
- **Controller scope vs program scope is a design decision** — controller tags are global and consume controller-wide memory; program tags are local and enable reuse; choose based on data lifetime and sharing needs.
- **The scan is cooperative** — in ControlLogix/CompactLogix, the OS schedules tasks; a long-running continuous task can starve others; keep tasks short and prioritize appropriately.
- **EtherNet/IP is the future** — while DH+/DeviceNet/ControlNet still work, EtherNet/IP is the strategic direction; design new systems for EtherNet/IP.
- **A tag without a description is a tag that will be misunderstood** — always add descriptions to tags; future maintainers will thank you.
- **UDTs are your friends** — User-Defined Types make programs more readable and maintainable; use them for structured data like motor parameters, PID loops, or recipe data.
- **The quality code tells you if you can trust the value** — every tag has a quality code; 0x00 (Good) means the value is valid; any other code means there is a problem; always check quality before using a consumed tag.
- **Produced and consumed tags have contracts** — when producing a tag, you promise to update it; when consuming, you depend on that promise; document these contracts.
- **A controller without a password is an open door** — always set a controller password; while not encryption, it prevents casual access.
- **Studio 5000 is the single source of truth** — keep the project file in source control; it contains the entire configuration.
- **Firmware versions matter** — different firmware versions have different features and bugs; keep a compatibility matrix and test upgrades.
- **The IO configuration must match the hardware** — if a module is configured but not present, or present but not configured, IO will not work; the configuration must match exactly.
- **Watchdog timeout is a design decision** — set it slightly longer than the longest possible scan; a too-short timeout causes nuisance faults; a too-long timeout misses real hangs.
- **Memory is not infinite** — controller memory is limited; monitor usage and leave room for future expansion and diagnostics.
- **Arrays are 0-based** — the first element is index 0; Array[1] is the second element; this is consistent with most programming languages.
- **REAL precision is limited** — 32-bit float has about 7 significant digits; for counting, use DINT/LINT; for financial calculations, use fixed-point arithmetic.
- **Controller time is not always accurate** — without an NTP server or external clock, controller time can drift; for time-critical applications, use a dedicated time source.
- **A faulted controller stops all IO** — when a controller goes to fault, all outputs freeze at their last value; this is a safety feature, but be aware that a faulted controller still drives outputs until cleared.
- **Cold start vs warm start** — cold start clears all memory and restarts from scratch; warm start preserves retentive memory; choose based on application needs.
- **The IO image is updated once per scan** — inputs are read at the start of the scan, outputs are written at the end; for fast-changing signals, use high-speed IO or interrupts.
- **CIP is the common language** — all Rockwell networks (EtherNet/IP, ControlNet, DeviceNet) use CIP at the application layer; understanding CIP helps with troubleshooting.
- **Use Add-On Instructions for complex functions** — for PID, motion, CAM, etc., use the built-in Add-On Instructions; they are well-tested and optimized.
- **Document your motion configuration** — motion groups, axes, CAM tables, and gearing must be documented; motion faults are hard to troubleshoot without documentation.
- **Test in emulate first** — Logix Emulate can catch most logic errors before hardware; reserve hardware testing for IO and timing validation.
- **Monitor scan time** — use the system tag `ControllerScanTime` to monitor performance; log warnings if it exceeds expected thresholds.
- **Use tasks for different priorities** — use continuous tasks for always-running logic, periodic tasks for time-based execution, and event tasks for triggered execution.
- **Avoid blocking calls in continuous tasks** — blocking calls (MSG, file operations) can cause watchdog timeouts; use non-blocking calls or move to separate tasks.
- **Use the right data type for the job** — BOOL for digital, INT/DINT for counting, REAL for analog, TIME for durations; mismatched types cause errors or inefficiencies.
- **Validate tag values** — always validate tag values from external sources (operators, sensors, other controllers) to ensure they are within expected ranges.
- **Use quality codes** — always check tag quality before using the value; a bad quality code means the value cannot be trusted.
- **Handle all error paths** — check return values, error codes, and quality codes; handle errors appropriately.
- **Use FactoryTalk Directory for user management** — centralize user authentication and authorization for better security.
- **Use FactoryTalk Linx for communication configuration** — simplifies network configuration and troubleshooting.
- **Plan for maintenance** — controllers have long lifetimes; design for maintainability, document thoroughly, and plan for future changes.
- **Consider energy efficiency** — some operations (analog IO, high-speed counting) consume more power; consider energy usage in battery-powered applications.
- **Use standardized libraries** — for common functions (PID, motion, communication), use standardized libraries; do not reinvent the wheel.
- **Test with real signals** — before deploying, test with real signals to verify the program handles real-world conditions correctly.
- **Monitor system health** — use diagnostic tools to monitor system health (scan time, memory usage, communication errors) and address issues proactively.
- **Use version control** — store controller projects in version control; enables rollback, comparison, and collaboration.
- **Test edge cases** — test with minimum/maximum values, rapid changes, power cycles, and other edge cases; these often reveal issues not caught by normal testing.
- **Document recovery procedures** — for each error condition, document the cause, impact, and recovery procedure; this is essential for troubleshooting.
