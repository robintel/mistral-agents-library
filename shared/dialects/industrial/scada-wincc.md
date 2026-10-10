---
type: platform
family: industrial
---

# Siemens WinCC

**The SCADA standard for Siemens automation**: WinCC (Windows Control
Center) provides **powerful visualization, alarming, trending, and reporting**
for industrial applications. From compact **WinCC Basic** to enterprise
**WinCC Unified**, it integrates seamlessly with SIMATIC PLCs and the
**TIA Portal** ecosystem.

## Eras

The era is declared by the **WinCC version** and **architecture**.

**WinCC Classic (1996)**: Original WinCC for Windows NT/2000/XP.
- **Version**: WinCC V5.x, V6.x
- **Platform**: Windows-based
- **Integration**: STEP 7, SIMATIC NET
- **Features**: Basic SCADA functionality
- **Status**: Discontinued but still in use

**WinCC V7 (2008)**: Modernized WinCC with enhanced features.
- **Version**: WinCC V7.0-V7.5
- **Platform**: Windows XP/7/10
- **Integration**: STEP 7 V5.x, TIA Portal
- **Features**: Enhanced visualization, Web Navigator, User Archives
- **Status**: Supported

**WinCC Professional (2013)**: Mid-range SCADA for TIA Portal.
- **Version**: V13-V17
- **Platform**: Windows 7/10/11
- **Integration**: TIA Portal, SIMATIC PLCs
- **Features**: Integrated engineering, WinCC/WinCC Unified compatibility
- **Use Case**: Machine-level to small plant-level applications

**WinCC Advanced (2013)**: High-end SCADA for TIA Portal.
- **Version**: V13-V17
- **Platform**: Windows Server 2012/2016/2019/2022
- **Integration**: TIA Portal, SIMATIC PLCs, PCS 7
- **Features**: Distributed systems, redundancy, high availability
- **Use Case**: Plant-level to enterprise-level applications

**WinCC Unified (2018)**: Web-based, cross-platform SCADA.
- **Version**: V15-V18
- **Platform**: Web-based (HTML5), Windows/Linux
- **Integration**: TIA Portal, WinCC Professional/Advanced, OPC UA
- **Features**: Web clients, mobile access, cloud connectivity
- **Use Case**: Modern, distributed, cross-platform applications

**WinCC OA (Open Architecture) (2000)**: Enterprise SCADA.
- **Version**: 3.18+ (acquired from ETAP)
- **Platform**: Windows/Linux
- **Integration**: OPC, OPC UA, SQL, web services
- **Features**: High scalability, redundancy, distributed architecture
- **Use Case**: Large enterprise applications, utilities, oil & gas

## Architecture

### System Components

**WinCC Server**: Central server for data acquisition, processing, archiving.
- **Runtime**: Core runtime engine
- **Database**: SQL Server for configuration, User Archives, alarms
- **Communication**: OPC, OPC UA, S7, PROFIBUS, PROFINET
- **Web Server**: For WinCC Web Navigator (V7+) and Unified

**WinCC Client**: Operator interface.
- **Runtime**: WinCC Runtime (single user)
- **Client**: WinCC Client (multi-user)
- **Web Client**: Browser-based (Web Navigator, Unified)
- **Mobile Client**: Tablet/phone access (WinCC Unified)

**WinCC Engineering**: Configuration and development.
- **Graphics Designer**: Screen development
- **Alarm Logging**: Alarm configuration
- **Tag Logging**: Tag configuration and archiving
- **Report Designer**: Report configuration
- **User Administrator**: User management

### Distributed Systems

**Single-Station**: Single server with local clients.
- **Use Case**: Small applications, single machine
- **Components**: Server + 1-n clients

**Multi-Station**: Multiple servers with shared data.
- **Use Case**: Medium applications, multiple machines
- **Components**: Multiple servers, shared database

**Distributed System**: Multiple servers with distributed functions.
- **Use Case**: Large applications, distributed architecture
- **Components**: Data servers, archive servers, redundant servers

**Redundant System**: High-availability with redundant servers.
- **Use Case**: Critical applications, 24/7 operation
- **Components**: Primary + standby servers, automatic failover

### Communication Architecture

**OPC Classic**: Standard OPC Data Access (DA).
- **Protocol**: DCOM-based
- **Use**: Legacy systems, Windows-only

