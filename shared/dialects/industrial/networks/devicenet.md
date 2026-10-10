---
type: protocol
family: industrial
---

# DeviceNet

**The device-level industrial network**: DeviceNet is a **simple, robust, and
cost-effective** industrial network for connecting **sensors, actuators, and
other simple devices** to higher-level controllers. Built on **Controller Area
Network (CAN)** technology, it provides **deterministic, real-time communication**
for device-level automation.

## Eras

The era is declared by the **DeviceNet specification version** and **adoption period**.

**DeviceNet v1.0 (1994)**: Original specification.
- **Technology**: Based on CAN 2.0A
- **Data Rate**: 125 kbps, 250 kbps, 500 kbps
- **Devices**: Basic I/O devices
- **Status**: Legacy, mostly replaced

**DeviceNet v2.0 (1998)**: Enhanced specification.
- **Technology**: Based on CAN 2.0B
- **Data Rate**: 125 kbps, 250 kbps, 500 kbps
- **Devices**: Enhanced device support, improved error handling
- **Features**: Group 2 Only servers, improved configuration
- **Status**: Current, widely adopted

**DeviceNet Adoption Periods**:
- **Early Adoption (1994-2000)**: Initial adoption in automotive and packaging
- **Growth (2000-2010)**: Widespread adoption across industries
- **Maturity (2010-Present)**: Mature, stable, widely supported
- **Future**: Continued use for simple device connectivity, gradually replacing with EtherNet/IP

## Architecture

### Protocol Stack

DeviceNet uses a **simplified 7-layer protocol stack** based on CAN:

**Layer 7 - Application**: DeviceNet Application Layer
- **Function**: Device-specific application functionality
- **Services**: I/O messaging, explicit messaging, device configuration
- **Objects**: Device objects, I/O points, parameters

**Layer 6 - Presentation**: DeviceNet Presentation Layer
- **Function**: Data representation and encoding
- **Encoding**: DeviceNet message format, data types

**Layer 5 - Session**: DeviceNet Session Layer
- **Function**: Session management between devices
- **Connections**: I/O connections, explicit connections

**Layer 4 - Transport**: DeviceNet Transport Layer
- **Function**: Message segmentation and reassembly
- **Fragmentation**: Split large messages into multiple CAN frames

**Layer 3 - Network**: DeviceNet Network Layer
- **Function**: Network management and addressing
- **Addressing**: MAC ID (Media Access Control Identifier)

**Layer 2 - Data Link**: CAN (Controller Area Network)
- **Function**: Frame formatting, error detection, arbitration
- **Standard**: CAN 2.0B
- **Frame Types**: Data frames, remote frames, error frames, overload frames

**Layer 1 - Physical**: CAN Physical Layer
- **Function**: Physical transmission
- **Media**: Twisted pair (DeviceNet trunk and drop lines)
- **Signaling**: Differential signaling (CAN_H, CAN_L)
- **Connectors**: Open-style (for trunk), 5-way (for drops)

### CAN Bus Basics

**CAN Frame Structure**:
- **Start of Frame (SOF)**: Dominant bit (0)
- **Arbitration ID**: 11-bit or 29-bit identifier (DeviceNet uses 11-bit)
- **Remote Transmission Request (RTR)**: Dominant (0) for data frame, recessive (1) for remote frame
- **Identifier Extension (IDE)**: Dominant (0) for 11-bit ID
- **Reserved Bit (r0)**: Reserved, must be dominant (0)
- **Data Length Code (DLC)**: 4-bit, specifies number of data bytes (0-8)
- **Data Field**: 0-8 bytes of data
- **CRC**: 15-bit Cyclic Redundancy Check
- **ACK Slot**: Acknowledgment slot (dominant = ACK, recessive = NACK)
- **ACK Delimiter**: Recessive bit (1)
- **End of Frame (EOF)**: 7 recessive bits (1111111)
- **Interframe Space**: 3 recessive bits (111)

**Arbitration**:
- **Mechanism**: Non-destructive arbitration based on arbitration ID
- **Priority**: Lower ID = higher priority
- **Behavior**: Devices with lower ID win arbitration, higher ID devices back off
- **Result**: No data loss during bus contention

**Error Detection**:
- **CRC Check**: 15-bit CRC for data integrity
- **Bit Monitoring**: Each device monitors bus level vs. transmitted level
- **Bit Stuffing**: Maximum of 5 consecutive bits of same polarity
- **Frame Check**: SOF, EOF, ACK delimiter verification
- **Error Frames**: Special frames transmitted on error detection

### DeviceNet Network Topology

**Trunk-Line/Drop-Line Topology**:
- **Trunk Line**: Main communication line (thick cable)
- **Drop Lines**: Branches from trunk to devices (thin cables)
- **Length Limits**:
  - Total network length: Up to 500m at 125 kbps
  - Trunk length: Up to 500m
  - Drop length: Up to 6m (total across all drops)
  - Number of drops: Up to 64 per trunk segment

