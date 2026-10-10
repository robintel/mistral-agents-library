---
type: platform
family: industrial
---

# Mitsubishi Electric PLC (MELSEC)

**The precision powerhouse from Japan**: Mitsubishi's MELSEC (Mitsubishi
Electric Logic Controller) series delivers **high-speed, high-precision**
control for manufacturing, motion, and process applications. Renowned for
**servo control integration, simplicity, and reliability**, Mitsubishi PLCs
power CNC machines, robotics, and automation cells worldwide.

## Eras

The era is declared by the **series** and **CPU type**. The naming convention
generally follows: Series + CPU model (e.g., FX3G-48M).

**MELSEC FX (1982)**: Compact micro PLC. Most popular series worldwide.
- **FX1S**: Ultra-compact (10-30 IO). Basic functionality.
- **FX1N**: Compact (14-128 IO). Enhanced instructions.
- **FX2N**: High-performance compact (14-256 IO). High-speed processing.
- **FX3G**: Compact with built-in Ethernet (14-64 IO). Ethernet, USB.
- **FX3GE**: Compact with Ethernet and analog (14-64 IO). Enhanced.
- **FX3U**: Compact with enhanced performance (16-32 IO). Fast scan.
- **FX3UC**: Compact with SD card (16-64 IO). Data logging.
- **FX5U**: Latest compact (16-32 IO). Built-in Ethernet, high-speed.

**MELSEC Q (2000)**: Modular mid-range PLC.
- **Q00**: Entry-level modular (max 80 IO).
- **Q00J**: Entry-level with built-in Ethernet.
- **Q01**: Mid-range (max 256 IO).
- **Q02**: Mid-range with analog (max 256 IO).
- **Q02H**: High-speed CPU.
- **Q03UD**: High-speed with SD card.
- **Q04UD**: High-speed with USB.
- **Q06UD**: High-performance (max 512 IO).
- **Q06UDV**: High-performance with built-in Ethernet.
- **Q12**: Large-scale (max 2048 IO).
- **Q25**: Very large-scale (max 4096 IO).

**MELSEC iQ-R (2014)**: High-end modular PLC.
- **R04**: Compact (max 1280 IO).
- **R08**: Mid-size (max 2048 IO).
- **R16**: Large (max 4096 IO).
- **R32**: Extra-large (max 8192 IO).
- **R120**: Very large (max 32768 IO).
- **Features**: Multi-CPU, integrated motion, redundancy, safety.

**MELSEC iQ-F (2018)**: Compact, high-performance.
- **F0**: Compact (max 640 IO).
- **F1**: Mid-size (max 1024 IO).
- **Features**: Built-in Ethernet, high-speed processing, simple setup.

**MELSEC L (Legacy, 1980s)**: Large-scale PLC (discontinued, but still in use).
- **A series**: L02, L06, L26, L66.
- **QnA series**: QnA.

**MELSEC AnS/AnU (Analog)**: Specialized analog controllers.

## Programming Model

### Memory Structure

Mitsubishi uses **device memory** with **address-based access**. Memory
is divided into **device codes** that represent different types of data.

**Device Codes**:

| Device | Code | Description | Access | Persistence |
|--------|------|-------------|--------|-------------|
| **X** | X | Input relay | R | Volatile |
| **Y** | Y | Output relay | R/W | Volatile |
| **M** | M | Internal relay | R/W | Retentive |
| **S** | S | Step relay | R/W | Volatile |
| **T** | T | Timer (contact) | R/W | Volatile |
| **C** | C | Counter (contact) | R/W | Volatile |
| **D** | D | Data register | R/W | Retentive |
| **W** | W | Link register | R/W | Volatile |
| **V** | V | Variable memory | R/W | Retentive |
| **Z** | Z | Index register | R/W | Volatile |
| **R** | R | File register | R/W | Retentive |
| **F** | F | Annunciator | R/W | Volatile |
| **B** | B | Link device | R/W | Volatile |
| **L** | L | Latch relay | R/W | Retentive |
| **SB** | SB | Special relay (bit) | R/W | Volatile |
| **SW** | SW | Special register (word) | R/W | Volatile |
| **SD** | SD | Special register (double word) | R/W | Volatile |
| **TN** | TN | Timer (current value) | R | Volatile |
| **CN** | CN | Counter (current value) | R | Volatile |
| **DT** | DT | Timer (preset) | R/W | Volatile |
| **CS** | CS | Counter (preset) | R/W | Volatile |