**OPC UA**: Modern OPC Unified Architecture.
- **Protocol**: TCP/IP, binary or JSON
- **Security**: Username/password, certificates
- **Use**: Modern systems, cross-platform

**SIMATIC S7 Protocol**: Direct S7 communication.
- **Protocol**: ISO-on-TCP (port 102)
- **Use**: Direct PLC communication

**PROFIBUS/PROFINET**: Direct fieldbus communication.
- **Use**: Distributed IO, drives

## Configuration

### Project Structure

**Project**: Contains all configurations, graphics, archives.
- **Tag Management**: Tag definitions, data types, connections
- **Graphics**: Screens, faceplates, symbols
- **Alarms**: Alarm definitions, groups, priorities
- **Archives**: Tag archives, alarm archives, report archives
- **Reports**: Report definitions, templates
- **Users**: User definitions, roles, permissions

**Tag Management**:
- **Tag**: Named data point with address, data type, access rights
- **Tag Types**:
  - **Internal Tag**: Local to project
  - **External Tag**: Connected to external device (PLC, OPC, etc.)
  - **Calculated Tag**: Calculated from other tags
  - **System Tag**: System information (scan time, status, etc.)
- **Address**: PLC address (e.g., DB1.DBW0 for S7)
- **Data Type**: BOOL, INT, DINT, REAL, STRING, etc.
- **Access Rights**: Read-only, read-write, write-only

**Graphics**:
- **Screen**: Operator interface screen
- **Faceplate**: Reusable control element
- **Symbol**: Reusable graphic element
- **Window**: Pop-up window
- **Trend**: Real-time or historical trend
- **Alarm View**: Alarm display and acknowledgment
- **Report View**: Report display and printing

### Data Archiving

**Tag Archive**: Historical tag data.
- **Cyclic**: Data collected at fixed intervals
- **Triggered**: Data collected on trigger (change, threshold, etc.)
- **Compressed**: Data compressed for long-term storage
- **Storage**: SQL Server database

**Alarm Archive**: Historical alarm data.
- **Cyclic**: All alarms stored
- **Filtered**: Alarms filtered by priority, group, etc.
- **Storage**: SQL Server database

**Report Archive**: Historical report data.
- **Storage**: File system or SQL Server

### Alarming

**Alarm Definition**:
- **Tag**: Associated tag
- **Condition**: Alarm condition (value, range, rate of change, etc.)
- **Priority**: Alarm priority (1-1000, 1=highest)
- **Group**: Alarm group
- **Type**: Analog, digital, system
- **Message**: Alarm message (with placeholders)
- **Help**: Alarm help text

**Alarm States**:
- **Normal**: No alarm
- **Incoming**: Alarm triggered, not acknowledged
- **Acknowledged**: Alarm acknowledged, not cleared
- **Cleared**: Alarm cleared
- **Acknowledged & Cleared**: Alarm acknowledged and cleared

**Alarm Actions**:
- **Display**: Show in alarm view
- **Sound**: Play alarm sound
- **Print**: Print alarm
- **Email**: Send email notification
- **SMS**: Send SMS notification
- **Script**: Execute script

## Features

### Visualization

**Graphics**:
- **Dynamic**: Data-driven graphics
- **Vector**: Scalable vector graphics
- **Animation**: Object animation based on data
- **Scripts**: VBA scripts for complex interactions
- **Faceplates**: Reusable control elements
- **Symbols**: Reusable graphic elements
- **Layers**: Multiple layers for complex graphics
- **Zooming**: Zoom and pan for large graphics

**Controls**:
- **Buttons**: Push buttons, toggle buttons, radio buttons
- **Input Fields**: Text input, numeric input, date/time input
- **Sliders**: Analog value adjustment
- **Dropdowns**: Selection from list
- **Checkboxes**: Boolean selection
- **List Views**: Tabular data display
- **Tree Views**: Hierarchical data display

**Data Binding**:
- **Tag Binding**: Bind controls to tags
- **Expression Binding**: Bind controls to expressions
- **Script Binding**: Bind controls to script functions

### Reporting

**Report Designer**:
- **Templates**: Pre-defined report templates
- **Custom**: Custom report design
- **Data Sources**: Tag data, alarm data, system data
- **Output**: PDF, Excel, Word, HTML

