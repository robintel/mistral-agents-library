---
type: platform
family: industrial
---

# Ignition by Inductive Automation

**The modern, web-based SCADA**: Ignition is a **cross-platform, web-enabled**
SCADA system that runs on any OS. Built on **Java, SQL, and Python**, it
offers **unlimited tags, distributed architecture, and cloud connectivity**
with a **100% web-based** operator interface.

## Eras

The era is declared by the **Ignition version** and **architecture changes**.

**Ignition 7 (2010)**: First stable release.
- **Platform**: Java 6+
- **Architecture**: Single server, Swing-based Gateway
- **Features**: Basic SCADA, OPC connectivity, reporting
- **Database**: H2 (default), MySQL, SQL Server, Oracle
- **Web Interface**: Basic web-based operator interface

**Ignition 7.5 (2012)**: Enhanced features.
- **Platform**: Java 7+
- **Features**: Alarming, scripting (Jython), gateway clustering
- **Database**: Support for PostgreSQL

**Ignition 7.6-7.9 (2013-2017)**: Maturity period.
- **Features**: Enhanced reporting, UDTs, tag browsers
- **Security**: Role-based access control, SSL
- **Performance**: Improved performance and scalability

**Ignition 8.0 (2018)**: Major architectural shift.
- **Platform**: Java 8+
- **Architecture**: Microservices, modular gateway
- **Web Interface**: HTML5-based, fully responsive
- **Features**: Perspective (new visualization framework), Edge devices
- **Database**: MariaDB (default), all major databases

**Ignition 8.1 (2020)**: Perspective improvements.
- **Features**: Enhanced Perspective, better mobile support
- **Performance**: Improved rendering, better performance
- **Cloud**: Better cloud connectivity

**Ignition 2021 (8.1.x)**: Perspective as primary.
- **Features**: Perspective as default visualization
- **Edge**: Enhanced Edge device support
- **Security**: Improved security features

**Ignition 2022+ (8.1+)**: Current versions.
- **Features**: Continuous improvements, new modules
- **Platform**: Java 11+
- **Cloud**: Enhanced cloud connectivity, Cirrus Link

## Architecture

### System Components

**Gateway**: Core server for data acquisition, processing, and serving clients.
- **Runtime**: Java-based runtime engine
- **Database**: SQL database for configuration, tags, alarms, history
- **Communication**: OPC, OPC UA, MQTT, SQL, REST, etc.
- **Web Server**: Embedded Jetty web server
- **Security**: Authentication, authorization, encryption

**Designer**: Development environment (Windows only).
- **Project Management**: Configure projects, tags, alarms, reports
- **Screen Design**: Design Vision and Perspective screens
- **Scripting**: Python (Jython) scripting
- **Testing**: Test screens, scripts, expressions

**Clients**: Operator interfaces.
- **Vision Client**: Windows-based thick client (deprecated in 8.1+)
- **Perspective Client**: Web-based thin client (HTML5)
- **Mobile Client**: Tablet/phone access (Perspective)
- **Designer Client**: Development client (Designer)

### Distributed Architecture

**Single Gateway**: Single server for small applications.
- **Use Case**: Small applications, single machine
- **Components**: Gateway + clients

**Gateway Network**: Multiple gateways with shared data.
- **Use Case**: Medium to large applications, distributed systems
- **Components**: Multiple gateways, shared tags
- **Communication**: Gateway-to-gateway communication via MQTT

**Gateway Clustering**: High-availability with redundant gateways.
- **Use Case**: Critical applications, 24/7 operation
- **Components**: Primary + standby gateways, automatic failover
- **Requires**: Enterprise edition

**Edge Architecture**: Distributed edge devices.
- **Edge Devices**: Ignition Edge (Raspberry Pi, Linux, Windows IoT)
- **Communication**: MQTT to central gateway
- **Use Case**: Distributed systems, IIoT

### Communication Architecture

**OPC Classic**: Standard OPC Data Access (DA).
- **Protocol**: DCOM-based
- **Use**: Legacy systems, Windows-only
- **Module**: OPC-UA Module (also supports OPC Classic)

**OPC UA**: Modern OPC Unified Architecture.
- **Protocol**: TCP/IP, binary or JSON
- **Security**: Username/password, certificates
- **Module**: OPC-UA Module
- **Use**: Modern systems, cross-platform

