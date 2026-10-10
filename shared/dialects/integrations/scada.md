---
type: integration
family: industrial
---

# SCADA / HMI Integration Patterns

**Supervisory Control and Data Acquisition and Human-Machine Interface common patterns**:
This contract defines the standard approaches, protocols, and best practices for
integrating industrial devices and protocols with SCADA systems and HMI
interfaces. It serves as a shared reference for all industrial protocol dialects.

## SCADA System Categories

### Commercial SCADA Platforms

**Tier 1 - Enterprise SCADA**:
- **Siemens WinCC / WinCC OA**: Full-featured, high availability, distributed architecture
- **AVEVA System Platform (Wonderware)**: Object-oriented, modular, industry-specific libraries
- **GE Intelligent Platforms iFIX**: Microsoft-centric, OPC-focused, flexible
- **Honeywell Experion**: Process industry focus, integrated control and SCADA
- **Emerson DeltaV**: Process automation, integrated control and SCADA
- **Yokogawa CENTUM VP**: Distributed control, high reliability, advanced graphics

**Tier 2 - Industrial SCADA**:
- **Ignition by Inductive Automation**: Web-based, cross-platform, modern architecture
- **Citect SCADA**: High performance, alarm management, reporting, Cicode scripting
- **Schneider Electric Citect SCADA**: Formerly Citect, now part of EcoStruxure
- **Advanced SCADA (Advantech)**: Industrial-focused, OPC UA native, edge computing
- **Codesys**: PLC-based, integrated development, standard protocols
- **Beijer Electronics**: Flexible, protocol-rich, industrial HMI/SCADA

**Tier 3 - Open Source / Lightweight**:
- **SCADA-LTS**: Open-source, Linux-based, MySQL/PostgreSQL backend
- **FreeSCADA**: Web-based, modular, multiple protocol support
- **OpenSCADA**: Real-time, distributed, cross-platform
- **Node-RED**: Flow-based, IoT-focused, extensible via nodes
- **Grafana**: Visualization-focused, plugin architecture, time-series optimized

**Tier 4 - Cloud-Native SCADA**:
- **Ignition Cloud**: Cloud-hosted Ignition
- **AVEVA Cloud SCADA**: Cloud-based System Platform
- **Siemens MindSphere Visualization**: Cloud-based HMI/SCADA
- **PTC ThingWorx Mashups**: Web-based, drag-and-drop, cloud-native

## Protocol Connectivity Matrix

### Native Protocol Support

| SCADA Platform | OPC UA | OPC DA | Modbus | DNP3 | IEC 61850 | EtherNet/IP | PROFINET | BACnet | Custom Drivers |
|----------------|--------|--------|--------|------|-----------|------------|----------|--------|----------------|
| Siemens WinCC | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| AVEVA System Platform | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ignition | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Citect SCADA | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| GE iFIX | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Honeywell Experion | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |

### Integration Approaches

**Direct Native Driver**:
- **Description**: SCADA platform has built-in driver for the protocol
- **Pros**: Best performance, full feature support, native integration
- **Cons**: Limited to supported protocols, vendor lock-in
- **Use Case**: Standard industrial protocols (Modbus, OPC UA, etc.)
- **Examples**: Siemens WinCC with S7 protocol, Ignition with Modbus TCP

**OPC UA Server/Client**:
- **Description**: Device or gateway provides OPC UA server; SCADA connects as client
- **Pros**: Standard interface, vendor-independent, rich information model
- **Cons**: Additional layer, potential latency, OPC UA server required
- **Use Case**: Modern devices, cross-vendor integration
- **Best Practice**: Use OPC UA whenever available for future-proofing

**OPC DA Server/Client**:
- **Description**: Legacy OPC interface using COM/DCOM
- **Pros**: Widely supported, mature, good performance
- **Cons**: Windows-only, COM dependencies, firewall challenges
- **Use Case**: Legacy systems, Windows-based SCADA
- **Migration Path**: Migrate to OPC UA for cross-platform support

**Protocol Gateway/Converter**:
- **Description**: Dedicated device converts between protocols
- **Pros**: Flexible, supports unsupported protocols, isolated conversion
- **Cons**: Additional hardware cost, single point of failure
- **Use Case**: Proprietary protocols, legacy devices, protocol translation
- **Examples**: Kepware KEPServerEX, Software Toolbox TOP Server