**Report Types**:
- **Cyclic**: Generated at fixed intervals
- **Triggered**: Generated on trigger
- **On Demand**: Generated on user request
- **Shift**: Generated at shift change
- **Daily**: Generated daily
- **Weekly**: Generated weekly
- **Monthly**: Generated monthly

**Report Distribution**:
- **Print**: Direct printing
- **File**: Save to file
- **Email**: Send via email
- **FTP**: Upload via FTP
- **Cloud**: Upload to cloud storage

### User Management

**Users**:
- **Name**: User name
- **Password**: User password
- **Role**: User role (Administrator, Engineer, Operator, etc.)
- **Permissions**: Access permissions (read, write, execute)
- **Login/Logout**: Track user sessions

**Roles**:
- **Administrator**: Full access
- **Engineer**: Configuration access
- **Operator**: Runtime access
- **Viewer**: Read-only access
- **Custom**: User-defined roles

**Authentication**:
- **Local**: Local user database
- **Windows**: Windows authentication
- **LDAP**: LDAP/Active Directory authentication
- **Radius**: Radius authentication

### Security

**Data Security**:
- **Encryption**: Data encryption in transit and at rest
- **Signing**: Digital signatures for data integrity
- **Access Control**: Role-based access control
- **Audit Logging**: Track user actions and system events

**Communication Security**:
- **Firewall**: Protect communication ports
- **VPN**: Secure remote access
- **TLS/SSL**: Encrypt communication
- **Certificates**: X.509 certificates for authentication

**Application Security**:
- **User Permissions**: Fine-grained user permissions
- **Screen Permissions**: Screen-level access control
- **Tag Permissions**: Tag-level access control
- **Script Security**: Script execution permissions

## Engineering Tools

### WinCC Explorer

**Project Management**:
- **Project Tree**: Hierarchical view of project
- **Import/Export**: Import and export project components
- **Compare**: Compare project versions
- **Backup**: Project backup and restore

**Configuration**:
- **Tag Management**: Configure tags and connections
- **Alarm Management**: Configure alarms and groups
- **Archive Management**: Configure archives
- **Report Management**: Configure reports
- **User Management**: Configure users and roles

### Graphics Designer

**Screen Design**:
- **Toolbox**: Graphic elements and controls
- **Property Grid**: Element properties
- **Event Handler**: Event-driven actions
- **Script Editor**: VBA script editor
- **Preview**: Live preview of screens

**Animation**:
- **Visibility**: Show/hide based on conditions
- **Position**: Move based on data
- **Size**: Resize based on data
- **Color**: Change color based on data
- **Rotation**: Rotate based on data
- **Blinking**: Blink based on conditions

### Alarm Logging Configuration

**Alarm Configuration**:
- **Alarm Definition**: Define alarm conditions
- **Alarm Groups**: Group alarms by category
- **Alarm Priorities**: Set alarm priorities
- **Alarm Actions**: Define alarm actions
- **Alarm Filtering**: Filter alarms by conditions

**Alarm Views**:
- **Alarm List**: Table of active alarms
- **Alarm Detail**: Detailed alarm information
- **Alarm History**: Historical alarm view
- **Alarm Statistics**: Alarm statistics and analysis

### Tag Logging Configuration

**Tag Configuration**:
- **Tag Selection**: Select tags to archive
- **Archive Type**: Cyclic, triggered, compressed
- **Archive Interval**: Data collection interval
- **Archive Storage**: Database storage configuration
- **Archive Retention**: Data retention policy

### Report Designer

**Report Design**:
- **Template Selection**: Select report template
- **Data Binding**: Bind report elements to data
- **Layout**: Design report layout
- **Style**: Apply styles to report elements
- **Preview**: Preview report output

## Best Practices

### Project Design
- **Modular Design**: Break project into modular components
- **Reusable Elements**: Use faceplates, symbols, and templates
- **Consistent Naming**: Use consistent naming conventions
- **Documentation**: Document project structure, tags, alarms
- **Version Control**: Use version control for project files
- **Backup**: Regular backup of project files