**MQTT**: Lightweight publish-subscribe protocol.
- **Protocol**: TCP/IP, MQTT v3.1.1
- **Broker**: Embedded or external (Mosquitto, HiveMQ, etc.)
- **Module**: MQTT Engine Module
- **Use**: IoT, edge devices, cloud connectivity

**SQL**: Database connectivity.
- **Databases**: MariaDB (default), MySQL, PostgreSQL, SQL Server, Oracle
- **Module**: Core gateway functionality
- **Use**: Tag storage, alarm logging, reporting

**REST API**: HTTP/HTTPS API.
- **Protocol**: REST/JSON
- **Use**: Web services, cloud integration
- **Access**: Via Python scripts or custom modules

**Custom Modules**: Extend functionality.
- **Python**: Write custom modules in Python
- **Java**: Write custom modules in Java
- **SDK**: Ignition SDK for module development

## Modules

### Core Modules (Included)

**Tag System**: Hierarchical, unlimited tag system.
- **Tag Providers**: OPC, SQL, Memory, Expression
- **Tag Types**: All standard data types + custom
- **UDTs**: User-Defined Types for structured data
- **Tag Browsing**: Browse OPC servers, SQL databases
- **Tag Search**: Full-text search across tags

**Alarm System**: Comprehensive alarming.
- **Alarm Pipelines**: Configure alarm processing
- **Alarm Notifications**: Email, SMS, voice, custom scripts
- **Alarm Journaling**: Historical alarm logging
- **Alarm Shelving**: Temporarily suppress alarms
- **Alarm Escalation**: Escalate unacknowledged alarms

**Reporting**: Flexible reporting system.
- **Report Design**: Drag-and-drop report designer
- **Data Sources**: Tags, SQL, custom
- **Output**: PDF, Excel, Word, HTML, CSV
- **Scheduling**: Scheduled, on-demand, triggered
- **Distribution**: Print, email, FTP, cloud

**Security**: Role-based access control.
- **Users**: Local or LDAP/Active Directory
- **Roles**: Customizable roles with permissions
- **Permissions**: Fine-grained permissions (read, write, execute, configure)
- **Authentication**: Username/password, certificates, OAuth2
- **Audit Logging**: Track user actions and system events

### Optional Modules (Paid)

**Vision**: Legacy visualization module.
- **Screens**: Windows-based thick client screens
- **Components**: Rich component library
- **Scripts**: Jython (Python) scripting
- **Templates**: Reusable screen templates
- **Status**: Deprecated in favor of Perspective (still supported)

**Perspective**: Modern web-based visualization.
- **Screens**: HTML5-based, responsive, web-native
- **Components**: Modern component library
- **Scripts**: JavaScript + Python scripting
- **Templates**: Reusable component templates
- **Mobile**: Built-in mobile support
- **Theming**: Custom themes and styles

**OPC-UA Module**: OPC Classic and OPC UA connectivity.
- **OPC Classic**: DCOM-based OPC DA
- **OPC UA**: Binary and JSON encoding
- **Tag Browsing**: Browse OPC UA servers
- **Security**: Username/password, certificates
- **Performance**: Optimized for high-performance data access

**MQTT Engine Module**: MQTT connectivity.
- **Broker**: Embedded or external
- **Topics**: Publish/subscribe to MQTT topics
- **QoS**: Quality of Service levels 0, 1, 2
- **Retain**: Retained messages
- **Security**: TLS/SSL, username/password

**SFC (Sequential Function Chart)**: IEC 61131-3 SFC.
- **Steps**: Sequential control steps
- **Transitions**: Conditions for step transitions
- **Actions**: Actions performed in steps
- **Integration**: With alarming, tag system

**EAM (Enterprise Administration Module)**: Multi-gateway management.
- **Gateway Management**: Manage multiple gateways from one interface
- **Deployment**: Deploy projects to multiple gateways
- **Monitoring**: Monitor gateway health, status
- **Security**: Centralized user management

**History Module**: Historical data collection.
- **Tag History**: Store historical tag values
- **Alarm History**: Store historical alarm data
- **Report History**: Store historical report data
- **Storage**: SQL database, file-based
- **Aggregation**: Data aggregation for performance

**Circus Link**: Cloud connectivity.
- **Cloud Platform**: Inductive Automation's cloud platform
- **Features**: Remote monitoring, data storage, analytics
- **Security**: Secure cloud connectivity
- **Scalability**: Scales with your needs