**Physical Media**:
- **Trunk Cable**:
  - Type: Flat or round, 5-conductor (CAN_H, CAN_L, V+, V-, GND)
  - Conductor Size: 18 AWG (0.82 mm²) or larger
  - Shielding: Shielded for noise immunity
  - Color Coding: Typically purple for DeviceNet

- **Drop Cable**:
  - Type: Round, 5-conductor
  - Conductor Size: 20-18 AWG
  - Length: Up to 6m per drop
  - Connectors: 5-way open-style connectors

- **Power Distribution**:
  - Voltage: 24V DC nominal (11-25V DC range)
  - Current: Up to 8A per trunk segment
  - Power to devices: Via trunk cable (V+ and V-)
  - Power tapping: Via drop cables

### Network Components

**Trunk Cable**:
- **Purpose**: Main communication and power distribution
- **Types**:
  - Thin (18 AWG): Up to 100m at 500 kbps
  - Thick (16 AWG): Up to 500m at 125 kbps
- **Connectors**: Open-style connectors for tapping

**Power Supply**:
- **Purpose**: Provide 24V DC power to the network
- **Types**:
  - Standard: 24V DC, 5-10A
  - Redundant: Dual power supplies for high availability
- **Connection**: To trunk cable at power tap points

**Terminators**:
- **Purpose**: Prevent signal reflections at network ends
- **Type**: 120 Ohm resistor
- **Placement**: One at each end of the trunk
- **Requirement**: Mandatory for proper network operation

**Taps**:
- **Purpose**: Connect drop cables to trunk
- **Types**:
  - Open-style: For connecting drop cables
  - Closed-style: For end of trunk
- **Installation**: Screw or clamp to trunk cable

**Drop Cables**:
- **Purpose**: Connect devices to trunk
- **Types**: 5-conductor cables with connectors
- **Length**: Up to 6m per drop
- **Connectors**: 5-way connectors (male for device, female for tap)

### DeviceNet Device Types

**Device Types**:
- **Slave Devices**: Most common, respond to master requests
  - I/O modules (digital, analog)
  - Sensors (photoelectric, proximity, pressure, temperature)
  - Actuators (valves, motors, relays)
  - Drives (VFDs, servo drives)
  - HMIs (Human-Machine Interfaces)

- **Master Devices**: Initiate communication
  - PLCs (Programmable Logic Controllers)
  - PCs (Personal Computers with DeviceNet cards)
  - Gateways (Protocol converters)
  - Configuration tools

- **Scanner Devices**: Special master devices
  - Scan slave devices for I/O data
  - Typically integrated into PLCs
  - Examples: Allen-Bradley 1756-DNB, 1769-SDN

### DeviceNet Object Model

**DeviceNet Objects**:

**Identity Object (Class 0x01)**:
- **Purpose**: Device identification
- **Attributes**:
  - Vendor ID: 1 byte, assigned by ODVA
  - Device Type: 1 byte, assigned by vendor
  - Product Code: 1 byte, assigned by vendor
  - Revision: Major (1 byte), Minor (1 byte)
  - Status: 2 bytes, device status
  - Serial Number: 4 bytes, device serial number
  - Product Name: 16 bytes, ASCII product name

**Message Router Object (Class 0x02)**:
- **Purpose**: Message routing between objects
- **Attributes**:
  - Routing table for object instances
  - Message handling configuration

**DeviceNet Object (Class 0x03)**:
- **Purpose**: DeviceNet-specific functionality
- **Attributes**:
  - MAC ID: Device address on the network (0-63)
  - Baud Rate: Current baud rate (125, 250, 500 kbps)
  - Node Address: Device address (1-63, 0 = not assigned)

**Assembly Object (Class 0x04)**:
- **Purpose**: Data assembly and disassembly
- **Attributes**:
  - Instance list for data exchange
  - Configuration of data points

**Connection Object (Class 0x05)**:
- **Purpose**: Connection management
- **Attributes**:
  - Connection parameters (RPI, connection size, etc.)
  - Connection state

**I/O Point Objects**:
- **Discrete Input Point (Class 0x1B)**: Digital input
- **Discrete Output Point (Class 0x1C)**: Digital output
- **Analog Input Point (Class 0x1D)**: Analog input
- **Analog Output Point (Class 0x1E)**: Analog output

**Parameter Object (Class 0x0F)**:
- **Purpose**: Parameter storage and access
- **Attributes**: Parameter values, descriptions, access rights

### Device Profiles

**Standard Device Profiles**:

**Simple I/O Device Profile**:
- **Purpose**: Basic digital and analog I/O
- **Objects**: Identity, DeviceNet, Assembly, I/O Points
- **Data Types**: Bool, Int, Float
- **Use Case**: Simple sensors, actuators, I/O modules

