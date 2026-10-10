---
type: platform
family: industrial
---

# Wonderware InTouch

**The window into your process**: Wonderware InTouch provides a
**graphically rich, highly configurable** HMI/SCADA solution for
industrial automation. Known for its **powerful graphics, flexibility,
and integration** with the **Wonderware System Platform**, InTouch is
widely used in process industries worldwide.

## Eras

The era is declared by the **InTouch version** and **architecture**.

**InTouch 7.x (1990s)**: Early versions for Windows 3.1/95/NT.
- **Platform**: Windows-based
- **Features**: Basic HMI functionality
- **Integration**: DDE, OPC Classic
- **Graphics**: Basic graphics, limited animation
- **Status**: Discontinued

**InTouch 8.x (2000)**: Enhanced features for Windows 2000/XP.
- **Features**: Enhanced graphics, WindowMaker, WindowViewer
- **Integration**: OPC Classic, ODBC
- **Scripting**: VBScript
- **Status**: Discontinued but still in use

**InTouch 9.x (2005)**: Modern architecture.
- **Platform**: Windows XP/7
- **Features**: Enhanced graphics, security, integration
- **Integration**: OPC Classic, OPC UA, SQL
- **Scripting**: VBScript, JScript
- **Status**: Discontinued

**InTouch 10.x (2010)**: Current generation.
- **Platform**: Windows 7/10/11, Windows Server
- **Features**: Modern graphics, enhanced security, web access
- **Integration**: OPC Classic, OPC UA, SQL, REST
- **Scripting**: VBScript, JScript, Python (via custom)
- **Architecture**: 64-bit support, improved performance
- **Status**: Supported

**InTouch 2014 R2+ (2014)**: Latest version.
- **Platform**: Windows 8.1/10/11, Windows Server 2012/2016/2019/2022
- **Features**: HTML5 support, mobile access, cloud connectivity
- **Integration**: Enhanced OPC UA, MQTT, REST
- **Scripting**: VBScript, JScript, Python
- **Architecture**: 64-bit, multi-touch support
- **Status**: Current

**InTouch for System Platform**: Integrated with Wonderware System Platform.
- **Features**: Seamless integration with System Platform
- **Use Case**: Large, distributed applications

## Architecture

### System Components

**Development**:
- **WindowMaker**: Development environment for creating applications.
- **Graphics**: Draw, import, animate graphics.
- **Scripts**: Write VBScript/JScript scripts.
- **Database**: Configure tag database, ODBC connections.
- **Alarms**: Configure alarms, events, actions.
- **Reports**: Configure reports, printing.

**Runtime**:
- **WindowViewer**: Runtime environment for operator interface.
- **Multiple Windows**: Open multiple windows simultaneously.
- **Security**: User authentication, access control.
- **Alarms**: Alarm display, acknowledgment, logging.
- **Trends**: Real-time and historical trends.
- **Reports**: Report generation, display, printing.

**Server**:
- **Alarm Server**: Alarm management, logging, distribution.
- **History Server**: Historical data collection, storage.
- **Report Server**: Report generation, distribution.
- **Communication Server**: OPC, DDE, SQL, custom drivers.

### Distributed Architecture

**Single Station**: Single development/runtime station.
- **Use Case**: Small applications, single machine
- **Components**: WindowMaker + WindowViewer on same machine

**Client-Server**: Separate development and runtime stations.
- **Use Case**: Medium applications, separate development/runtime
- **Components**: Development station + runtime station(s)

**Distributed System**: Multiple runtime stations with shared data.
- **Use Case**: Large applications, distributed systems
- **Components**: Multiple WindowViewer stations + central servers

**Redundant System**: High-availability with redundant servers.
- **Use Case**: Critical applications, 24/7 operation
- **Components**: Primary + standby servers, automatic failover
- **Requires**: System Platform

### Integration with System Platform

**Wonderware System Platform**: Enterprise SCADA framework.
- **Architecture**: Distributed, scalable, redundant
- **Components**: Application Server, Historian, Alarm Provider, etc.
- **Integration**: InTouch as HMI client
- **Features**: Centralized configuration, distributed data, high availability

