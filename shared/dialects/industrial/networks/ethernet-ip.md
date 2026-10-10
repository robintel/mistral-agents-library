---
type: protocol
family: industrial
---

# EtherNet/IP and CIP (Common Industrial Protocol)

**The backbone of industrial Ethernet**: EtherNet/IP is the **most widely adopted
industrial Ethernet protocol** in North America, built on standard Ethernet
and TCP/IP with the **Common Industrial Protocol (CIP)** at the application layer.
It provides **real-time, deterministic communication** for industrial automation,
combining the familiarity of Ethernet with the performance requirements of control systems.

## Eras

The era is declared by the **CIP specification version** and **EtherNet/IP adoption**.

**CIP v1.0 (1990s)**: Original specification.
- **Focus**: Basic industrial communication
- **Transport**: Implicit messaging only
- **Protocols**: DeviceNet, ControlNet
- **Status**: Legacy, foundation for later versions

**CIP v2.0 (2000)**: Enhanced capabilities.
- **Transport**: Implicit + Explicit messaging
- **Protocols**: EtherNet/IP, DeviceNet, ControlNet
- **Features**: Improved object model, connection management
- **Status**: Widely adopted

**CIP v3.0+ (2005)**: Modern industrial networking.
- **Transport**: Full explicit messaging, UCMM (Unconnected Message Manager)
- **Protocols**: EtherNet/IP as primary, DeviceNet, ControlNet
- **Features**: Enhanced object library, security, performance
- **Status**: Current, actively used

**EtherNet/IP Adoption**:
- **Early (2000-2005)**: Initial adoption, mostly for configuration
- **Growth (2005-2015)**: Widespread adoption for I/O and control
- **Mature (2015-Present)**: Dominant industrial Ethernet protocol in North America
- **Future**: Continued evolution with TSN (Time-Sensitive Networking) integration

## Architecture

### Protocol Stack

EtherNet/IP uses a **7-layer protocol stack** that builds on standard Ethernet:

**Layer 7 - Application**: CIP (Common Industrial Protocol)
- **Function**: Industrial application protocol
- **Services**: Connection management, I/O messaging, explicit messaging
- **Objects**: Device profiles, data access, configuration

**Layer 6 - Presentation**: CIP
- **Function**: Data representation and encoding
- **Encoding**: CIP message format, data types

**Layer 5 - Session**: CIP
- **Function**: Connection establishment and management
- **Connections**: Explicit connections, I/O connections

**Layer 4 - Transport**: TCP (for Explicit Messaging) / UDP (for Implicit Messaging)
- **Function**: End-to-end communication
- **Ports**: TCP 44818 (Explicit), UDP 2222 (Implicit)

**Layer 3 - Network**: IP
- **Function**: Network addressing and routing
- **IPv4/IPv6**: Both supported

**Layer 2 - Data Link**: Ethernet (IEEE 802.3)
- **Function**: Frame formatting, MAC addressing
- **Standard Ethernet**: 10/100/1000 Mbps

**Layer 1 - Physical**: Ethernet
- **Function**: Physical transmission
- **Media**: Twisted pair (copper), fiber optic
- **Connectors**: RJ-45, M12, etc.

### CIP Architecture

**CIP Object Model**: Everything in CIP is an object with attributes and services.

**Object Classes**:
- **Identity Object (Class 0x01)**: Device identification (vendor, product type, serial number)
- **Message Router Object (Class 0x02)**: Message routing between objects
- **DeviceNet Object (Class 0x03)**: DeviceNet-specific functionality
- **Assembly Object (Class 0x04)**: Data assembly and disassembly
- **Connection Object (Class 0x05)**: Connection management
- **Connection Manager Object (Class 0x06)**: Connection creation and management
- **Parameter Object (Class 0x0F)**: Parameter storage and access
- **Parameter Group Object (Class 0x10)**: Grouped parameter access
- **Discrete Input Point (Class 0x1B)**: Digital input data
- **Discrete Output Point (Class 0x1C)**: Digital output data
- **Analog Input Point (Class 0x1D)**: Analog input data
- **Analog Output Point (Class 0x1E)**: Analog output data
- **Preset Single Integer (Class 0x1F)**: Integer parameter
- **Preset Single Floating Point (Class 0x20)**: Floating-point parameter
- **Command Block Object (Class 0x28)**: Command execution
- **File Object (Class 0x35)**: File transfer and management
- **Electronic Data Sheet (EDS) Object (Class 0x3F)**: Device description

