---
type: protocol
family: industrial
---

# PROFINET

**Industrial Ethernet** for automation: Siemens' open standard that brings
**real-time communication** to Ethernet networks. Combining standard IT
Ethernet with industrial requirements for **deterministic, synchronized**
communication. Widely used in factory automation, process industries, and
building automation.

## Eras

The era is declared by the **PROFINET version** and **real-time class**.

**PROFINET IO (2003)**: Initial release, based on PROFIBUS IO concepts
adapted for Ethernet. Supports **Real-Time (RT)** communication.

**PROFINET CBA (Component-Based Automation, 2003)**: For distributed
applications with distributed intelligence. Supports **Real-Time (RT)**.

**PROFINET IRT (Isochronous Real-Time, 2006)**: Introduction of
**Isochronous Real-Time** for highly synchronized motion control and
drive applications.

**PROFINET MRP (Media Redundancy Protocol, 2007)**: Ring topology support
for high availability. Works with RT and IRT.

**PROFINET v2.3 (2010)**: Introduction of **MRPD (Media Redundancy for
Planned Duplication)** for dual-ring topologies.

**PROFINET v2.4 (2014)**: Enhanced features including **OPC UA** integration,
**TSN (Time-Sensitive Networking)** profiles, and improved diagnostics.

**PROFINET over TSN (2018+)**: Convergence with IEEE TSN standards for
interoperable real-time Ethernet.

## Network Topologies

### Supported Topologies

| Topology | Description | Real-Time Support | Redundancy |
|----------|-------------|-------------------|------------|
| **Line** | Standard Ethernet daisy-chain | RT, IRT | No |
| **Star** | Central switch with radial connections | RT, IRT | No |
| **Ring** | Closed loop with MRP redundancy | RT, IRT | Yes (MRP) |
| **Dual Ring** | Two parallel rings with MRPD | RT, IRT | Yes (MRPD) |
| **Tree** | Hierarchical network structure | RT | No |
| **Mesh** | Fully connected (via switches) | RT | No |

### Media Redundancy Protocol (MRP)

**Purpose**: Ensure communication continuity in case of cable breaks.

**Mechanism**:
- Forms a **ring topology** with managed switches
- **MRP Manager**: One switch elected as manager
- **Ring Test Frames**: Sent periodically to detect ring integrity
- **Failover Time**: < 200ms (typical: 50-200ms)
- **Recovery Time**: < 200ms after failure is repaired

**MRP States**:
- **Open**: Ring is broken, traffic flows in both directions
- **Closed**: Ring is intact, traffic flows in one direction (blocked port)
- **Intermediate**: Transitional state during failover

### Media Redundancy for Planned Duplication (MRPD)

**Purpose**: Higher availability with dual-ring topology.

**Mechanism**:
- Two **independent rings** (Ring A and Ring B)
- **MRPD Manager**: Manages both rings
- **Load Balancing**: Traffic can be distributed across both rings
- **Failover**: If one ring fails, traffic continues on the other

## Real-Time Classes

### RT_CLASS_1 (Real-Time Class 1)

**Mechanism**: Software-based real-time using **priority tagging** (VLAN priority)

**Characteristics**:
- **Latency**: 1-10ms (depending on network load)
- **Jitter**: ±1ms (software-based)
- **Implementation**: Standard Ethernet switches with QoS support
- **Synchronization**: No hardware synchronization required
- **Use Cases**: General IO, non-critical motion control

**Frame Format**: Standard Ethernet frame with VLAN tag (priority bits set)

### RT_CLASS_2 (Real-Time Class 2)

**Mechanism**: Hardware-assisted real-time using **cut-through switching**

**Characteristics**:
- **Latency**: < 1ms (typical: 200-500µs)
- **Jitter**: ±1µs (hardware-based)
- **Implementation**: PROFINET-specific switches with cut-through forwarding
- **Synchronization**: Hardware timestamping
- **Use Cases**: Motion control, synchronized drives, high-speed IO

**Frame Format**: PROFINET Real-Time (PN-RT) frame with special EtherType

### RT_CLASS_3 (Real-Time Class 3 - IRT)

**Mechanism**: **Isochronous Real-Time** with **hardware synchronization**

