---
type: integration
family: industrial
---

# MES Integration Patterns

**Manufacturing Execution System common patterns**: This contract defines the standard
approaches, protocols, and best practices for integrating industrial devices and
systems with MES platforms. It serves as a shared reference for all industrial
protocol and platform dialects.

## MES System Categories

### Tier 1 - Enterprise MES

**SAP ME / MII (Manufacturing Integration and Intelligence)**:
- **Platform**: SAP NetWeaver, HANA
- **Focus**: End-to-end manufacturing execution, analytics, intelligence
- **Industries**: Discrete manufacturing, process industries, hybrid
- **Deployment**: On-premises, cloud, hybrid
- **Integration**: SAP ERP, PLM, SCADA, shop floor systems
- **Strengths**: Deep ERP integration, advanced analytics, global scale

**Oracle Manufacturing Operations Center**:
- **Platform**: Oracle Database, Java-based
- **Focus**: Production execution, quality management, maintenance
- **Industries**: Discrete, process, food & beverage, life sciences
- **Deployment**: On-premises, cloud
- **Integration**: Oracle E-Business Suite, JD Edwards, SCADA
- **Strengths**: Oracle ecosystem integration, advanced planning, compliance

**GE Digital Proficy**:
- **Platform**: .NET-based, Windows-centric
- **Focus**: Real-time manufacturing execution, operations management
- **Industries**: Discrete manufacturing, power generation, oil & gas
- **Deployment**: On-premises
- **Integration**: GE Intelligent Platforms, iFIX, CIMPLICITY
- **Strengths**: Real-time capabilities, process optimization, GE equipment integration

**Rockwell FactoryTalk ProductionCentre**:
- **Platform**: Microsoft .NET, SQL Server
- **Focus**: Production monitoring, tracking, genealogy
- **Industries**: Discrete manufacturing, automotive, CPG
- **Deployment**: On-premises
- **Integration**: FactoryTalk suite, Allen-Bradley controllers
- **Strengths**: Rockwell automation ecosystem, production tracking, genealogy

**Siemens Opcenter (formerly SIMATIC IT)**:
- **Platform**: Java-based, open architecture
- **Focus**: Digital manufacturing, Industry 4.0, paperless production
- **Industries**: Automotive, aerospace, machinery, electronics
- **Deployment**: On-premises, cloud
- **Integration**: SIMATIC controllers, TIA Portal, MindSphere
- **Strengths**: Siemens automation integration, digital twin, Industry 4.0

### Tier 2 - Industry-Specific MES

**Camstar (Siemens)**:
- **Focus**: Electronics, semiconductor, medical device manufacturing
- **Strengths**: High-tech manufacturing, complex workflows, compliance

**Apriso (Dassault Systemes)**:
- **Focus**: Automotive, industrial equipment manufacturing
- **Strengths**: Global manufacturing, flexible production, lean manufacturing

**Infor MES**:
- **Focus**: Food & beverage, pharmaceuticals, chemicals
- **Strengths**: Infor ERP integration, industry-specific workflows

**QAD MES**:
- **Focus**: Automotive, life sciences, consumer products
- **Strengths**: QAD ERP integration, automotive industry expertise

**Epicor MES**:
- **Focus**: Discrete manufacturing, metal fabrication
- **Strengths**: Epicor ERP integration, SME manufacturing

### Tier 3 - Open Source / Cloud-Native MES

**OpenMES**:
- **Platform**: Open-source, Java-based
- **Focus**: Basic MES functionality for SMEs
- **Strengths**: Low cost, customizable, community support

**FlexMES**:
- **Platform**: Cloud-native, microservices
- **Focus**: Flexible manufacturing, cloud deployment
- **Strengths**: Scalability, modern architecture, subscription model

**Litmus Edge MES**:
- **Platform**: Edge computing, IoT-focused
- **Focus**: Edge-based MES for distributed manufacturing
- **Strengths**: Edge deployment, real-time processing, IoT integration

## MES Functional Areas

### Production Management