**Other Modules**:
- **BACnet**: Building automation protocol
- **DNP3**: SCADA protocol for utilities
- **Modbus**: Modbus TCP/RTU connectivity
- **Allen-Bradley**: Direct Allen-Bradley PLC connectivity
- **Siemens**: Direct Siemens PLC connectivity
- **SQL Bridge**: SQL database connectivity
- **Web Dev**: Web development tools
- **Mobile**: Mobile-specific features

## Configuration

### Project Structure

**Project**: Container for all configurations.
- **Tags**: Tag definitions, providers, UDTs
- **Alarms**: Alarm definitions, pipelines, notifications
- **Reports**: Report definitions, templates, schedules
- **Screens**: Vision and Perspective screens
- **Scripts**: Project scripts, event scripts
- **Security**: Users, roles, permissions
- **Gateways**: Gateway configurations (for Gateway Network)

**Tag System**:
- **Tag**: Named data point with address, data type, access rights
- **Tag Providers**:
  - **OPC**: OPC Classic or OPC UA server
  - **SQL**: SQL database table/column
  - **Memory**: Internal memory tag
  - **Expression**: Calculated from other tags
  - **Python**: Custom tag provider via Python
- **Tag Paths**: Hierarchical paths (Folder/Subfolder/Tag)
- **UDTs**: User-Defined Types for structured data
- **Tag Groups**: Group tags for organization, access control

**Tag Data Types**:
- **Basic**: Bool, Int1-Int8, UInt1-UInt8, Float, Double, String
- **Date/Time**: Date, Time, DateTime
- **Binary**: Byte, Byte[], Int16[], Int32[], Float[]
- **Custom**: User-defined types via UDTs

**Alarm Configuration**:
- **Alarm**: Alarm definition with conditions
- **Pipeline**: Alarm processing pipeline
- **Notification**: Email, SMS, voice, script
- **Journal**: Historical alarm logging
- **Shelving**: Temporarily suppress alarms
- **Escalation**: Escalate unacknowledged alarms

**Report Configuration**:
- **Report**: Report definition with templates
- **Data Source**: Tags, SQL, custom
- **Schedule**: Cyclic, triggered, on-demand
- **Output**: PDF, Excel, Word, HTML, CSV
- **Distribution**: Print, email, FTP, cloud

### Screen Design (Perspective)

**View**: Container for screen content.
- **Root View**: Main container
- **Nested Views**: Reusable view components
- **Parameters**: View parameters for customization
- **Theming**: Custom themes, styles

**Components**:
- **Basic**: Labels, text fields, buttons, sliders, switches
- **Containers**: Rectangles, circles, paths, SVGs
- **Charts**: Line, bar, pie, scatter, trend, histogram
- **Data**: Tables, lists, grids, repeaters
- **Layout**: Flexbox, grid, tabs, accordions
- **Forms**: Form inputs, validation, submission
- **Media**: Images, videos, web cams
- **Custom**: Custom components via JavaScript

**Data Binding**:
- **Tag Binding**: Bind to tag values
- **Property Binding**: Bind to component properties
- **Expression Binding**: Bind to expressions
- **Script Binding**: Bind to script functions

**Events**:
- **User Events**: Click, double-click, mouse down/up, etc.
- **System Events**: Startup, shutdown, resize, etc.
- **Custom Events**: User-defined events
- **Event Handlers**: Python or JavaScript

**Scripts**:
- **Project Scripts**: Global scripts
- **View Scripts**: View-specific scripts
- **Event Scripts**: Event-driven scripts
- **Python**: Full Python 2.7 support
- **JavaScript**: Full JavaScript (ES6+) support

### Security Configuration

**Users**:
- **Local**: Local user database
- **LDAP**: LDAP/Active Directory authentication
- **OAuth2**: OAuth2 authentication (via custom module)
- **SAML**: SAML authentication (via custom module)

**Roles**:
- **Default Roles**: Admin, Designer, User, Anonymous
- **Custom Roles**: User-defined roles
- **Permissions**: Read, Write, Execute, Configure
- **Inheritance**: Role permission inheritance

**Security Zones**:
- **Project Level**: Project-wide security
- **Screen Level**: Screen-specific security
- **Tag Level**: Tag-specific security
- **Component Level**: Component-specific security

## Features

### Visualization

**Perspective Features**:
- **Responsive Design**: Automatically adapts to screen size
- **Touch Support**: Full touch support for mobile devices
- **Animation**: CSS animations, property animations
- **Transforms**: Translate, rotate, scale, skew
- **Theming**: Custom themes, color schemes, fonts
- **Internationalization**: Multi-language support
- **Accessibility**: WCAG 2.1 compliant, screen reader support