**CIP Services**:
- **Get_Attribute_Single**: Read a single attribute from an object
- **Set_Attribute_Single**: Write a single attribute to an object
- **Get_Attribute_All**: Read all attributes from an object
- **Set_Attribute_All**: Write all attributes to an object
- **Find_Next_Object_Instance**: Discover object instances
- **Reset**: Reset an object or device
- **Start**: Start an object or device
- **Stop**: Stop an object or device
- **Create**: Create a new object instance
- **Delete**: Delete an object instance
- **Multiple Service Packet**: Execute multiple services in one message

### Communication Models

**Explicit Messaging**:
- **Purpose**: Non-real-time, request/response communication
- **Transport**: TCP/IP (port 44818)
- **Use Cases**: Configuration, diagnostics, file transfer, non-time-critical data
- **Connection**: Requires explicit connection establishment
- **Messaging**: Unicast (one-to-one) or multicast (one-to-many)
- **Delivery**: Guaranteed delivery with acknowledgment
- **Applications**: HMI, configuration tools, engineering workstations

**Implicit Messaging (I/O Messaging)**:
- **Purpose**: Real-time, cyclic I/O data exchange
- **Transport**: UDP/IP (port 2222)
- **Use Cases**: Real-time control, I/O data exchange, time-critical operations
- **Connection**: Uses I/O connections with configured RPI (Requested Packet Interval)
- **Messaging**: Unicast only (one-to-one)
- **Delivery**: Not guaranteed (UDP), relies on cyclic polling
- **Applications**: PLC-to-PLC communication, real-time control systems
- **Performance**: Deterministic, low latency (< 10ms typical)

**UCMM (Unconnected Message Manager)**:
- **Purpose**: Unconnected explicit messaging
- **Transport**: UDP/IP (port 2222)
- **Use Cases**: Device discovery, non-critical explicit messaging
- **Connection**: No connection establishment required
- **Messaging**: Unicast or multicast
- **Delivery**: Best-effort (UDP), no acknowledgment
- **Applications**: Device discovery, network configuration

## Device Profiles

### Standard Device Profiles

**Generic Device Profile**:
- **Purpose**: Basic device functionality
- **Objects**: Identity, Message Router, Assembly, Connection Manager
- **Services**: Standard CIP services
- **Use Case**: Simple devices, custom devices

**I/O Device Profile**:
- **Purpose**: Digital and analog I/O
- **Objects**: Identity, Message Router, Assembly, Discrete Input/Output Points, Analog Input/Output Points
- **Services**: Standard CIP services + I/O-specific services
- **Data Types**: Bool, Int, Float, String
- **Use Case**: I/O modules, remote I/O

**Motion Control Profile**:
- **Purpose**: Motion control devices (servos, drives)
- **Objects**: Identity, Message Router, Assembly, Axis objects, Motion Group objects
- **Services**: Standard CIP services + motion-specific services
- **Data Types**: Position, velocity, acceleration, torque
- **Use Case**: Servo drives, motion controllers, CNC machines

**Safety Device Profile (CIP Safety)**:
- **Purpose**: Safety-rated devices
- **Objects**: Identity, Message Router, Safety-related objects
- **Services**: Safety-specific services with built-in redundancy and verification
- **Safety Level**: SIL 3, PLe, Category 4
- **Use Case**: Safety relays, light curtains, emergency stop devices
- **Protocol**: CIP Safety on separate network or VLAN

**Energy Profile (CIP Energy)**:
- **Purpose**: Energy monitoring and management
- **Objects**: Identity, Message Router, Energy objects (power, energy, demand)
- **Services**: Energy-specific services
- **Use Case**: Energy meters, power monitors, demand management