**Characteristics**:
- **Latency**: < 1ms (typical: 100-300µs)
- **Jitter**: < 1µs (synchronized across entire network)
- **Implementation**: Specialized switches with hardware clock synchronization
- **Synchronization**: Distributed clock via PTP (IEEE 1588)
- **Use Cases**: Highly synchronized motion control, multi-axis coordination

**Frame Format**: PROFINET Isochronous Real-Time (PN-IRT) frame

### Comparison Table

| Feature | RT_CLASS_1 | RT_CLASS_2 | RT_CLASS_3 (IRT) |
|---------|-----------|-----------|-----------------|
| **Latency** | 1-10ms | < 1ms | < 1ms |
| **Jitter** | ±1ms | ±1µs | < 1µs |
| **Hardware Required** | QoS switches | Cut-through switches | IRT switches |
| **Synchronization** | None | Hardware timestamping | PTP (IEEE 1588) |
| **Topology** | Any | Any | Line, Ring |
| **Cost** | Low (standard switches) | Medium | High |
| **Use Cases** | General IO | Motion control | Multi-axis sync |

## Communication Models

### Provider-Consumer Model (IO)

**Most common model** for PROFINET IO.

```
┌─────────────┐       PROFINET       ┌─────────────┐
│   IO         │  ┌─────────────────┐ │   IO        │
│ Controller   │  │  Real-Time       │ │ Device      │
│ (Provider)   │◄─┤  Communication   │─►│ (Consumer)  │
└─────────────┘  └─────────────────┘ └─────────────┘
                     (Cyclic)
```

- **Provider**: Produces data (IO Controller or IO Device)
- **Consumer**: Consumes data (IO Device or IO Controller)
- **Communication**: Cyclic, real-time data exchange
- **Data**: Process data (IO data), diagnostic data

### Client-Server Model (CBA)

**Component-Based Automation** model.

```
┌─────────────┐       PROFINET       ┌─────────────┐
│   Component  │  ┌─────────────────┐ │   Component  │
│   A (Client) │  │  Acyclic          │ │   B (Server)│
└─────────────┘  │  Communication    │ └─────────────┘
                 └─────────────────┘
```

- **Client**: Requests data or invokes methods
- **Server**: Provides data or executes methods
- **Communication**: Acyclic (request-response)
- **Use Cases**: Distributed automation, engineering

### Publisher-Subscriber Model (Optional)

**For future extensions** (similar to OPC UA PubSub).

## Device Model

### PROFINET Devices

| Device Type | Role | Description |
|-------------|------|-------------|
| **IO Controller** | Master | Controls the communication, typically a PLC |
| **IO Device** | Slave | Peripheral device (IO, drives, sensors) |
| **IO Supervisor** | Monitoring | Monitors network and devices (optional) |
| **Engineering Station** | Configuration | Configures network and devices |
| **PN/PN Coupler** | Gateway | Connects PROFINET to other networks (PROFIBUS, etc.) |

### Device Access Points (DAP)

Each PROFINET device has **one or more Device Access Points**.

**DAP Types**:
- **IO-DAP**: For IO communication (cyclic data exchange)
- **CBA-DAP**: For Component-Based Automation
- **DCP-DAP**: For Discovery and Configuration Protocol
- **PN-RT-DAP**: For Real-Time communication
- **PN-IRT-DAP**: For Isochronous Real-Time communication

### GSD Files

**Generic Station Description** files describe PROFINET devices.

**GSDML format**: XML-based device description
**GSD file contents**:
- Device identification (vendor, type, version)
- Communication capabilities (RT classes supported)
- IO data structure and parameters
- Diagnostic capabilities
- Configuration parameters
- Supported topologies

**GSD file naming**: Vendor_DeviceType_Vx.xx.gsdml

## DCP (Discovery and Basic Configuration Protocol)

**Purpose**: Automatic device discovery and configuration.

### DCP Services

| Service | Description | Request/Response |
|---------|-------------|------------------|
| **Hello** | Device announces itself on network | Hello (broadcast) |
| **Get/Set** | Read/write device parameters | Request/Response |
| **Identify** | Request device identification | Request/Response |
| **Reset** | Reset device to factory defaults | Request/Response |
| **Signal** | Signal device (LED control, etc.) | Request/Response |

### DCP Hello Message

Sent periodically (every 1-10 seconds) by devices to announce presence.

**Hello Message Contents**:
- Device MAC address
- Device IP address configuration (DHCP, static, etc.)
- Device name
- Vendor ID
- Device type
- Supported services
- Device roles (IO-Controller, IO-Device, etc.)

