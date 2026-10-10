---
type: protocol
family: industrial
---

# OPC UA (Open Platform Communications Unified Architecture)

The **platform-independent, service-oriented, secure** industrial
interoperability standard. Unlike its predecessor (OPC Classic/DCOM),
OPC UA works across Windows, Linux, embedded devices, and the cloud.
It is the foundation of **Industry 4.0** and **Industrial Internet
of Things (IIoT)**.

## Eras

The era is declared by the **specification version** and **transport
mechanism**.

**OPC UA 1.00 (2008)**: Initial release, core services
**OPC UA 1.01-1.04 (2009-2018)**: Enhancements, bug fixes, clarifications
**OPC UA 1.05 (2022)**: Latest version with major improvements

**Transport eras**:
- **OPC UA Classic**: TCP-based, original transport
- **OPC UA over TSN (Time-Sensitive Networking)**: Real-time capable
- **OPC UA over MQTT**: Lightweight, cloud-friendly
- **OPC UA over AMQP**: Message-oriented transport
- **OPC UA over HTTPS**: Web-friendly transport
- **OPC UA PubSub**: Publisher-Subscriber model (not request-response)

## Architecture Overview

OPC UA is **service-oriented**: everything is a **service** that operates
on an **information model**. The model defines the data; the services
access and manipulate it.

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    OPC UA Application                      │
├─────────────────┬─────────────────┬───────────────────┤
│   Information    │     Services     │   Communication    │
│      Model       │  (Operations)    │     (Transport)    │
└────────┬────────┴────────┬────────┴──────────┬────────┘
         │                 │                 │
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
│ Address Space    │ │ Read/Write │ │ TCP/HTTPS   │
│ - Nodes          │ │ Browse     │ │ UA SC       │
│ - References     │ │ Subscribe  │ │ MQTT/AMQP   │
│ - Types          │ │ Call       │ │ TSN         │
│ - Views          │ │ Monitor    │ │ ...         │
└─────────────────┘ └─────────────┘ └─────────────┘
```

## Information Model

The **Address Space** is the heart of OPC UA. It is a **graph of
nodes** connected by **references**. Each node represents something
in the real world: a variable, a method, an object, a data type.

### Node Classes

| Class | Description | Example |
|-------|-------------|---------|
| **Object** | Represents an entity with identity | Machine, Device, Motor |
| **Variable** | Represents a value | Temperature, Speed, Pressure |
| **Method** | Represents an executable function | StartMotor, ResetCounter |
| **ObjectType** | Template for Objects | MotorType, DeviceType |
| **VariableType** | Template for Variables | TemperatureType, AnalogValueType |
| **MethodType** | Template for Methods | StartStopMethodType |
| **DataType** | Defines data structures | Int32, String, CustomStruct |
| **ReferenceType** | Defines reference semantics | HierarchicalReferences, Organizes |
| **View** | Subset of Address Space | EngineeringView, OperatorView |

### Node IDs

Each node has a **unique Node ID** within the server. Node IDs can be:

- **Numeric**: `ns=2;i=12345` (namespace index + integer)
- **String**: `ns=2;s=MyNode` (namespace index + string)
- **Opaque**: `ns=2;opaque=...` (namespace index + byte string)
- **GUID**: `ns=2;g=...` (namespace index + GUID)

**Namespace**: Each server can define multiple namespaces (identified by index)

### References

References connect nodes and define relationships. Each reference has:
- **ReferenceType**: Defines the type of relationship
- **IsForward**: Direction of the reference
- **TargetNode**: The node being referenced

**Common ReferenceTypes**:
- **HierarchicalReferences**: Parent-child relationships
- **Organizes**: Non-hierarchical grouping
- **HasTypeDefinition**: Instance to Type relationship
- **HasComponent**: Object has a component
- **HasProperty**: Object has a property

### Address Space Hierarchy

```
Root
  ├─ Objects
  │   ├─ Server
  │   │   ├─ ServerStatus
  │   │   ├─ Namespaces
  │   │   └─ ...
  │   └─ MyDevice
  │       ├─ Temperature (Variable)
  │       ├─ Pressure (Variable)
  │       └─ StartMotor (Method)
  ├─ Types
  │   ├─ ObjectTypes
  │   │   └─ MyDeviceType
  │   ├─ VariableTypes
  │   │   └─ SensorType
  │   └─ DataTypes
  │       └─ MyCustomStruct
  └─ Views
      ├─ EngineeringView
      └─ OperatorView