### Vendor-Specific Profiles

**Allen-Bradley/ Rockwell Automation**:
- **Devices**: ControlLogix, CompactLogix, MicroLogix, Flex I/O, Kinetix drives
- **Extensions**: Enhanced object library, custom services
- **Integration**: Tight integration with Studio 5000, FactoryTalk

**Omron**:
- **Devices**: NJ, NX, Sysmac controllers
- **Extensions**: Sysmac-specific objects and services
- **Integration**: Sysmac Studio, CX-One

**Schneider Electric**:
- **Devices**: Quantum, Premium, M340, M580
- **Extensions**: Unity Pro integration, custom objects
- **Integration**: EcoStruxure, Unity Pro

**Mitsubishi**:
- **Devices**: Q series, iQ-R, iQ-F
- **Extensions**: Custom CIP implementation
- **Integration**: GX Works2, GX Developer

**Other Vendors**:
- **B&R**: X20, X90, APOLLON
- **GE Intelligent Platforms**: RX3i, RX7i, PACSystems
- **Honeywell**: ControlEdge, Smart Multiplexer
- **Yokogawa**: STARDOM, FA-M3

## Configuration

### Device Configuration

**EDS (Electronic Data Sheet) File**:
- **Purpose**: Device description file
- **Format**: XML-based (IEC 61804-2 EDDL)
- **Content**: Device identity, object definitions, parameters, communication settings
- **Use**: Automatic device configuration, parameter validation, HMI integration
- **Tools**: EDS file editors, configuration tools

**Configuration Parameters**:
- **IP Address**: Device IP address, subnet mask, default gateway
- **Host Name**: Device hostname (optional)
- **CIP Identity**: Vendor ID, Product Type, Product Code, Revision
- **Connection Parameters**: RPI (Requested Packet Interval), connection size
- **I/O Configuration**: Input/output configuration, data types, scaling
- **Security**: Authentication, authorization, encryption settings

### Network Configuration

**IP Addressing**:
- **IPv4**: Standard IPv4 addressing (recommended for industrial networks)
- **IPv6**: Supported but less common in industrial environments
- **Subnet**: Proper subnet design for network segmentation
- **VLAN**: Virtual LAN for traffic isolation and prioritization

**Ethernet Configuration**:
- **Speed**: Auto-negotiation or fixed (10/100/1000 Mbps)
- **Duplex**: Auto or fixed (half/full duplex)
- **Flow Control**: Enable/disable flow control
- **Jumbo Frames**: Support for jumbo frames (up to 9000 bytes)

**Switch Configuration**:
- **Port Configuration**: Speed, duplex, flow control per port
- **QoS**: Quality of Service settings for traffic prioritization
- **IGMP**: Internet Group Management Protocol for multicast
- **STP/RSTP**: Spanning Tree Protocol for network redundancy
- **Port Security**: MAC address filtering, port locking

### Connection Configuration

**I/O Connections**:
- **Purpose**: Real-time I/O data exchange
- **Type**: Input-only, Output-only, or Both
- **RPI (Requested Packet Interval)**: Cyclic communication rate (typically 1-100ms)
- **Connection Size**: Number of bytes per packet
- **Watchdog Timeout**: Timeout for connection monitoring
- **Inhibit Time**: Time to inhibit connection after timeout

**Explicit Connections**:
- **Purpose**: Non-real-time, request/response communication
- **Type**: Point-to-point
- **Priority**: Connection priority (0-255)
- **Connection Parameters**: Packet size, timeout, retry
- **Security**: Authentication, encryption settings

## Features

### Real-Time Performance

**Deterministic Communication**:
- **Cyclic I/O**: Guaranteed cyclic data exchange at configured RPI
- **Jitter**: Minimal jitter (< 1ms typical)
- **Latency**: Low latency (< 10ms typical for I/O messaging)
- **Synchronization**: Time synchronization via IEEE 1588 (PTP) or NTP