**Component Library**:
- **Basic Components**: 50+ built-in components
- **Charts**: 10+ chart types with customization
- **Data Components**: Tables, lists, grids with sorting, filtering, pagination
- **Layout Components**: Flexbox, grid, responsive layouts
- **Form Components**: Input fields, validation, submission
- **Custom Components**: Create reusable custom components

**Templates**:
- **Component Templates**: Reusable component configurations
- **View Templates**: Reusable view layouts
- **Project Templates**: Pre-configured project structures
- **UDT Templates**: Reusable user-defined types

### Alarming

**Alarm Features**:
- **Multi-State**: Support for multi-state alarms
- **Hysteresis**: Deadband for analog alarms
- **Latched**: Latching alarms that require manual reset
- **Acknowledgment**: Alarm acknowledgment with comments
- **Shelving**: Temporarily suppress alarms
- **Escalation**: Escalate unacknowledged alarms
- **Grouping**: Group related alarms
- **Filtering**: Filter alarms by state, priority, group, etc.
- **Statistics**: Alarm statistics and analysis

**Alarm States**:
- **Normal**: No alarm
- **Active**: Alarm condition met, not acknowledged
- **Acknowledged**: Alarm acknowledged, not cleared
- **Cleared**: Alarm cleared
- **Acknowledged & Cleared**: Alarm acknowledged and cleared
- **Shelved**: Alarm temporarily suppressed
- **Disabled**: Alarm disabled

**Alarm Actions**:
- **Display**: Show in alarm view
- **Sound**: Play alarm sound
- **Flash**: Flash screen component
- **Email**: Send email notification
- **SMS**: Send SMS notification
- **Voice**: Voice call notification
- **Script**: Execute custom script

### Reporting

**Report Features**:
- **Drag-and-Drop Designer**: Intuitive report design
- **Templates**: Pre-defined report templates
- **Data Binding**: Bind to tags, SQL, custom data
- **Expressions**: Calculated values, conditional formatting
- **Grouping**: Data grouping, aggregation
- **Sorting**: Data sorting
- **Filtering**: Data filtering
- **Charts**: Embed charts in reports
- **Images**: Embed images in reports
- **Bar Codes**: Generate bar codes
- **QR Codes**: Generate QR codes

**Report Types**:
- **Tabular**: Table-based reports
- **Form**: Form-based reports
- **Dashboard**: Dashboard-style reports
- **Custom**: Custom layout reports
- **Excel**: Excel-based reports (xlsx)

**Report Output**:
- **PDF**: Adobe PDF
- **Excel**: Microsoft Excel (xlsx)
- **Word**: Microsoft Word (docx)
- **HTML**: Web page
- **CSV**: Comma-separated values
- **Text**: Plain text
- **JSON**: JSON data

### Scripting

**Python Scripting**:
- **Version**: Python 2.7 (Jython)
- **Libraries**: Standard Python libraries + Ignition extensions
- **Ignition Extensions**: system, tag, alarm, report, security, etc.
- **Custom Modules**: Import custom Python modules
- **Error Handling**: try/except for error handling

**JavaScript Scripting**:
- **Version**: ECMAScript 6+
- **Libraries**: Standard JavaScript libraries
- **Ignition Extensions**: perspective, system, etc.
- **Custom Modules**: Import custom JavaScript modules
- **Error Handling**: try/catch for error handling

**Script Types**:
- **Project Scripts**: Global scripts, run at startup
- **View Scripts**: View-specific scripts
- **Event Scripts**: Event-driven scripts
- **Tag Scripts**: Tag change scripts
- **Alarm Scripts**: Alarm trigger scripts
- **Report Scripts**: Report generation scripts

### Data Connectivity

**OPC Connectivity**:
- **OPC Classic**: DCOM-based OPC DA
- **OPC UA**: Binary and JSON encoding
- **Tag Browsing**: Browse OPC servers
- **Data Access**: Read/write OPC tags
- **Historical Data**: OPC HDA support
- **Performance**: Optimized for high-performance

**MQTT Connectivity**:
- **Broker**: Embedded or external MQTT broker
- **Topics**: Publish/subscribe to MQTT topics
- **QoS**: Quality of Service levels 0, 1, 2
- **Retain**: Retained messages
- **Security**: TLS/SSL, username/password
- **Tag Integration**: MQTT tags integrated with tag system