```

### Information Modeling Patterns

#### 1. Instance-Type Pattern

```
MyDeviceType (ObjectType)
  ├─ Temperature (Variable)
  │   └─ HasTypeDefinition → TemperatureType
  ├─ Pressure (Variable)
  │   └─ HasTypeDefinition → PressureType
  └─ StartMotor (Method)
      └─ HasTypeDefinition → StartStopMethodType

MyDevice (Object)
  ├─ HasTypeDefinition → MyDeviceType
  ├─ Temperature (Variable Instance)
  │   └─ HasTypeDefinition → TemperatureType
  ├─ Pressure (Variable Instance)
  │   └─ HasTypeDefinition → PressureType
  └─ StartMotor (Method Instance)
```

#### 2. Component Pattern

```
Machine (Object)
  ├─ HasComponent → Motor1 (Object)
  │   └─ HasTypeDefinition → MotorType
  ├─ HasComponent → Motor2 (Object)
  │   └─ HasTypeDefinition → MotorType
  └─ HasComponent → Sensor1 (Object)
      └─ HasTypeDefinition → SensorType
```

#### 3. Hierarchical Pattern

```
Plant (Object)
  └─ HasComponent → Line1 (Object)
      └─ HasComponent → Machine1 (Object)
          └─ HasComponent → Temperature (Variable)
```

#### 4. Property Pattern

```
Device (Object)
  ├─ HasProperty → Manufacturer (Variable)
  ├─ HasProperty → Model (Variable)
  └─ HasProperty → SerialNumber (Variable)