**Production Order Management**:
- **Order Creation**: Create production orders from ERP or manually
- **Order Scheduling**: Schedule orders based on priorities, resources, constraints
- **Order Release**: Release orders to the shop floor
- **Order Tracking**: Track order progress in real-time
- **Order Completion**: Mark orders as complete with all associated data

**Work Instruction Management**:
- **Standard Work**: Define standard work procedures
- **Work Instructions**: Create detailed work instructions for operators
- **Visual Work Instructions**: Include images, videos, animations
- **Version Control**: Manage versions of work instructions
- **Digital Sign-off**: Electronic sign-off by operators

**Bill of Materials (BOM) Management**:
- **BOM Definition**: Define product structure and components
- **BOM Versioning**: Manage versions of BOMs
- **BOM Comparison**: Compare different BOM versions
- **Effectivity Dates**: Manage BOMs by date or serial number
- **Where-Used**: Find all products that use a specific component

**Recipe / Formulation Management**:
- **Recipe Definition**: Define process parameters and settings
- **Recipe Versioning**: Manage versions of recipes
- **Recipe Scaling**: Scale recipes based on batch size
- **Recipe Validation**: Validate recipe parameters
- **Recipe Security**: Control access to recipes

### Shop Floor Execution

**Shop Floor Data Collection**:
- **Manual Entry**: Operators manually enter production data
- **Automatic Collection**: Data automatically collected from machines
- **Barcode/RFID**: Use barcodes or RFID for material and product tracking
- **Time Collection**: Track labor time by operator, work center, operation
- **Quantity Collection**: Track quantities produced, scrap, rework

**Material Management**:
- **Material Tracking**: Track raw materials, WIP, finished goods
- **Material Consumption**: Record material usage by operation
- **Material Issuance**: Issue materials from inventory to production
- **Material Return**: Return unused materials to inventory
- **Lot / Batch Tracking**: Track materials by lot or batch

**Tool and Equipment Management**:
- **Tool Tracking**: Track tools and their locations
- **Tool Calibration**: Manage tool calibration schedules and records
- **Tool Maintenance**: Track tool maintenance requirements
- **Equipment Status**: Monitor equipment availability and status
- **Preventive Maintenance**: Schedule and track preventive maintenance

**Quality Management**:
- **Inspection Plans**: Define inspection requirements for products
- **Inspection Execution**: Perform inspections according to plans
- **Defect Tracking**: Track defects and non-conformances
- **SPC (Statistical Process Control)**: Monitor process capability and control
- **CAPA (Corrective and Preventive Action)**: Manage quality improvement actions

### Process Control and Monitoring

**Process Parameter Management**:
- **Parameter Definition**: Define process parameters and limits
- **Parameter Monitoring**: Monitor parameters in real-time
- **Parameter Control**: Automatically control parameters based on rules
- **Parameter Historization**: Store historical parameter data
- **Parameter Analysis**: Analyze parameter trends and correlations

**State Management**:
- **State Definition**: Define equipment and process states
- **State Transitions**: Define valid state transitions
- **State Monitoring**: Monitor current state of equipment and processes
- **State Change Tracking**: Track when and why states change
- **State-Based Control**: Execute actions based on state changes

**Performance Monitoring**:
- **OEE (Overall Equipment Effectiveness)**: Monitor availability, performance, quality
- **Cycle Time**: Track time to complete production cycles
- **Throughput**: Monitor production rate and output
- **Downtime Tracking**: Record reasons and duration of downtime
- **Efficiency Analysis**: Analyze efficiency by operation, work center, product

### Planning and Scheduling

**Production Planning**:
- **Master Production Schedule (MPS)**: High-level production plan
- **Material Requirements Planning (MRP)**: Plan material requirements
- **Capacity Planning**: Plan based on available capacity
- **Resource Planning**: Plan labor, equipment, tools
- **Constraint Management**: Identify and manage production constraints

**Detailed Scheduling**:
- **Operation Scheduling**: Schedule individual operations
- **Sequence Optimization**: Optimize operation sequences
- **Resource Allocation**: Allocate resources to operations
- **Dependency Management**: Manage dependencies between operations
- **Real-Time Adjustments**: Adjust schedules based on real-time events