**SQL Connectivity**:
- **Databases**: MariaDB, MySQL, PostgreSQL, SQL Server, Oracle
- **Tag Storage**: Store tags in SQL database
- **Alarm Storage**: Store alarms in SQL database
- **Report Storage**: Store reports in SQL database
- **Custom Queries**: Execute custom SQL queries
- **Stored Procedures**: Execute stored procedures

**REST API Connectivity**:
- **HTTP/HTTPS**: REST/JSON APIs
- **Authentication**: Basic, OAuth2, JWT
- **Methods**: GET, POST, PUT, DELETE, PATCH
- **Custom Headers**: Custom HTTP headers
- **Error Handling**: HTTP error handling

## Best Practices

### Project Design
- **Modular Design**: Break project into modular components
- **Reusable Elements**: Use templates, UDTs, component templates
- **Consistent Naming**: Use consistent naming conventions
- **Documentation**: Document project structure, tags, alarms, reports
- **Version Control**: Use version control for project files
- **Backup**: Regular backup of gateway and database

### Tagging
- **Hierarchical Tags**: Use folder structure for tags (Machine/Pump/Status)
- **Meaningful Names**: Use descriptive tag names
- **UDTs**: Use User-Defined Types for structured data
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
- **Alarm Comments**: Require comments for alarm acknowledgment

### Reporting
- **Purposeful Reports**: Generate only necessary reports
- **Clear Layout**: Design reports with clear layout
- **Accurate Data**: Ensure report data is accurate
- **Automated Distribution**: Automate report distribution
- **Scheduled Reports**: Schedule reports appropriately

### Visualization (Perspective)
- **Responsive Design**: Design for different screen sizes
- **Touch-Friendly**: Design for touch interfaces
- **Consistent Layout**: Use consistent screen layouts
- **Intuitive Navigation**: Clear and intuitive navigation
- **Performance**: Optimize screens for performance
- **Accessibility**: Design for accessibility

### Security
- **Least Privilege**: Grant minimum necessary permissions
- **Strong Passwords**: Use strong passwords for users
- **Password Policies**: Enforce password policies
- **Audit Logging**: Enable audit logging
- **Network Security**: Secure the network infrastructure
- **Remote Access**: Secure remote access
- **Data Encryption**: Encrypt sensitive data
- **Regular Audits**: Conduct regular security audits

### Performance
- **Tag Optimization**: Optimize tag providers and update rates
- **Screen Optimization**: Optimize screens for performance
- **Query Optimization**: Optimize SQL queries
- **Cache**: Use caching where appropriate
- **Load Testing**: Test performance under load
- **Monitoring**: Monitor gateway performance

## Migration Paths

### Vision → Perspective
- Web-based architecture
- Reuse tag system, alarms, reports
- Redesign screens for web
- Benefits: Cross-platform, modern architecture, mobile support

### Single Gateway → Gateway Network
- Distributed architecture
- Reuse project configurations
- Add gateway-to-gateway communication
- Benefits: Scalability, distributed systems

### Gateway Network → Gateway Clustering
- High-availability architecture
- Reuse gateway configurations
- Add automatic failover
- Benefits: High availability, redundancy

### Ignition 7 → Ignition 8
- New architecture with microservices
- Reuse project configurations with adjustments
- Add Perspective, Edge support
- Benefits: Modern architecture, better performance

## Integration

### PLC Integration

**Allen-Bradley**:
- **OPC UA**: Direct OPC UA connectivity
- **EtherNet/IP**: Via OPC UA or custom module
- **ControlLogix**: Optimized tag browsing
- **CompactLogix**: Full support

**Siemens**:
- **OPC UA**: Direct OPC UA connectivity
- **S7 Protocol**: Via OPC UA or custom module
- **PROFINET**: Via OPC UA
- **SIMATIC**: Optimized tag browsing

**Schneider**:
- **OPC UA**: Direct OPC UA connectivity
- **Modbus TCP**: Via OPC UA or custom module
- **Uni-Telway**: Via OPC UA or custom module
- **Modicon**: Optimized tag browsing

**Mitsubishi**:
- **OPC UA**: Direct OPC UA connectivity
- **MC Protocol**: Via OPC UA or custom module
- **CC-Link**: Via OPC UA or custom module
- **MELSEC**: Optimized tag browsing

**Other PLCs**: OPC, OPC UA, Modbus TCP.

### HMI Integration

**Ignition Vision**: Windows-based thick client.
**Ignition Perspective**: Web-based thin client.
**Third-Party HMI**: OPC, OPC UA.
**Mobile HMI**: Perspective mobile access.