**InTouch in System Platform**:
- **Role**: HMI client
- **Connection**: To Application Server
- **Data Access**: Tags, alarms, history from System Platform
- **Benefits**: Centralized management, distributed architecture

## Configuration

### Application Structure

**Application**: Container for all windows, tags, alarms, scripts, etc.

**Window**: Operator interface screen.
- **Graphics**: Static and dynamic graphics
- **Symbols**: Reusable graphic elements
- **Animations**: Data-driven animations
- **Scripts**: VBScript/JScript event handlers
- **Security**: Window-level access control

**Symbol**: Reusable graphic element.
- **Definition**: Graphic + scripts + properties
- **Instances**: Multiple instances of a symbol
- **Parameters**: Symbol parameters for customization
- **Library**: Symbol library for reuse

**Tag Database**:
- **Tags**: Named data points
- **Tag Types**: Memory, I/O, Calculated, SQL, OPC
- **Data Types**: Bool, Int, Float, String, Date/Time, etc.
- **Address**: PLC address (e.g., N7:0 for Allen-Bradley)
- **Access**: Read-only, read-write, write-only

**Alarm Configuration**:
- **Alarm**: Alarm definition with conditions
- **Priority**: Alarm priority (1-1000)
- **Group**: Alarm group
- **Type**: Digital, analog, rate-of-change, deviation
- **Message**: Alarm message (with placeholders)
- **Sound**: Alarm sound
- **Actions**: Script, email, print, etc.

**Trend Configuration**:
- **Trend**: Real-time or historical trend
- **Pen**: Trend pen with tag, color, style
- **Time Range**: Display time range
- **Update Rate**: Data update rate
- **Data Source**: Real-time, historical, calculated

**Report Configuration**:
- **Report**: Report definition with template
- **Data Source**: Tags, SQL, custom
- **Schedule**: Cyclic, triggered, on-demand
- **Output**: PDF, Excel, HTML, text
- **Distribution**: Print, email, FTP

### Scripting

**VBScript**: Primary scripting language (default).
- **Event Handlers**: Button click, tag change, window open, etc.
- **Functions**: Sub procedures, functions
- **Objects**: InTouch objects, ActiveX objects
- **Error Handling**: On Error Resume Next / On Error GoTo

**JScript**: Alternative scripting language.
- **Event Handlers**: Same as VBScript
- **Functions**: JavaScript functions
- **Objects**: Same as VBScript
- **Error Handling**: try/catch

**Python**: Via custom integration (not native).

**Script Types**:
- **Window Scripts**: Window-level scripts
- **Symbol Scripts**: Symbol-level scripts
- **Tag Scripts**: Tag change scripts
- **Alarm Scripts**: Alarm trigger scripts
- **Global Scripts**: Application-wide scripts

**Common Objects**:
- **Application**: Root object for application control
- **Window**: Current window object
- **Symbol**: Current symbol object
- **Tag**: Tag object for data access
- **Alarm**: Alarm object for alarm management
- **Trend**: Trend object for trend control
- **Report**: Report object for report control

### Security

**Users**:
- **Local**: Local user database
- **Windows**: Windows authentication
- **LDAP**: LDAP/Active Directory authentication

**Roles**:
- **Default Roles**: Administrator, Engineer, Operator, Viewer
- **Custom Roles**: User-defined roles
- **Permissions**: Read, Write, Execute, Configure

**Security Zones**:
- **Application Level**: Application-wide security
- **Window Level**: Window-specific security
- **Tag Level**: Tag-specific security
- **Symbol Level**: Symbol-specific security
- **Alarm Level**: Alarm-specific security

## Features

### Graphics

**Graphic Elements**:
- **Shapes**: Lines, rectangles, circles, polygons, etc.
- **Text**: Static text, dynamic text (tag-based)
- **Images**: Bitmap, vector, animated
- **Buttons**: Push buttons, toggle buttons, radio buttons
- **Input Fields**: Text input, numeric input, date/time input
- **Sliders**: Analog value adjustment
- **Gauges**: Analog gauges (circular, linear, etc.)
- **Charts**: Trend charts, bar charts, pie charts
- **Tables**: Data tables, alarm lists, etc.