```

## Services

OPC UA defines **35 services** organized into **service sets**. Services
are the operations that clients can invoke on servers.

### Service Sets

#### Discovery Services
| Service | Purpose |
|---------|---------|
| GetEndpoints | Discover server endpoints |
| FindServers | Discover servers on network |
| GetServer | Get server information |

#### Secure Channel Services
| Service | Purpose |
|---------|---------|
| OpenSecureChannel | Establish secure channel |
| CloseSecureChannel | Close secure channel |

#### Session Services
| Service | Purpose |
|---------|---------|
| CreateSession | Create client session |
| ActivateSession | Activate session with user identity |
| CloseSession | Close session |

#### Node Management Services
| Service | Purpose |
|---------|---------|
| AddNodes | Add nodes to address space |
| DeleteNodes | Remove nodes from address space |

#### View Services
| Service | Purpose |
|---------|---------|
| Browse | Browse address space |
| BrowseNext | Continue browsing |

#### Query Services
| Service | Purpose |
|---------|---------|
| QueryFirst | Execute query |
| QueryNext | Get next query results |

#### Attribute Services
| Service | Purpose |
|---------|---------|
| Read | Read node attributes |
| Write | Write node attributes |
| HistoryRead | Read historical data |
| HistoryUpdate | Update historical data |

#### Method Services
| Service | Purpose |
|---------|---------|
| Call | Call a method on a node |

#### Monitored Item Services
| Service | Purpose |
|---------|---------|
| CreateMonitoredItems | Create monitored items |
| DeleteMonitoredItems | Delete monitored items |
| ModifyMonitoredItems | Modify monitored items |
| SetMonitoringMode | Set monitoring mode |
| SetTriggering | Set triggering |
| GetMonitoredItemInfo | Get monitored item info |

#### Subscription Services
| Service | Purpose |
|---------|---------|
| CreateSubscription | Create subscription |
| ModifySubscription | Modify subscription |
| DeleteSubscriptions | Delete subscriptions |
| SetPublishingMode | Set publishing mode |
| Publish | Publish notification messages |
| Republish | Request republish of notifications |
| TransferSubscription | Transfer subscription to another session |

### Common Service Sequences

#### Connecting to a Server

```
1. GetEndpoints → Discover server endpoints
2. OpenSecureChannel → Establish secure channel
3. CreateSession → Create session
4. ActivateSession → Activate session with credentials
```

#### Reading a Variable

```
1. Browse → Find Variable NodeId
2. Read → Read Variable value
```

#### Writing a Variable

```
1. Browse → Find Variable NodeId
2. Write → Write new value
```

#### Calling a Method

```
1. Browse → Find Method NodeId
2. Browse → Find Method input argument definitions
3. Call → Call method with input arguments
```

#### Subscribing to Data Changes

```
1. CreateSubscription → Create subscription
2. CreateMonitoredItems → Create monitored items for variables
3. SetMonitoringMode → Set monitoring mode to Reporting
4. SetTriggering → Set triggering for monitored items
```

## Data Access

### Attribute Model

Every node has **attributes** that define its characteristics:

| Attribute | Applies To | Description |
|-----------|------------|-------------|
| NodeId | All | Unique identifier of the node |
| NodeClass | All | Class of the node (Object, Variable, etc.) |
| BrowseName | All | Human-readable name |
| DisplayName | All | Display name (localized) |
| Description | All | Description (localized) |
| WriteMask | All | Write permissions |
| UserWriteMask | All | User-specific write permissions |
| IsAbstract | ObjectType, VariableType, MethodType, DataType | Whether type is abstract |
| Symmetric | ReferenceType | Whether reference is symmetric |
| InverseName | ReferenceType | Inverse name of reference |
| ContainsNoLoops | ReferenceType | Whether reference can have loops |
| EventNotifier | View | Whether view can contain events |
| Value | Variable | Value of the variable |
| DataType | Variable | Data type of the variable |
| ValueRank | Variable | Dimensionality of value (-1=any, 0=scalar, 1=1D, etc.) |
| ArrayDimensions | Variable | Dimensions of array value |
| AccessLevel | Variable | Read/write access level |
| UserAccessLevel | Variable | User-specific access level |
| MinimumSamplingInterval | Variable | Minimum sampling interval |
| Historizing | Variable | Whether value is historized |
| Executable | Method | Whether method is executable |
| UserExecutable | Method | User-specific executable permission |
| Length | DataType | Length of data type in bytes |

### Variable Data Types

OPC UA defines a rich set of **built-in data types**:

| DataType | OPC UA Name | Description | Size |
|----------|-------------|-------------|------|
| Boolean | Boolean | True/False | 1 bit |
| SByte | SByte | Signed 8-bit integer | 1 byte |
| Byte | Byte | Unsigned 8-bit integer | 1 byte |
| Int16 | Int16 | Signed 16-bit integer | 2 bytes |
| UInt16 | UInt16 | Unsigned 16-bit integer | 2 bytes |
| Int32 | Int32 | Signed 32-bit integer | 4 bytes |
| UInt32 | UInt32 | Unsigned 32-bit integer | 4 bytes |
| Int64 | Int64 | Signed 64-bit integer | 8 bytes |
| UInt64 | UInt64 | Unsigned 64-bit integer | 8 bytes |
| Float | Float | 32-bit IEEE 754 floating point | 4 bytes |
| Double | Double | 64-bit IEEE 754 floating point | 8 bytes |
| String | String | UTF-8 encoded string | Variable |
| DateTime | DateTime | Timestamp (100ns resolution) | 8 bytes |
| ByteString | ByteString | Sequence of bytes | Variable |
| XmlElement | XmlElement | XML element | Variable |
| NodeId | NodeId | Node identifier | Variable |
| ExpandedNodeId | ExpandedNodeId | Expanded node identifier | Variable |
| StatusCode | StatusCode | Status code | 4 bytes |
| QualifiedName | QualifiedName | Namespace-indexed name | Variable |
| LocalizedText | LocalizedText | Localized text | Variable |

### Custom Data Types

Users can define **custom data types** (Structure, Enumeration, Opaque):

**Structure**:
```
MySensorData (Structure)
  ├─ Timestamp (DateTime)
  ├─ Temperature (Float)
  ├─ Pressure (Float)
  └─ Status (UInt32)
```

**Enumeration**:
```
MotorState (Enumeration)
  ├─ 0: Idle
  ├─ 1: Running
  ├─ 2: Stopped
  └─ 3: Error