### DCP Device Configuration

**IP Configuration Methods**:
1. **DHCP**: Automatic IP assignment
2. **Static**: Manual IP configuration
3. **DCP Set**: Temporary IP assignment via DCP
4. **LLDP**: Link Layer Discovery Protocol

**Device Naming**:
- **DCP Name**: User-assigned name (e.g., "Motor_Drive_1")
- **Asset ID**: User-assigned identifier for asset management
- **Station Name**: Configuration name

## Communication Stack

### Layer Model

```
┌─────────────────────────────────────────────────────────┐
│                 Application Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│  │   IO        │  │   DCP       │  │   Other        │   │
│  │  (Cyclic)    │  │  (Acyclic)  │  │   Services     │   │
│  └─────────────┘  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                 Real-Time Layer                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  PN-RT (Real-Time) / PN-IRT (Isochronous RT)         │  │
│  └─────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│                 Ethernet Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│  │   MAC        │  │   VLAN       │  │   IP (optional) │   │
│  │  (Required)   │  │  (QoS)       │  │   (for CBA)     │   │
│  └─────────────┘  └─────────────┘  └─────────────────┘   │
├─────────────────────────────────────────────────────────┤
│                 Physical Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐   │
│  │  100BASE-TX  │  │  1000BASE-T  │  │   Fiber        │   │
│  │  (Copper)    │  │  (Copper)    │  │   (Optional)    │   │
│  └─────────────┘  └─────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Frame Types

**Standard Ethernet Frame** (for non-real-time communication):
- MAC header (6+6 bytes)
- VLAN tag (4 bytes, optional, for QoS)
- EtherType (2 bytes)
- Payload (46-1500 bytes)
- FCS (4 bytes)

**PN-RT Frame** (Real-Time):
- MAC header (6+6 bytes)
- **PN-RT EtherType**: 0x8892
- **Frame ID**: 2 bytes (for sequencing)
- **Priority**: 2 bytes
- **Payload**: Process data
- **CRC**: 4 bytes

**PN-IRT Frame** (Isochronous Real-Time):
- **Preamble**: 8 bytes (for clock synchronization)
- **Start Frame Delimiter**: 1 byte
- **MAC header**: 6+6 bytes
- **PN-IRT EtherType**: 0x8892
- **Frame ID**: 2 bytes
- **Cycle Counter**: 2 bytes
- **Payload**: Process data
- **CRC**: 4 bytes

## IO Data Exchange

### Cyclic Data Exchange

**Basic Principle**: Data is exchanged cyclically at a **fixed send clock**.

**Send Clock**:
- **Fixed**: Constant interval (e.g., 1ms, 2ms, 4ms, 8ms, 16ms)
- **Synchronized**: All devices use same clock (via PTP)
- **Configuration**: Set in engineering tool

**Cyclic Data Types**:
1. **Process Data**: Input/output data (cyclic)
2. **Diagnostic Data**: Device status, errors (acyclic or cyclic)
3. **Parameter Data**: Configuration data (acyclic)
4. **Alarm Data**: Alarms and events (acyclic)

### IO Data Structure

**Input/Output Data**:
- **Process Data Object (PDO)**: Container for IO data
- **PDO Types**: Input PDO, Output PDO
- **PDO Mapping**: Links application objects to PDOs
- **Subslot Model**: Hierarchical addressing

**Addressing**:
```
Device → Slot → Subslot → Index → Bit/Byte
```

**Example**:
- Device: IO-Device with MAC 00:11:22:33:44:55
- Slot: 1 (IO module)
- Subslot: 1 (Digital input module)
- Index: 0 (First channel)
- Bit: 0 (First bit)
- Address: 00:11:22:33:44:55 / 1 / 1 / 0 / 0

### Real-Time Data Exchange

**RT_CLASS_1/2**:
- Uses **priority-tagged frames**
- **VLAN Priority**: 6 (highest) for real-time traffic
- **QoS**: Differentiated Services Code Point (DSCP)

**RT_CLASS_3 (IRT)**:
- Uses **synchronized frames**
- **PTP (IEEE 1588)**: Precision Time Protocol for clock synchronization
- **Cycle Time**: Fixed cycle time (e.g., 250µs, 500µs, 1ms)
- **Jitter Compensation**: Hardware-based

### Data Consistency

**Consistency Classes**:
- **Class 1**: No special consistency requirements
- **Class 2**: All IO data of one device consistent within one cycle
- **Class 3**: All IO data of all devices consistent (requires IRT)

## Configuration

### Network Configuration

**Steps**:
1. **Network Design**: Define topology, devices, IP addressing
2. **Switch Configuration**: Configure QoS, VLANs, MRP/MRPD
3. **Device Configuration**: Configure IP, device names, DCP
4. **IO Configuration**: Define IO data exchange, PDOs
5. **Real-Time Configuration**: Configure RT classes, cycle times
6. **Commissioning**: Download configuration to devices
7. **Testing**: Verify communication, performance

### Engineering Tools

| Tool | Vendor | Description |
|------|--------|-------------|
| **TIA Portal** | Siemens | Totally Integrated Automation Portal |
| **STEP 7** | Siemens | PLC programming and configuration |
| **SIMATIC NET** | Siemens | Network configuration tool |
| **PRONETA** | Siemens | PROFINET network analyzer |
| **Wireshark** | Open Source | Network protocol analyzer (with PROFINET dissector) |
| **PROFINET Tools** | PI (PROFIBUS International) | Various tools for PROFINET |

### GSDML Import

**Process**:
1. Obtain GSDML file from device vendor
2. Import into engineering tool
3. Device appears in device catalog
4. Drag and drop into network topology
5. Configure device parameters

## Performance and Timing

### Cycle Times

**Typical Cycle Times**:
- **RT_CLASS_1**: 1-10ms
- **RT_CLASS_2**: 200µs - 1ms
- **RT_CLASS_3 (IRT)**: 100-500µs

**Factors Affecting Cycle Time**:
- Network load
- Number of devices
- Amount of IO data
- RT class
- Switch performance
- Cable length

### Jitter

**Jitter Requirements**:
- **RT_CLASS_1**: ±1ms (software-based)
- **RT_CLASS_2**: ±1µs (hardware-based)
- **RT_CLASS_3 (IRT)**: < 1µs (synchronized)

**Jitter Sources**:
- Switch processing delay
- Cable length differences
- Clock drift
- Network congestion

### Synchronization

**PTP (IEEE 1588)**:
- **Precision Time Protocol** for clock synchronization
- **Master Clock**: One device elected as PTP master
- **Slave Clocks**: All other devices synchronize to master
- **Accuracy**: < 1µs (for IRT)
- **Sync Interval**: Typically 1-10 seconds

**PTP Message Types**:
- **Sync**: Sent by master with timestamp
- **Follow_Up**: Contains precise timestamp of Sync message
- **Delay_Req**: Sent by slave to measure delay
- **Delay_Resp**: Response from master with timestamp

## Diagnostic and Maintenance

### Diagnostic Data

**Diagnostic Information**:
- **Device Status**: Online/Offline, Error states
- **Communication Status**: RT class, cycle time, jitter
- **Port Status**: Link status, speed, duplex
- **Error Counters**: CRC errors, timeouts, retries
- **Alarm Information**: Active alarms, alarm history

**Diagnostic Access**:
- **Acynamic**: Via engineering tool
- **Cyclic**: As part of IO data (diagnostic PDO)
- **SNMP**: Simple Network Management Protocol (for switches)
- **Web Interface**: Many devices have web-based diagnostics

### Error Handling

**Error Classes**:
| Class | Description | Severity |
|-------|-------------|----------|
| **Fatal** | Device cannot operate | Critical |
| **Recoverable** | Device can recover with action | High |
| **Transient** | Temporary error, self-recovering | Medium |
| **Warning** | Non-critical issue | Low |

**Error Recovery**:
- **Automatic Retry**: For transient errors
- **Device Reset**: For recoverable errors
- **Power Cycle**: For fatal errors
- **Reconfiguration**: For configuration errors

### Maintenance Tasks

**Regular Maintenance**:
- Monitor network traffic and errors
- Verify redundancy status (MRP/MRPD)
- Check device firmware versions
- Update GSDML files
- Test failover procedures

**Troubleshooting Tools**:
- **PRONETA**: Siemens PROFINET analyzer
- **Wireshark**: Protocol analyzer with PROFINET dissector
- **Ping**: Basic connectivity test
- **DCP Hello Monitor**: Monitor DCP Hello messages
- **MRP Test**: Test redundancy failover

## Security

### Security Mechanisms

**Authentication**:
- **None**: No authentication (not recommended)
- **Device Authentication**: MAC-based authentication
- **User Authentication**: Username/password for engineering access

**Encryption**:
- **None**: No encryption (default)
- **TLS/SSL**: For CBA communication (optional)
- **IPsec**: For IP-based security (optional)

**Access Control**:
- **Physical Access**: Control access to network components
- **Network Segmentation**: Isolate PROFINET network from other networks
- **Firewall**: Restrict access to PROFINET ports
- **VLAN**: Separate PROFINET traffic from other traffic

**Security Best Practices**:
- Use **network segmentation** to isolate PROFINET
- Implement **VLANs** for different traffic types
- Use **firewalls** to restrict access
- Enable **DCP authentication** where available
- Regularly **update firmware** on all devices
- Monitor for **unauthorized devices**
- Implement **change management** procedures

### Security Standards

- **IEC 62443**: Industrial network and system security
- **NIST SP 800-82**: Guide to Industrial Internet of Things (IIoT) Security
- **PI Security Guideline**: PROFINET International security recommendations

## Integration with Other Systems

### PROFINET to PROFIBUS

**PN/PN Coupler**: Connects PROFINET to PROFIBUS networks
- **Function**: Transparent gateway between networks
- **Configuration**: Map PROFINET IO data to PROFIBUS IO data
- **Performance**: Adds latency (typically < 1ms)

### PROFINET to OPC UA

**OPC UA Server**: Provides OPC UA interface to PROFINET data
- **Function**: Expose PROFINET data via OPC UA
- **Integration**: Many PLCs support OPC UA server functionality
- **Use Cases**: Cloud integration, enterprise systems, MES/ERP

### PROFINET to MQTT

**MQTT Gateway**: Publishes PROFINET data to MQTT broker
- **Function**: Convert PROFINET data to MQTT messages
- **Use Cases**: Cloud applications, IoT platforms, analytics

### PROFINET to Other Fieldbuses

| Fieldbus | Gateway | Description |
|----------|---------|-------------|
| **Modbus TCP** | Protocol Gateway | Convert PROFINET to Modbus TCP |
| **EtherNet/IP** | Protocol Gateway | Convert PROFINET to EtherNet/IP |
| **DeviceNet** | PN/PN Coupler | Connect via PROFIBUS gateway |
| **CANopen** | PN/PN Coupler | Connect via PROFIBUS gateway |

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| **No DCP Hello** | Device not discovered | Check DCP configuration, verify network connectivity |
| **IP Conflict** | Duplicate IP address | Verify IP addressing, use DHCP or unique static IPs |
| **VLAN Mismatch** | No communication | Verify VLAN configuration on all switches |
| **QoS Not Configured** | Real-time performance issues | Configure QoS priority on switches |
| **MRP Not Converging** | Redundancy not working | Check MRP configuration, verify ring topology |
| **PTP Not Synchronized** | IRT jitter | Verify PTP configuration, check master clock |
| **CRC Errors** | Data corruption | Check cables, verify switch ports |
| **Timeout** | Slow or no response | Check network load, verify device status |
| **GSDML Mismatch** | Configuration errors | Verify GSDML file version matches device firmware |
| **Cycle Time Too Short** | Communication errors | Increase cycle time, reduce IO data |
| **Jitter Too High** | Poor synchronization | Check PTP configuration, verify RT class |
| **Port Flapping** | Switch port going up/down | Check cable connections, verify port configuration |
| **Switch Overload** | Packet loss | Check switch load, verify network design |
| **Firmware Incompatibility** | Communication issues | Update firmware on all devices |
| **DCP Name Conflict** | Multiple devices with same name | Assign unique DCP names |

## Best Practices

### Network Design
- **Use appropriate topology** for the application (line, star, ring)
- **Implement redundancy** (MRP/MRPD) for critical applications
- **Segment network** based on traffic types and criticality
- **Use managed switches** with PROFINET support
- **Avoid daisy-chaining** switches (use star topology for switches)
- **Limit network diameter** (max 7 switches between devices)
- **Use fiber optic** for long distances (> 100m) or EMI-sensitive areas

### Cabling
- **Use PROFINET-certified cables** (CAT 5e or better)
- **Follow cabling standards** (TIA-568 for copper, IEC 61158 for fiber)
- **Limit cable length** (100m for copper, varies for fiber)
- **Avoid cable bundling** with power cables (EMI)
- **Use proper grounding** for shields
- **Label all cables** for easy identification

### Configuration
- **Use unique device names** (DCP names)
- **Assign unique IP addresses** (static or DHCP)
- **Configure QoS** on all switches
- **Set appropriate cycle times** based on application requirements
- **Configure diagnostics** for all devices
- **Document all configurations**
- **Test failover** procedures regularly

### Commissioning
- **Verify all devices** are discovered via DCP
- **Test communication** between all devices
- **Verify redundancy** failover times
- **Test performance** (cycle times, jitter)
- **Verify diagnostics** are working
- **Test alarms** and error handling
- **Document test results**

### Maintenance
- **Monitor network** traffic and errors
- **Update firmware** regularly
- **Backup configurations** before making changes
- **Document changes** to network and devices
- **Perform regular audits** of network health
- **Train personnel** on PROFINET concepts and troubleshooting

## Debugging Tips

### Basic Checks
- **Check link lights** on all devices and switches
- **Verify IP addresses** (no conflicts)
- **Check DCP Hello** messages (are all devices announcing?)
- **Ping devices** (basic connectivity)
- **Check switch logs** for errors
- **Verify VLAN** configuration

### Advanced Debugging
- **Use PRONETA** for PROFINET-specific analysis
- **Capture traffic** with Wireshark (filter for EtherType 0x8892)
- **Check PTP synchronization** status
- **Verify MRP/MRPD** ring status
- **Test with known-good** device
- **Check cable certification**

### Wireshark Filters

**Filter for PROFINET traffic**:
```
eth.type == 0x8892  # PN-RT frames
eth.type == 0x8892 && pn_rt.fid == 0x0001  # Specific Frame ID
ip.addr == 192.168.1.100 && tcp.port == 34964  # CBA traffic (port varies)
```

**Filter for DCP traffic**:
```
udp.port == 4840  # DCP port
llc.dsap == 0xAA && llc.ssap == 0xAA  # LLC layer for DCP
```

**Filter for PTP traffic**:
```
udp.port == 319 || udp.port == 320  # PTP event and general ports
```

### Common Commands

**Windows (PowerShell)**:
```powershell
# Check network connectivity
Test-NetConnection 192.168.1.100 -Port 34964