### MES/ERP Integration

**SAP**: OPC UA, web services, SQL.
**Oracle**: OPC UA, SQL, web services.
**Microsoft Dynamics**: OPC UA, SQL, web services.
**Other MES/ERP**: OPC, OPC UA, SQL, REST APIs.

### Cloud Integration

**Circus Link**: Inductive Automation's cloud platform.
- **Features**: Remote monitoring, data storage, analytics
- **Security**: Secure cloud connectivity
- **Scalability**: Scales with your needs

**AWS**:
- **Connection**: MQTT, REST APIs, SQL
- **Services**: IoT Core, Lambda, S3, RDS, etc.

**Azure**:
- **Connection**: MQTT, REST APIs, SQL
- **Services**: IoT Hub, Functions, Blob Storage, SQL Database, etc.

**Google Cloud**:
- **Connection**: MQTT, REST APIs
- **Services**: Pub/Sub, Cloud Functions, Cloud Storage, etc.

### Database Integration

**MariaDB**: Default database (free, included).
**MySQL**: Popular open-source database.
**PostgreSQL**: Advanced open-source database.
**SQL Server**: Microsoft SQL Server.
**Oracle**: Oracle Database.
**Custom**: Any JDBC-compatible database.

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Gateway not starting | No access | Check Java version, database connection, ports, logs |
| Database connection error | Data loss | Verify database configuration, check credentials, test connection |
| OPC connection error | No data | Verify OPC server, check network, test connection, check security |
| Tag not found | No data | Verify tag name, check provider, test connection |
| Alarm not triggering | Missed alarms | Verify alarm condition, check tag value, test logic |
| Report not generating | No reports | Verify report configuration, check schedule, test triggers |
| Screen not loading | Blank screen | Verify screen configuration, check permissions, test in designer |
| User cannot login | No access | Verify user configuration, check permissions, test credentials |
| Slow performance | Poor responsiveness | Optimize tags, screens, queries, check hardware, monitor logs |
| Memory leak | Gateway crash | Monitor memory usage, restart gateway, check for bugs, update Java |
| Network congestion | Slow communication | Optimize network, segment traffic, check bandwidth, use QoS |
| Database corruption | Data loss | Regular database backup, use redundancy, check for errors |

## Implementation Examples

### Python (Tag System)
```python
# Project script to create tags
from system.tag import TagManager

# Get tag manager
tagManager = TagManager.getInstance()

# Create a folder
folder = tagManager.getFolder("MyFolder")
if not folder:
    folder = tagManager.addFolder("MyFolder")

# Create a tag in the folder
myTag = tagManager.addTag("MyFolder/MyTag", "INT", "Memory")
myTag.setValue(1234)

# Get tag value
tagPath = "MyFolder/MyTag"
tag = tagManager.getTag(tagPath)
if tag:
    value = tag.getValue()
    print(f"Tag value: {value}")

# Set tag value
tag.setValue(5678)
```

### Python (Alarm System)
```python
# Project script to configure alarms
from system.alarm import AlarmManager

# Get alarm manager
alarmManager = AlarmManager.getInstance()

# Create an alarm
alarmName = "MyAlarm"
alarm = alarmManager.getAlarm(alarmName)
if not alarm:
    alarm = alarmManager.addAlarm(alarmName, "MyFolder/MyTag", ">", 100)
    alarm.setPriority(5)
    alarm.setDisplayPath("Alarms/MyAlarm")
    alarm.setMessage("Temperature too high!")
    alarm.setEnabled(True)

# Add notification
alarm.addNotification("Email", "admin@example.com", "Alarm: {0}")
```

### Python (Reporting)
```python
# Project script to generate a report
from system.report import ReportManager

# Get report manager
reportManager = ReportManager.getInstance()

# Get report
reportName = "MyReport"
report = reportManager.getReport(reportName)
if report:
    # Set report parameters
    report.setParameter("StartDate", "2024-01-01")
    report.setParameter("EndDate", "2024-01-31")
    
    # Generate report
    report.generate()
    
    # Export report
    report.export("C:/Reports/MyReport.pdf", "PDF")
```

### JavaScript (Perspective)
```javascript
// View script in Perspective
// Change color based on tag value
function updateColor() {
    const myTag = perspective.view.getTag("MyFolder/MyTag");
    const value = myTag.value;
    
    if (value > 100) {
        perspective.view.rootContainer.style.backgroundColor = "red";
    } else if (value > 50) {
        perspective.view.rootContainer.style.backgroundColor = "yellow";
    } else {
        perspective.view.rootContainer.style.backgroundColor = "green";
    }
}

// Call on startup and tag change
updateColor();
perspective.view.onTagChange("MyFolder/MyTag", updateColor);
```