```

**Opaque**:
- Binary data with defined byte length
- Used for protocol buffers, custom binary formats

## Security Model

OPC UA has **built-in security** at the protocol level, unlike OPC Classic.

### Security Mechanisms

| Mechanism | Description | Use Case |
|-----------|-------------|----------|
| **Authentication** | Username/Password, X.509 Certificate | User authentication |
| **Authorization** | Role-based access control | User permissions |
| **Encryption** | AES-128, AES-256 | Confidentiality |
| **Integrity** | SHA-1, SHA-256 | Tamper detection |
| **Signing** | RSA, ECDSA | Message signing |
| **Audit** | Security audit logging | Compliance |

### Security Policies

OPC UA defines **security policies** that combine authentication,
encryption, and signing:

| Policy | Security Level | Authentication | Encryption | Signing | Algorithm |
|--------|----------------|--------------|-----------|---------|----------|
| None | None | Anonymous | No | No | - |
| Basic128Rsa15 | Low | Username/Password | No | Yes | RSA-15, SHA-1 |
| Basic256 | Low | Username/Password | No | Yes | RSA-2048, SHA-1 |
| Basic256Sha256 | Medium | Username/Password | No | Yes | RSA-2048, SHA-256 |
| Aes128Sha256RsaOaep | Medium | X.509 Certificate | Yes | Yes | AES-128, SHA-256, RSA-2048 |
| Aes256Sha256RsaPss | High | X.509 Certificate | Yes | Yes | AES-256, SHA-256, RSA-4096 |

### Certificate Management

OPC UA uses **X.509 certificates** for:
- **Application certificates**: Identify applications
- **User certificates**: Identify users (optional)
- **Server certificates**: Identify servers

**Certificate chain**:
```
Root CA Certificate
    └─ Issuer CA Certificate
            └─ Application Certificate