**Custom Driver Development**:
- **Description**: Develop custom driver for SCADA platform
- **Pros**: Tailored to specific needs, full control
- **Cons**: Development cost, maintenance overhead, testing required
- **Use Case**: Unique protocols, specialized requirements
- **Tools**: SCADA platform SDKs, driver development kits

**API-Based Integration**:
- **Description**: Use REST, SOAP, or other APIs for integration
- **Pros**: Modern approach, flexible, platform-independent
- **Cons**: May require custom development, performance overhead
- **Use Case**: Cloud-based systems, custom applications
- **Examples**: REST APIs for cloud SCADA, web services

## Data Access Patterns

### Real-Time Data

**Polling**:
- **Description**: SCADA periodically requests data from devices
- **Interval**: Configurable based on data criticality (100ms to minutes)
- **Pros**: Simple, predictable, easy to implement
- **Cons**: Network overhead, latency, missed updates between polls
- **Optimization**: Use adaptive polling (faster for critical, slower for non-critical)
- **Best Practice**: Match polling rate to data volatility and importance

**Event-Driven**:
- **Description**: Devices push data to SCADA on change or event
- **Types**:
  - **Change of Value (COV)**: Data pushed when value changes beyond deadband
  - **Change of State (COS)**: Data pushed on discrete state changes
  - **Exception Reporting**: Data pushed on alarm/abnormal conditions
- **Pros**: Efficient, low latency, reduced network traffic
- **Cons**: More complex, requires device support
- **Protocol Support**: OPC UA PubSub, MQTT, proprietary push mechanisms
- **Best Practice**: Use for critical data and alarms; combine with polling for backup

**Subscription**:
- **Description**: SCADA subscribes to data changes; device pushes updates
- **Pros**: Efficient, real-time, scalable
- **Cons**: Requires protocol support, state management
- **Protocol Support**: OPC UA subscriptions, MQTT subscriptions
- **Best Practice**: Ideal for high-frequency data; monitor subscription health

### Historical Data

**Data Logging**:
- **Description**: SCADA stores historical data for analysis and reporting
- **Storage Types**:
  - **Time-Series Database**: Optimized for time-stamped process data
  - **Relational Database**: For structured data, events, alarms
  - **File-Based**: CSV, Excel, custom formats
- **Retention**: Configurable based on regulatory and business requirements
- **Compression**: Data compression for efficient storage
- **Aggregation**: Automatic aggregation (min, max, avg, etc.)

**Data Retrieval**:
- **Time Range Queries**: Retrieve data between specific timestamps
- **Aggregation Queries**: Retrieve aggregated data (hourly, daily, etc.)
- **Raw Data**: Retrieve individual data points
- **Export**: Export to various formats (CSV, Excel, PDF)

**Data Visualization**:
- **Trend Charts**: Time-series data visualization
- **XY Plots**: Correlation analysis
- **Bar Charts**: Statistical data
- **Tables**: Tabular data display
- **Dashboards**: Customizable overview displays

### Alarm and Event Data

**Alarm Management**:
- **Alarm Definition**: Configurable alarm conditions (high/low, rate of change, etc.)
- **Alarm States**: Active, Acknowledged, Cleared, Return to Normal
- **Alarm Priorities**: Critical, High, Medium, Low
- **Alarm Groups**: Grouping alarms by area, equipment, or type
- **Alarm Suppression**: Temporarily suppress alarms during maintenance
- **Alarm Escalation**: Escalate unacknowledged alarms

**Event Management**:
- **Event Types**: Operator actions, system events, device events
- **Event Logging**: Timestamped log of all events
- **Event Filtering**: Filter events by type, time, severity
- **Event Correlation**: Correlate related events

## SCADA Platform-Specific Patterns

### Siemens WinCC / WinCC OA

**Architecture**:
- **WinCC**: Windows-based, COM architecture, C++/VB scripting
- **WinCC OA**: Open Architecture, cross-platform, C/C++/Python/Java scripting
- **Redundancy**: Hot standby, warm standby, distributed servers
- **Clients**: Thin clients, web clients, mobile access