**Bandwidth Optimization**:
- **RPI Selection**: Optimize RPI based on application requirements
- **Data Packing**: Pack multiple data points into single packets
- **Change of State (COS)**: Only transmit data when it changes
- **Deadband**: Only transmit data when it changes by a threshold

**Network Efficiency**:
- **Multicast**: Use multicast for one-to-many communication
- **UDP**: Use UDP for real-time I/O to avoid TCP overhead
- **TCP**: Use TCP for non-real-time to ensure reliable delivery
- **QoS**: Quality of Service for traffic prioritization

### Device Discovery and Integration

**Device Discovery**:
- **UCMM Discovery**: Unconnected Message Manager for device discovery
- **Broadcast Discovery**: Broadcast-based discovery (limited to local subnet)
- **Multicast Discovery**: Multicast-based discovery (across subnets)
- **EDS-based Discovery**: Automatic discovery using EDS files

**Integration Methods**:
- **Configuration Tools**: Vendor-specific configuration tools (Studio 5000, Sysmac Studio)
- **HMI Integration**: Automatic integration with HMI/SCADA systems
- **OPC UA**: OPC UA server for standard interface
- **MQTT**: MQTT client for cloud/IIoT integration
- **REST API**: REST API for custom integration

### Security

**CIP Security**:
- **Authentication**: Username/password, certificate-based
- **Authorization**: Role-based access control
- **Encryption**: Data encryption for sensitive communications
- **Integrity**: Message authentication, data verification
- **Audit**: Security event logging and auditing

**Network Security**:
- **Firewall**: Firewall rules for EtherNet/IP traffic
- **VPN**: Virtual Private Network for secure remote access
- **VLAN**: Virtual LAN for network segmentation
- **IDS/IPS**: Intrusion Detection/Prevention Systems
- **Port Security**: Physical port security, MAC address filtering

**Device Security**:
- **Secure Boot**: Verify firmware integrity at boot
- **Device Authentication**: Authenticate devices before allowing communication
- **Certificate Management**: X.509 certificate generation, management, renewal
- **Firmware Updates**: Secure firmware update mechanisms
- **Tamper Detection**: Detect physical tampering with devices

## Best Practices

### Network Design
- **Network Segmentation**: Segment industrial networks from IT networks
- **VLAN Usage**: Use VLANs to separate different types of traffic (I/O, HMI, engineering)
- **QoS Configuration**: Configure QoS to prioritize real-time traffic
- **Redundancy**: Implement network redundancy (dual switches, RSTP)
- **Bandwidth Planning**: Plan for sufficient bandwidth (real-time traffic + engineering + HMI)
- **Latency Considerations**: Design for low latency (< 10ms for control traffic)

### Device Configuration
- **Use EDS Files**: Always use EDS files for device configuration
- **Validate Configurations**: Validate device configurations before deployment
- **Optimize RPI**: Select appropriate RPI based on application requirements
- **Monitor Connections**: Monitor connection status and health
- **Configure Timeouts**: Set appropriate timeouts for connections and devices
- **Use Descriptive Names**: Use descriptive names for devices, connections, and tags

### Security Design
- **Defense in Depth**: Implement multiple layers of security (device, network, application)
- **Least Privilege**: Grant minimum necessary permissions
- **Network Segmentation**: Segment networks to limit blast radius
- **Encryption**: Use encryption for sensitive data
- **Authentication**: Require authentication for all access
- **Audit Logging**: Enable audit logging for security events
- **Regular Audits**: Conduct regular security audits

### Performance Optimization
- **Optimize RPI**: Balance RPI with application requirements and network capacity
- **Use COS/Deadband**: Use Change of State and deadband filtering to reduce traffic
- **Data Packing**: Pack data efficiently to reduce packet count
- **Multicast**: Use multicast for one-to-many communication
- **Monitor Performance**: Monitor network performance and latency
- **Load Testing**: Test performance under expected and peak loads