**Complex I/O Device Profile**:
- **Purpose**: Advanced I/O with configuration
- **Objects**: Identity, DeviceNet, Assembly, I/O Points, Parameters
- **Features**: Configurable I/O, parameter storage
- **Use Case**: Configurable sensors, smart I/O modules

**Motion Control Device Profile**:
- **Purpose**: Motion control devices
- **Objects**: Identity, DeviceNet, Assembly, Motion-related objects
- **Features**: Position control, velocity control, status monitoring
- **Use Case**: Drives, motors, motion controllers

**Safety Device Profile**:
- **Purpose**: Safety-rated devices
- **Objects**: Identity, DeviceNet, Safety-related objects
- **Safety Level**: SIL 2, Category 3
- **Use Case**: Safety sensors, safety relays, emergency stop devices
- **Requirement**: Dual-channel communication, built-in redundancy

**Vendor-Specific Profiles**:
- **Allen-Bradley**: 1794 Flex I/O, 1734 Point I/O, 1732 ArmorBlock I/O
- **Omron**: E3Z photoelectric sensors, E2B proximity sensors, G9SP safety sensors
- **Schneider**: XBT photoelectric sensors, XS proximity sensors
- **Siemens**: ET200S I/O, SIMATIC sensors
- **Balluff**: BES photoelectric sensors, BNS proximity sensors
- **ifm**: Various sensors and I/O modules

## Configuration

### Device Configuration

**MAC ID (Media Access Control Identifier)**:
- **Purpose**: Unique device address on the network
- **Range**: 0-63 (64 possible devices per network)
- **Assignment**:
  - 0: Not assigned (default)
  - 1-63: Assigned addresses
- **Configuration**: Via DIP switches, rotary switches, or software
- **Rules**: Each device must have a unique MAC ID

**Baud Rate**:
- **Options**: 125 kbps, 250 kbps, 500 kbps
- **Selection**: All devices on a network must use the same baud rate
- **Trade-offs**:
  - 125 kbps: Longest distance (500m), most devices
  - 250 kbps: Medium distance (250m), good balance
  - 500 kbps: Shortest distance (100m), fastest communication
- **Auto-Baud**: Some devices support automatic baud rate detection

**EDS (Electronic Data Sheet) File**:
- **Purpose**: Device description file
- **Format**: XML-based (IEC 61804-2 EDDL)
- **Content**:
  - Device identity (Vendor ID, Device Type, Product Code, Revision)
  - Object definitions and attributes
  - Parameter descriptions and defaults
  - Communication settings
  - I/O configuration
- **Use**: Automatic device configuration, parameter validation, HMI integration
- **Tools**: EDS file editors, configuration tools

**Configuration Parameters**:
- **Device Parameters**: Device-specific settings (filter time, scaling, etc.)
- **I/O Configuration**: Input/output configuration, data types, scaling
- **Network Parameters**: MAC ID, baud rate, network settings
- **Security Parameters**: Access control, password protection

### Network Configuration

**Network Design**:
- **Segmentation**: Divide network into segments if needed
- **Bridging**: Use bridges to connect multiple DeviceNet networks
- **Repeaters**: Use repeaters to extend network length
- **Redundancy**: Implement redundant power supplies for high availability

**Power Configuration**:
- **Power Supply Sizing**:
  - Calculate total current draw of all devices
  - Add 20-25% margin for safety
  - Consider inrush current during startup
- **Power Distribution**:
  - Use trunk cable for power distribution
  - Tap power at multiple points for better distribution
  - Consider voltage drop over long distances

**Grounding**:
- **Purpose**: Reduce noise, improve communication reliability
- **Grounding Points**: Ground at power supply and at intervals along trunk
- **Ground Wire**: Use separate ground wire (not part of trunk cable)
- **Grounding Method**: Single-point grounding recommended

## Features

### Real-Time Performance

**Deterministic Communication**:
- **Cyclic I/O**: Polling-based I/O data exchange
- **Polling Rate**: Configurable (typically 1-100ms)
- **Jitter**: Minimal jitter (CAN-based arbitration)
- **Latency**: Low latency (< 10ms typical)

**Network Capacity**:
- **Maximum Devices**: 64 per network segment
- **Maximum Data**: Up to 8 bytes per message
- **Maximum Network Length**: 500m at 125 kbps
- **Maximum Drops**: 64 per trunk segment

**Error Handling**:
- **CAN Error Detection**: Automatic error detection and handling
- **Error Frames**: Special frames transmitted on error detection
- **Error Recovery**: Automatic recovery from bus errors
- **Error Counters**: Track error counts for bus health monitoring

### Device Discovery and Integration

**Device Discovery**:
- **Network Scan**: Scan network to discover connected devices
- **EDS-based Discovery**: Automatic discovery using EDS files
- **Manual Discovery**: Manual device configuration
- **Tools**: Configuration tools, network scanners

**Integration Methods**:
- **PLC Integration**: Direct integration with PLCs via scanner modules
- **HMI Integration**: Integration with HMI/SCADA systems
- **Gateway Integration**: Integration via protocol gateways
- **OPC Integration**: OPC server for standard interface
- **Custom Integration**: Custom development via APIs