**Advanced Planning and Scheduling (APS)**:
- **Finite Capacity Scheduling**: Schedule considering actual capacity
- **What-If Analysis**: Simulate schedule changes before implementing
- **Bottleneck Identification**: Identify production bottlenecks
- **Optimization**: Automatically optimize schedules based on objectives
- **Scenario Planning**: Plan for different production scenarios

### Quality and Compliance

**Quality Data Collection**:
- **Automatic Collection**: Collect quality data from machines and sensors
- **Manual Inspection**: Operators perform manual inspections
- **Sample Management**: Manage sampling plans and samples
- **Test Results**: Record test results and measurements
- **Statistical Analysis**: Perform statistical analysis on quality data

**Compliance Management**:
- **Regulatory Compliance**: Ensure compliance with industry regulations
- **Standard Compliance**: Comply with industry standards (ISO, ANSI, etc.)
- **Audit Trails**: Maintain comprehensive audit trails
- **Document Control**: Control and manage quality documents
- **Certification Management**: Track certifications and approvals

**Non-Conformance Management**:
- **Defect Tracking**: Track defects and quality issues
- **Root Cause Analysis**: Identify root causes of quality issues
- **Containment Actions**: Implement actions to contain quality issues
- **Corrective Actions**: Implement permanent fixes for quality issues
- **Preventive Actions**: Implement actions to prevent recurrence

## Integration Architecture Patterns

### Data Flow Patterns

**Bottom-Up Data Collection**:
- **Description**: Data flows from shop floor devices to MES
- **Sources**: PLCs, sensors, SCADA systems, manual entry
- **Transformations**: Filtering, aggregation, validation, enrichment
- **Destination**: MES database, MES applications
- **Frequency**: Real-time to batch (depending on data type)

**Top-Down Work Distribution**:
- **Description**: Work orders and instructions flow from MES to shop floor
- **Sources**: ERP, MES planning, manual creation
- **Transformations**: Work instruction generation, BOM expansion, recipe selection
- **Destination**: Shop floor displays, operator terminals, machines
- **Frequency**: As needed, event-driven

**Bidirectional Synchronization**:
- **Description**: Data flows both ways between MES and other systems
- **MES to ERP**: Production data, completion confirmations, quality data
- **ERP to MES**: Work orders, BOMs, material data, production schedules
- **Synchronization**: Real-time, batch, or event-driven
- **Conflict Resolution**: Define rules for resolving data conflicts

### Integration Methods

**Direct Database Integration**:
- **Description**: MES and other systems share a common database
- **Pros**: Simple, real-time, no data duplication
- **Cons**: Tight coupling, database dependency, performance impact
- **Use Case**: Same-vendor systems, tightly integrated applications
- **Implementation**: Shared database schema, common tables, stored procedures

**API-Based Integration**:
- **Description**: Systems communicate via APIs (REST, SOAP, GraphQL)
- **Pros**: Loose coupling, platform-independent, flexible
- **Cons**: Development required, potential latency, versioning
- **Use Case**: Cross-vendor systems, cloud integrations
- **Implementation**: REST APIs, SOAP web services, GraphQL endpoints

**Message-Based Integration**:
- **Description**: Systems communicate via messages (MQTT, AMQP, JMS)
- **Pros**: Decoupled, scalable, reliable, real-time
- **Cons**: Complexity, message broker dependency
- **Use Case**: Event-driven architectures, IoT integrations
- **Implementation**: MQTT brokers, AMQP servers, message queues

**File-Based Integration**:
- **Description**: Systems exchange data via files (CSV, XML, JSON)
- **Pros**: Simple, universal, batch-oriented
- **Cons**: Latency, file management overhead, error handling
- **Use Case**: Batch data exchange, legacy systems
- **Implementation**: File drop folders, SFTP servers, cloud storage

**Service-Oriented Integration**:
- **Description**: Systems expose and consume services
- **Pros**: Reusable, modular, scalable
- **Cons**: Service discovery, orchestration complexity
- **Use Case**: Microservices architecture, service-oriented architectures
- **Implementation**: Service buses, API gateways, service registries

### Protocol-Specific Integration