### JavaScript (Event Handler)
```javascript
// Button click event handler
function onButtonClick(event) {
    const button = event.source;
    const myTag = perspective.view.getTag("MyFolder/MyTag");
    
    // Increment tag value
    myTag.value = (myTag.value || 0) + 1;
    myTag.write();
    
    // Show confirmation
    perspective.view.showMessage("Value incremented!");
}

// Assign to button
perspective.view.getComponent("MyButton").onClick = onButtonClick;
```

## Vendor Ecosystem

**Ignition Products**: Ignition (Core), Vision, Perspective, OPC-UA Module, MQTT Engine, SFC, EAM, History, Circus Link, Edge
**PLC Integration**: Allen-Bradley, Siemens, Schneider, Mitsubishi, and hundreds of others via OPC, OPC UA, MQTT
**HMI**: Ignition Vision, Ignition Perspective
**MES/ERP**: SAP, Oracle, Microsoft Dynamics, and others
**Cloud**: Circus Link, AWS, Azure, Google Cloud
**Databases**: MariaDB, MySQL, PostgreSQL, SQL Server, Oracle, and others
**Modules**: 100+ third-party modules available

## Resources

- **Inductive Automation**: [inductiveautomation.com](https://www.inductiveautomation.com)
- **Ignition Documentation**: [docs.inductiveautomation.com](https://docs.inductiveautomation.com)
- **Ignition Forum**: [forum.inductiveautomation.com](https://forum.inductiveautomation.com)
- **Ignition University**: [university.inductiveautomation.com](https://university.inductiveautomation.com)
- **Ignition Exchange**: [exchange.inductiveautomation.com](https://exchange.inductiveautomation.com)
- **Circus Link**: [circuslink.com](https://www.circuslink.com)
- **OPC UA**: [opcfoundation.org](https://opcfoundation.org)
- **MQTT**: [mqtt.org](https://mqtt.org)

## Standing Rules

- **A tag is a named value with a path** — tags in Ignition have hierarchical paths (Folder/Subfolder/Tag); use this structure to organize your data.
- **The gateway is the single source of truth** — all data flows through the gateway; clients only connect to the gateway, not directly to devices.
- **A tag without a description is a tag that will be misunderstood** — always add descriptions to tags; future maintainers (including you) will thank you.
- **UDTs are for structure, not for type safety** — User-Defined Types organize related data, but Ignition is dynamically typed; do not rely on UDTs for type safety.
- **Perspective is the future, Vision is the past** — Perspective is the modern, web-based visualization framework; Vision is legacy; design new projects for Perspective.
- **Scripting is Python by default, JavaScript by necessity** — Python (Jython) is the primary scripting language; JavaScript is used for Perspective event handlers; use the right tool for the job.
- **The tag system is hierarchical and unlimited** — tags can be organized in folders and subfolders with no practical limit; use this to create logical, maintainable structures.
- **OPC UA is the preferred protocol** — while OPC Classic works, OPC UA is more secure, platform-independent, and feature-rich; use OPC UA when possible.
- **A gateway network is a distributed system** — multiple gateways can share data via MQTT; use this for distributed systems, but be aware of the networking complexity.
- **Security is role-based and fine-grained** — Ignition has powerful security features; use them to implement least-privilege access control.
- **Alarms should be actionable** — every alarm should have a clear cause and a defined action; if an alarm cannot be acted upon, reconsider whether it should be an alarm.
- **Reports should provide value** — do not generate reports just because you can; every report should serve a purpose.
- **Perspective screens should be responsive** — Perspective automatically adapts to screen size; design with this in mind and test on different devices.
- **The designer is for development, the client is for runtime** — never use the designer as a runtime client; it is a development tool only.
- **Backup your gateway** — the gateway configuration and database contain all your work; back them up regularly.
- **Use version control for projects** — store project files in version control; this enables rollback, comparison, and collaboration.
- **Test in a non-production environment** — test changes in a staging environment before deploying to production.
- **Monitor gateway health** — use the gateway status page to monitor health, performance, and issues.
- **Keep Java updated** — Ignition runs on Java; keep it updated for security and performance.
- **Use the right database for the job** — MariaDB is free and works well for most applications; use SQL Server or Oracle for enterprise applications.
- **Optimize tag update rates** — faster update rates consume more resources; set appropriate rates for each tag.
- **Use tag expressions for calculated values** — tag expressions can calculate values without scripting; use them for simple calculations.
- **Document your alarm pipelines** — alarm pipelines define how alarms are processed; document them for maintainability.
- **Test alarm conditions** — verify that all alarms trigger and clear correctly; do not assume they work without testing.
- **Use alarm shelving for maintenance** — shelving temporarily suppresses alarms during maintenance; use it to prevent alarm flooding.
- **Configure alarm notifications appropriately** — not all alarms need notifications; configure notifications based on importance and urgency.
- **Use alarm groups for organization** — alarm groups make alarm management easier; use them to organize related alarms.
- **Set appropriate alarm priorities** — priorities should reflect the importance of the alarm; do not set all alarms to high priority.
- **Require alarm acknowledgment** — require operators to acknowledge important alarms; do not allow alarms to be ignored.
- **Use alarm comments for context** — alarm comments provide context for why an alarm was acknowledged or cleared; require comments for important alarms.
- **Monitor alarm statistics** — alarm statistics can reveal patterns and issues; use them for predictive maintenance.
- **Use tag history for analysis** — tag history enables trend analysis and predictive maintenance; use it for critical tags.
- **Optimize report schedules** — reports can consume significant resources; schedule them appropriately and avoid overlap.
- **Use report parameters for flexibility** — report parameters make reports more flexible; use them to customize report content.
- **Test report generation** — verify that all reports generate correctly with the expected data.
- **Use Perspective for new projects** — Perspective is the modern, web-based visualization framework; use it for all new projects.
- **Design for touch interfaces** — many Perspective clients are touch-based; design with this in mind.
- **Use components appropriately** — Perspective has a rich component library; use the right component for the job.
- **Optimize screen performance** — complex screens can be slow; optimize for performance.
- **Use theming for consistency** — themes ensure consistent styling across the application; use them to maintain a professional appearance.
- **Test on multiple devices** — Perspective is responsive; test on different screen sizes to ensure it works correctly.
- **Use nested views for reusability** — nested views can be reused across screens; use them to avoid duplication.
- **Pass parameters to views** — view parameters make views more flexible; use them to customize view behavior.
- **Use event handlers for interactivity** — event handlers enable user interaction; use them to create responsive, interactive screens.
- **Handle errors in scripts** — scripts can fail; use try/except (Python) or try/catch (JavaScript) to handle errors gracefully.
- **Use the Ignition SDK for custom modules** — the SDK enables custom module development; use it to extend Ignition's functionality.
- **Contribute to the community** — Ignition has an active community; contribute modules, scripts, and knowledge to help others.
- **Use the Exchange for modules** — the Ignition Exchange has hundreds of free and paid modules; use it to extend Ignition's functionality without custom development.
- **Monitor module performance** — third-party modules can impact performance; monitor their performance and resource usage.
- **Keep modules updated** — module updates often include bug fixes and new features; keep modules updated.
- **Test module compatibility** — not all modules are compatible with all Ignition versions; test compatibility before deploying.
- **Use MQTT for edge devices** — MQTT is lightweight and ideal for edge devices; use it for distributed systems and IoT.
- **Configure MQTT QoS appropriately** — QoS 0 is fire-and-forget, QoS 1 is at-least-once, QoS 2 is exactly-once; choose based on the use case.
- **Use retained messages for configuration** — MQTT retained messages persist across broker restarts; use them for configuration data.
- **Secure MQTT connections** — use TLS/SSL and authentication to secure MQTT connections.
- **Use SQL for historical data** — SQL databases are ideal for historical data storage; use them for tag history, alarm history, and reporting.
- **Optimize SQL queries** — complex queries can be slow; optimize them for performance.
- **Use indexes for performance** — database indexes can significantly improve query performance; use them on frequently queried columns.
- **Monitor database size** — historical data can consume significant storage; monitor database size and implement retention policies.
- **Backup databases regularly** — databases contain all your historical data; back them up regularly.
- **Use REST APIs for integration** — REST APIs enable integration with web services; use them for MES, ERP, and cloud integration.
- **Secure REST API connections** — use HTTPS and authentication to secure REST API connections.
- **Handle API errors gracefully** — APIs can fail; handle errors gracefully to maintain system stability.
- **Cache API responses** — API responses can be cached to improve performance and reduce load on external systems.
- **Monitor API performance** — APIs can be slow; monitor their performance and optimize as needed.
