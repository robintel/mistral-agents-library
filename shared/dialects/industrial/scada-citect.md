---
type: platform
family: industrial
---

# Citect SCADA

**The industry standard for visualizing and controlling industrial processes**: Citect SCADA
provides **high-performance, real-time visualization and control** for industrial
automation. Known for its **speed, reliability, and scalability**, Citect SCADA
is widely used in manufacturing, utilities, oil & gas, and transportation industries.

## Eras

The era is declared by the **Citect SCADA version** and **architecture changes**.

**Citect 4.x (1990s)**: Early versions for Windows 3.1/95.
- **Platform**: Windows-based
- **Features**: Basic HMI functionality, limited graphics
- **Integration**: DDE, OPC Classic (added later)
- **Graphics**: Basic vector graphics
- **Status**: Discontinued

**Citect 5.x (2000)**: Enhanced features for Windows 2000/XP.
- **Features**: Enhanced graphics, Cicode scripting
- **Integration**: OPC Classic, ODBC, Modbus
- **Performance**: Improved rendering, better performance
- **Status**: Discontinued but still in use

**Citect 6.x (2005)**: Modern architecture.
- **Platform**: Windows XP/7
- **Features**: Advanced graphics, security, web access
- **Integration**: OPC Classic, OPC UA (added in 6.1+), SQL, DNP3
- **Scripting**: Enhanced Cicode, VBScript
- **Status**: Discontinued

**Citect 7.0-7.2 (2010)**: Current generation.
- **Platform**: Windows 7/10/11, Windows Server
- **Features**: Modern graphics, enhanced security, web client
- **Integration**: OPC Classic, OPC UA, SQL, REST, MQTT
- **Scripting**: Cicode, VBScript, JScript
- **Architecture**: 64-bit support, improved performance
- **Status**: Supported

**Citect 7.5+ (2015)**: Latest versions.
- **Platform**: Windows 8.1/10/11, Windows Server 2012/2016/2019/2022
- **Features**: HTML5 support, mobile access, cloud connectivity
- **Integration**: Enhanced OPC UA, MQTT, REST, cloud platforms
- **Security**: Improved security features, TLS/SSL
- **Architecture**: 64-bit, multi-touch support
- **Status**: Current

**Citect SCADA 2018+**: Modern versions with enhanced features.
- **Features**: Continuous improvements, new protocols
- **Platform**: Java-based for some components
- **Cloud**: Enhanced cloud connectivity

## Architecture

### System Components