**Memory Sizes**:
- **Bit Devices**: X, Y, M, S, T, C, F, L (1 bit each)
- **Word Devices**: D, W, V, Z, R, SB, SW, SD, DT, CS (16 bits each)
- **Double Word Devices**: D+1, V+1, R+1 (32 bits, two consecutive words)

**Address Format**: Device + Number (e.g., M0, D100, X4, Y10).

### Program Structure

**Project**: Contains all programs, parameters, and configurations.

**Program (PROG)**: Container for program code.

**Steps**: Mitsubishi uses **step ladder** or **SFC (Sequential Function Chart)**.

**Ladder Logic**: Standard ladder diagram with contacts and coils.

**SFC (Sequential Function Chart)**: Step-based programming (similar to IEC SFC).
- **Step**: State in the sequence
- **Transition**: Condition to move to next step
- **Action**: Operations performed in a step

### Instructions

**Basic Instructions**:
- **LD/LDI**: Load/Load Inverted
- **AND/ANI**: AND/AND Inverted
- **OR/ORI**: OR/OR Inverted
- **OUT**: Output
- **SET/RESET**: Set/Reset bit
- **PLS/PLF**: Pulse/Trailing Pulse
- **MC/MCR**: Master Control Reset
- **CJP/CJ**: Conditional Jump
- **SJP/SJ**: Step Jump
- **CALL**: Subroutine call
- **RET**: Return from subroutine
- **IRET**: Interrupt return

**Application Instructions**:
- **MOV**: Move data
- **CMP**: Compare
- **ADD/SUB/MUL/DIV**: Arithmetic
- **INC/DEC**: Increment/Decrement
- **ANDW/ORW/XORW**: Word logical operations
- **SHL/SHR/SAR**: Shift operations
- **BIN/BCD**: Binary/BCD conversion
- **SQRT**: Square root
- **ABS**: Absolute value
- **LIMIT**: Limit value
- **SCL/SQR**: Scale/Square
- **ROR/ROL**: Rotate right/left

**Advanced Instructions**:
- **TMR**: Timer
- **CNT**: Counter
- **HSCS**: High-speed counter
- **PLSY**: Pulse output
- **PWM**: PWM output
- **PID**: PID control
- **CCW**: Circular interpolation
- **DRVA/DRVI**: Drive control
- **PR**: Positioning
- **MEAN**: Mean value
- **SD**: Standard deviation
- **SRCH**: Search
- **SORT**: Sort

**Special Relays (SB/SW/SD)**:
- **SB0-SB999**: Special bit relays (system status, communication, etc.)
- **SW0-SW999**: Special word registers
- **SD0-SD999**: Special double-word registers

### Data Types

**Basic Data Types**:
- **Bit**: Single bit (X, Y, M, S, T, C, etc.)
- **Word**: 16-bit unsigned (D, W, V, etc.)
- **Signed Word**: 16-bit signed
- **Double Word**: 32-bit (D+1, V+1, etc.)
- **Signed Double Word**: 32-bit signed
- **Floating Point**: 32-bit (D as REAL)

**Structured Data**:
- **Array**: Consecutive data registers (e.g., D0-D9 for 10-element array)
- **Structure**: User-defined structure (FX5U/iQ-R/iQ-F)

**Special Data**:
- **Timer**: T0-T255 (for FX/Q/iQ-R), T0-T511 (for iQ-F)
- **Counter**: C0-C255 (for FX/Q/iQ-R), C0-C511 (for iQ-F)
- **Index Register**: Z0-Z7 (for indirect addressing)