**Animations**:
- **Visibility**: Show/hide based on conditions
- **Position**: Move based on data
- **Size**: Resize based on data
- **Color**: Change color based on data
- **Rotation**: Rotate based on data
- **Blinking**: Blink based on conditions
- **Fill**: Fill level based on data
- **Line**: Line properties based on data

**Symbols**:
- **Library**: Symbol library for reuse
- **Parameters**: Symbol parameters for customization
- **Instances**: Multiple instances of a symbol
- **Inheritance**: Inherit properties from library symbols

**Layers**:
- **Multiple Layers**: Organize graphics in layers
- **Layer Visibility**: Show/hide entire layers
- **Layer Order**: Z-order control

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
- **Distribution**: Email, SMS, print, script

**Alarm Types**:
- **Digital**: Boolean alarm (on/off)
- **Analog**: Analog alarm (high/low)
- **Rate-of-Change**: Rate-of-change alarm
- **Deviation**: Deviation from setpoint alarm
- **Expression**: Expression-based alarm
- **Custom**: Custom alarm via script

**Alarm Views**:
- **Alarm List**: Table of active alarms
- **Alarm Detail**: Detailed alarm information
- **Alarm History**: Historical alarm view
- **Alarm Summary**: Alarm summary and statistics

### Trending

**Trend Features**:
- **Real-Time**: Real-time trend display
- **Historical**: Historical trend display
- **Multi-Pen**: Multiple pens per trend
- **Zoom/Pan**: Zoom and pan for detailed analysis
- **Cursor**: Cursor for precise value reading
- **Annotations**: Add annotations to trends
- **Export**: Export trend data

**Trend Types**:
- **Line**: Line chart
- **Bar**: Bar chart
- **Pie**: Pie chart
- **Scatter**: Scatter plot
- **Area**: Area chart
- **Step**: Step chart
- **XY**: XY plot

**Data Sources**:
- **Real-Time**: Live data from tags
- **Historical**: Historical data from database
- **Calculated**: Calculated values
- **SQL**: Data from SQL queries

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
- **Text**: Plain text

**Report Distribution**:
- **Print**: Direct printing
- **File**: Save to file
- **Email**: Send via email
- **FTP**: Upload via FTP

## Best Practices

### Application Design
- **Modular Design**: Break application into modular components
- **Reusable Elements**: Use symbols, templates, window templates
- **Consistent Naming**: Use consistent naming conventions
- **Documentation**: Document application structure, windows, tags, alarms
- **Version Control**: Use version control for application files
- **Backup**: Regular backup of application files

### Window Design
- **User-Centered**: Design for the user, not the developer
- **Consistent Layout**: Use consistent window layouts
- **Intuitive Navigation**: Clear and intuitive navigation
- **Responsive Design**: Design for different screen sizes
- **Color Scheme**: Use consistent color scheme
- **Accessibility**: Design for accessibility

### Graphics Design
- **Layered Approach**: Use layers to organize graphics
- **Symbol Usage**: Use symbols for reusable elements
- **Animation**: Use animation for dynamic data
- **Performance**: Optimize graphics for performance
- **Clarity**: Ensure graphics are clear and understandable
- **Consistency**: Maintain consistent graphic styles

### Tagging
- **Meaningful Names**: Use descriptive tag names
- **Hierarchical Tags**: Use naming conventions for hierarchy
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

### Trending
- **Purposeful Trends**: Create only necessary trends
- **Clear Pen Names**: Use descriptive pen names
- **Appropriate Update Rates**: Set update rates based on data volatility
- **Time Ranges**: Set appropriate time ranges
- **Data Retention**: Configure historical data retention

### Scripting
- **Error Handling**: Always implement error handling
- **Comments**: Comment complex scripts
- **Reusable Functions**: Create reusable functions
- **Avoid Long Scripts**: Break long scripts into smaller functions
- **Test Scripts**: Test scripts thoroughly before deployment

### Security
- **Least Privilege**: Grant minimum necessary permissions
- **Strong Passwords**: Use strong passwords for users
- **Password Policies**: Enforce password policies
- **Audit Logging**: Enable audit logging
- **Network Security**: Secure the network infrastructure
- **Remote Access**: Secure remote access

## Migration Paths