# Get ARP table
arp -a

# Ping test
ping 192.168.1.100
```

**Linux**:
```bash
# Check network connectivity
nc -zv 192.168.1.100 34964

# Get ARP table
arp -n

# Ping test
ping 192.168.1.100

# Capture DCP traffic (using tcpdump)
tcpdump -i eth0 -nn udp port 4840
```

## Implementation Examples

### Python (Using pypnet)

```python
from pypnet import ProfinetIOController

# Create controller
controller = ProfinetIOController(
    ip_address="192.168.1.1",
    device_name="MyController"
)

# Add IO device
io_device = controller.add_io_device(
    mac_address="00:11:22:33:44:55",
    ip_address="192.168.1.100",
    device_name="IO_Device_1",
    gsdml_file="Device_V1.gsdml"
)

# Configure IO data
# Input: 8 bytes from device
# Output: 8 bytes to device
io_device.configure_io(
    input_size=8,
    output_size=8,
    send_clock=4  # 4ms cycle time
)

# Start communication
controller.start()

# Access IO data
while True:
    input_data = io_device.get_input_data()
    output_data = bytearray(8)
    # Process input_data and set output_data
    io_device.set_output_data(output_data)
    time.sleep(0.004)  # Match send clock
```

### Node.js (Using node-profinet)

```javascript
const { ProfinetIOController } = require('node-profinet');