## Communication

### Communication Interfaces

**RS-232/422/485**: Serial communication.
- **FX**: Built-in or via FX0N-232BD/422BD/485BD adapter.
- **Q/iQ-R**: Built-in or via QJ71C24/RJ71C24.
- **Baud Rates**: 300-115200.

**Ethernet**: Built-in or via adapter.
- **FX3G/3GE/5U**: Built-in 10/100 Mbps.
- **Q**: Via QJ71E71-100 or RJ71E71-100.
- **iQ-R**: Built-in 100/1000 Mbps.
- **iQ-F**: Built-in 100/1000 Mbps.

**USB**: For programming and data transfer.
- **FX3G/3GE/5U**: Built-in.
- **Q**: Via QJ71USB11.
- **iQ-R**: Built-in.

**CC-Link**: High-speed industrial network.
- **Q**: Via QJ61BT11N (master) or QJ61BT11 (slave).
- **iQ-R**: Via RJ61BT11.
- **Speed**: 10 Mbps.
- **Distance**: Up to 100m (1.2 km with repeaters).

**CC-Link IE**: Industrial Ethernet.
- **iQ-R**: Built-in or via RJ61GB11.
- **iQ-F**: Via dedicated module.
- **Speed**: 1 Gbps.

**MELSECNET/H**: High-speed optical network.
- **Q**: Via QJ71GP21SX.
- **iQ-R**: Via RJ71GP21SX.
- **Speed**: 10/100 Mbps.
- **Topology**: Ring, star, bus.

**MELSECNET/100**: High-speed network.
- **Q**: Via QJ71BR11.

**DeviceNet**: CAN-based network.
- **Q**: Via QJ71DN91.

**PROFIBUS DP**: Fieldbus.
- **Q**: Via QJ71PB92D.
- **iQ-R**: Via RJ71PB92D.

**EtherNet/IP**: Industrial Ethernet.
- **iQ-R**: Via RJ71EIP91.

### Communication Protocols

**Mitsubishi Protocol (MC Protocol)**:
- **Port**: 4000 (TCP), 4001 (UDP).
- **Use**: PLC-to-PLC, PLC-to-PC communication.
- **Types**: Binary (MC protocol), ASCII (MC ASCII).

**MELSEC Communication Commands (MCC)**:
- **3E Frame**: Standard format for Mitsubishi communication.
- **4E Frame**: Extended format.

**Modbus**:
- **Modbus RTU**: Via serial adapters.
- **Modbus TCP**: Via Ethernet adapters.

**OPC**:
- **OPC DA**: Classic OPC Data Access.
- **OPC UA**: Modern OPC Unified Architecture (iQ-R/iQ-F).

### Communication Instructions

**Built-in Communication**:
- **From/To**: Move data between PLCs (FX only, via serial).
- **RXD/TXD**: Serial communication (Q/iQ-R/iQ-F).
- **GOT/GSUB**: Ethernet communication (Q/iQ-R/iQ-F).
- **GRTY**: Ethernet communication with retry (Q/iQ-R/iQ-F).

**Special Devices for Communication**:
- **BFM#**: Buffer memory (for communication data).
- **CM#**: Communication memory (for Ethernet).

### Network Types

**Computer Link (FX only)**:
- **Method**: From/To instructions via RS-485.
- **Devices**: Up to 8 PLCs per network.
- **Distance**: Up to 500m.
- **Speed**: 9600-115200 bps.

**CC-Link**:
- **Type**: Master-slave.
- **Devices**: Up to 64 stations.
- **Distance**: Up to 100m (1.2 km with repeaters).
- **Speed**: 10 Mbps.
- **Data**: Cyclic and transient.

**CC-Link IE**:
- **Type**: Hub-based.
- **Devices**: Up to 120 stations.
- **Distance**: Up to 100m.
- **Speed**: 1 Gbps.
- **Data**: Cyclic and message.