### InTouch 7.x/8.x → InTouch 10.x
- New architecture with enhanced features
- Reuse windows, tags, alarms with adjustments
- Add modern graphics, security, integration
- Benefits: Modern platform, better performance, enhanced features

### InTouch 9.x → InTouch 10.x/2014
- Enhanced features and performance
- Reuse windows, tags, alarms with minimal adjustments
- Add HTML5 support, mobile access
- Benefits: Improved performance, modern features

### InTouch Standalone → InTouch for System Platform
- Integration with Wonderware System Platform
- Reuse windows, tags, alarms with adjustments
- Add distributed architecture, central management
- Benefits: Scalability, distributed systems, central management

## Integration

### PLC Integration

**Allen-Bradley**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity
- **DDE**: Direct DDE connectivity (legacy)
- **SuiteLink**: Direct driver connectivity
- **Optimized**: Optimized tag browsing, data access

**Siemens**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity
- **S7 Protocol**: Via OPC or custom driver
- **PROFINET**: Via OPC UA

**Schneider**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity
- **Modbus TCP**: Via OPC or custom driver
- **Uni-Telway**: Via OPC or custom driver

**Mitsubishi**:
- **OPC Classic**: Direct OPC connectivity
- **OPC UA**: Direct OPC UA connectivity
- **MC Protocol**: Via OPC or custom driver
- **CC-Link**: Via OPC or custom driver

**Other PLCs**: OPC Classic, OPC UA, Modbus TCP, DDE.

### HMI Integration

**InTouch as HMI**: Primary HMI solution.
**Third-Party HMI**: OPC Classic, OPC UA.
**Web HMI**: Web-based access (via System Platform).
**Mobile HMI**: Mobile access (via System Platform).

### MES/ERP Integration

**Wonderware MES**: Direct integration with Wonderware System Platform.
**SAP**: OPC, OPC UA, SQL, web services.
**Oracle**: OPC, OPC UA, SQL, web services.
**Other MES/ERP**: OPC, OPC UA, SQL, REST APIs.

### Cloud Integration

**Wonderware Cloud**: Wonderware's cloud platform (via System Platform).
**AWS**: OPC UA, MQTT, REST APIs.
**Azure**: OPC UA, MQTT, REST APIs.
**Google Cloud**: OPC UA, MQTT, REST APIs.

### Database Integration

**SQL Databases**: SQL Server, Oracle, MySQL, PostgreSQL.
**Wonderware Historian**: High-performance historical database.
**Custom Databases**: Any ODBC-compatible database.

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| DDE connection error | No data | Verify DDE server, check configuration |
| OPC connection error | No data | Verify OPC server, check network, test connection |
| Tag not found | No data | Verify tag name, check address, test connection |
| Alarm not triggering | Missed alarms | Verify alarm condition, check tag value, test logic |
| Trend not updating | Static display | Verify tag binding, check data access, test refresh |
| Report not generating | No reports | Verify report configuration, check schedule, test triggers |
| Window not loading | Blank screen | Verify window configuration, check permissions, test in WindowMaker |
| User cannot login | No access | Verify user configuration, check permissions, test credentials |
| Script error | Functionality failure | Check script syntax, enable error handling, test in WindowMaker |
| Graphics not animating | Static graphics | Verify animation configuration, check tag binding, test in WindowMaker |
| Slow performance | Poor responsiveness | Optimize graphics, reduce tag update rates, check hardware |
| Memory leak | Application crash | Monitor memory usage, restart application, check for bugs |
| Network congestion | Slow communication | Optimize network, segment traffic, check bandwidth |

## Implementation Examples

### VBScript (Tag Access)
```vbs
' Window script to read and write tags

' Read a tag
Dim myTagValue
myTagValue = GetTagValue("MyTag")
MsgBox "MyTag value: " & myTagValue

' Write a tag
SetTagValue "MyTag", 1234

' Read a tag from a specific PLC
Dim plcTagValue
plcTagValue = GetTagValue("PLC1.MyTag")
MsgBox "PLC1.MyTag value: " & plcTagValue

' Write a tag to a specific PLC
SetTagValue "PLC1.MyTag", 5678
```