**Integration Methods**:
- **SIMATIC S7**: Native integration with Siemens PLCs
- **OPC**: OPC UA, OPC DA support
- **SQL**: Database access via SQL
- **C API**: C API for custom integrations
- **WinCC Scripting**: VBA, C++, Python (WinCC OA)

**Best Practices**:
- Use WinCC OA for new projects (cross-platform, modern)
- Use OPC UA for device integration
- Implement redundancy for critical applications
- Use structured tags for better organization
- Leverage WinCC libraries for common functions

**Common Defects**:
- COM registration issues (WinCC)
- Script errors causing SCADA crashes
- Database connection failures
- Redundancy synchronization issues
- License management problems

### Ignition by Inductive Automation

**Architecture**:
- **Web-Based**: HTML5, JavaScript, responsive design
- **Modular**: Gateway (server) + Designer (development) + clients
- **Cross-Platform**: Windows, Linux, macOS, Docker
- **Scalable**: Single gateway to distributed enterprise

**Integration Methods**:
- **OPC UA**: Native OPC UA client and server
- **MQTT**: Built-in MQTT engine (Sparkplug B support)
- **SQL**: Database connectors (SQL Server, MySQL, PostgreSQL, Oracle)
- **REST API**: RESTful API for custom integrations
- **Python**: Python scripting for custom modules
- **Expression Language**: Tag-based expressions for data manipulation

**Tag System**:
- **Tag Types**: Memory, OPC, SQL, Expression, UDT (User Defined Types)
- **Tag Hierarchy**: Folder structure for organization
- **UDTs**: Reusable tag structures
- **Tag Events**: Event scripts on tag changes
- **Tag History**: Automatic historical data storage

**Best Practices**:
- Use UDTs for consistent device modeling
- Leverage Expression language for data processing
- Use MQTT Sparkplug B for IIoT device integration
- Implement security zones for different user types
- Use Perspective for modern, responsive HMI

**Common Defects**:
- Gateway memory issues (Java heap)
- Tag scan rate too fast causing performance problems
- Database connection pooling issues
- Web browser compatibility issues
- MQTT broker connectivity problems

### AVEVA System Platform (Wonderware)

**Architecture**:
- **Object-Oriented**: Everything is an object with properties and methods
- **Distributed**: Distributed architecture with multiple nodes
- **Modular**: Application server, InTouch HMI, Industrial Application Server
- **Scalable**: From small to enterprise-wide deployments

**Integration Methods**:
- **OPC**: OPC UA, OPC DA, OPC HDA
- **SuiteLink**: Native AVEVA protocol for application communication
- **ODBC**: Database access
- **Web Services**: SOAP and REST APIs
- **DDE**: Dynamic Data Exchange (legacy)

**Object Model**:
- **Templates**: Reusable object templates
- **Instances**: Specific instances of templates
- **Properties**: Data values, alarms, events
- **Methods**: Actions that can be performed on objects
- **Scripts**: VBScript, .NET languages

**Best Practices**:
- Use object templates for consistent modeling
- Leverage SuiteLink for internal application communication
- Use AVEVA's Industrial Application Server for complex logic
- Implement proper security with Windows authentication
- Use InTouch for HMI, System Platform for backend

**Common Defects**:
- COM/DCOM configuration issues
- Object reference errors in scripts
- SuiteLink communication failures
- Database connection timeouts
- License server connectivity issues

### Citect SCADA

**Architecture**:
- **Client-Server**: Multiple clients connecting to a central server
- **High Performance**: Optimized for high-speed data acquisition
- **Alarm Focused**: Advanced alarm management capabilities
- **Reporting**: Built-in reporting and trend analysis

**Integration Methods**:
- **OPC**: OPC UA, OPC DA
- **Cicode**: C-like scripting language for custom logic
- **I/O Devices**: Native I/O device drivers
- **SQL**: Database access for historical data
- **DDE**: Dynamic Data Exchange

**Cicode Scripting**:
- **Functions**: User-defined functions
- **Trends**: Trend collection and analysis
- **Alarms**: Alarm generation and management
- **Reports**: Report generation
- **Genies**: Reusable graphic objects with embedded Cicode