**Configuration Tools**:
- **Vendor Tools**:
  - Allen-Bradley: RSNetWorx for DeviceNet
  - Omron: CX-Net, DeviceNet Configurator
  - Schneider: Unity Pro, DeviceNet Configurator
  - Siemens: STEP 7, TIA Portal
- **Generic Tools**: DeviceNet configuration software, EDS file editors

### Power Management

**Power Distribution**:
- **Trunk Power**: Power distributed via trunk cable (V+ and V-)
- **Drop Power**: Power tapped from trunk via drop cables
- **Power Taps**: Connect power supplies to trunk at multiple points
- **Power Isolation**: Isolate power for different segments

**Power Monitoring**:
- **Voltage Monitoring**: Monitor network voltage
- **Current Monitoring**: Monitor current draw of devices
- **Power Quality**: Monitor power quality and stability
- **Fault Detection**: Detect power-related faults

**Power Protection**:
- **Fuses**: Use fuses to protect against short circuits
- **Circuit Breakers**: Use circuit breakers for overload protection
- **Surge Protection**: Use surge protectors for transient protection
- **Redundancy**: Use redundant power supplies for high availability

## Best Practices

### Network Design
- **Plan Network Layout**: Plan network topology before installation
- **Calculate Lengths**: Ensure total network length is within limits
- **Count Devices**: Ensure number of devices is within limits
- **Select Baud Rate**: Choose appropriate baud rate based on network length
- **Plan Power Distribution**: Ensure sufficient power for all devices
- **Segment Networks**: Use bridges or repeaters for large networks
- **Document Network**: Document network layout, device addresses, configurations

### Installation
- **Use Quality Cable**: Use high-quality DeviceNet cable
- **Proper Termination**: Always install terminators at both ends of trunk
- **Secure Connections**: Ensure all connections are secure and tight
- **Avoid Sharp Bends**: Avoid sharp bends in cable (minimum bend radius)
- **Separate from Power**: Keep DeviceNet cable separate from high-power cables
- **Ground Properly**: Ground network at power supply and at intervals
- **Test Before Power**: Test cable continuity before applying power
- **Label Devices**: Label all devices with MAC ID and description

### Device Configuration
- **Unique MAC IDs**: Ensure all devices have unique MAC IDs
- **Match Baud Rate**: Ensure all devices use the same baud rate
- **Use EDS Files**: Use EDS files for device configuration when available
- **Configure Parameters**: Configure device parameters as needed
- **Test Communication**: Test communication with each device
- **Document Configuration**: Document device configurations

### Maintenance and Troubleshooting
- **Regular Inspection**: Regularly inspect network for physical issues
- **Monitor Errors**: Monitor CAN error counters and bus health
- **Test Connectivity**: Regularly test connectivity with all devices
- **Check Power**: Monitor power supply and distribution
- **Update Firmware**: Keep device firmware up to date
- **Maintain Spares**: Maintain inventory of spare devices and components
- **Document Changes**: Document all network changes

### Security
- **Physical Security**: Protect network from physical access
- **MAC ID Protection**: Protect against MAC ID spoofing
- **Access Control**: Implement access control for configuration tools
- **Network Isolation**: Isolate DeviceNet network from other networks
- **Monitor Traffic**: Monitor network traffic for anomalies
- **Audit Access**: Audit access to configuration tools

### Performance Optimization
- **Optimize Polling Rate**: Balance polling rate with network capacity
- **Use Efficient Data**: Minimize data size, use appropriate data types
- **Group Data**: Group related data points for efficient communication
- **Monitor Load**: Monitor network load and device response times
- **Load Testing**: Test network performance under expected loads

## Migration Paths

### DeviceNet to EtherNet/IP
- **Benefits**: Higher speed, longer distances, standard Ethernet infrastructure
- **Challenges**: Wiring changes, protocol differences, device compatibility
- **Approach**: Use protocol gateways/converters for gradual migration
- **Tools**: Protocol converters, gateway devices, configuration tools
- **Considerations**: EtherNet/IP uses TCP/IP and CIP, DeviceNet uses CAN and CIP

### DeviceNet to PROFINET
- **Benefits**: Higher speed, standard Ethernet, PROFINET-specific features
- **Challenges**: Protocol differences, device compatibility
- **Approach**: Use PROFINET/DeviceNet gateways
- **Tools**: Protocol gateways, configuration tools
- **Considerations**: PROFINET uses different object model and communication methods

### DeviceNet to IO-Link
- **Benefits**: Simplified wiring, point-to-point topology
- **Challenges**: Different topology, limited to sensor/actuator level
- **Approach**: Replace DeviceNet with IO-Link for simple devices
- **Tools**: IO-Link masters, configuration tools
- **Considerations**: IO-Link is point-to-point, DeviceNet is multi-drop