```

**Certificate validation**:
- Check certificate is not expired
- Check certificate is not revoked
- Check certificate is signed by trusted CA
- Check certificate matches expected identity

**Certificate formats**:
- **DER**: Binary format
- **PEM**: Base64-encoded format (most common)

### User Authentication

OPC UA supports multiple authentication methods:

| Method | Description | Security |
|--------|-------------|----------|
| Anonymous | No authentication | None |
| Username/Password | Simple authentication | Low |
| X.509 Certificate | Certificate-based authentication | High |

**Username/Password**:
- Transmitted securely over encrypted channel
- Stored securely on server
- Can be combined with certificate authentication

**X.509 Certificate**:
- Client presents certificate
- Server verifies certificate chain and revocation
- No password required
- Strongest authentication method

## Transport Mechanisms

### OPC UA Binary over TCP (UA TCP)

- **Port**: 4840 (default)
- **Protocol**: UA Binary protocol over TCP
- **Features**: Full OPC UA functionality
- **Use case**: Standard OPC UA communication

**Connection**:
```
Client → OpenSecureChannel (TCP) → Server
Client → CreateSession → Server
```

### OPC UA over HTTPS (UA HTTPS)

- **Port**: 443 (default) or configurable
- **Protocol**: UA Binary protocol over HTTPS
- **Features**: Full OPC UA functionality with web-friendly transport
- **Use case**: Web browsers, firewalls that block non-standard ports

**Advantage**: Works through HTTP proxies and firewalls

### OPC UA over TSN (Time-Sensitive Networking)

- **Protocol**: UA Binary protocol over IEEE 802.1 TSN
- **Features**: Real-time communication, bounded latency, time synchronization
- **Use case**: Industrial automation, motion control, real-time systems

**TSN features**:
- **Time-aware shaping**: Schedule traffic based on time
- **Preemption**: Priority-based traffic preemption
- **Synchronization**: Precision Time Protocol (PTP, IEEE 1588)

### OPC UA PubSub (Publisher-Subscriber)

- **Model**: Publisher-Subscriber (not request-response)
- **Transport**: UDP, Ethernet, MQTT, AMQP, etc.
- **Features**: One-to-many, real-time, efficient for data distribution
- **Use case**: IoT, edge computing, real-time data distribution

**PubSub models**:
- **Publisher**: Publishes data without knowing subscribers
- **Subscriber**: Receives data without knowing publishers
- **Broker**: Optional, for message distribution

**PubSub configuration**:
- **Message Security**: Signing and/or encryption
- **QoS**: Quality of Service settings
- **Transport**: UDP, MQTT, AMQP, etc.

### OPC UA over MQTT

- **Protocol**: OPC UA messages over MQTT
- **Features**: Lightweight, cloud-friendly, works with existing MQTT infrastructure
- **Use case**: Cloud integration, IoT, edge-to-cloud communication

**MQTT topics**:
- **Discovery**: `opcua/discovery/`
- **Messages**: `opcua/msg/{serverId}/`
- **Security**: TLS for encryption, client certificates for authentication

### OPC UA over AMQP

- **Protocol**: OPC UA messages over AMQP (Advanced Message Queuing Protocol)
- **Features**: Message-oriented, reliable, enterprise-grade
- **Use case**: Enterprise integration, financial services

## Address Space Standardization

OPC UA defines **standard information models** for common use cases.

### Companion Specifications

| Specification | Description | Vendor |
|---------------|-------------|--------|
| **OPC UA for Devices (DI)** | Device information model | OPC Foundation |
| **OPC UA for Machinery** | Machinery information model | OPC Foundation |
| **OPC UA for Analytical Instruments** | Lab equipment model | OPC Foundation |
| **OPC UA for CNC Machines** | CNC machine model | OPC Foundation |
| **OPC UA for Robots** | Robot information model | OPC Foundation |
| **OPC UA for AutoID** | Barcode/RFID reader model | AIM (Association for Automatic Identification and Mobility) |
| **OPC UA for Weighing Devices** | Scale information model | OIML (International Organization of Legal Metrology) |
| **OPC UA for Woodworking Machines** | Woodworking machinery model | OPC Foundation + VDMA |
| **OPC UA for Packaging Machines** | Packaging machinery model | OMAC (Organization for Machine Automation and Control) |

### Vendor-Specific Models

Many vendors provide **OPC UA information models** for their devices:

| Vendor | Devices | Information Model |
|--------|---------|-------------------|
| **Siemens** | S7-1200, S7-1500, TIA Portal | Siemens OPC UA Server |
| **Allen-Bradley** | ControlLogix, CompactLogix | Rockwell OPC UA Server |
| **Schneider** | M241, M251, M262 | Schneider OPC UA Server |
| **Beckhoff** | TwinCAT | Beckhoff OPC UA Server |
| **B&R** | Automation Runtime | B&R OPC UA Server |
| **CODESYS** | CODESYS runtime | CODESYS OPC UA Server |
| **PLCopen** | PLCopen-compliant devices | PLCopen OPC UA Server |

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Connection failure | Cannot communicate | Check network, verify endpoint, check firewall |
| Authentication failure | Access denied | Verify credentials, check certificate, verify security policy |
| Browse failure | Cannot discover nodes | Check namespace, verify node exists, check access rights |
| Read failure | Cannot read value | Check node ID, verify data type, check access rights |
| Write failure | Cannot write value | Check node ID, verify data type, check access rights, check write mask |
| Method call failure | Cannot call method | Check method ID, verify input arguments, check access rights |
| Subscription failure | No data updates | Check subscription settings, verify monitored items, check network |
| Timeout | Slow or no response | Increase timeout, check server load, verify network |
| Certificate error | Connection rejected | Verify certificate chain, check revocation, verify identity |
| Security policy mismatch | Connection rejected | Verify security policy on both client and server |
| Memory leak | Server crash | Monitor memory usage, restart server periodically |
| Performance issues | Slow response | Optimize queries, reduce subscription rate, use appropriate data access |

## Best Practices

### Server Configuration

- **Use appropriate security policy**: Match security level to requirements
- **Configure certificates properly**: Use valid certificates, proper CA chain
- **Set reasonable timeouts**: Balance responsiveness and reliability
- **Enable audit logging**: Log security events and access attempts
- **Limit concurrent connections**: Prevent resource exhaustion
- **Use namespace isolation**: Separate different applications into different namespaces
- **Implement proper shutdown**: Clean up sessions and subscriptions on shutdown
- **Monitor server health**: Monitor CPU, memory, connections, errors
- **Regular backups**: Backup address space and configuration

### Client Configuration

- **Use appropriate security policy**: Match server security policy
- **Validate certificates**: Verify server certificate chain and identity
- **Set reasonable timeouts**: Balance responsiveness and reliability
- **Implement retry logic**: Retry failed operations with backoff
- **Cache node information**: Cache Browse results to reduce discovery overhead
- **Use subscriptions efficiently**: Subscribe only to needed data, appropriate rate
- **Handle disconnections**: Detect and reconnect when connection drops
- **Monitor client health**: Monitor connection status, errors, performance

### Information Modeling

- **Use standard models**: Leverage companion specifications when available
- **Model consistently**: Use consistent naming and modeling patterns
- **Document model**: Document address space structure and semantics
- **Use meaningful names**: Use descriptive BrowseNames and DisplayNames
- **Use appropriate data types**: Choose data types that match the data
- **Use type system**: Define types for reuse across instances
- **Validate model**: Use OPC UA tools to validate address space
- **Version model**: Use NamespaceVersion to track model changes

### Performance

- **Use subscriptions**: Prefer subscriptions over polling for dynamic data
- **Batch reads**: Read multiple values in single Read request
- **Use appropriate rate**: Match subscription rate to data change rate
- **Use data access**: Use Read/Write for static data, Subscriptions for dynamic
- **Use views**: Use Views to limit browse scope and improve performance
- **Use indexing**: Use appropriate indexing for large address spaces
- **Monitor performance**: Monitor request/response times, subscription updates

### Security

- **Use appropriate security policy**: Match security level to requirements
- **Use certificates**: Use X.509 certificates for strong authentication
- **Rotate certificates**: Regularly rotate certificates
- **Revoke certificates**: Revoke compromised or unused certificates
- **Use role-based access**: Configure appropriate access levels for different users
- **Enable audit logging**: Log all access attempts and security events
- **Monitor security**: Monitor for unusual access patterns
- **Keep software updated**: Regularly update OPC UA stack for security patches

## Debugging Tips

### OPC UA Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| **UaExpert** | OPC UA client and server | Testing, debugging, browsing |
| **UaCtt** | OPC UA Certification Test Tool | Compliance testing |
| **OPC UA .NET Client** | .NET OPC UA client library | Development, testing |
| **OPC UA .NET Server** | .NET OPC UA server library | Server development |
| **open62541** | Open-source OPC UA stack (C) | Development, testing |
| **python-opcua** | Python OPC UA library | Scripting, testing |
| **Node-OPCUA** | Node.js OPC UA library | Web development, testing |
| **Prosys OPC UA Browser** | Web-based OPC UA browser | Quick testing, exploration |
| **OPC UA Modeler** | Address space modeling tool | Model development |

### Debugging Techniques

- **Check endpoints**: Use GetEndpoints to verify server endpoints
- **Test connection**: Use OpenSecureChannel and CreateSession
- **Browse address space**: Use Browse to explore available nodes
- **Read values**: Use Read to verify data access
- **Write values**: Use Write to test write access
- **Call methods**: Use Call to test method execution
- **Monitor subscriptions**: Use CreateSubscription and CreateMonitoredItems
- **Check certificates**: Verify certificate chain and validity
- **Check security policy**: Verify security policy compatibility
- **Enable logging**: Enable verbose logging on client and server
- **Use Wireshark**: Capture OPC UA TCP traffic (with UA dissector)

### Common Issues

- **Endpoint mismatch**: Client and server have different endpoints
- **Security policy mismatch**: Client and server use different security policies
- **Certificate issues**: Expired, revoked, or invalid certificates
- **Namespace mismatch**: Client looks for nodes in wrong namespace
- **Node ID mismatch**: Client uses wrong Node ID
- **Data type mismatch**: Client expects different data type than server provides
- **Access denied**: Client lacks permissions for operation
- **Subscription rate too high**: Server cannot handle subscription rate
- **Memory issues**: Server running out of memory
- **Network issues**: Firewall, proxy, or connectivity problems

## Implementation Examples

### Python (opcua)

```python
from opcua import Client, ua