**Best Practices**:
- Use Genies for reusable HMI components
- Leverage Cicode for complex logic and calculations
- Implement proper alarm management with deadbands and filtering
- Use trends for historical data analysis
- Optimize I/O device scanning rates

**Common Defects**:
- Cicode syntax errors causing crashes
- I/O device communication failures
- Trend file corruption
- Alarm flooding due to improper deadbands
- Database connection issues

## HMI Design Patterns

### Visualization Hierarchy

**Level 0 - Overview**:
- **Purpose**: High-level process overview
- **Content**: Process flow diagrams, key metrics, status indicators
- **Users**: Operators, supervisors, managers
- **Update Rate**: Seconds to minutes
- **Navigation**: Drill-down to detailed views

**Level 1 - Process Area**:
- **Purpose**: Area or unit-specific monitoring
- **Content**: Equipment status, process variables, alarms for specific area
- **Users**: Operators, area supervisors
- **Update Rate**: 100ms to seconds
- **Navigation**: Drill-down to equipment details

**Level 2 - Equipment Detail**:
- **Purpose**: Detailed equipment monitoring and control
- **Content**: Individual device parameters, detailed status, control elements
- **Users**: Operators, maintenance technicians
- **Update Rate**: 10-100ms
- **Navigation**: Access to configuration and diagnostics

**Level 3 - Diagnostics**:
- **Purpose**: Troubleshooting and maintenance
- **Content**: Detailed diagnostics, historical data, device health
- **Users**: Maintenance technicians, engineers
- **Update Rate**: As needed, on-demand
- **Navigation**: Access to configuration tools

### Graphic Design Principles

**Clarity**:
- **Prioritize Information**: Most important information most visible
- **Group Related**: Group related data and controls together
- **Consistent Layout**: Use consistent layouts across similar screens
- **Visual Hierarchy**: Use size, color, position to indicate importance

**Usability**:
- **Intuitive Navigation**: Clear path to related information
- **Contextual Help**: Provide help for complex controls
- **Feedback**: Visual feedback for user actions
- **Accessibility**: Color-blind safe, readable fonts, proper contrast

**Performance**:
- **Minimize Animation**: Avoid unnecessary animations
- **Optimize Updates**: Only update changed elements
- **Lazy Loading**: Load detailed data on-demand
- **Caching**: Cache frequently accessed data

**Safety**:
- **Critical Alarms**: Highly visible, unmissable indicators
- **Safe Colors**: Red for danger, green for safe, yellow for warning
- **Interlocks**: Prevent unsafe operations
- **Confirmation**: Confirm critical actions

### Standard Graphic Elements

**Trend Displays**:
- **Time Range**: Configurable historical period
- **Data Points**: Display individual data points or aggregated
- **Cursor**: Interactive cursor for value inspection
- **Zoom**: Zoom in/out for detailed analysis
- **Annotations**: Add notes and markers to trends

**Alarm Displays**:
- **Alarm List**: Sortable, filterable list of active alarms
- **Alarm Details**: Detailed information for selected alarm
- **Alarm History**: Historical alarm data
- **Alarm Trends**: Alarm occurrence over time

**Control Elements**:
- **Buttons**: Momentary, latching, toggle
- **Sliders**: Analog value adjustment
- **Dropdowns**: Discrete value selection
- **Numeric Entry**: Precise value input
- **Check Boxes**: Boolean value toggles

**Status Indicators**:
- **Lamps**: Binary status (on/off)
- **Gauges**: Analog value display (radial, linear)
- **Meters**: Bar graph style indicators
- **Text**: Numeric or textual status display
- **Symbols**: Icon-based status indication

## Security Patterns

### Authentication and Authorization

**User Management**:
- **User Groups**: Operators, Engineers, Administrators, Viewers
- **Permissions**: Read-only, Read/Write, Configuration, Administration
- **Authentication**: Password, Windows authentication, LDAP, Active Directory
- **Session Management**: Session timeout, automatic logout

**Access Control**:
- **Area-Based**: Access limited to specific process areas
- **Function-Based**: Access limited to specific functions (control, monitoring)
- **Time-Based**: Access limited to specific time windows
- **Audit Trail**: Log all user actions for accountability