**OPC UA Integration**:
- **Description**: Use OPC UA for real-time data exchange
- **Data Access**: Read/write process variables, browse address space
- **Method Calls**: Execute methods on OPC UA servers
- **Subscription**: Real-time data subscriptions
- **Information Model**: Use OPC UA information model for semantic integration
- **Best Practice**: Map MES data model to OPC UA information model

**SQL Database Integration**:
- **Description**: Use SQL for data exchange with relational databases
- **Query**: SELECT, INSERT, UPDATE, DELETE operations
- **Stored Procedures**: Use stored procedures for complex operations
- **Views**: Use database views for specific data subsets
- **Triggers**: Use triggers for automatic actions
- **Best Practice**: Optimize queries, use connection pooling, implement proper error handling

**REST API Integration**:
- **Description**: Use RESTful APIs for integration
- **Resources**: Map MES entities to REST resources
- **Methods**: Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- **Status Codes**: Handle HTTP status codes appropriately
- **Authentication**: Implement API authentication (OAuth2, API keys, Basic Auth)
- **Pagination**: Handle paginated results
- **Rate Limiting**: Respect API rate limits

**MQTT Integration**:
- **Description**: Use MQTT for lightweight, reliable messaging
- **Topics**: Define topic hierarchy for different data types
- **QoS**: Use appropriate Quality of Service levels (0, 1, 2)
- **Retained Messages**: Use retained messages for persistent data
- **Last Will**: Implement Last Will and Testament for device disconnects
- **Authentication**: Implement MQTT authentication and TLS

## MES Platform-Specific Patterns

### SAP ME / MII

**Architecture**:
- **Platform**: SAP NetWeaver, HANA database
- **Components**: ME (Manufacturing Execution), MII (Manufacturing Integration and Intelligence)
- **Deployment**: On-premises, cloud, hybrid
- **Integration**: SAP ERP, PLM, shop floor systems

**Integration Methods**:
- **BAPI (Business API)**: SAP's standard API for integration
- **IDoc (Intermediate Document)**: Document-based integration
- **OData**: RESTful data access
- **RFC (Remote Function Call)**: Direct function calls
- **Web Services**: SOAP-based integration
- **Direct Database**: Shared database access

**Data Model**:
- **Production Orders**: SAP production order structure
- **Operations**: Manufacturing operations with BOM and routing
- **Confirmation**: Production confirmations with time and quantities
- **Material**: Material master data and movements
- **Equipment**: Equipment master data and status

**Best Practices**:
- Use BAPI for standard SAP integrations
- Use IDoc for batch data exchange
- Leverage SAP's manufacturing industry solutions
- Implement proper authorization using SAP roles
- Use SAP's plant data collection (PDC) interface for shop floor integration

**Common Defects**:
- BAPI authorization errors
- IDoc mapping errors
- Database locks and deadlocks
- Performance issues with large data volumes
- Version compatibility issues

### Oracle Manufacturing Operations Center

**Architecture**:
- **Platform**: Oracle Database, Java-based applications
- **Components**: Production, Quality, Maintenance, Inventory
- **Deployment**: On-premises, cloud
- **Integration**: Oracle E-Business Suite, JD Edwards, SCADA

**Integration Methods**:
- **PL/SQL APIs**: Database stored procedures and packages
- **REST Services**: RESTful web services
- **SOAP Services**: SOAP-based web services
- **Java APIs**: Java-based integration
- **File Import/Export**: CSV, XML file exchange

**Data Model**:
- **Work Orders**: Oracle work order structure
- **Work Centers**: Manufacturing work centers with capabilities
- **Operations**: Manufacturing operations with standards
- **Material Transactions**: Material movements and consumption
- **Quality Results**: Quality inspection and test results

**Best Practices**:
- Use PL/SQL for database-intensive operations
- Leverage Oracle's Advanced Supply Chain Planning (ASCP)
- Use Oracle's Manufacturing Operations Center SDK
- Implement proper data validation and error handling
- Use Oracle's workflow capabilities for approval processes

**Common Defects**:
- PL/SQL errors and exceptions
- Java memory issues
- Database connection pooling problems
- Complex query performance issues
- Integration version mismatches