### Graphics Design
- **User-Centered**: Design for the user, not the developer
- **Consistent Layout**: Use consistent screen layouts
- **Intuitive Navigation**: Clear and intuitive navigation
- **Responsive Design**: Design for different screen sizes
- **Color Scheme**: Use consistent color scheme
- **Accessibility**: Design for accessibility (color blindness, etc.)
- **Performance**: Optimize graphics for performance

### Tagging
- **Meaningful Names**: Use descriptive tag names
- **Hierarchical Tags**: Use hierarchical tag names (Machine.Pump.Status)
- **Tag Groups**: Group related tags
- **Tag Descriptions**: Add descriptions to tags
- **Tag Units**: Specify units for analog tags
- **Tag Access**: Set appropriate access rights

### Alarming
- **Clear Conditions**: Define clear alarm conditions
- **Meaningful Messages**: Use descriptive alarm messages
- **Appropriate Priorities**: Set priorities based on importance
- **Alarm Groups**: Group related alarms
- **Alarm Filtering**: Filter alarms for different users
- **Alarm Acknowledgment**: Require acknowledgment for important alarms

### Archiving
- **Purposeful Archiving**: Archive only necessary data
- **Appropriate Intervals**: Set intervals based on data volatility
- **Compression**: Use compression for long-term storage
- **Retention Policies**: Define clear retention policies
- **Storage Management**: Monitor archive storage usage

### Reporting
- **Purposeful Reports**: Generate only necessary reports
- **Clear Layout**: Design reports with clear layout
- **Accurate Data**: Ensure report data is accurate
- **Automated Distribution**: Automate report distribution
- **Scheduled Reports**: Schedule reports appropriately

### Security
- **Least Privilege**: Grant minimum necessary permissions
- **Strong Passwords**: Use strong passwords for users
- **Password Policies**: Enforce password policies
- **Audit Logging**: Enable audit logging
- **Network Security**: Secure the network infrastructure
- **Remote Access**: Secure remote access
- **Data Encryption**: Encrypt sensitive data
- **Regular Audits**: Conduct regular security audits

## Migration Paths

### WinCC Classic → WinCC V7
- New project structure with enhanced features
- Reuse graphics, alarms, archives with adjustments
- Add Web Navigator, User Archives
- Benefits: Enhanced features, modern platform

### WinCC V7 → WinCC Professional/Advanced
- TIA Portal integration
- Reuse graphics, alarms, archives with adjustments
- Add distributed systems, redundancy
- Benefits: Integrated engineering, high availability

### WinCC Professional → WinCC Unified
- Web-based architecture
- Reuse graphics, alarms, archives with adjustments
- Add web clients, mobile access
- Benefits: Cross-platform, modern architecture

### WinCC V7 → WinCC OA
- Enterprise architecture
- Reuse concepts with significant adjustments
- Add scalability, redundancy
- Benefits: High scalability, distributed architecture

## Integration

### PLC Integration

**SIMATIC S7**: Direct integration via S7 protocol.
- **Connection**: ISO-on-TCP (port 102)
- **Data Access**: Direct tag access
- **Diagnostics**: PLC diagnostics integration

**SIMATIC S7-1200/1500**: TIA Portal integration.
- **Connection**: PROFINET, OPC UA
- **Data Access**: Optimized tag access
- **Diagnostics**: Integrated diagnostics

**Other PLCs**: OPC, OPC UA, Modbus TCP.
- **Allen-Bradley**: OPC, OPC UA, EtherNet/IP
- **Schneider**: OPC, OPC UA, Modbus TCP
- **Mitsubishi**: OPC, OPC UA, MC protocol

### HMI Integration

**SIMATIC WinCC Runtime**: Integrated WinCC runtime.
**Third-Party HMI**: OPC, OPC UA.
**Web HMI**: Web Navigator, WinCC Unified.
**Mobile HMI**: Tablet/phone access.

### MES/ERP Integration

**SIMATIC IT**: Direct integration.
- **Connection**: OPC UA, SQL
- **Data Exchange**: Production data, quality data, alarms

**SAP Integration**:
- **Connection**: OPC UA, web services, IDoc
- **Data Exchange**: Production data, orders, recipes

**Other MES/ERP**: OPC, OPC UA, SQL, REST APIs.

### Cloud Integration

**MindSphere**: Siemens' cloud platform.
- **Connection**: OPC UA, MQTT
- **Data Exchange**: Production data, alarms, analytics