### Single Network to Segmented Network
- **Benefits**: Improved performance, reduced network load
- **Challenges**: Additional hardware, configuration complexity
- **Approach**: Use bridges or repeaters to segment network
- **Tools**: DeviceNet bridges, repeaters, configuration tools
- **Testing**: Thoroughly test communication across segments

## Integration

### PLC Integration

**Allen-Bradley**:
- **Scanner Modules**:
  - 1756-DNB: ControlLogix DeviceNet scanner
  - 1769-SDN: CompactLogix DeviceNet scanner
  - 1794-ADN: Flex I/O DeviceNet adapter
- **Configuration**: RSLogix 5000, Studio 5000
- **Features**: Full DeviceNet support, optimized performance
- **Integration**: Tight integration with Rockwell Automation products

**Omron**:
- **Scanner Modules**:
  - NJ Series: Built-in DeviceNet master
  - Sysmac: DeviceNet master support
- **Configuration**: Sysmac Studio, CX-Net
- **Features**: Full DeviceNet support, configuration tools
- **Integration**: Tight integration with Omron products

**Schneider Electric**:
- **Scanner Modules**:
  - TSXDMZ: DeviceNet master for Modicon
  - BMXDMM: DeviceNet master for Quantum/Premium
- **Configuration**: Unity Pro, Concept
- **Features**: Full DeviceNet support, configuration tools
- **Integration**: Tight integration with Schneider products

**Siemens**:
- **Scanner Modules**:
  - CP 343-5: DeviceNet module for S7-300
  - CP 1518-4: DeviceNet module for S7-1500
- **Configuration**: STEP 7, TIA Portal
- **Features**: Full DeviceNet support, configuration tools
- **Integration**: Tight integration with SIMATIC products

### SCADA Integration

**Ignition**:
- **Connectivity**: Native DeviceNet driver or via OPC
- **Configuration**: Drag-and-drop configuration
- **Features**: Tag browsing, alarm integration, trend display
- **Performance**: Optimized for high-performance data access

**Wonderware**:
- **Connectivity**: Native DeviceNet driver or via OPC
- **Configuration**: InTouch, System Platform
- **Features**: Tag access, alarming, reporting
- **Integration**: Full integration with Wonderware products

**Siemens WinCC**:
- **Connectivity**: Via OPC or custom driver
- **Configuration**: WinCC configuration
- **Features**: Tag access, HMI, alarming
- **Integration**: Full integration with SIMATIC products

**Citect SCADA**:
- **Connectivity**: Native DeviceNet driver or via OPC
- **Configuration**: Citect Studio
- **Features**: Tag access, graphics, alarming
- **Integration**: Full integration with Citect products

### MES/ERP Integration

**SAP**:
- **Connectivity**: Via OPC, DeviceNet-to-Ethernet gateways
- **Data Exchange**: Production data, device status, maintenance data
- **Integration**: Custom development or third-party connectors

**Oracle**:
- **Connectivity**: Via OPC, DeviceNet-to-Ethernet gateways
- **Data Exchange**: Production data, asset data, work orders
- **Integration**: Custom development or third-party connectors

**Microsoft Dynamics**:
- **Connectivity**: Via OPC, DeviceNet-to-Ethernet gateways
- **Data Exchange**: Production data, inventory data
- **Integration**: Custom development or third-party connectors

### Cloud Integration

**AWS IoT**:
- **Connectivity**: Via MQTT, REST APIs, or DeviceNet-to-cloud gateways
- **Services**: IoT Core, IoT Greengrass, IoT Analytics
- **Features**: Device management, data storage, analytics
- **Gateways**: DeviceNet-to-MQTT gateways, DeviceNet-to-REST gateways

**Azure IoT**:
- **Connectivity**: Via MQTT, REST APIs, or Azure IoT Edge
- **Services**: IoT Hub, IoT Edge, Time Series Insights
- **Features**: Device management, data processing, analytics
- **Gateways**: DeviceNet-to-MQTT gateways, Azure IoT Edge devices

**Google Cloud**:
- **Connectivity**: Via MQTT, REST APIs, or custom gateways
- **Services**: Cloud IoT Core, Pub/Sub, Cloud Functions
- **Features**: Device management, data storage, processing
- **Gateways**: DeviceNet-to-MQTT gateways, custom gateway devices

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Device not found | No communication | Verify MAC ID, check network connectivity, test with configuration tool |
| Communication error | No data | Verify baud rate, check MAC IDs, test CAN bus health |
| Termination missing | Communication errors | Install terminators at both ends of trunk, verify resistance |
| Grounding error | Communication errors | Verify grounding, check ground connections, improve grounding |
| Power error | No communication | Verify power supply, check power connections, test power distribution |
| Cable error | Communication errors | Verify cable integrity, check cable connections, replace damaged cable |
| MAC ID conflict | Communication errors | Verify MAC IDs are unique, check device addresses, resolve conflicts |
| Baud rate mismatch | No communication | Verify all devices use same baud rate, check baud rate settings |
| Network too long | Communication errors | Verify network length, reduce length, use repeaters/bridges |
| Too many devices | Communication errors | Verify device count, reduce number of devices, segment network |
| Connector error | Communication errors | Verify connector integrity, check connector pins, replace damaged connector |
| EDS file error | Configuration failure | Verify EDS file, check file format, update EDS file |
| Firmware mismatch | Communication failure | Verify firmware versions, update firmware, check compatibility |
| CAN bus error | Communication failure | Check CAN error counters, verify bus health, investigate root cause |
| Power supply error | No power | Verify power supply, check power connections, test with multimeter |
| Short circuit | Power failure | Check for short circuits, verify insulation, use proper cable |