### VBScript (Alarm Handling)
```vbs
' Alarm trigger script

' Get alarm information
Dim alarmName, alarmMessage, alarmPriority
alarmName = Alarm.Name
alarmMessage = Alarm.Message
alarmPriority = Alarm.Priority

' Log alarm to file
Dim fso, file
Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.OpenTextFile("C:\Alarms\Alarms.log", 8, True)
file.WriteLine Now & ", " & alarmName & ", " & alarmMessage & ", Priority: " & alarmPriority
file.Close

' Send email notification
Dim email
Set email = CreateObject("CDO.Message")
email.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
email.Configuration.Fields.Item("http://schemas.microsoft.com/cdo/configuration/smtpserver") = "smtp.example.com"
email.Configuration.Fields.Update
email.From = "alarm@example.com"
email.To = "operator@example.com"
email.Subject = "Alarm: " & alarmName
email.TextBody = alarmMessage
email.Send
```

### VBScript (Button Click Event)
```vbs
' Button click event handler

' Get the tag value
Dim currentValue
currentValue = GetTagValue("Machine.Status")

' Toggle the value
If currentValue = 0 Then
    SetTagValue "Machine.Status", 1
    SetTagValue "Machine.StatusText", "RUN"
Else
    SetTagValue "Machine.Status", 0
    SetTagValue "Machine.StatusText", "STOP"
End If

' Update button appearance
Me.BackColor = IIf(GetTagValue("Machine.Status") = 1, RGB(0, 255, 0), RGB(255, 0, 0))
Me.Text = IIf(GetTagValue("Machine.Status") = 1, "Stop", "Start")
```

### VBScript (Trend Configuration)
```vbs
' Configure a trend at runtime

' Get trend object
Dim myTrend
Set myTrend = Window("MyWindow").Trend("MyTrend")

' Add a pen
Dim myPen
Set myPen = myTrend.Pens.Add("Temperature")

' Configure pen
myPen.TagName = "Machine.Temperature"
myPen.Color = RGB(255, 0, 0)
myPen.LineStyle = 0 ' Solid line
myPen.LineWidth = 2
myPen.Symbol = 1 ' Circle symbol

' Set time range
myTrend.TimeRange.Start = Now - 1 ' 1 day ago
myTrend.TimeRange.End = Now
myTrend.TimeRange.Span = 1 ' 1 day

' Set update rate
myTrend.UpdateRate = 1000 ' 1 second

' Enable trend
myTrend.Enabled = True
```

## Vendor Ecosystem

**InTouch Products**: InTouch, InTouch for System Platform
**System Platform**: Wonderware System Platform, Application Server, Historian, Alarm Provider
**PLC Integration**: Allen-Bradley, Siemens, Schneider, Mitsubishi, and hundreds of others via OPC, DDE, SuiteLink, custom drivers
**HMI**: InTouch as primary HMI
**MES/ERP**: Wonderware MES, SAP, Oracle, and others
**Cloud**: Wonderware Cloud, AWS, Azure, Google Cloud
**Databases**: SQL Server, Oracle, MySQL, Wonderware Historian
**Drivers**: SuiteLink, DDE, OPC, OPC UA, Modbus, and hundreds of others

## Resources