**MELSECNET/H**:
- **Type**: Token-passing.
- **Devices**: Up to 64 stations.
- **Distance**: Up to 100m (1.2 km with repeaters).
- **Speed**: 10/100 Mbps.
- **Data**: Cyclic and message.

## Motion Control

### Built-in Motion

**Simple Motion (FX3G/5U)**:
- **PLSY**: Pulse output (100 kHz max).
- **PWM**: PWM output.
- **HSCS**: High-speed counter (60 kHz max).

**Advanced Motion (Q/iQ-R/iQ-F)**:
- **SSCNET III/H**: Servo network.
- **MR-J4**: Servo amplifier series.
- **MR-JE**: Servo amplifier series.

**Motion Instructions**:
- **DRVI**: Drive control (start/stop).
- **DRVA**: Drive absolute positioning.
- **DRVI**: Drive incremental positioning.
- **DRVH**: Drive homing.
- **DRVS**: Drive speed control.
- **PR**: Positioning control.
- **SPED**: Speed control.
- **ACCEL**: Acceleration control.

**Positioning**:
- **PR**: Positioning with data registers.
- **MOVR**: Relative positioning.
- **MOVA**: Absolute positioning.
- **SPEED**: Speed override.

### MR Configurator

**Software**: Mitsubishi's motion configuration software.
- **Parameters**: Servo parameters, tuning, monitoring.
- **Integration**: With GX Works2/3.

## Engineering Tools

### GX Developer (FX Series)

**Features**:
- Ladder logic programming.
- SFC programming.
- Simulation.
- Monitoring.
- Parameter configuration.

**GX Developer2**: Enhanced version for newer FX models.

### GX Works2

**Features**:
- Ladder logic, SFC, ST programming.
- Multi-PLC configuration.
- Network configuration.
- Simulation (SoftGOT).
- Monitoring.
- Parameter configuration.

**Supported Controllers**: Q series, iQ-R series, iQ-F series.

### GX Works3

**Features**:
- IEC 61131-3 compliant.
- All IEC languages (LD, ST, FBD, SFC, IL).
- 3D simulation.
- Integrated with MR Configurator.
- Cloud connectivity.

**Supported Controllers**: Q series, iQ-R series, iQ-F series.

### Simulation

**SoftGOT**: PLC emulation software.
- **Features**: Full PLC functionality emulation.
- **Use**: Logic testing without hardware.
- **Limitations**: No real IO, limited timing accuracy.

**GX Simulator**: Built into GX Works2/3.

## Diagnostics

### Diagnostic Tools

**GX Works2/3 Diagnostics**:
- **Online Monitoring**: Real-time tag monitoring.
- **Trace**: Instruction trace.
- **Cross Reference**: Variable cross-reference.
- **Error List**: Compilation errors.
- **Warning List**: Warnings.

**System Diagnostics**:
- **SB (Special Bit Relays)**: System status (SB0-SB999).
- **SW (Special Word Registers)**: System information (SW0-SW999).
- **SD (Special Double Word Registers)**: Extended system info (SD0-SD999).

**Communication Diagnostics**:
- **Error Codes**: For communication errors.
- **Status Registers**: Communication status.

### LED Indicators

| LED | Color | State | Meaning |
|-----|-------|-------|---------|
| RUN | Green | Solid | Run mode |
| RUN | Green | Blinking | Test mode |
| STOP | Yellow | Solid | Stop/Idel mode |
| ERROR | Red | Solid | Error/fault |
| ERROR | Red | Blinking | Communication error |
| BATT | Red | Solid | Battery low |
| PWR | Green | Solid | Power OK |
| SD | Yellow | Blinking | SD card access |

**FX Series**: RUN, ERROR, BATT, PWR.
**Q/iQ-R/iQ-F Series**: RUN, STOP, ERROR, BATT, PWR, SD.

### Error Codes