## Implementation Examples

### C# (DeviceNet Scanner - Allen-Bradley)
```csharp
using System;
using System.Threading;
using LibPlcCommunication.DeviceNet;

class Program
{
    static void Main(string[] args)
    {
        // Create DeviceNet scanner
        var scanner = new DeviceNetScanner();
        
        // Open scanner on COM port or Ethernet adapter
        // For Ethernet: scanner.Open("192.168.1.100")
        // For COM port: scanner.Open("COM1", 500000)
        scanner.Open("COM1", 500000); // 500 kbps
        
        try
        {
            // Scan network to discover devices
            var devices = scanner.Scan();
            Console.WriteLine("Discovered {0} devices:", devices.Count);
            foreach (var device in devices)
            {
                Console.WriteLine("MAC ID: {0}, Vendor: {1}, Product: {2}",
                    device.MacId, device.VendorId, device.ProductCode);
            }
            
            // Connect to a specific device
            var device = scanner.Connect(10); // MAC ID 10
            
            // Read I/O data
            var inputData = device.ReadDiscreteInputs();
            var outputData = device.ReadDiscreteOutputs();
            var analogInput = device.ReadAnalogInputs();
            var analogOutput = device.ReadAnalogOutputs();
            
            Console.WriteLine("Discrete Inputs: {0}", string.Join(", ", inputData));
            Console.WriteLine("Discrete Outputs: {0}", string.Join(", ", outputData));
            Console.WriteLine("Analog Inputs: {0}", string.Join(", ", analogInput));
            Console.WriteLine("Analog Outputs: {0}", string.Join(", ", analogOutput));
            
            // Write output data
            device.WriteDiscreteOutput(0, true); // Set output 0 to true
            device.WriteAnalogOutput(0, 50); // Set analog output 0 to 50%
            
            // Read device parameters
            var parameters = device.ReadParameters();
            foreach (var param in parameters)
            {
                Console.WriteLine("Parameter {0}: {1} = {2}", 
                    param.Instance, param.Name, param.Value);
            }
            
            // Set device parameter
            device.WriteParameter(100, 250); // Set parameter 100 to value 250
        }
        finally
        {
            // Close scanner
            scanner.Close();
        }
    }
}
```

### Python (DeviceNet using pyDeviceNet)
```python
from pydevicenet import DeviceNetScanner, DeviceNetDevice
import time

# Create scanner
scanner = DeviceNetScanner()

# Open scanner
# For serial port: scanner.open('/dev/ttyUSB0', 500000)
# For Ethernet: scanner.open('192.168.1.100')
scanner.open('/dev/ttyUSB0', 500000)  # 500 kbps

try:
    # Scan network
    devices = scanner.scan()
    print(f"Discovered {len(devices)} devices:")
    for device_info in devices:
        print(f"MAC ID: {device_info.mac_id}, "
              f"Vendor: {device_info.vendor_id:04X}, "
              f"Product: {device_info.product_code:04X}")
    
    # Connect to device with MAC ID 10
    device = scanner.connect(10)
    
    # Read I/O data
    inputs = device.read_discrete_inputs()
    outputs = device.read_discrete_outputs()
    analog_inputs = device.read_analog_inputs()
    analog_outputs = device.read_analog_outputs()
    
    print(f"Discrete Inputs: {inputs}")
    print(f"Discrete Outputs: {outputs}")
    print(f"Analog Inputs: {analog_inputs}")
    print(f"Analog Outputs: {analog_outputs}")
    
    # Write output
    device.write_discrete_output(0, True)  # Set output 0 to True
    device.write_analog_output(0, 50)  # Set analog output 0 to 50%
    
    # Read device identity
    identity = device.get_identity()
    print(f"Device Identity:")
    print(f"  Vendor ID: {identity.vendor_id:04X}")
    print(f"  Device Type: {identity.device_type:04X}")
    print(f"  Product Code: {identity.product_code:04X}")
    print(f"  Revision: {identity.revision_major}.{identity.revision_minor}")
    print(f"  Serial Number: {identity.serial_number:08X}")
    print(f"  Product Name: {identity.product_name}")
    
    # Read parameters
    parameters = device.read_parameters()
    for param in parameters:
        print(f"Parameter {param.instance}: {param.name} = {param.value}")
    
    # Set parameter
    device.write_parameter(100, 250)
    
finally:
    # Close scanner
    scanner.close()
```