**Data Security**:
- **Encryption**: Encrypt sensitive data in transit and at rest
- **Integrity**: Ensure data has not been tampered with
- **Confidentiality**: Protect sensitive process information
- **Availability**: Ensure data is available when needed

### Secure Communication

**Network Security**:
- **Firewalls**: Protect SCADA network from external access
- **VLANs**: Segment SCADA traffic from other network traffic
- **VPNs**: Secure remote access
- **DMZ**: Demilitarized zone for external access

**Protocol Security**:
- **TLS/SSL**: Encrypt OPC UA, REST, and web traffic
- **OPC UA Security**: Use appropriate security policies (None, Basic, AES-128, AES-256)
- **Certificate Management**: Properly manage X.509 certificates
- **Key Rotation**: Regularly rotate encryption keys

## Integration Architecture Patterns

### Direct Integration

**Point-to-Point**:
- **Description**: Direct connection between device and SCADA
- **Pros**: Simple, low latency, no intermediate devices
- **Cons**: Limited scalability, no redundancy
- **Use Case**: Small systems, critical devices

**Hub-and-Spoke**:
- **Description**: Central SCADA server with multiple device connections
- **Pros**: Centralized management, scalable
- **Cons**: Single point of failure, potential bottleneck
- **Use Case**: Medium to large systems

### Multi-Tier Integration

**Edge Tier**:
- **Function**: Data collection, filtering, local processing
- **Components**: Edge gateways, protocol converters
- **Location**: Close to devices, in the field
- **Latency**: Milliseconds to seconds

**Aggregation Tier**:
- **Function**: Data aggregation, consolidation, buffering
- **Components**: Aggregation servers, historians
- **Location**: Control room or data center
- **Latency**: Seconds to minutes

**Presentation Tier**:
- **Function**: Data visualization, user interaction
- **Components**: SCADA servers, HMI clients, web portals
- **Location**: Control room, offices, remote access
- **Latency**: As needed by users

### Distributed Integration

**Peer-to-Peer**:
- **Description**: SCADA clients communicate directly with each other
- **Pros**: Decentralized, scalable, no single point of failure
- **Cons**: Complex synchronization, consistency challenges
- **Use Case**: Large distributed systems

**Federated**:
- **Description**: Multiple independent SCADA systems share data
- **Pros**: Autonomous operation, scalable
- **Cons**: Data synchronization complexity
- **Use Case**: Multi-site operations, regional autonomy

### Hybrid Integration

**Cloud-Connected**:
- **Description**: On-premises SCADA with cloud connectivity
- **Components**: Cloud gateway, cloud services
- **Cloud Services**: Data storage, analytics, remote access
- **Connectivity**: Intermittent or continuous
- **Use Case**: Remote monitoring, cloud analytics, disaster recovery

**Edge-to-Cloud**:
- **Description**: Edge devices connect directly to cloud SCADA
- **Components**: Edge devices with cloud connectivity
- **Protocols**: MQTT, REST, WebSockets
- **Use Case**: Remote locations, cloud-native SCADA

## Data Modeling Patterns

### Tag-Based Model

**Tag Definition**:
- **Tag Name**: Unique identifier for the data point
- **Tag Type**: Analog Input, Analog Output, Digital Input, Digital Output
- **Data Type**: Integer, Float, Boolean, String, etc.
- **Engineering Units**: Physical units (degrees, psi, gallons, etc.)
- **Range**: Minimum and maximum values
- **Deadband**: Change threshold for event reporting
- **Scan Rate**: How often the tag is read

**Tag Organization**:
- **Hierarchical**: Tags organized by process area, equipment, function
- **Functional**: Tags organized by control function
- **Custom**: Tags organized by user-defined criteria

**Tag Relationships**:
- **Parent-Child**: Hierarchical relationships between tags
- **Dependencies**: Tags that depend on other tags
- **Calculations**: Tags calculated from other tags
- **Aggregations**: Tags that aggregate multiple source tags

### Object-Based Model