# Connect to server
client = Client("opc.tcp://localhost:4840")
client.connect()

# Browse address space
root = client.get_root_node()
print(f"Root node: {root}")

objects = root.get_child(["2:Objects"])
print(f"Objects folder: {objects}")

# Browse recursively
def browse_node(node, indent=0):
    for child in node.get_children():
        print("  " * indent + f"{child}")
        browse_node(child, indent + 1)

browse_node(objects)

# Read a variable
myvar = client.get_node("ns=2;i=12345")
print(f"Value: {myvar.get_value()}")

# Write a variable
myvar.set_value(ua.DataValue(ua.Variant(42.0, ua.VariantType.Double)))

# Call a method
method = client.get_node("ns=2;i=67890")
result = method.call([ua.Variant(10, ua.VariantType.Int32)])
print(f"Method result: {result}")

# Subscribe to data changes
def datachange_notification(node, val, data):
    print(f"Node {node} changed: {val}")

sub = client.create_subscription(100, datachange_notification)
myvar.subscribe_datachange(sub)

# Disconnect
client.disconnect()
```

### Node.js (node-opcua)

```javascript
const { OPCUAClient, MessageSecurityMode } = require("node-opcua");

// Create client
const client = OPCUAClient.create({
    endpointMustExist: false,
    securityMode: MessageSecurityMode.NONE,
    securityPolicy: SecurityPolicy.None
});