### C (DeviceNet using Open DeviceNet)
```c
#include <stdio.h>
#include <string.h>
#include "opendevicenet.h"

int main()
{
    dn_handle_t scanner;
    dn_device_t *device;
    uint8_t inputs[8], outputs[8];
    uint16_t analog_inputs[4], analog_outputs[4];
    int i;
    
    // Open scanner
    // For serial: dn_open_serial("/dev/ttyUSB0", 500000, &scanner)
    // For Ethernet: dn_open_ethernet("192.168.1.100", &scanner)
    if (dn_open_serial("/dev/ttyUSB0", 500000, &scanner) != DN_OK) {
        fprintf(stderr, "Failed to open scanner\n");
        return 1;
    }
    
    // Scan network
    dn_device_info_t device_list[64];
    int device_count = dn_scan(scanner, device_list, 64);
    printf("Discovered %d devices:\n", device_count);
    for (i = 0; i < device_count; i++) {
        printf("MAC ID: %d, Vendor: %04X, Product: %04X\n",
               device_list[i].mac_id,
               device_list[i].vendor_id,
               device_list[i].product_code);
    }
    
    // Connect to device with MAC ID 10
    if (dn_connect(scanner, 10, &device) != DN_OK) {
        fprintf(stderr, "Failed to connect to device\n");
        dn_close(scanner);
        return 1;
    }
    
    // Read I/O data
    if (dn_read_discrete_inputs(device, inputs, 8) == DN_OK) {
        printf("Discrete Inputs: ");
        for (i = 0; i < 8; i++) printf("%d ", inputs[i]);
        printf("\n");
    }
    
    if (dn_read_discrete_outputs(device, outputs, 8) == DN_OK) {
        printf("Discrete Outputs: ");
        for (i = 0; i < 8; i++) printf("%d ", outputs[i]);
        printf("\n");
    }
    
    if (dn_read_analog_inputs(device, analog_inputs, 4) == DN_OK) {
        printf("Analog Inputs: ");
        for (i = 0; i < 4; i++) printf("%d ", analog_inputs[i]);
        printf("\n");
    }
    
    if (dn_read_analog_outputs(device, analog_outputs, 4) == DN_OK) {
        printf("Analog Outputs: ");
        for (i = 0; i < 4; i++) printf("%d ", analog_outputs[i]);
        printf("\n");
    }
    
    // Write output
    uint8_t output_data = 1;
    dn_write_discrete_output(device, 0, &output_data, 1);
    
    uint16_t analog_output_data = 50;
    dn_write_analog_output(device, 0, &analog_output_data, 1);
    
    // Read device identity
    dn_identity_t identity;
    if (dn_get_identity(device, &identity) == DN_OK) {
        printf("Device Identity:\n");
        printf("  Vendor ID: %04X\n", identity.vendor_id);
        printf("  Device Type: %04X\n", identity.device_type);
        printf("  Product Code: %04X\n", identity.product_code);
        printf("  Revision: %d.%d\n", identity.revision_major, identity.revision_minor);
        printf("  Serial Number: %08X\n", identity.serial_number);
    }
    
    // Disconnect and close
    dn_disconnect(device);
    dn_close(scanner);
    
    return 0;
}
```

## Vendor Ecosystem

**DeviceNet Products**:
- **Network Infrastructure**: Cables, taps, terminators, power supplies
- **Devices**: I/O modules, sensors, actuators, drives, HMIs
- **Scanners**: PLC scanner modules, PC scanner cards, gateway devices
- **Configuration Tools**: Network scanners, configuration software, EDS file editors

**Major Vendors**:
- **Allen-Bradley/Rockwell Automation**: 1794 Flex I/O, 1734 Point I/O, 1732 ArmorBlock I/O, DeviceNet scanners
- **Omron**: E3Z photoelectric sensors, E2B proximity sensors, G9SP safety sensors, DeviceNet masters
- **Schneider Electric**: XBT photoelectric sensors, XS proximity sensors, DeviceNet scanners
- **Siemens**: ET200S I/O, SIMATIC sensors, DeviceNet modules
- **Balluff**: BES photoelectric sensors, BNS proximity sensors, BML laser sensors
- **ifm efector**: Various sensors (pressure, temperature, flow, level)
- **Banner Engineering**: Photoelectric sensors, proximity sensors, safety sensors
- **Turck**: Proximity sensors, photoelectric sensors, I/O modules
- **SICK**: Photoelectric sensors, proximity sensors, encoders
- **Keyence**: Photoelectric sensors, proximity sensors, measurement sensors
- **Molex**: DeviceNet infrastructure (cables, taps, terminators)
- **Belden**: DeviceNet cables, connectivity solutions
- **Lumberg**: DeviceNet connectors, cable assemblies