### Rockwell FactoryTalk ProductionCentre

**Architecture**:
- **Platform**: Microsoft .NET, SQL Server
- **Components**: Production, Tracking, Genealogy, Downtime
- **Deployment**: On-premises
- **Integration**: FactoryTalk suite, Allen-Bradley controllers

**Integration Methods**:
- **FactoryTalk Directory**: Service discovery and directory services
- **OPC UA**: Native OPC UA support
- **SQL**: SQL Server database access
- **.NET APIs**: .NET-based integration
- **ActiveX/COM**: Legacy COM-based integration

**Data Model**:
- **Production Tracking**: Track production by order, part, serial number
- **Genealogy**: Track component genealogy and history
- **Downtime Tracking**: Record and analyze downtime reasons
- **Performance Tracking**: Monitor OEE and other performance metrics
- **Work Instructions**: Digital work instructions for operators

**Best Practices**:
- Use FactoryTalk Directory for service discovery
- Leverage FactoryTalk View for HMI integration
- Use FactoryTalk Historian for historical data
- Implement FactoryTalk Security for authentication and authorization
- Use FactoryTalk Metrics for performance monitoring

**Common Defects**:
- COM registration issues
- .NET version compatibility problems
- SQL Server connection issues
- FactoryTalk service communication failures
- License management issues

### Siemens Opcenter (SIMATIC IT)

**Architecture**:
- **Platform**: Java-based, open architecture
- **Components**: Production, Quality, Maintenance, Warehouse
- **Deployment**: On-premises, cloud
- **Integration**: SIMATIC controllers, TIA Portal, MindSphere

**Integration Methods**:
- **OPC UA**: Native OPC UA support
- **SIMATIC IT API**: Java-based APIs
- **Web Services**: REST and SOAP services
- **Database**: Oracle, SQL Server, PostgreSQL
- **MindSphere**: Cloud integration with Siemens MindSphere

**Data Model**:
- **Production Orders**: Siemens production order structure
- **Operations**: Manufacturing operations with resources
- **Recipes**: Process recipes and parameters
- **Quality Inspections**: Quality inspection plans and results
- **Maintenance Orders**: Maintenance work orders and execution

**Best Practices**:
- Use OPC UA for real-time data exchange with SIMATIC controllers
- Leverage SIMATIC IT's digital manufacturing capabilities
- Integrate with TIA Portal for engineering data
- Use MindSphere for cloud-based analytics and monitoring
- Implement proper role-based access control

**Common Defects**:
- OPC UA connection issues
- Java memory and performance problems
- Database connection failures
- Integration configuration errors
- Version compatibility issues

### GE Digital Proficy

**Architecture**:
- **Platform**: .NET-based, Windows-centric
- **Components**: Proficy Smart Factory, Proficy Process Systems
- **Deployment**: On-premises
- **Integration**: GE Intelligent Platforms, iFIX, CIMPLICITY

**Integration Methods**:
- **Proficy API**: .NET-based APIs
- **OPC**: OPC UA, OPC DA support
- **SQL**: Database access
- **Web Services**: SOAP and REST services
- **CIMPLICITY Integration**: Integration with CIMPLICITY SCADA

**Data Model**:
- **Production Execution**: Execute and track production operations
- **Process Control**: Monitor and control process parameters
- **Quality Management**: Manage quality inspections and testing
- **Maintenance**: Track equipment maintenance
- **Performance Analysis**: Analyze production performance

**Best Practices**:
- Use Proficy API for custom integrations
- Leverage Proficy's real-time capabilities
- Integrate with iFIX or CIMPLICITY for SCADA
- Use Proficy's analytics capabilities
- Implement proper security and authentication

**Common Defects**:
- .NET runtime errors
- OPC server connection issues
- Database performance problems
- Integration timeout errors
- Configuration mismatches

## Data Mapping Patterns

### MES to Industrial Protocol Mapping

**Production Data**:
- **MES Concept**: Work orders, operations, production quantities
- **Protocol Data**: Device status, cycle counts, part counts
- **Mapping**: Map device counters to production quantities
- **Aggregation**: Aggregate device data to operation level
- **Validation**: Validate production data against expected values