// Connect to server
client.connect("opc.tcp://localhost:4840", (err) => {
    if (err) {
        console.error("Connection error:", err);
        return;
    }
    
    // Browse address space
    const rootFolder = client.getRootFolder();
    rootFolder.browse((err, references) => {
        if (err) {
            console.error("Browse error:", err);
            return;
        }
        references.forEach(ref => {
            console.log(ref.nodeId.toString(), ref.browseName.toString());
        });
    });
    
    // Read a variable
    const nodeId = "ns=2;i=12345";
    client.readVariableValue(nodeId, (err, dataValue) => {
        if (err) {
            console.error("Read error:", err);
            return;
        }
        console.log("Value:", dataValue.value.value);
    });
    
    // Write a variable
    client.writeSingleNode(
        nodeId,
        new Variant({ dataType: DataType.Double, value: 42.0 }),
        (err, statusCode) => {
            if (err) {
                console.error("Write error:", err);
                return;
            }
            console.log("Write successful:", statusCode);
        }
    );
    
    // Disconnect
    setTimeout(() => {
        client.disconnect((err) => {
            if (err) console.error("Disconnect error:", err);
        });
    }, 10000);
});
```

### C++ (open62541)

```c
#include <open62541/client.h>
#include <open62541/client_config_default.h>

UA_Client *client = UA_Client_new();
UA_ClientConfig_setDefault(UA_Client_getConfig(client));

// Connect to server
UA_StatusCode status = UA_Client_connect(client, "opc.tcp://localhost:4840");
if(status != UA_STATUSCODE_GOOD) {
    UA_Client_delete(client);
    return;
}

// Browse address space
UA_BrowseRequest browseRequest;
UA_BrowseRequest_init(&browseRequest);
browseRequest.requestedMaxReferencesPerNode = 0;
browseRequest.nodesToBrowse = UA_Array_new(1, &UA_TYPES[UA_TYPE_NODEID]);
browseRequest.nodesToBrowse[0] = UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER);

UA_BrowseResponse browseResponse = UA_Client_Service_browse(client, browseRequest);

// Read a variable
UA_NodeId nodeId = UA_NODEID_NUMERIC(2, 12345);
UA_Variant value;
UA_Variant_init(&value);
status = UA_Client_readValueAttribute(client, nodeId, &value);
if(status == UA_STATUSCODE_GOOD && UA_Variant_hasScalarType(&value, &UA_TYPES[UA_TYPE_DOUBLE])) {
    UA_Double val = *(UA_Double *)value.data;
    printf("Value: %f\n", val);
}

// Write a variable
UA_Double newValue = 42.0;
status = UA_Client_writeValueAttribute(client, nodeId, UA_TYPES[UA_TYPE_DOUBLE], &newValue);