### Maintenance and Troubleshooting
- **Document Configurations**: Document all network and device configurations
- **Backup Configurations**: Regularly backup device and network configurations
- **Monitor Health**: Monitor device and network health
- **Test Connectivity**: Regularly test connectivity and communication
- **Firmware Updates**: Keep device firmware up to date
- **Spare Parts**: Maintain inventory of spare devices and components

## Migration Paths

### DeviceNet to EtherNet/IP
- **Benefits**: Higher speed, longer distances, standard Ethernet infrastructure
- **Challenges**: Wiring changes, configuration updates
- **Approach**: Gradual migration, dual-network operation during transition
- **Tools**: Configuration tools, migration utilities

### ControlNet to EtherNet/IP
- **Benefits**: Standard Ethernet, higher bandwidth, future-proof
- **Challenges**: Deterministic performance, synchronization
- **Approach**: Careful planning, performance testing, phased migration
- **Considerations**: Use CIP Sync for time synchronization

### Proprietary to EtherNet/IP
- **Benefits**: Standardization, interoperability, vendor independence
- **Challenges**: Protocol translation, device compatibility
- **Approach**: Use gateway devices, protocol converters
- **Tools**: Protocol converters, gateway configurations

### Single Network to Redundant Network
- **Benefits**: High availability, fault tolerance
- **Challenges**: Network design, configuration, cost
- **Approach**: Implement RSTP, dual switches, redundant paths
- **Testing**: Thoroughly test failover and redundancy

## Integration

### PLC Integration

**Allen-Bradley**:
- **Native Support**: Full native support for EtherNet/IP
- **Devices**: ControlLogix, CompactLogix, MicroLogix, Flex I/O
- **Configuration**: Studio 5000, RSLogix 5000
- **Performance**: Optimized for Rockwell Automation devices
- **Extensions**: Enhanced object library, custom services

**Omron**:
- **Native Support**: Full native support
- **Devices**: NJ, NX, Sysmac controllers
- **Configuration**: Sysmac Studio
- **Integration**: Tight integration with CX-One
- **Extensions**: Sysmac-specific objects

**Schneider Electric**:
- **Native Support**: Full support
- **Devices**: Quantum, Premium, M340, M580
- **Configuration**: Unity Pro
- **Integration**: EcoStruxure platform
- **Extensions**: Custom objects for Unity Pro

**Mitsubishi**:
- **Support**: Via custom implementation or gateway
- **Devices**: Q series, iQ-R, iQ-F
- **Configuration**: GX Works2, GX Developer
- **Integration**: Custom CIP implementation

**Other Vendors**:
- **B&R**: Full support via X20, X90 controllers
- **GE**: Full support via RX3i, RX7i controllers
- **Honeywell**: Full support via ControlEdge
- **Yokogawa**: Full support via STARDOM

### SCADA Integration

**Ignition**:
- **Connectivity**: Native EtherNet/IP driver
- **Configuration**: Drag-and-drop configuration
- **Performance**: Optimized for high-performance data access
- **Features**: Tag browsing, alarm integration, trend display

**Wonderware**:
- **Connectivity**: Native EtherNet/IP driver
- **Configuration**: InTouch, System Platform
- **Integration**: Full integration with Wonderware products
- **Features**: Tag access, alarming, reporting

**Siemens WinCC**:
- **Connectivity**: Via OPC UA or custom driver
- **Configuration**: WinCC configuration
- **Integration**: Full integration with SIMATIC products
- **Features**: Tag access, HMI, alarming

**Citect SCADA**:
- **Connectivity**: Native EtherNet/IP driver
- **Configuration**: Citect Studio
- **Integration**: Full integration with Citect products
- **Features**: Tag access, graphics, alarming

### MES/ERP Integration

**SAP**:
- **Connectivity**: Via OPC UA, REST APIs, or custom integration
- **Data Exchange**: Production data, quality data, maintenance data
- **Integration**: Custom development or third-party connectors

**Oracle**:
- **Connectivity**: Via OPC UA, SQL, REST APIs
- **Data Exchange**: Production data, asset data, work orders
- **Integration**: Custom development or third-party connectors