**Object Definition**:
- **Object Type**: Equipment, Process, Area, System
- **Properties**: Data values associated with the object
- **Methods**: Actions that can be performed on the object
- **Events**: Events generated by the object
- **Relationships**: Connections to other objects

**Object Hierarchy**:
- **Site**: Top-level container for a location
- **Area**: Major process area within a site
- **Unit**: Equipment unit or process cell
- **Equipment**: Individual devices or equipment
- **Component**: Sub-components of equipment

**Object Templates**:
- **Reusable**: Create templates for common object types
- **Inheritance**: Objects inherit properties and methods from templates
- **Customization**: Customize individual instances as needed

### Information Model (OPC UA)

**Namespace**:
- **Purpose**: Container for related information
- **Organization**: Organize by vendor, application, or function
- **URI**: Unique identifier for the namespace

**Nodes**:
- **Object Nodes**: Represent objects (equipment, processes, etc.)
- **Variable Nodes**: Represent data values
- **Method Nodes**: Represent callable methods
- **View Nodes**: Represent subsets of the address space
- **Reference Types**: Define relationships between nodes

**Node Attributes**:
- **NodeId**: Unique identifier for the node
- **NodeClass**: Type of node (Object, Variable, Method, etc.)
- **BrowseName**: Human-readable name
- **DisplayName**: Localized display name
- **Description**: Detailed description
- **DataType**: Data type of the node (for variables)
- **Value**: Current value (for variables)

## Common Integration Defects and Mitigations

| Defect | Impact | Detection | Mitigation |
|--------|--------|-----------|------------|
| Communication Failure | No data | Heartbeat monitoring | Check connections, verify device status, test communication |
| Tag Not Found | Missing data | Error logging, validation | Verify tag name, check configuration, test with diagnostic tools |
| Type Mismatch | Incorrect data | Data validation, type checking | Verify data types, check tag definitions, align data models |
| Scan Rate Too Fast | Performance issues | Performance monitoring, CPU usage | Reduce scan rate, implement adaptive scanning |
| Scan Rate Too Slow | Stale data | Data freshness monitoring, user reports | Increase scan rate, implement event-based updates |
| Memory Leak | System instability | Memory monitoring, performance degradation | Restart application, update software, check for known issues |
| Database Connection Failure | Historical data loss | Connection monitoring, error logging | Verify database, check credentials, test connectivity |
| OPC Server Crash | No data access | OPC server monitoring, heartbeat | Restart OPC server, check configuration, verify dependencies |
| Protocol Violation | Communication error | Protocol validation, error codes | Verify protocol compliance, check device firmware, update drivers |
| Time Synchronization | Incorrect timestamps | Time drift monitoring, audit logs | Synchronize clocks, verify NTP configuration, check time sources |
| Alarm Flooding | Operator overload | Alarm rate monitoring, user reports | Implement deadbands, add alarm filtering, configure alarm suppression |
| Redundancy Failure | Single point of failure | Redundancy monitoring, heartbeat | Check redundancy configuration, verify failover, test redundancy |
| Security Violation | Unauthorized access | Security audit, intrusion detection | Review permissions, check authentication, investigate security events |

## Standing Rules

1. **OPC UA First**: When integrating new devices, prefer OPC UA over legacy protocols for future-proofing and cross-platform compatibility.

2. **Security by Design**: Always implement appropriate security measures - authentication, authorization, encryption, and audit logging.

3. **Performance by Design**: Design for performance from the start - appropriate scan rates, efficient data models, optimized graphics.

4. **Maintainability**: Design with maintenance in mind - consistent naming, clear organization, comprehensive documentation.

5. **User-Centric**: Design HMI with the user in mind - intuitive navigation, clear information hierarchy, appropriate alarm management.

6. **Defense in Depth**: Implement multiple layers of security - network, protocol, application, and physical security.

7. **Monitor Everything**: Monitor all critical aspects - communication, data quality, performance, security, and user activity.

8. **Document Everything**: Document all configurations, integrations, changes, and procedures for maintenance and troubleshooting.

9. **Test Thoroughly**: Test all integrations thoroughly - communication, data access, alarm handling, failover scenarios.

10. **Plan for Failure**: Assume failures will happen and design systems that fail safely and recover gracefully.