// Disconnect
UA_Client_disconnect(client);
UA_Client_delete(client);
```

## Integration Patterns

### Client-Server Architecture

```
OPC UA Client (SCADA/HMI/Application) ↔ OPC UA Server (PLC/Device/Gateway)
```

- **Client**: Connects to server, reads/writes data, calls methods
- **Server**: Hosts address space, provides data, executes methods
- **Communication**: Request-response over TCP or HTTPS

### Gateway Pattern

```
External System ↔ OPC UA Gateway ↔ Field Devices
```

- **Gateway**: Translates between OPC UA and other protocols (Modbus, PROFIBUS, etc.)
- **Functions**: Protocol translation, data concentration, buffering
- **Use cases**: Connect legacy devices to OPC UA, integrate with other systems

### PubSub Architecture

```
Publisher (OPC UA Server) → MQTT Broker → Subscriber (OPC UA Client)
```

- **Publisher**: Publishes data without knowing subscribers
- **Subscriber**: Receives data without knowing publishers
- **Broker**: Distributes messages (optional)
- **Use cases**: IoT, edge-to-cloud, real-time data distribution

### Cloud Integration

```
Edge Device (OPC UA Server) ↔ OPC UA over HTTPS ↔ Cloud (OPC UA Client)
```

- **Edge**: Runs OPC UA server, collects data from local devices
- **Cloud**: Connects via HTTPS, processes and stores data
- **Security**: TLS for encryption, certificates for authentication
- **Use cases**: Remote monitoring, data analytics, predictive maintenance

### Historical Data Access

```
OPC UA Client → Read Historical Data → OPC UA Server → History Database
```

- **History**: Store and retrieve historical data
- **Methods**: ReadRaw, ReadAtTime, ReadModified, ReadAnnotation
- **Storage**: Can be file-based, database, or cloud
- **Use cases**: Trending, auditing, analysis

### Alarms and Conditions

```
Device → Raise Alarm → OPC UA Server → Subscribe to Alarms → OPC UA Client
```

- **Alarms**: Event notifications for abnormal conditions
- **Conditions**: State changes (normal to warning to error)
- **Subscription**: Clients subscribe to alarm notifications
- **Use cases**: Alarm management, event-driven actions

## Companion Specifications Implementation

### OPC UA for Devices (DI)

**Device Information Model**:
```
Server
  └─ Objects
      └─ DeviceSet
          └─ Device_1 (ObjectType: DeviceType)
              ├─ DeviceInformation (FolderType)
              │   ├─ Manufacturer (Property)
              │   ├─ Model (Property)
              │   ├─ SerialNumber (Property)
              │   ├─ HardwareRevision (Property)
              │   └─ SoftwareRevision (Property)
              └─ DeviceStatus (FolderType)
                  ├─ OperationalState (Property)
                  ├─ CommunicationState (Property)
                  └─ FaultState (Property)
```

**DeviceType attributes**:
- **DeviceClass**: Class of device (Controller, Sensor, Actuator, etc.)
- **DeviceHealth**: Health status (Good, Warning, Error)
- **DeviceState**: Operational state (Idle, Running, Stopped, etc.)

### OPC UA for AutoID

**AutoID Information Model**:
```
Server
  └─ Objects
      └─ AutoID
          └─ Scanner_1 (ObjectType: AutoIDScannerType)
              ├─ ScannerInformation
              │   ├─ Manufacturer
              │   ├─ Model
              │   └─ SerialNumber
              ├─ ScannerStatus
              │   ├─ OperationalState
              │   └─ CommunicationState
              └─ LastReadData (Variable)
                  ├─ Data (String)
                  ├─ Timestamp (DateTime)
                  └─ ScannerID (String)
```

**ReaderDeviceType**: Base type for all AutoID readers
**BarcodeReaderType**: Type for barcode readers
**RFIDReaderType**: Type for RFID readers

## Standing Rules

- **The Address Space is the contract** — everything in OPC UA is
  defined in the address space; if it is not modeled, it does not exist.
- **Node IDs are the keys** — Node IDs uniquely identify nodes;
  change a Node ID, break all references.
- **References define the structure** — the graph of nodes and references
  is the information model; design it carefully.
- **Services are the operations** — all interactions are through services;
  there are no back doors.
- **Security is mandatory** — even if None is allowed, use Basic256 or
  better; a server without security is a server at risk.
- **Certificates are the identity** — the certificate identifies the
  application; a certificate without a proper chain is a certificate
  to distrust.
- **Subscriptions are efficient** — for dynamic data, a subscription
  is more efficient than polling; use it when you can.
- **PubSub is for distribution** — when one-to-many matters, PubSub
  is the pattern; when request-response matters, client-server is.
- **The companion specifications are the vocabulary** — use the standard
  models when available; invent your own only when necessary.
- **Namespaces are the boundaries** — use namespaces to separate concerns;
  a single namespace for everything is a namespace that will break.