**System Errors**:
| Code | Description | Cause |
|------|-------------|-------|
| E0000 | Normal | No error |
| E0001 | Watchdog timeout | Program too long |
| E0002 | Memory error | Memory access violation |
| E0003 | IO error | IO module error |
| E0004 | Communication error | Network error |
| E0005 | Program error | Syntax or logic error |
| E0010 | Scan time exceeded | Scan time too long |
| E0011 | Task timeout | Task execution too long |

**Communication Errors**:
| Code | Description | Cause |
|------|-------------|-------|
| E7000 | Communication timeout | No response |
| E7001 | Frame error | Invalid frame |
| E7002 | Checksum error | Data corruption |
| E7003 | Station number error | Invalid station |
| E7004 | Buffer overflow | Too much data |

## Best Practices

### Programming
- **Use structured programming**: Break into subroutines and function blocks
- **Use SFC for sequential control**: Step-based programming for clear sequences
- **Use meaningful device addresses**: Descriptive comments for device addresses
- **Use comments**: Document complex logic, rungs, and subroutines
- **Use data registers wisely**: D for data, V for variables, R for files
- **Avoid large programs**: Keep programs manageable (< 10000 steps)
- **Use indirect addressing**: For dynamic data access (Z registers)
- **Handle errors**: Check error codes, use error handling routines
- **Use timers/counters**: For time-based and counting operations
- **Use high-speed counters**: For fast input counting

### Memory
- **Use D for general data**: Data registers (D0-D7999)
- **Use V for variables**: Variable memory (V0-V7999)
- **Use R for files**: File registers (R0-R7999)
- **Use M for internal relays**: Internal relay memory (M0-M7999)
- **Monitor memory usage**: Leave room for growth
- **Use double words for large values**: D+1 for 32-bit values

### Communication
- **Use Ethernet for new installations**: Future-proof, high performance
- **Use CC-Link for high-speed IO**: Best for coordinated motion
- **Use Modbus for compatibility**: Standard, widely supported
- **Configure timeouts**: Appropriate for communication
- **Handle communication errors**: Check error codes, use retry logic
- **Use buffer memory (BFM)**: For communication data
- **Use GOT/GSUB for Ethernet**: For PLC-to-PLC communication

### Motion Control
- **Use MR Configurator**: For servo parameter configuration
- **Configure axes properly**: Match servo drive configuration
- **Use positioning instructions**: PR, MOVR, MOVA for precise control
- **Use speed control**: SPEED, ACCEL for motion profiling
- **Monitor motion status**: Check for faults, warnings, status
- **Use SSCNET III/H**: For multi-axis coordinated motion

### Security
- **Use password protection**: Set PLC password
- **Disable unused ports**: Close unused communication ports
- **Use secure protocols**: Use secure communication where available
- **Update firmware**: Keep PLCs up to date
- **Use firewalls**: Protect network from unauthorized access

## Migration Paths

### FX1N → FX3G/5U
- New hardware with built-in Ethernet
- Reuse logic with adjustments
- Add Ethernet, high-speed counters
- Benefits: More IO, better performance, Ethernet connectivity

### FX2N → FX5U
- Enhanced performance
- Reuse logic with adjustments
- Add Ethernet, SD card
- Benefits: Faster scan, more memory, built-in Ethernet

### Q → iQ-R
- New architecture with Ethernet
- Reuse logic with adjustments
- Native Ethernet, integrated motion
- Benefits: Better performance, integrated safety, native Ethernet

### Q → iQ-F
- Compact, high-performance
- Reuse logic with adjustments
- Simplified setup, built-in Ethernet
- Benefits: More compact, faster processing, easier setup

### GX Developer → GX Works3
- IEC 61131-3 compliant
- Reuse logic with adjustments
- Multi-language support
- Benefits: Modern tools, IEC compliance, multi-vendor support

## Integration