**Development**:
- **Citect Studio**: Development environment for creating applications.
- **Graphics**: Draw, import, animate graphics.
- **Scripts**: Write Cicode scripts (Citect's proprietary scripting language).
- **Database**: Configure tag database, ODBC connections.
- **Alarms**: Configure alarms, events, actions.
- **Trends**: Configure real-time and historical trends.
- **Reports**: Configure reports, printing.

**Runtime**:
- **Citect Display Client**: Runtime environment for operator interface.
- **Multiple Displays**: Open multiple displays simultaneously.
- **Security**: User authentication, access control.
- **Alarms**: Alarm display, acknowledgment, logging.
- **Trends**: Real-time and historical trend display.
- **Reports**: Report generation, display, printing.

**Server**:
- **Citect Server**: Core server for data acquisition and processing.
- **Alarm Server**: Alarm management, logging, distribution.
- **History Server**: Historical data collection, storage.
- **Report Server**: Report generation, distribution.
- **Communication Server**: OPC, DDE, SQL, custom drivers.

### Distributed Architecture

**Single Station**: Single development/runtime station.
- **Use Case**: Small applications, single machine
- **Components**: Citect Studio + Display Client on same machine

**Client-Server**: Separate development and runtime stations.
- **Use Case**: Medium applications, separate development/runtime
- **Components**: Development station + runtime station(s)

**Distributed System**: Multiple runtime stations with shared data.
- **Use Case**: Large applications, distributed systems
- **Components**: Multiple Display Clients + central servers

**Redundant System**: High-availability with redundant servers.
- **Use Case**: Critical applications, 24/7 operation
- **Components**: Primary + standby servers, automatic failover

### Cluster Architecture

**Citect Cluster**: Multiple servers working together.
- **Use Case**: Large, distributed applications
- **Components**: Multiple Citect Servers, shared database
- **Communication**: Cluster communication via TCP/IP
- **Benefits**: Load balancing, redundancy, scalability

### Web Architecture

**Citect Web Client**: Web-based access to Citect SCADA.
- **Platform**: HTML5, JavaScript
- **Features**: Thin client, browser-based access
- **Use Case**: Remote access, mobile access
- **Requires**: Citect Web Server

**Citect Mobile**: Mobile access to Citect SCADA.
- **Platform**: iOS, Android
- **Features**: Touch-optimized interface
- **Use Case**: Mobile operators, field technicians

## Configuration

### Project Structure

**Project**: Container for all configurations.
- **Pages**: Operator interface screens (displays)
- **Tags**: Tag definitions, addresses, data types
- **Alarms**: Alarm definitions, conditions, actions
- **Trends**: Trend definitions, pens, data sources
- **Reports**: Report definitions, templates, schedules
- **Scripts**: Cicode scripts, event scripts
- **Security**: Users, roles, permissions

**Page**: Operator interface screen.
- **Graphics**: Static and dynamic graphics
- **Symbols**: Reusable graphic elements (Genies)
- **Animations**: Data-driven animations
- **Scripts**: Cicode event handlers
- **Security**: Page-level access control

**Genie**: Reusable graphic element (Citect's term for symbols).
- **Definition**: Graphic + scripts + properties
- **Instances**: Multiple instances of a Genie
- **Parameters**: Genie parameters for customization
- **Library**: Genie library for reuse

**Tag Database**:
- **Tags**: Named data points
- **Tag Types**: Memory, I/O, Calculated, SQL, OPC
- **Data Types**: Bool, Int, Float, String, Date/Time, etc.
- **Address**: PLC address (e.g., N7:0 for Allen-Bradley, DB1.DBW0 for Siemens)
- **Access**: Read-only, read-write, write-only
- **Scaling**: Linear, square root, logarithmic scaling

**Alarm Configuration**:
- **Alarm**: Alarm definition with conditions
- **Priority**: Alarm priority (1-999)
- **Group**: Alarm group
- **Type**: Digital, analog, rate-of-change, deviation, expression
- **Message**: Alarm message (with placeholders)
- **Sound**: Alarm sound
- **Actions**: Script, email, print, SMS, etc.
- **Hysteresis**: Deadband for analog alarms
- **Latched**: Latching alarms that require manual reset

**Trend Configuration**:
- **Trend**: Real-time or historical trend
- **Pen**: Trend pen with tag, color, style
- **Time Range**: Display time range
- **Update Rate**: Data update rate
- **Data Source**: Real-time, historical, calculated
- **Retention**: Historical data retention

**Report Configuration**:
- **Report**: Report definition with template
- **Data Source**: Tags, SQL, custom
- **Schedule**: Cyclic, triggered, on-demand
- **Output**: PDF, Excel, HTML, text, CSV
- **Distribution**: Print, email, FTP, cloud

### Scripting (Cicode)

**Cicode**: Citect's proprietary scripting language (C-like syntax).
- **Event Handlers**: Button click, tag change, window open, alarm trigger, etc.
- **Functions**: Subroutines, functions
- **Variables**: Local, global, system variables
- **Operators**: Arithmetic, logical, bitwise, comparison
- **Control Structures**: if/else, switch/case, for, while, do/while
- **Error Handling**: try/catch (in newer versions), ReturnError()

**Common Cicode Functions**:
- **Tag Access**: TagRead(), TagWrite(), TagExists()
- **Alarm Functions**: AlarmOn(), AlarmOff(), AlarmAck()
- **Page Functions**: PageNew(), PageClose(), PageShow(), PageHide()
- **Genie Functions**: GenieShow(), GenieHide(), GenieMove(), GenieSize()
- **String Functions**: StrCat(), StrLeft(), StrRight(), StrMid(), InStr()
- **Math Functions**: Abs(), Sqrt(), Sin(), Cos(), Tan(), Log(), Exp()
- **Date/Time Functions**: Date(), Time(), DateTime(), DayOfWeek(), DayOfYear()
- **File I/O**: FileOpen(), FileRead(), FileWrite(), FileClose()
- **System Functions**: SysInfo(), SysCommand(), SysBeep()

**Script Types**:
- **Page Scripts**: Page-level scripts
- **Genie Scripts**: Genie-level scripts
- **Tag Scripts**: Tag change scripts
- **Alarm Scripts**: Alarm trigger scripts
- **Global Scripts**: Application-wide scripts
- **Event Scripts**: Event-driven scripts

**System Variables**:
- **@Tag**: Current tag name
- **@Value**: Current tag value
- **@Page**: Current page name
- **@Genie**: Current Genie name
- **@User**: Current user name
- **@Date**: Current date
- **@Time**: Current time
- **@Error**: Last error code
- **@ErrorMsg**: Last error message

### Security

**Users**:
- **Local**: Local user database
- **Windows**: Windows authentication
- **LDAP**: LDAP/Active Directory authentication

**Roles**:
- **Default Roles**: Administrator, Engineer, Operator, Viewer
- **Custom Roles**: User-defined roles
- **Permissions**: Read, Write, Execute, Configure, Admin

**Security Zones**:
- **Project Level**: Project-wide security
- **Page Level**: Page-specific security
- **Tag Level**: Tag-specific security
- **Genie Level**: Genie-specific security
- **Alarm Level**: Alarm-specific security

## Features

### Graphics

**Graphic Elements**:
- **Shapes**: Lines, rectangles, circles, arcs, polygons, etc.
- **Text**: Static text, dynamic text (tag-based)
- **Images**: Bitmap, vector, animated GIF
- **Buttons**: Push buttons, toggle buttons, radio buttons, checkboxes
- **Input Fields**: Text input, numeric input, date/time input
- **Sliders**: Analog value adjustment
- **Gauges**: Analog gauges (circular, linear, etc.)
- **Charts**: Trend charts, bar charts, pie charts, XY plots
- **Tables**: Data tables, alarm lists, tag lists
- **Custom Graphics**: Draw custom shapes, import DXF files

**Animations**:
- **Visibility**: Show/hide based on conditions
- **Position**: Move based on data
- **Size**: Resize based on data
- **Color**: Change color based on data
- **Rotation**: Rotate based on data
- **Blinking**: Blink based on conditions
- **Fill**: Fill level based on data
- **Line**: Line properties based on data
- **Custom Animations**: Create custom animations via scripting

**Genies**:
- **Library**: Genie library for reuse
- **Parameters**: Genie parameters for customization
- **Instances**: Multiple instances of a Genie
- **Inheritance**: Inherit properties from library Genies
- **Custom Genies**: Create custom Genies

**Layers**:
- **Multiple Layers**: Organize graphics in layers
- **Layer Visibility**: Show/hide entire layers
- **Layer Order**: Z-order control

**Templates**:
- **Page Templates**: Reusable page layouts
- **Genie Templates**: Reusable Genie configurations
- **Alarm Templates**: Reusable alarm configurations
- **Trend Templates**: Reusable trend configurations

### Alarming

**Alarm Features**:
- **Multi-State**: Support for multi-state alarms
- **Hysteresis**: Deadband for analog alarms
- **Latched**: Latching alarms that require manual reset
- **Acknowledgment**: Alarm acknowledgment with comments
- **Shelving**: Temporarily suppress alarms
- **Grouping**: Group related alarms
- **Filtering**: Filter alarms by state, priority, group, etc.
- **Statistics**: Alarm statistics and analysis
- **Distribution**: Email, SMS, print, script, voice

**Alarm Types**:
- **Digital**: Boolean alarm (on/off)
- **Analog**: Analog alarm (high/low, high-high/low-low)
- **Rate-of-Change**: Rate-of-change alarm
- **Deviation**: Deviation from setpoint alarm
- **Expression**: Expression-based alarm
- **Custom**: Custom alarm via Cicode

**Alarm States**:
- **Normal**: No alarm
- **Active**: Alarm condition met, not acknowledged
- **Acknowledged**: Alarm acknowledged, not cleared
- **Cleared**: Alarm cleared
- **Acknowledged & Cleared**: Alarm acknowledged and cleared
- **Shelved**: Alarm temporarily suppressed
- **Disabled**: Alarm disabled

**Alarm Views**:
- **Alarm List**: Table of active alarms
- **Alarm Detail**: Detailed alarm information
- **Alarm History**: Historical alarm view
- **Alarm Summary**: Alarm summary and statistics
- **Alarm Trend**: Alarm trend display

### Trending

**Trend Features**:
- **Real-Time**: Real-time trend display
- **Historical**: Historical trend display
- **Multi-Pen**: Multiple pens per trend (up to 16)
- **Zoom/Pan**: Zoom and pan for detailed analysis
- **Cursor**: Cursor for precise value reading
- **Annotations**: Add annotations to trends
- **Export**: Export trend data (CSV, Excel, etc.)
- **Print**: Print trend charts

**Trend Types**:
- **Line**: Line chart
- **Bar**: Bar chart
- **Pie**: Pie chart
- **Scatter**: Scatter plot
- **XY**: XY plot
- **Area**: Area chart
- **Step**: Step chart
- **Digital**: Digital trend

**Data Sources**:
- **Real-Time**: Live data from tags
- **Historical**: Historical data from database
- **Calculated**: Calculated values
- **SQL**: Data from SQL queries

**Pen Types**:
- **Line**: Line pen
- **Bar**: Bar pen
- **Step**: Step pen
- **Scatter**: Scatter pen
- **Area**: Area pen

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

**Report Output**:
- **Print**: Direct printing
- **PDF**: Adobe PDF
- **Excel**: Microsoft Excel
- **HTML**: Web page
- **CSV**: Comma-separated values
- **Text**: Plain text

**Report Distribution**:
- **Print**: Direct printing
- **File**: Save to file
- **Email**: Send via email
- **FTP**: Upload via FTP
- **Web**: Publish to web

## Best Practices

### Application Design
- **Modular Design**: Break application into modular components
- **Reusable Elements**: Use Genies, templates, page templates
- **Consistent Naming**: Use consistent naming conventions
- **Documentation**: Document application structure, pages, tags, alarms
- **Version Control**: Use version control for application files
- **Backup**: Regular backup of application files
- **Testing**: Test thoroughly before deployment

### Page Design
- **User-Centered**: Design for the user, not the developer
- **Consistent Layout**: Use consistent page layouts
- **Intuitive Navigation**: Clear and intuitive navigation
- **Responsive Design**: Design for different screen sizes and resolutions
- **Color Scheme**: Use consistent color scheme (consider color blindness)
- **Accessibility**: Design for accessibility (keyboard navigation, screen readers)

### Graphics Design
- **Layered Approach**: Use layers to organize graphics
- **Genie Usage**: Use Genies for reusable elements
- **Animation**: Use animation for dynamic data, but avoid excessive animation
- **Performance**: Optimize graphics for performance
- **Clarity**: Ensure graphics are clear and understandable
- **Consistency**: Maintain consistent graphic styles
- **Aspect Ratios**: Maintain consistent aspect ratios

### Tagging
- **Meaningful Names**: Use descriptive tag names
- **Hierarchical Tags**: Use naming conventions for hierarchy (Area/Line/Machine/Tag)
- **Tag Groups**: Group related tags
- **Tag Descriptions**: Add descriptions to tags
- **Tag Units**: Specify units for analog tags
- **Tag Access**: Set appropriate access rights
- **Tag Addressing**: Use consistent addressing conventions
- **Tag Scaling**: Use appropriate scaling for analog tags

### Alarming
- **Clear Conditions**: Define clear alarm conditions
- **Meaningful Messages**: Use descriptive alarm messages (include tag name, value, limit)
- **Appropriate Priorities**: Set priorities based on importance and urgency
- **Alarm Groups**: Group related alarms for easier management
- **Alarm Filtering**: Filter alarms for different users and roles
- **Alarm Acknowledgment**: Require acknowledgment for important alarms
- **Alarm Comments**: Require comments for alarm acknowledgment
- **Alarm Hysteresis**: Use hysteresis to prevent alarm fluttering
- **Alarm Latched**: Use latched alarms for conditions that require manual intervention

### Trending
- **Purposeful Trends**: Create only necessary trends
- **Clear Pen Names**: Use descriptive pen names
- **Appropriate Update Rates**: Set update rates based on data volatility
- **Time Ranges**: Set appropriate time ranges (consider operational needs)
- **Data Retention**: Configure historical data retention based on storage and needs
- **Pen Colors**: Use consistent pen colors across the application
- **Trend Scaling**: Use appropriate scaling for trend axes

### Scripting
- **Error Handling**: Always implement error handling (ReturnError(), try/catch)
- **Comments**: Comment complex scripts and logic
- **Reusable Functions**: Create reusable functions and subroutines
- **Avoid Long Scripts**: Break long scripts into smaller functions
- **Test Scripts**: Test scripts thoroughly before deployment
- **Variable Naming**: Use meaningful variable names
- **Avoid Hard-Coded Values**: Use tags or constants instead of hard-coded values
- **Use System Functions**: Leverage built-in Cicode functions

### Security
- **Least Privilege**: Grant minimum necessary permissions
- **Strong Passwords**: Use strong passwords for users
- **Password Policies**: Enforce password policies (expiration, complexity)
- **Audit Logging**: Enable audit logging for user actions and system events
- **Network Security**: Secure the network infrastructure (firewalls, VPNs)
- **Remote Access**: Secure remote access (VPN, encryption)
- **Data Encryption**: Encrypt sensitive data in transit and at rest
- **Regular Audits**: Conduct regular security audits
- **User Training**: Train users on security best practices

### Performance
- **Tag Optimization**: Optimize tag providers and update rates
- **Page Optimization**: Optimize pages for performance (limit complex graphics)
- **Query Optimization**: Optimize SQL queries
- **Cache**: Use caching where appropriate
- **Load Testing**: Test performance under load
- **Monitoring**: Monitor application performance
- **Hardware**: Ensure hardware meets application requirements

## Migration Paths

### Citect 5.x/6.x → Citect 7.x
- New architecture with enhanced features
- Reuse pages, tags, alarms, scripts with adjustments
- Add modern graphics, security, web access
- Benefits: Modern platform, better performance, enhanced features

### Citect 7.0-7.2 → Citect 7.5+
- Enhanced features and performance
- Reuse pages, tags, alarms, scripts with minimal adjustments
- Add HTML5 support, mobile access, cloud connectivity
- Benefits: Improved performance, modern features, better accessibility

### Citect Standalone → Citect Cluster
- Integration with Citect Cluster for distributed architecture
- Reuse pages, tags, alarms, scripts with adjustments
- Add load balancing, redundancy, scalability
- Benefits: High availability, scalability, fault tolerance

## Integration

### PLC Integration

**Allen-Bradley**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity (7.1+)
- **DDE**: Direct DDE connectivity (legacy)
- **Citect Drivers**: Native Citect drivers
- **Optimized**: Optimized tag browsing, data access
- **Protocols**: DF1, Ethernet/IP, ControlNet

**Siemens**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity (7.1+)
- **S7 Protocol**: Via OPC or native driver
- **PROFINET**: Via OPC UA
- **PROFIBUS**: Via native driver or OPC
- **Optimized**: Optimized for Siemens PLCs

**Schneider**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity (7.1+)
- **Modbus TCP**: Via OPC or native driver
- **Uni-Telway**: Via OPC or native driver
- **Fipway**: Via native driver
- **Optimized**: Optimized for Schneider PLCs

**Mitsubishi**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity (7.1+)
- **MC Protocol**: Via OPC or native driver
- **CC-Link**: Via OPC or native driver
- **Optimized**: Optimized for Mitsubishi PLCs

**Other PLCs**: OPC Classic, OPC UA, Modbus TCP, DNP3, IEC 60870-5-101/104, and hundreds of others via native drivers or OPC.

### HMI Integration

**Citect Display Client**: Primary HMI solution (Windows-based).
**Citect Web Client**: Web-based thin client.
**Citect Mobile**: Mobile access (iOS, Android).
**Third-Party HMI**: OPC Classic, OPC UA.
**Custom HMI**: Via Cicode scripting and custom integration.

### MES/ERP Integration

**SAP**: OPC, OPC UA, SQL, web services, custom integration.
**Oracle**: OPC, OPC UA, SQL, web services, custom integration.
**Microsoft Dynamics**: OPC, OPC UA, SQL, web services.
**Other MES/ERP**: OPC, OPC UA, SQL, REST APIs, custom integration.

### Cloud Integration

**AVEVA Cloud**: AVEVA's cloud platform (Citect is part of AVEVA).
- **Features**: Remote monitoring, data storage, analytics
- **Security**: Secure cloud connectivity
- **Scalability**: Scales with your needs

**AWS**:
- **Connection**: OPC UA, MQTT, REST APIs, SQL
- **Services**: IoT Core, Lambda, S3, RDS, EC2, etc.

**Azure**:
- **Connection**: OPC UA, MQTT, REST APIs, SQL
- **Services**: IoT Hub, Functions, Blob Storage, SQL Database, VMs, etc.

**Google Cloud**:
- **Connection**: OPC UA, MQTT, REST APIs
- **Services**: Pub/Sub, Cloud Functions, Cloud Storage, Compute Engine, etc.

### Database Integration

**SQL Server**: Microsoft SQL Server (native support).
**Oracle**: Oracle Database (native support).
**MySQL**: MySQL Database (native support).
**PostgreSQL**: PostgreSQL Database.
**SQLite**: SQLite Database.
**Custom**: Any ODBC-compatible database.
**Citect Historian**: High-performance historical database.

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| OPC connection error | No data | Verify OPC server, check network, test connection, check DCOM settings |
| DDE connection error | No data | Verify DDE server, check configuration, check Windows settings |
| Tag not found | No data | Verify tag name, check address, test connection, check OPC browser |
| Alarm not triggering | Missed alarms | Verify alarm condition, check tag value, test logic, check alarm enable |
| Alarm not clearing | Stuck alarms | Verify alarm clear condition, check hysteresis, test logic, check tag scaling |
| Trend not updating | Static display | Verify tag binding, check data access, test refresh, check trend enable |
| Report not generating | No reports | Verify report configuration, check schedule, test triggers, check data source |
| Page not loading | Blank screen | Verify page configuration, check permissions, test in Citect Studio |
| User cannot login | No access | Verify user configuration, check permissions, test credentials, check license |
| Script error | Functionality failure | Check script syntax, enable error handling, test in Citect Studio, check Cicode |
| Graphics not animating | Static graphics | Verify animation configuration, check tag binding, test in Citect Studio |
| Slow performance | Poor responsiveness | Optimize graphics, reduce tag update rates, check hardware, monitor network |
| Memory leak | Application crash | Monitor memory usage, restart application, check for bugs, update Citect |
| Network congestion | Slow communication | Optimize network, segment traffic, check bandwidth, use QoS, check firewalls |
| License expired | Application shutdown | Check license, contact vendor, renew license |
| Database connection error | Data loss | Verify database configuration, check credentials, test connection, check network |

## Implementation Examples

### Cicode (Tag Access)
```c
// Cicode to read and write tags

// Read a tag
int myTagValue;
myTagValue = TagRead("MyTag");

// Write a tag
TagWrite("MyTag", 1234);

// Read a tag with error handling
int tagValue;
if (TagExists("MyTag")) {
    tagValue = TagRead("MyTag");
    printf("MyTag value: %d", tagValue);
} else {
    ReturnError("Tag not found: MyTag");
}

// Read a tag from a specific PLC
int plcTagValue;
plcTagValue = TagRead("PLC1.MyTag");
printf("PLC1.MyTag value: %d", plcTagValue);

// Write a tag to a specific PLC
TagWrite("PLC1.MyTag", 5678);

// Read a float tag
float floatValue;
floatValue = TagReadFloat("Temperature");
printf("Temperature: %.2f", floatValue);

// Write a float tag
TagWriteFloat("Setpoint", 100.5);

// Read a string tag
char stringValue[256];
TagReadString("Status", stringValue, 256);
printf("Status: %s", stringValue);

// Write a string tag
TagWriteString("Message", "Hello, World!");
```

### Cicode (Alarm Handling)
```c
// Alarm trigger script

// Get alarm information
char alarmName[256], alarmMessage[256];
int alarmPriority;

strcpy(alarmName, @AlarmName);
strcpy(alarmMessage, @AlarmMessage);
alarmPriority = @AlarmPriority;

// Log alarm to file
FILE *file;
file = fopen("C:\\Alarms\\Alarms.log", "a");
if (file != NULL) {
    fprintf(file, "%s, %s, %s, Priority: %d\n", 
            SysTime(), alarmName, alarmMessage, alarmPriority);
    fclose(file);
}

// Send email notification (requires email configuration)
char emailSubject[256], emailBody[512];
sprintf(emailSubject, "Alarm: %s", alarmName);
sprintf(emailBody, "Time: %s\nMessage: %s\nPriority: %d", 
        SysTime(), alarmMessage, alarmPriority);
SysEmail("operator@example.com", emailSubject, emailBody);

// Acknowledge alarm
AlarmAck(alarmName);
```

### Cicode (Button Click Event)
```c
// Button click event handler

// Get the tag value
int currentValue;
currentValue = TagRead("Machine.Status");

// Toggle the value
if (currentValue == 0) {
    TagWrite("Machine.Status", 1);
    TagWrite("Machine.StatusText", "RUN");
    // Change button color to green
    GenieSetBackColor("StartButton", RGB(0, 255, 0));
    GenieSetText("StartButton", "Stop");
} else {
    TagWrite("Machine.Status", 0);
    TagWrite("Machine.StatusText", "STOP");
    // Change button color to red
    GenieSetBackColor("StartButton", RGB(255, 0, 0));
    GenieSetText("StartButton", "Start");
}
```

### Cicode (Trend Configuration)
```c
// Configure a trend at runtime

// Add a pen to a trend
TrendAddPen("MyTrend", "Temperature");

// Configure pen
TrendSetPenTag("MyTrend", "Temperature", "Machine.Temperature");
TrendSetPenColor("MyTrend", "Temperature", RGB(255, 0, 0));
TrendSetPenStyle("MyTrend", "Temperature", 0); // 0 = Solid line
TrendSetPenWidth("MyTrend", "Temperature", 2);

// Set time range (last 24 hours)
TrendSetTimeRange("MyTrend", SysDateTime() - 86400, SysDateTime());

// Set update rate (1 second)
TrendSetUpdateRate("MyTrend", 1000);

// Enable trend
TrendEnable("MyTrend", 1);

// Set Y-axis scale
TrendSetYAxis("MyTrend", 0, 100, 10); // Min, Max, Major Grid

// Set Y-axis title
TrendSetYAxisTitle("MyTrend", "Temperature (C)");
```

### Cicode (Page Navigation)
```c
// Navigate between pages

// Open a new page
PageNew("Overview");

// Close current page
PageClose();

// Show a page
PageShow("Detail");

// Hide a page
PageHide("Detail");

// Navigate to a page (close current, open new)
PageGoto("Overview");

// Check if a page is open
if (PageExists("Detail")) {
    PageShow("Detail");
} else {
    PageNew("Detail");
}
```

## Vendor Ecosystem

**Citect Products**: Citect SCADA, Citect Historian, Citect Reports, Citect Facility, Citect for Windows
**Parent Company**: AVEVA (formerly Schneider Electric)
**PLC Integration**: Allen-Bradley, Siemens, Schneider, Mitsubishi, GE, Honeywell, Emerson, and hundreds of others via OPC, OPC UA, native drivers, and custom protocols
**HMI**: Citect Display Client, Citect Web Client, Citect Mobile
**MES/ERP**: SAP, Oracle, Microsoft Dynamics, and others
**Cloud**: AVEVA Cloud, AWS, Azure, Google Cloud
**Databases**: SQL Server, Oracle, MySQL, PostgreSQL, SQLite, Citect Historian, and any ODBC-compatible database
**Drivers**: OPC Classic, OPC UA, Modbus TCP/RTU, DNP3, IEC 60870-5-101/104, DF1, Ethernet/IP, PROFINET, PROFIBUS, and hundreds of others

## Resources

- **AVEVA Citect SCADA**: [aveva.com/citect-scada](https://www.aveva.com/en/products/citect-scada)
- **Citect SCADA Documentation**: [aveva.com/citect-docs](https://www.aveva.com/en/support/citect-scada-documentation)
- **AVEVA Support**: [aveva.com/support](https://www.aveva.com/en/support)
- **AVEVA University**: [aveva.com/university](https://www.aveva.com/en/services/training)
- **AVEVA Community**: [aveva.com/community](https://www.aveva.com/en/community)
- **OPC UA**: [opcfoundation.org](https://opcfoundation.org)
- **DNP3**: [dnp.org](https://www.dnp.org)
- **IEC 60870-5**: [iec.ch](https://www.iec.ch)

## Standing Rules

- **A page is a window into the process** — each page should present a clear, focused view of a specific aspect of the process; do not overload pages with too much information.
- **A Genie is a reusable component** — Genies enable reuse of graphics and logic; create Genies for common elements to improve consistency and maintainability.
- **A tag is a named reference to data** — tags in Citect are named references to data points; use meaningful names that describe the data and its location.
- **An alarm is a call to action** — every alarm should have a clear cause and a defined action; if an alarm cannot be acted upon, reconsider whether it should be an alarm.
- **Cicode should be simple and focused** — Citect scripts are typically short and focused on specific tasks; avoid complex, monolithic scripts.
- **Error handling is essential** — scripts can fail and crash the application; implement error handling (ReturnError) to ensure the application remains stable.
- **The Citect Studio is for development, Display Client is for runtime** — never use Citect Studio as a runtime client; it is a development tool only.
- **Test in Display Client before deploying** — always test applications in Display Client before deploying to production; Studio and Display Client can behave differently.
- **Use layers to organize graphics** — layers make complex graphics more manageable; use them to separate different types of information and improve performance.
- **Use Genies for consistency** — Genies ensure consistent appearance and behavior; use them for common elements like pumps, valves, motors, tanks.
- **Document your application** — document page purposes, tag definitions, alarm configurations, and script logic; this is essential for maintenance and troubleshooting.
- **Backup your application** — Citect application files (*.prj, *.pg*, *.gen, etc.) contain all your work; back them up regularly and before making changes.
- **Use version control** — store application files in version control; this enables rollback, comparison, and collaboration.
- **Monitor application performance** — complex applications can be slow; monitor performance and optimize as needed (reduce graphics complexity, lower update rates).
- **Limit the number of open pages** — too many open pages can consume significant memory; limit the number or implement page management.
- **Use appropriate update rates** — faster update rates consume more resources and network bandwidth; set appropriate rates for each tag based on data volatility and need.
- **Avoid hard-coded values** — use tags or constants instead of hard-coded values; this makes the application more flexible and maintainable.
- **Use tag groups for organization** — tag groups make tag management easier; use them to organize related tags by area, line, machine, etc.
- **Test alarm conditions thoroughly** — verify that all alarms trigger and clear correctly; do not assume they work without testing, and test hysteresis and latched behavior.
- **Use alarm groups for filtering** — alarm groups enable filtering by user/role; use them to present relevant alarms to different users.
- **Require alarm acknowledgment** — require operators to acknowledge important alarms; do not allow alarms to be ignored or automatically cleared.
- **Use alarm comments for context** — alarm comments provide context for why an alarm was acknowledged or cleared; require comments for important alarms.
- **Monitor alarm statistics** — alarm statistics can reveal patterns and issues; use them for predictive maintenance and system optimization.
- **Use trends for analysis** — trends enable analysis of process data; use them to identify issues, optimize performance, and understand behavior.
- **Optimize trend performance** — trends can be resource-intensive; optimize them by limiting the number of pens, update rates, and time ranges.
- **Use appropriate time ranges** — set time ranges based on the data being analyzed; too short and you miss patterns, too long and the trend becomes cluttered and slow.
- **Test reports thoroughly** — verify that all reports generate correctly with the expected data; do not assume they work without testing, and test with different time ranges and parameters.
- **Use report parameters for flexibility** — report parameters make reports more flexible; use them to customize report content based on user needs.
- **Schedule reports appropriately** — reports can consume significant resources; schedule them during off-peak hours where possible, and consider report complexity.
- **Use security zones for access control** — security zones enable fine-grained access control; use them to limit access to sensitive information and functionality.
- **Test all user roles** — verify that each user role has the appropriate permissions; do not assume roles are configured correctly, and test with actual users.
- **Use Windows authentication for simplicity** — Windows authentication simplifies user management; use it where possible to reduce administrative overhead.
- **Monitor user sessions** — track user logins and logouts; this can help identify issues, security concerns, and usage patterns.
- **Implement session timeouts** — inactive sessions should time out to prevent unauthorized access and free up licenses.
- **Use meaningful tag descriptions** — tag descriptions provide context for the data; use them to make the application more understandable and maintainable.
- **Document script logic** — Cicode scripts can be complex; document their purpose and logic for maintainability and troubleshooting.
- **Use reusable script functions** — reusable functions reduce duplication and improve maintainability; create a library of common Cicode functions.
- **Avoid infinite loops** — infinite loops can crash the application; implement safeguards (counters, timeouts) to prevent them.
- **Use the right data type for the job** — match tag data types to the PLC data types; mismatches can cause scaling errors and unexpected behavior.
- **Validate all inputs** — validate inputs from operators and external systems to ensure they are within expected ranges and formats.
- **Use expressions for calculated values** — expressions can calculate values without scripting; use them for simple calculations to reduce script complexity.
- **Test on different screen resolutions** — applications should work on different screen resolutions; test on various monitor sizes and DPI settings.
- **Use a consistent color scheme** — consistent colors improve usability; define a color palette and use it consistently across the application.
- **Consider color blindness** — use color-blind friendly color schemes; provide alternative indicators (patterns, text) where color is critical.
- **Use Citect Cluster for large applications** — for large, distributed applications, consider using Citect Cluster for load balancing, redundancy, and scalability.
- **Monitor license usage** — Citect uses a license server; monitor license usage to avoid running out of licenses and application shutdowns.
- **Plan for license expiration** — licenses have expiration dates; plan for renewal well in advance to avoid unexpected downtime.