- **Wonderware**: [wonderware.com](https://www.wonderware.com)
- **InTouch Documentation**: [wonderware.com/intouch](https://www.wonderware.com/en-us/products/intouch)
- **System Platform**: [wonderware.com/system-platform](https://www.wonderware.com/en-us/products/system-platform)
- **Wonderware Support**: [wonderware.com/support](https://www.wonderware.com/en-us/support)
- **Wonderware University**: [wonderware.com/university](https://www.wonderware.com/en-us/services/training)
- **OPC UA**: [opcfoundation.org](https://opcfoundation.org)
- **Aveva**: [aveva.com](https://www.aveva.com) (Wonderware is now part of AVEVA)

## Standing Rules

- **A window is a view into the process** — each window should present a clear, focused view of a specific aspect of the process; do not overload windows with too much information.
- **A symbol is a reusable component** — symbols enable reuse of graphics and logic; create symbols for common elements to improve consistency and maintainability.
- **A tag is a named reference to data** — tags in InTouch are named references to data points; use meaningful names that describe the data.
- **An alarm is a call to action** — every alarm should have a clear cause and a defined action; if an alarm cannot be acted upon, reconsider whether it should be an alarm.
- **Scripts should be simple and focused** — InTouch scripts are typically short and focused on specific tasks; avoid complex, monolithic scripts.
- **Error handling is essential** — scripts can fail; implement error handling to ensure the application remains stable.
- **The WindowMaker is for development, WindowViewer is for runtime** — never use WindowMaker as a runtime client; it is a development tool only.
- **Test in WindowViewer before deploying** — always test applications in WindowViewer before deploying to production; WindowMaker and WindowViewer can behave differently.
- **Use layers to organize graphics** — layers make complex graphics more manageable; use them to separate different types of information.
- **Use symbols for consistency** — symbols ensure consistent appearance and behavior; use them for common elements like pumps, valves, motors.
- **Document your application** — document window purposes, tag definitions, alarm configurations, and script logic; this is essential for maintenance.
- **Backup your application** — InTouch application files contain all your work; back them up regularly and before making changes.
- **Use version control** — store application files in version control; this enables rollback, comparison, and collaboration.
- **Monitor application performance** — complex applications can be slow; monitor performance and optimize as needed.
- **Limit the number of open windows** — too many open windows can consume significant memory; limit the number or implement window management.
- **Use appropriate update rates** — faster update rates consume more resources; set appropriate rates for each tag and trend.
- **Avoid hard-coded values** — use tags or constants instead of hard-coded values; this makes the application more flexible and maintainable.
- **Use tag groups for organization** — tag groups make tag management easier; use them to organize related tags.
- **Test alarm conditions thoroughly** — verify that all alarms trigger and clear correctly; do not assume they work without testing.
- **Use alarm groups for filtering** — alarm groups enable filtering; use them to present relevant alarms to different users.
- **Require alarm acknowledgment** — require operators to acknowledge important alarms; do not allow alarms to be ignored.
- **Use alarm comments for context** — alarm comments provide context for why an alarm was acknowledged or cleared; require comments for important alarms.
- **Monitor alarm statistics** — alarm statistics can reveal patterns and issues; use them for predictive maintenance.
- **Use trends for analysis** — trends enable analysis of process data; use them to identify issues and optimize performance.
- **Optimize trend performance** — trends can be resource-intensive; optimize them by limiting the number of pens, update rates, and time ranges.
- **Use appropriate time ranges** — set time ranges based on the data being analyzed; too short and you miss patterns, too long and the trend becomes cluttered.
- **Test reports thoroughly** — verify that all reports generate correctly with the expected data; do not assume they work without testing.
- **Use report parameters for flexibility** — report parameters make reports more flexible; use them to customize report content.
- **Schedule reports appropriately** — reports can consume significant resources; schedule them during off-peak hours where possible.
- **Use security zones for access control** — security zones enable fine-grained access control; use them to limit access to sensitive information.
- **Test all user roles** — verify that each user role has the appropriate permissions; do not assume roles are configured correctly.
- **Use Windows authentication for simplicity** — Windows authentication simplifies user management; use it where possible.
- **Monitor user sessions** — track user logins and logouts; this can help identify issues and security concerns.
- **Implement session timeouts** — inactive sessions should time out to prevent unauthorized access.
- **Use meaningful tag descriptions** — tag descriptions provide context for the data; use them to make the application more understandable.
- **Document script logic** — scripts can be complex; document their purpose and logic for maintainability.
- **Use reusable script functions** — reusable functions reduce duplication and improve maintainability; create a library of common functions.
- **Avoid infinite loops** — infinite loops can crash the application; implement safeguards to prevent them.
- **Use the right data type for the job** — match tag data types to the PLC data types; mismatches can cause issues.
- **Validate all inputs** — validate inputs from operators and external systems to ensure they are within expected ranges.
- **Use expressions for calculated values** — expressions can calculate values without scripting; use them for simple calculations.
- **Test on different screen sizes** — applications should work on different screen sizes; test on various resolutions.
- **Use System Platform for large applications** — for large, distributed applications, consider using Wonderware System Platform with InTouch as the HMI client.