**AWS/Azure**:
- **Connection**: OPC UA, MQTT, REST APIs
- **Data Exchange**: Custom data exchange

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Database connection error | Data loss | Verify SQL Server configuration, check credentials |
| OPC connection error | No data | Verify OPC server, check network, test connection |
| Tag not found | No data | Verify tag name, check address, test connection |
| Alarm not triggering | Missed alarms | Verify alarm condition, check tag value, test logic |
| Archive not working | No historical data | Verify archive configuration, check storage, test connection |
| Report not generating | No reports | Verify report configuration, check schedule, test triggers |
| Graphics not updating | Static display | Verify tag binding, check data access, test refresh |
| User cannot login | No access | Verify user configuration, check permissions, test credentials |
| Slow performance | Poor responsiveness | Optimize graphics, reduce archive intervals, check hardware |
| Memory leak | System crash | Monitor memory usage, restart server, check for bugs |
| Network congestion | Slow communication | Optimize network, segment traffic, check bandwidth |
| Database corruption | Data loss | Regular database backup, use redundancy, check for errors |

## Implementation Examples

### Python (Using OPC UA)
```python
from opcua import Client

# Connect to WinCC OPC UA server
client = Client("opc.tcp://192.168.0.1:4840")
client.connect()

# Browse namespace
root = client.get_root_node()
print("Root node:", root)

# Read tag
myvar = client.get_node("ns=2;s=MyTag")
print("MyTag value:", myvar.get_value())

# Write tag
myvar.set_value(1234)

# Close
client.disconnect()
```

### Node.js (Using node-opcua)
```javascript
const opcua = require("node-opcua");

// Connect to WinCC OPC UA server
const client = opcua.OPCUAClient.create({
    endpoint_must_exist: false
});

client.connect("opc.tcp://192.168.0.1:4840", (err) => {
    if (err) {
        console.error("Error:", err);
        return;
    }

    // Read tag
    const nodeId = opcua.makeNodeId(1234, 2);
    client.readVariableValue(nodeId, (err, dataValue) => {
        if (err) {
            console.error("Error:", err);
        } else {
            console.log("Value:", dataValue.toString());
        }
    });

    // Write tag
    client.writeSingleNode(nodeId, new opcua.Variant({dataType: opcua.DataType.Double, value: 1234.0}), (err) => {
        if (err) console.error("Error:", err);
    });
});
```

### C# (Using OPC UA .NET)
```csharp
using System;
using Opc.Ua.Client;

// Connect to WinCC OPC UA server
var endpoint = CoreClientUtils.SelectEndpoint("opc.tcp://192.168.0.1:4840", false);
var endpointConfiguration = EndpointConfiguration.Create();
var application = new ApplicationInstance
{
    ApplicationName = "MyClient",
    ApplicationType = ApplicationType.Client,
    ApplicationConfiguration = applicationConfiguration
};

var client = new Application(application);
client.Connect(endpoint, false).Wait();

// Read tag
var nodeId = new NodeId(1234, 2);
var dataValue = client.ReadValueAsync(nodeId).Result;
Console.WriteLine($"Value: {dataValue.Value}");

// Write tag
client.WriteValueAsync(nodeId, new DataValue(new Variant(1234))).Wait();

// Disconnect
client.Disconnect().Wait();
```

## Vendor Ecosystem

**WinCC Products**: WinCC Classic, WinCC V7, WinCC Professional, WinCC Advanced, WinCC Unified, WinCC OA
**PLC Integration**: SIMATIC S7, S7-1200, S7-1500, Allen-Bradley, Schneider, Mitsubishi
**HMI**: SIMATIC WinCC Runtime, WinCC Web Navigator, WinCC Unified
**MES/ERP**: SIMATIC IT, SAP, other MES/ERP
**Cloud**: MindSphere, AWS, Azure
**Databases**: SQL Server, Oracle, MySQL

## Resources