**ODVA (Open DeviceNet Vendors Association)**:
- **Organization**: Industry association for DeviceNet and EtherNet/IP
- **Standards**: DeviceNet specification, EDS format, conformance testing
- **Certification**: DeviceNet conformance testing and certification
- **Resources**: [odva.org](https://www.odva.org)

## Resources

- **ODVA**: [odva.org](https://www.odva.org)
- **DeviceNet Specification**: [ODVA DeviceNet Specifications](https://www.odva.org/technology-standards/device-level/device-net/)
- **DeviceNet Books**:
  - DeviceNet Specification Volume 1: Network and Physical Layer
  - DeviceNet Specification Volume 2: Device Profile
  - DeviceNet Specification Volume 3: Application Layer
- **DeviceNet Tools**:
  - RSNetWorx for DeviceNet (Allen-Bradley)
  - DeviceNet Configurator (Omron)
  - DeviceNet Scanner (various vendors)
- **DeviceNet Documentation**:
  - Vendor-specific documentation for DeviceNet products
  - Application notes, installation guides, troubleshooting guides

## Standing Rules

- **A MAC ID is a device's address on the network** — each DeviceNet device must have a unique MAC ID (1-63); MAC ID 0 means unassigned, and duplicate MAC IDs will cause communication conflicts.
- **The baud rate must be consistent** — all devices on a DeviceNet network must use the same baud rate (125, 250, or 500 kbps); mismatched baud rates will prevent communication.
- **Terminators are mandatory** — every DeviceNet trunk must have a 120 Ohm terminator at each end; missing terminators cause signal reflections and communication errors.
- **DeviceNet is a CAN-based network** — it inherits CAN's arbitration, error detection, and fault tolerance; understand CAN fundamentals to effectively design and troubleshoot DeviceNet networks.
- **Power is distributed via the trunk** — DeviceNet uses the trunk cable to distribute 24V DC power to devices; ensure your power supply can handle the total current draw of all devices.
- **EDS files simplify configuration** — Electronic Data Sheet files describe device capabilities and parameters; use them to automate configuration and ensure compatibility.
- **The trunk-line/drop-line topology is fixed** — DeviceNet uses a specific topology with a main trunk and drops to devices; follow this topology for reliable operation.
- **Cable quality matters** — DeviceNet cable must meet specification (conductor size, shielding, etc.); using substandard cable can cause communication issues.
- **Grounding is essential** — proper grounding reduces noise and improves reliability; ground the network at the power supply and at intervals along the trunk.
- **Network length limits are absolute** — DeviceNet has strict length limits (500m at 125 kbps, 250m at 250 kbps, 100m at 500 kbps); exceeding these limits will cause communication failures.
- **Device count limits are absolute** — a DeviceNet network can support a maximum of 64 devices; attempting to connect more will cause communication issues.
- **The drop line length is limited** — each drop line can be a maximum of 6m long, and the total length of all drop lines cannot exceed 6m; plan your network layout accordingly.
- **Use the right connectors** — DeviceNet uses specific connectors (open-style for trunk, 5-way for drops); using wrong connectors will cause connection issues.
- **Test before power** — always test cable continuity and connections before applying power to the network.
- **Label everything** — label devices with MAC ID, description, and location; this makes troubleshooting much easier.
- **Document your network** — document the network layout, device addresses, baud rate, and configurations; this is essential for maintenance and troubleshooting.
- **Monitor CAN error counters** — DeviceNet devices track CAN errors; monitor these counters to detect and diagnose communication issues.
- **Use redundant power for critical applications** — for 24/7 operation, use redundant power supplies to prevent power-related failures from taking down the network.
- **Segment large networks** — for networks with many devices or long distances, use bridges or repeaters to segment the network and maintain performance.
- **Avoid mixing baud rates** — never mix devices with different baud rates on the same network; this will cause communication failures.
- **Use EDS files for configuration** — EDS files contain device-specific information that simplifies configuration; use them whenever possible.
- **Validate configurations** — after configuring a network, validate the configuration with a network scanner or configuration tool.
- **Test communication thoroughly** — after setting up a network, test communication with every device to ensure proper operation.
- **Maintain spare parts** — keep spare devices, cables, taps, and terminators on hand for quick replacement in case of failure.
- **Train maintenance personnel** — ensure maintenance personnel understand DeviceNet basics, troubleshooting, and proper maintenance procedures.
- **Regularly inspect the network** — periodically inspect the network for physical issues, damaged cables, loose connections, etc.
- **Update firmware** — keep device firmware up to date for bug fixes, performance improvements, and new features.
- **Consider environmental factors** — DeviceNet networks often operate in harsh environments; consider temperature, humidity, vibration, and other factors in your network design.
- **Use appropriate cable for the environment** — for harsh environments, use cable rated for the conditions (temperature, chemical exposure, etc.).
- **Plan for future expansion** — when designing a network, leave room for additional devices, cable runs, and power requirements.