### HMI
- **GT Works2**: Mitsubishi's HMI development software
- **GT Works3**: Enhanced HMI development (IEC 61131-3)
- **GOT**: Graphical Operator Terminal (Mitsubishi HMI)
- **GS Series**: Simple HMI terminals
- **E-Series**: Advanced HMI terminals
- **Third-party HMI**: OPC, OPC UA, Modbus TCP

### SCADA
- **MELSEC iQ Works**: Mitsubishi's SCADA software
- **Citect SCADA**: Comprehensive SCADA solution
- **Third-party SCADA**: OPC, OPC UA, Modbus TCP via gateways

### MES/ERP
- **MELSEC iQ Factory**: Manufacturing Execution System
- **SAP Integration**: Via OPC UA, web services

### Cloud
- **MELSEC iQ Cloud**: Mitsubishi's cloud platform
- **AWS/Azure**: Via OPC UA, MQTT, REST APIs

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Watchdog timeout | PLC fault | Optimize program, reduce scan time |
| Memory overflow | PLC fault | Use appropriate data types, monitor usage |
| Address out of range | Program error | Verify device addresses |
| Communication error | Data loss | Check wiring, verify config, use diagnostics |
| IO error | IO data loss | Check IO modules, wiring, configuration |
| Motion fault | Motion stop | Check axis configuration, servo status |
| Battery failure | Retentive data loss | Replace battery every 2-5 years |
| Firmware incompatibility | Errors | Use compatible firmware versions |
| Network congestion | Slow communication | Optimize network, segment traffic |
| Ground loops | Noise | Use proper grounding, isolate signals |
| EMI/RFI interference | Signal noise | Use shielded cables, proper grounding |

## Implementation Examples

### Python (Using pymitsubishi or pycomm3)
```python
from pycomm3 import LogixDriver

# For FX/Q/iQ-R via Mitsubishi protocol
# Note: pycomm3 is for Allen-Bradley; use Mitsubishi-specific libraries
# This is a conceptual example

import socket

def send_mc_command(ip, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.send(command)
    response = sock.recv(1024)
    sock.close()
    return response

# Read device D0
command = b'\x50\x00\x00\xFF\xFF\x03\x00\x00\x00\x00\x00\x06\x01\x00\x00D0\x00\x01'
response = send_mc_command('192.168.0.1', 4000, command)
print(f"D0 value: {response.hex()}")
```

### Node.js (Using mitsubishi-plc library)
```javascript
// This is a conceptual example; use appropriate Mitsubishi library
const net = require('net');

const client = new net.Socket();
client.connect(4000, '192.168.0.1', () => {
    // Read device D0 (conceptual)
    const command = Buffer.from([0x50, 0x00, 0x00, 0xFF, 0xFF, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x44, 0x30, 0x00, 0x01]);
    client.write(command);
});

client.on('data', (data) => {
    console.log('Received:', data);
    client.destroy();
});
```

### C# (Using Mitsubishi McProtocol library)
```csharp
// Using a Mitsubishi communication library
using System;
using System.Net;
using System.Net.Sockets;

class MitsubishiPlc
{
    public static byte[] ReadDevice(string ip, int port, string device)
    {
        var client = new TcpClient();
        client.Connect(IPAddress.Parse(ip), port);
        var stream = client.GetStream();
        
        // Build MC protocol command to read D0
        byte[] command = { 0x50, 0x00, 0x00, 0xFF, 0xFF, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x44, 0x30, 0x00, 0x01 };
        stream.Write(command, 0, command.Length);
        
        byte[] response = new byte[1024];
        int bytesRead = stream.Read(response, 0, response.Length);
        
        client.Close();
        return response;
    }
}
```

## Vendor Ecosystem