- **Siemens WinCC**: [siemens.com/wincc](https://new.siemens.com/global/en/products/automation/industry-software/wincc.html)
- **WinCC Documentation**: [support.industry.siemens.com/wincc](https://support.industry.siemens.com/wincc)
- **TIA Portal**: [siemens.com/tia-portal](https://new.siemens.com/global/en/products/automation/industry-software/automation-systems/tia-portal.html)
- **OPC UA**: [opcfoundation.org](https://opcfoundation.org)
- **SIMATIC IT**: [siemens.com/simatic-it](https://new.siemens.com/global/en/products/automation/industry-software/simatic-it.html)
- **MindSphere**: [mindsphere.io](https://mindsphere.io)

## Standing Rules

- **A tag is a contract between the SCADA and the process** — each tag represents a specific piece of data with a defined meaning; never repurpose tags.
- **The graphics are for the operator, not the engineer** — design graphics that are intuitive and useful for operators; do not design for technical impressiveness.
- **Alarms must be actionable** — every alarm should have a clear cause and a defined action; if an alarm cannot be acted upon, it should not be an alarm.
- **Archives are for analysis, not storage** — archive only data that will be analyzed; do not archive data just to store it.
- **A report without a purpose is a waste of paper** — generate only reports that provide value; do not generate reports just because you can.
- **Security is not optional** — WinCC systems control critical processes; implement security measures appropriate to the risk.
- **The project file is the source of truth** — keep the project file in source control; it contains the entire configuration.
- **Backup before changes** — always backup the project before making changes; a small mistake can cause significant problems.
- **Test changes in a non-production environment** — test changes in a staging environment before deploying to production.
- **Monitor system health** — use diagnostic tools to monitor system health and address issues proactively.
- **Document the configuration** — document tag definitions, alarm configurations, archive settings, and report definitions.
- **Use consistent naming conventions** — use consistent naming for tags, alarms, screens, and other elements; this improves maintainability.
- **Limit the number of alarms** — too many alarms reduce effectiveness; prioritize and filter alarms appropriately.
- **Use alarm groups wisely** — group related alarms to make alarm management easier; do not create too many groups.
- **Set appropriate alarm priorities** — priorities should reflect the importance of the alarm; do not set all alarms to high priority.
- **Require alarm acknowledgment** — require operators to acknowledge important alarms; do not allow alarms to be ignored.
- **Use faceplates for consistency** — faceplates ensure consistent controls across the application; use them for common elements.
- **Test all alarm conditions** — verify that all alarms trigger and clear correctly; do not assume they work without testing.
- **Monitor archive storage** — archives can consume significant storage; monitor usage and implement retention policies.
- **Optimize graphics performance** — complex graphics can slow down the system; optimize for performance.
- **Use layers for complex graphics** — layers make complex graphics more manageable; use them for multi-state displays.
- **Implement user training** — operators need to understand how to use the system; implement training programs.
- **Use audit logging** — audit logging tracks user actions; enable it and review it regularly.
- **Secure remote access** — remote access is a security risk; secure it appropriately.
- **Use redundancy for critical systems** — redundant servers provide high availability; use them for critical applications.
- **Test failover procedures** — if you have redundant systems, test failover regularly to ensure it works correctly.
- **Monitor network performance** — network issues can cause data loss; monitor network performance and address issues.
- **Use appropriate data types** — match tag data types to the PLC data types; mismatches can cause issues.
- **Validate all inputs** — validate inputs from operators and external systems to ensure they are within expected ranges.
- **Use expressions for calculated values** — expressions can calculate values without programming; use them for simple calculations.
- **Document the HMI navigation** — operators need to understand how to navigate the system; document the navigation paths.
- **Use meaningful alarm messages** — alarm messages should clearly describe the problem and the required action.
- **Test all report schedules** — verify that all reports generate at the scheduled times; do not assume they work without testing.
- **Use report parameters** — report parameters make reports more flexible; use them to customize report content.
- **Monitor user sessions** — track user logins and logouts; this can help identify issues and security concerns.
- **Implement session timeouts** — inactive sessions should time out to prevent unauthorized access.
- **Use screen permissions** — limit access to sensitive screens; not all operators need access to all screens.
- **Test all user roles** — verify that each user role has the appropriate permissions; do not assume roles are configured correctly.
- **Use tag groups for organization** — tag groups make tag management easier; use them to organize related tags.
- **Implement data validation** — validate data before writing to tags; this prevents invalid data from causing issues.
- **Use trend analysis** — trends can reveal patterns and issues; use trend analysis for predictive maintenance.
- **Monitor system performance** — track scan times, memory usage, and other performance metrics; address performance issues proactively.