**Process Data**:
- **MES Concept**: Process parameters, setpoints, actual values
- **Protocol Data**: Analog inputs, process variables
- **Mapping**: Map protocol tags to MES parameters
- **Scaling**: Scale and convert protocol data to MES units
- **Timestamp**: Align timestamps between systems

**Equipment Data**:
- **MES Concept**: Equipment status, availability, utilization
- **Protocol Data**: Device states, run/stop/idle times
- **Mapping**: Map device states to MES equipment states
- **Calculation**: Calculate OEE and other metrics from device data
- **Validation**: Validate equipment state transitions

**Quality Data**:
- **MES Concept**: Inspection results, test measurements, defects
- **Protocol Data**: Sensor readings, vision system results
- **Mapping**: Map quality measurements to inspection characteristics
- **Validation**: Validate measurements against specifications
- **Storage**: Store quality data with proper context

**Material Data**:
- **MES Concept**: Material consumption, inventory movements
- **Protocol Data**: Scale readings, barcode scans, RFID tags
- **Mapping**: Map device readings to material transactions
- **Validation**: Validate material quantities and movements
- **Synchronization**: Synchronize material data with ERP

### Common Data Transformation Patterns

**Unit Conversion**:
- **Pattern**: Convert between different units of measure
- **Implementation**: Use conversion factors or libraries
- **Considerations**: Precision, rounding, unit systems (metric, imperial)
- **Example**: Convert device readings from raw units to engineering units

**Scaling**:
- **Pattern**: Scale values from device range to engineering range
- **Implementation**: Linear scaling, polynomial scaling, lookup tables
- **Considerations**: Deadbands, calibration, drift compensation
- **Example**: Scale 4-20mA signal to 0-100% range

**Aggregation**:
- **Pattern**: Combine multiple data points into aggregated values
- **Types**: Sum, Average, Minimum, Maximum, Count, First, Last
- **Implementation**: Time-based, count-based, event-based
- **Considerations**: Reset conditions, aggregation periods
- **Example**: Aggregate hourly production quantities

**Filtering**:
- **Pattern**: Filter data based on conditions or criteria
- **Types**: Threshold, Range, Rate of Change, Statistical
- **Implementation**: Real-time, batch, event-based
- **Considerations**: Filter criteria, false positives/negatives
- **Example**: Filter out noise or invalid data points

**Validation**:
- **Pattern**: Validate data quality and consistency
- **Types**: Range, Type, Format, Cross-check, Statistical
- **Implementation**: Real-time, batch, on-demand
- **Considerations**: Validation rules, error handling, default values
- **Example**: Validate process parameters against operating limits

## Performance Optimization Patterns

### Data Collection Optimization

**Sampling Rate**:
- **Pattern**: Optimize how often data is collected
- **Considerations**: Data volatility, importance, network bandwidth, storage
- **Approach**: Adaptive sampling, event-based, exception-based
- **Implementation**: Dynamic sampling based on conditions

**Data Volume**:
- **Pattern**: Optimize the amount of data collected
- **Considerations**: Storage requirements, network bandwidth, processing power
- **Approach**: Filtering, compression, aggregation, deadbanding
- **Implementation**: Collect only necessary data at appropriate detail

**Data Latency**:
- **Pattern**: Optimize how quickly data is available
- **Considerations**: Real-time requirements, decision-making timelines
- **Approach**: Prioritization, buffering, caching
- **Implementation**: Prioritize critical data, minimize processing delays

### Processing Optimization

**Batch Processing**:
- **Pattern**: Process data in batches rather than individually
- **Benefits**: Improved efficiency, reduced overhead
- **Considerations**: Batch size, timing, resource requirements
- **Implementation**: Accumulate data and process periodically

**Stream Processing**:
- **Pattern**: Process data as it arrives (streaming)
- **Benefits**: Real-time processing, low latency
- **Considerations**: Complexity, resource requirements, fault tolerance
- **Implementation**: Process data immediately upon receipt