// Create controller
const controller = new ProfinetIOController({
    ipAddress: '192.168.1.1',
    deviceName: 'MyController'
});

// Add IO device
const ioDevice = controller.addIODevice({
    macAddress: '00:11:22:33:44:55',
    ipAddress: '192.168.1.100',
    deviceName: 'IO_Device_1',
    gsdmlFile: 'Device_V1.gsdml'
});

// Configure IO data
ioDevice.configureIO({
    inputSize: 8,
    outputSize: 8,
    sendClock: 4 // 4ms cycle time
});

// Start communication
controller.start()
    .then(() => {
        // Communication started
        setInterval(() => {
            const inputData = ioDevice.getInputData();
            const outputData = new Uint8Array(8);
            // Process inputData and set outputData
            ioDevice.setOutputData(outputData);
        }, 4); // Match send clock
    })
    .catch(err => {
        console.error('Error:', err);
    });
```

### C (Using libpnet)

```c
#include <libpnet.h>
#include <stdio.h>

int main() {
    pn_controller_t *controller;
    pn_device_t *device;
    uint8_t input_data[8];
    uint8_t output_data[8] = {0};

    // Initialize controller
    controller = pn_controller_create("192.168.1.1", "MyController");

    // Add IO device
    device = pn_controller_add_io_device(
        controller,
        "00:11:22:33:44:55",
        "192.168.1.100",
        "IO_Device_1",
        "Device_V1.gsdml"
    );

    // Configure IO
    pn_device_configure_io(device, 8, 8, 4); // 8 in, 8 out, 4ms cycle

    // Start communication
    pn_controller_start(controller);

    // Main loop
    while (1) {
        pn_device_get_input_data(device, input_data);
        // Process input_data and set output_data
        pn_device_set_output_data(device, output_data);
        usleep(4000); // 4ms
    }

    pn_controller_destroy(controller);
    return 0;
}
```

## Vendor-Specific Notes

### Siemens

**Siemens PROFINET Devices**:
- **S7-1200**: Supports RT_CLASS_1, CBA, DCP
- **S7-1500**: Supports RT_CLASS_1, 2, 3 (IRT)
- **ET200SP**: Distributed IO with PROFINET
- **SINAMICS**: Drives with PROFINET
- **SIMOTICS**: Motors with PROFINET

**Siemens Tools**:
- **TIA Portal**: Primary engineering tool
- **STEP 7**: PLC programming
- **PRONETA**: Network analyzer
- **SIMATIC NET**: Network configuration

### Other Vendors

| Vendor | PROFINET Devices | Notes |
|--------|------------------|-------|
| **ABB** | AC500, AC800M | Supports PROFINET IO |
| **Beckhoff** | TwinCAT, EtherCAT | Supports PROFINET via gateways |
| **Bosch Rexroth** | IndraDrive, IndraLogic | Supports PROFINET |
| **Danfoss** | VLT, VACON | Drives with PROFINET |
| **Festo** | CPX, CMMS | Pneumatic systems with PROFINET |
| **Hirschmann** | Switches, routers | Industrial networking equipment |
| **Honeywell** | ControlEdge, HC900 | Process automation with PROFINET |
| **Mitsubishi** | iQ-R, iQ-F | Supports PROFINET via gateways |
| **Omron** | NJ, NX | Supports PROFINET |
| **Pepperl+Fuchs** | Sensors, IO | Industrial sensors with PROFINET |
| **Phoenix Contact** | Switches, IO | Industrial networking and IO |
| **Rockwell** | Allen-Bradley | Supports PROFINET via gateways |
| **Schneider** | Modicon M580, M262 | Supports PROFINET |
| **Sick** | Sensors | Industrial sensors with PROFINET |
| **Turck** | IO, sensors | Industrial IO and sensors |
| **WAGO** | IO, controllers | Industrial IO and controllers |
| **Weidmüller** | IO, switches | Industrial networking and IO |

## Certification

### PROFINET Certification

**PI (PROFIBUS International)** provides certification for:
- **Devices**: IO Devices, IO Controllers
- **Switches**: Managed switches for PROFINET
- **Cables**: PROFINET-certified cables
- **Tools**: Engineering and diagnostic tools

**Certification Levels**:
- **Class A**: Basic functionality
- **Class B**: Extended functionality (recommended)
- **Class C**: Full functionality with all features

**Certification Process**:
1. **Test at certified test lab**
2. **Submit test report** to PI
3. **Device receives certificate**
4. **Listed in PI device catalog**

### Compliance Testing

**Test Tools**:
- **PRONETA**: Siemens PROFINET analyzer
- **Wireshark**: Protocol analyzer
- **PI Test Tools**: Official PI test tools
- **Vendor Test Tools**: Vendor-specific test tools

**Test Cases**:
- DCP discovery and configuration
- IO data exchange (cyclic)
- Real-time performance (cycle time, jitter)
- Redundancy failover (MRP/MRPD)
- PTP synchronization
- Error handling
- Diagnostic functions

## Future Developments

### PROFINET over TSN

**IEEE TSN (Time-Sensitive Networking)** integration:
- **Standard**: IEEE 802.1Q (TSN)
- **Goal**: Interoperable real-time Ethernet
- **Benefits**: Vendor-independent real-time communication
- **Status**: In development, available in newer devices

**TSN Features**:
- **Time Synchronization**: IEEE 802.1AS (PTP)
- **Traffic Shaping**: IEEE 802.1Qbv (Time-Aware Shaper)
- **Preemption**: IEEE 802.1Qbu (Frame Preemption)
- **Redundancy**: IEEE 802.1CB (Frame Replication and Elimination)

### PROFINET and OPC UA

**Integration**:
- **OPC UA Server**: Many PROFINET devices now include OPC UA servers
- **Information Modeling**: Map PROFINET data to OPC UA information model
- **Security**: Use OPC UA security mechanisms for PROFINET data

### PROFINET and Cloud

**Cloud Integration**:
- **Gateways**: PROFINET to cloud gateways (MQTT, REST, OPC UA)
- **Edge Computing**: Process data at the edge before sending to cloud
- **Digital Twin**: Use PROFINET data for digital twin applications

### PROFINET Single Pair Ethernet (SPE)

**Single Pair Ethernet**:
- **Standard**: IEEE 802.3cg (10BASE-T1)
- **Goal**: PROFINET over single pair Ethernet
- **Benefits**: Reduced cabling, smaller connectors
- **Use Cases**: Small devices, sensors, actuators
- **Status**: In development

## Resources

### Standards and Specifications

- **PI PROFINET Specification**: Official PROFINET specification (PI)
- **IEC 61158**: Industrial communication networks - Fieldbus specifications
- **IEC 61784**: Industrial communication networks - Profiles
- **IEEE 802.1Q**: Time-Sensitive Networking standards
- **IEEE 1588**: Precision Time Protocol (PTP)

### Organizations

- **PI (PROFIBUS International)**: [www.profibus.com](https://www.profibus.com)
- **PROFINET International**: [www.us.profibus.com](https://www.us.profibus.com)
- **IEC**: [www.iec.ch](https://www.iec.ch)
- **IEEE**: [www.ieee.org](https://www.ieee.org)

### Documentation

- **PI PROFINET Guidelines**: Best practices and guidelines
- **Vendor Documentation**: Device-specific documentation
- **Training Courses**: PI-certified training courses

### Online Resources

- **PROFINET University**: [www.profinet-university.com](https://www.profinet-university.com)
- **PI Website**: [www.profibus.com](https://www.profibus.com)
- **PROFINET Wiki**: [wiki.profibus.com](https://wiki.profibus.com)

## Standing Rules

- **The IO Controller always initiates** — PROFINET IO is strictly
  master-slave; the IO Controller controls all cyclic communication.
- **DCP is the discovery protocol** — devices announce themselves via
  DCP Hello messages; a device not sending Hello is a device not on the
  network.
- **RT classes define the timing contract** — RT_CLASS_1 tolerates
  jitter of ±1ms, RT_CLASS_2 ±1µs, RT_CLASS_3 < 1µs; choose based on
  application requirements.
- **The Frame ID is the sequence number** — in RT communication, the
  Frame ID ensures data consistency; a missing Frame ID indicates lost
  data.
- **PTP synchronizes IRT** — Isochronous Real-Time requires Precision
  Time Protocol for sub-microsecond jitter; without PTP, IRT is not possible.
- **MRP provides redundancy** — the Media Redundancy Protocol forms a
  ring and recovers from cable breaks in < 200ms; without MRP, a cable
  break breaks the network.
- **GSDML defines the device contract** — the Generic Station Description
  Markup Language file specifies what a device can do and how it can be
  configured; a device without a GSDML file is a device that cannot be
  integrated.
- **The send clock is the heartbeat** — the fixed interval at which
  cyclic data is exchanged; all devices must adhere to it, or data
  consistency is lost.
- **VLAN priority 6 is for real-time** — in RT_CLASS_1 and RT_CLASS_2,
  real-time frames are tagged with priority 6; a switch that does not honor
  this priority breaks the timing contract.
- **A switch is a PROFINET participant** — managed switches are active
  participants in a PROFINET network, managing QoS, MRP, and PTP; using
  unmanaged switches breaks many PROFINET features.