**Microsoft Dynamics**:
- **Connectivity**: Via OPC UA, web services
- **Data Exchange**: Production data, inventory data
- **Integration**: Custom development or third-party connectors

### Cloud Integration

**AWS IoT**:
- **Connectivity**: Via MQTT, REST APIs, or custom gateway
- **Services**: IoT Core, IoT Greengrass, IoT Analytics
- **Features**: Device management, data storage, analytics

**Azure IoT**:
- **Connectivity**: Via MQTT, REST APIs, or Azure IoT Edge
- **Services**: IoT Hub, IoT Edge, Time Series Insights
- **Features**: Device management, data processing, analytics

**Google Cloud**:
- **Connectivity**: Via MQTT, REST APIs, or custom gateway
- **Services**: Cloud IoT Core, Pub/Sub, Cloud Functions
- **Features**: Device management, data storage, processing

### Database Integration

**SQL Databases**:
- **Connectivity**: Via ODBC, JDBC, or native drivers
- **Data Storage**: Historical data, configuration, alarm history
- **Examples**: SQL Server, PostgreSQL, MySQL, Oracle

**Time-Series Databases**:
- **Connectivity**: Via custom APIs or protocols
- **Data Storage**: Process data, sensor data, historical trends
- **Examples**: InfluxDB, TimescaleDB, OSIsoft PI, AVEVA Historian

**NoSQL Databases**:
- **Connectivity**: Via custom APIs or protocols
- **Data Storage**: Configuration, device metadata, events
- **Examples**: MongoDB, Cassandra, Redis

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Device not found | No communication | Verify IP address, check network connectivity, test with configuration tool |
| Connection timeout | No data | Check RPI settings, verify device configuration, test with configuration tool |
| Data mismatch | Incorrect data | Verify data types, check scaling, validate device configuration |
| Network congestion | Slow communication | Optimize RPI, use QoS, segment network, check bandwidth |
| Packet loss | Data loss | Check network quality, optimize RPI, use TCP for non-real-time |
| Duplicate IP | Communication failure | Verify IP addressing, check DHCP settings, use static IPs |
| DNS resolution error | No connectivity | Verify DNS configuration, use static IP addresses |
| Authentication error | No access | Verify credentials, check authentication settings, test authentication |
| Authorization error | Access denied | Verify permissions, check authorization settings, test authorization |
| EDS file error | Configuration failure | Verify EDS file, check file format, update EDS file |
| Firmware mismatch | Communication failure | Verify firmware versions, update firmware, check compatibility |
| Watchdog timeout | Connection drop | Increase watchdog timeout, check device health, investigate root cause |
| Port conflict | Communication failure | Check port usage, verify port configuration, use standard ports |
| VLAN misconfiguration | No communication | Verify VLAN settings, check switch configuration, test VLAN connectivity |
| QoS misconfiguration | Poor performance | Verify QoS settings, check switch configuration, prioritize critical traffic |
| Security breach | Data compromise | Isolate device, investigate breach, update credentials, patch vulnerabilities |

## Implementation Examples

### C# (EtherNet/IP Client - Explicit Messaging)
```csharp
using System;
using System.Net;
using System.Net.Sockets;
using LibPlcCommunication.EtherNetIp;

class Program
{
    static void Main(string[] args)
    {
        // Create EtherNet/IP client
        var client = new EtherNetIpClient();
        
        // Connect to device
        var device = client.Connect(IPAddress.Parse("192.168.1.10"));
        
        try
        {
            // Read tag value (explicit messaging)
            var tagName = "MyTag";
            var value = device.ReadTag(tagName);
            Console.WriteLine($"{tagName} = {value}");
            
            // Write tag value
            device.WriteTag(tagName, 1234);
            
            // Read multiple tags
            var tags = new[] { "Tag1", "Tag2", "Tag3" };
            var values = device.ReadTags(tags);
            foreach (var (tag, val) in tags.Zip(values))
            {
                Console.WriteLine($"{tag} = {val}");
            }
            
            // Get device identity
            var identity = device.GetIdentity();
            Console.WriteLine($