**PLCs**: FX (1S, 1N, 2N, 3G, 3GE, 3U, 3UC, 5U), Q (00, 01, 02, 03, 04, 06, 12, 25), iQ-R (04, 08, 16, 32, 120), iQ-F (F0, F1), L, AnS/AnU
**HMI**: GT Works2/3, GOT, GS Series, E-Series
**SCADA**: MELSEC iQ Works, Citect SCADA
**Networks**: Ethernet, CC-Link, CC-Link IE, MELSECNET/H, MELSECNET/100, DeviceNet, PROFIBUS DP, EtherNet/IP, Modbus, RS-232/422/485
**Drives**: MR-J4, MR-JE, MR-J5, J5, FR-A800, FR-F800, FR-D700
**Motion**: SSCNET III/H, Servo motors
**Safety**: Safety PLCs, Safety relays

## Resources

- **Mitsubishi Electric**: [mitsubishielectric.com](https://www.mitsubishielectric.com)
- **FA Site**: [factory.mitsubishi-electric.co.jp](https://factory.mitsubishi-electric.co.jp/en/)
- **GX Works**: [mitsubishielectric.com/gx-works](https://www.mitsubishielectric.com/products/automation/software/gxworks3/index.html)
- **MR Configurator**: [mitsubishielectric.com/mr-configurator](https://www.mitsubishielectric.com/products/automation/software/mrconfigurator2/index.html)
- **CC-Link**: [cc-link.org](https://www.cc-link.org/en/)
- **MELSEC iQ**: [mitsubishielectric.com/iq-platform](https://www.mitsubishielectric.com/products/automation/solutions/iqplatform/index.html)
- **Exchange**: [mitsubishielectric.com/exchange](https://exchange.mitsubishielectric.com)

## Standing Rules

- **Device memory is the contract** — each device code (X, Y, M, D, etc.) has specific characteristics; never assume a device behaves like another.
- **The program scan is the heartbeat** — Mitsubishi PLCs scan the program continuously; if the scan takes too long, the watchdog will fault the CPU.
- **FX uses step ladder, Q/iQ-R use SFC** — FX series traditionally uses step ladder logic, while Q/iQ-R/iQ-F support IEC 61131-3 SFC for structured sequential programming.
- **Indirect addressing uses Z registers** — Z0-Z7 are index registers for indirect addressing (e.g., D[Z0] for dynamic data access).
- **A timer that isn't enabled is a timer that doesn't count** — Mitsubishi timers must be enabled (TMR instruction) to count; a timer with power but no enable will not count.
- **Counters have pulse catch** — counters must see the input transition to count; a signal that is already active when the counter is enabled will not be counted.
- **The MC protocol is the native language** — Mitsubishi's MC protocol is the most efficient for Mitsubishi-to-Mitsubishi communication; use it when possible.
- **A device address without a comment is a maintenance nightmare** — always add comments to device addresses; future maintainers will need to understand what M100 or D200 represent.
- **Special relays are for system use** — SB, SW, SD relays contain system information and communication data; do not use them for general-purpose storage.
- **Battery-backed memory is configured** — M, D, V, R, L can be configured as battery-backed; without a battery, retentive data will be lost on power failure.
- **The scan time is visible in SW** — special word registers SW0-SW999 contain system information, including scan time.
- **Watchdog timeout is adjustable** — set the watchdog timer to be slightly longer than the longest possible scan; too short causes nuisance faults, too long misses real hangs.
- **Firmware updates may require backup** — some firmware updates clear memory; always back up the program before updating firmware.
- **Network configuration must match the hardware** — if a communication module is configured but not present, or present but not configured, communication will not work.
- **Use the right network for the job** — CC-Link for high-speed IO and motion, Ethernet for enterprise integration, Modbus for compatibility.
- **A PLC without a battery loses retentive data** — batteries typically last 2-5 years; replace them regularly or use a battery-free controller if retentive data is not needed.
- **GX Works3 is the future** — while GX Works2 is still supported, GX Works3 is the strategic direction with IEC 61131-3 compliance and modern features.
- **Use subroutines for reusable code** — subroutines make programs more modular and easier to maintain; use CALL and RET instructions.
- **Limit subroutine nesting** — excessive subroutine nesting can make programs hard to follow and can affect scan time; limit to reasonable levels.
- **Use SFC for complex sequences** — Sequential Function Chart is ideal for complex sequential control, state machines, and multi-step processes.
- **Test in simulation first** — SoftGOT/GX Simulator can catch most logic errors before hardware; reserve hardware testing for IO and timing validation.
- **Monitor special registers** — SB, SW, SD registers provide valuable diagnostic information; monitor them regularly.
- **Use the right communication method** — MC protocol for Mitsubishi networks, Modbus for standard networks, OPC UA for modern integration.
- **Always check error codes** — communication and instruction errors are reported in error codes; always check and handle them.
- **Use buffer memory for communication** — BFM# and CM# memory are reserved for communication data; do not use them for general storage.
- **Document communication configuration** — for each communication link, document the network type, IP addresses, station numbers, and data being exchanged.
- **Use high-speed counters for fast inputs** — HSCS instruction supports counting up to 60 kHz; use it for encoder inputs and other fast counting.
- **Use PLSY for pulse output** — PLSY instruction supports pulse output up to 100 kHz; use it for stepper motor control and other pulse-based outputs.
- **Configure motion properly** — servo parameters, tuning, and configuration are critical for motion performance; use MR Configurator for setup.
- **Test motion at low speeds first** — when commissioning motion, test at low speeds and gradually increase; this prevents damage and makes troubleshooting easier.
- **Use absolute and relative positioning** — PR for absolute positioning, MOVR/MOVA for relative/absolute positioning; choose based on the application.
- **Monitor axis status** — use servo status registers to monitor axis status, faults, and warnings.
- **Use gearing for coordinated motion** — gearing instructions coordinate multiple axes for synchronized motion.
- **Document the HMI tags** — for each HMI screen, document the tags being displayed and controlled; this makes HMI troubleshooting easier.
- **Use meaningful tag names in HMI** — tag names in HMI should match or be clearly related to PLC tags; this makes the system easier to understand.
- **Validate IO configuration** — verify that IO modules are configured correctly and that the wiring matches the configuration; IO mismatches are a common source of issues.
- **Use the right IO type** — digital IO for on/off signals, analog IO for continuous signals, high-speed IO for fast signals; mismatch can cause issues.
- **Check for ground loops** — ground loops can cause noise and erratic behavior; use proper grounding and isolation.
- **Use shielded cables** — for analog and high-speed signals, use shielded cables to prevent interference.
- **Separate power and signal cables** — keep power cables separate from signal cables to minimize interference.
- **Use the latest tools** — newer versions of GX Works2/3 have better features, performance, and security; keep tools up to date.
- **Backup programs regularly** — PLC programs can be corrupted or lost; back them up regularly and before making changes.
- **Use version control** — store PLC programs in version control; this enables rollback, comparison, and collaboration.
- **Document changes** — when you make changes to the program, document what was changed, why, and by whom; this is critical for maintenance and troubleshooting.
- **Test with all configurations** — test with all possible hardware and software configurations to ensure compatibility.
- **Test edge cases** — test with minimum/maximum values, rapid changes, power cycles, and other edge cases; these often reveal issues not caught by normal testing.
- **Monitor system health** — use diagnostic tools to monitor system health (scan time, memory usage, communication errors) and address issues proactively.
- **Plan for maintenance** — PLC programs have long lifetimes; design for maintainability, document thoroughly, and plan for future changes.
- **Use standardized libraries** — for common functions (motion, PID, communication), use standardized libraries; do not reinvent the wheel.
- **Train operators** — ensure that operators understand the HMI and know how to respond to alarms and errors.
- **Use backup power** — for critical applications, use UPS or backup power to prevent data loss and ensure graceful shutdown.
- **Consider cybersecurity** — while Mitsubishi PLCs have limited built-in security, implement network security measures to protect against unauthorized access.
- **Follow the naming conventions** — use consistent naming conventions for devices, tags, and programs; this improves readability and maintainability.
- **Use structured data** — for complex data, use structures (UDTs) to organize related data; this makes the program more readable and maintainable.