**Parallel Processing**:
- **Pattern**: Process multiple data items simultaneously
- **Benefits**: Improved throughput, reduced processing time
- **Considerations**: Resource requirements, data dependencies, synchronization
- **Implementation**: Use multiple threads or processes for parallel operations

### Integration Optimization

**Caching**:
- **Pattern**: Cache frequently accessed data
- **Benefits**: Reduced load on source systems, improved performance
- **Considerations**: Cache consistency, invalidation, memory usage
- **Implementation**: Cache reference data, historical data, computed values

**Batching**:
- **Pattern**: Batch multiple operations into single calls
- **Benefits**: Reduced network traffic, improved efficiency
- **Considerations**: Batch size, timing, error handling
- **Implementation**: Group read/write operations, combine multiple API calls

**Compression**:
- **Pattern**: Compress data for transmission
- **Benefits**: Reduced network bandwidth, faster transmission
- **Considerations**: Compression overhead, data loss (for lossy compression)
- **Implementation**: Compress payloads, use efficient data formats

## Common Integration Defects and Mitigations

| Defect | Impact | Detection | Mitigation |
|--------|--------|-----------|------------|
| Data Not Arriving | Missing production data | Data freshness monitoring, gap detection | Check connections, verify device status, test data flow |
| Data Duplication | Duplicate records | Data validation, duplicate detection | Implement idempotency, use unique identifiers, deduplicate data |
| Data Out of Sequence | Incorrect order | Sequence number monitoring, timestamp validation | Synchronize clocks, implement sequencing, buffer and reorder |
| Data Type Mismatch | Processing errors | Data type validation, error logging | Align data types, implement type conversion, validate mappings |
| Unit Mismatch | Incorrect values | Unit validation, range checking | Standardize units, implement unit conversion, validate mappings |
| Timestamp Mismatch | Temporal inconsistencies | Timestamp validation, drift detection | Synchronize clocks, use NTP, validate timestamp sources |
| Performance Issues | Slow processing | Performance monitoring, resource utilization | Optimize queries, tune sampling, improve data models |
| Memory Leak | System instability | Memory monitoring, performance degradation | Restart services, update software, check for known issues |
| Database Deadlock | Blocked operations | Deadlock detection, timeout monitoring | Optimize transactions, reduce lock times, implement timeouts |
| Integration Timeout | Failed operations | Timeout monitoring, error logging | Increase timeouts, optimize processing, check network |
| Authentication Error | Access denied | Authentication error logging | Verify credentials, check permissions, test authentication |
| Authorization Error | Operation denied | Authorization error logging | Verify roles, check permissions, test authorization |
| Protocol Violation | Communication error | Protocol validation, error codes | Verify protocol compliance, update drivers, check device firmware |
| Version Mismatch | Compatibility issues | Version checking, error logging | Align versions, implement version compatibility, update components |
| License Error | Functionality limited | License monitoring, error logging | Verify licenses, check license servers, renew licenses |

## Standing Rules

1. **Single Source of Truth**: Each piece of data should have a single, authoritative source. Avoid data duplication unless necessary for performance or availability.

2. **Data Ownership**: Clearly define which system owns which data. The owning system is responsible for data integrity, validation, and maintenance.

3. **Real-Time First**: Prioritize real-time data collection and processing for production-critical information. Batch processing is acceptable for non-critical data.

4. **Idempotency**: Design integrations to be idempotent - the same operation executed multiple times should have the same effect as executed once.

5. **Error Handling**: Always implement proper error handling and recovery mechanisms. Failures should be detected, logged, and handled gracefully.

6. **Performance by Design**: Design for performance from the beginning. Consider data volumes, frequencies, and processing requirements.

7. **Security by Design**: Implement appropriate security measures for all integrations - authentication, authorization, encryption, and audit logging.

8. **Monitor Everything**: Monitor all critical aspects of the integration - data flow, data quality, performance, security, and availability.

9. **Document Everything**: Document all integration designs, configurations, mappings, and procedures for maintenance and troubleshooting.

10. **Test Thoroughly**: Test all integrations thoroughly under various conditions - normal operation, edge cases, error conditions, and performance scenarios.
