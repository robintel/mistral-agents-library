---
type: integration
family: industrial
---

# ERP Integration Patterns

**Enterprise Resource Planning common patterns**: This contract defines the standard
approaches, protocols, and best practices for integrating manufacturing and industrial
systems with ERP platforms. It serves as a shared reference for all MES, SCADA, and
industrial protocol dialects.

## ERP System Categories

### Tier 1 - Enterprise ERP

**SAP ERP / S/4HANA**:
- **Platform**: SAP NetWeaver, HANA database
- **Industries**: All industries (manufacturing, retail, services, etc.)
- **Deployment**: On-premises, cloud (SAP S/4HANA Cloud)
- **Integration**: SAP ME/MII, PLM, CRM, SCM, BI
- **Strengths**: Comprehensive functionality, global scale, industry solutions
- **Manufacturing Focus**: Discrete, process, repetitive, lean manufacturing

**Oracle ERP Cloud / E-Business Suite**:
- **Platform**: Oracle Database, Fusion Middleware
- **Industries**: Manufacturing, retail, financial services, communications
- **Deployment**: On-premises (EBS), cloud (ERP Cloud)
- **Integration**: Oracle Manufacturing, SCM, CRM, BI
- **Strengths**: Deep integration across Oracle applications, advanced analytics
- **Manufacturing Focus**: Discrete, process, mixed-mode manufacturing

**Microsoft Dynamics 365 Finance & Operations**:
- **Platform**: Azure, .NET-based
- **Industries**: Manufacturing, retail, services, public sector
- **Deployment**: Cloud, on-premises (Dynamics AX)
- **Integration**: Dynamics 365 Supply Chain Management, Power Platform
- **Strengths**: Microsoft ecosystem integration, AI/ML capabilities, modern UX
- **Manufacturing Focus**: Discrete, process, lean, project-based manufacturing

**Infor ERP**:
- **Platform**: Infor OS, Amazon AWS (for cloud)
- **Industries**: Manufacturing, distribution, healthcare, public sector
- **Deployment**: On-premises, cloud
- **Integration**: Infor MES, SCM, CRM, BI
- **Strengths**: Industry-specific solutions, configurable, user-friendly
- **Manufacturing Focus**: Discrete, process, configure-to-order manufacturing

**IFS Applications**:
- **Platform**: Java-based, service-oriented
- **Industries**: Aerospace & defense, energy, manufacturing
- **Deployment**: On-premises, cloud
- **Integration**: IFS MES, EAM, FSM
- **Strengths**: Aerospace/defense expertise, asset management, field service
- **Manufacturing Focus**: Complex discrete, MRO, project-based manufacturing

### Tier 2 - Industry-Specific ERP

**QAD ERP**:
- **Focus**: Automotive, life sciences, consumer products, industrial
- **Strengths**: Automotive industry expertise, global manufacturing, lean

**Epicor ERP**:
- **Focus**: SME manufacturing, distribution
- **Strengths**: SME focus, configurable, user-friendly

**Plex Systems**:
- **Focus**: Cloud manufacturing ERP
- **Strengths**: Cloud-native, manufacturing-focused, smart manufacturing

**Acumatica**:
- **Focus**: Cloud ERP for SMEs
- **Strengths**: Cloud-native, scalable, manufacturing capabilities

**Rootstock**:
- **Focus**: Manufacturing, distribution on Salesforce platform
- **Strengths**: Salesforce integration, manufacturing workflows

### Tier 3 - Open Source ERP

**Odoo**:
- **Platform**: Python, PostgreSQL
- **Focus**: SMEs, manufacturing, e-commerce
- **Strengths**: Modular, open-source, customizable
- **Manufacturing Modules**: MRP, PLM, Quality, Maintenance

**ERPNext**:
- **Platform**: Python, MariaDB/PostgreSQL
- **Focus**: SMEs, manufacturing, distribution
- **Strengths**: Open-source, modern web interface, customizable

**ADempiere**:
- **Platform**: Java, PostgreSQL/Oracle
- **Focus**: Enterprise, manufacturing
- **Strengths**: Open-source, comprehensive functionality

**Apache OFBiz**:
- **Platform**: Java, various databases
- **Focus**: Enterprise, manufacturing, e-commerce
- **Strengths**: Open-source, component-based, extensible

## ERP Functional Areas for Manufacturing

### Production and Operations

**Production Planning**:
- **Master Production Schedule (MPS)**: High-level production plan
- **Material Requirements Planning (MRP)**: Plan material requirements
- **Capacity Requirements Planning (CRP)**: Plan capacity needs
- **Production Order Management**: Create and manage production orders
- **Shop Floor Control**: Monitor and control shop floor operations

**Production Execution**:
- **Production Order Release**: Release orders to production
- **Material Issuance**: Issue materials to production orders
- **Work in Process (WIP) Tracking**: Track WIP inventory and status
- **Production Confirmation**: Confirm production completions
- **Scrap and Rework**: Track and manage scrap and rework

**Product Data Management**:
- **Bill of Materials (BOM)**: Define product structure and components
- **Routing**: Define manufacturing operations and sequences
- **Work Centers**: Define production resources and capabilities
- **Standard Times**: Define standard times for operations
- **Product Costing**: Calculate product costs

### Supply Chain Management

**Procurement**:
- **Purchase Requisitions**: Request materials and services
- **Purchase Orders**: Create and manage purchase orders
- **Vendor Management**: Manage vendor information and performance
- **Receiving**: Receive and inspect purchased materials
- **Invoice Verification**: Verify vendor invoices against receipts

**Inventory Management**:
- **Inventory Tracking**: Track raw materials, WIP, finished goods
- **Warehouse Management**: Manage warehouse locations and movements
- **Lot / Serial Tracking**: Track materials and products by lot or serial number
- **Cycle Counting**: Perform periodic inventory counts
- **Inventory Valuation**: Value inventory using different methods

**Materials Management**:
- **Material Planning**: Plan material requirements and procurement
- **Material Reservation**: Reserve materials for production orders
- **Material Availability**: Check material availability for production
- **Material Substitution**: Substitute alternate materials when needed
- **Material Consumption**: Track material usage in production

### Financial Management

**Cost Management**:
- **Standard Costing**: Define and maintain standard costs
- **Actual Costing**: Track and calculate actual costs
- **Variance Analysis**: Analyze cost variances
- **Overhead Allocation**: Allocate overhead costs to products
- **Activity-Based Costing**: Cost based on activities and resources

**Budgeting and Forecasting**:
- **Budget Creation**: Create budgets for departments and projects
- **Budget Tracking**: Track actual spending against budgets
- **Forecasting**: Forecast future performance and requirements
- **Variance Analysis**: Analyze budget variances

**Accounting**:
- **General Ledger**: Maintain general ledger accounts
- **Accounts Payable**: Manage vendor payments
- **Accounts Receivable**: Manage customer invoicing and receipts
- **Fixed Assets**: Track and manage fixed assets
- **Financial Reporting**: Generate financial statements and reports

### Quality Management

**Quality Planning**:
- **Quality Standards**: Define quality standards and specifications
- **Inspection Plans**: Define inspection requirements and procedures
- **Test Procedures**: Define test procedures and acceptance criteria
- **Quality Documentation**: Manage quality documents and procedures

**Quality Execution**:
- **Inspection Results**: Record inspection results
- **Test Results**: Record test measurements and results
- **Defect Tracking**: Track defects and non-conformances
- **Non-Conforming Material**: Manage non-conforming materials

**Quality Analysis**:
- **SPC (Statistical Process Control)**: Monitor process capability and control
- **Trend Analysis**: Analyze quality trends over time
- **Root Cause Analysis**: Identify root causes of quality issues
- **Corrective Actions**: Implement corrective and preventive actions

## Integration Patterns

### ERP to MES Integration

**Production Data Flow**:
- **ERP to MES**: Production orders, BOMs, routings, work centers
- **MES to ERP**: Production confirmations, material consumption, scrap, quality data
- **Frequency**: Real-time, batch, or event-driven
- **Synchronization**: Two-way synchronization with conflict resolution

**Master Data Synchronization**:
- **Products**: Product masters, BOMs, routings
- **Materials**: Material masters, inventory data
- **Resources**: Work centers, equipment, tools
- **Employees**: Employee data, labor rates, qualifications
- **Synchronization**: Real-time, batch, or on-demand

**Transaction Data Flow**:
- **Production Transactions**: Order releases, confirmations, completions
- **Material Transactions**: Material issues, returns, consumption
- **Time Transactions**: Labor time, machine time, downtime
- **Quality Transactions**: Inspection results, test results, defects

### Integration Approaches

**Direct Integration**:
- **Description**: Direct database-to-database integration
- **Pros**: Real-time, simple, no intermediate layers
- **Cons**: Tight coupling, database dependency, performance impact
- **Use Case**: Same-vendor ERP and MES, tightly integrated applications
- **Implementation**: Shared database, replication, stored procedures

**API-Based Integration**:
- **Description**: Integration via APIs (REST, SOAP, GraphQL)
- **Pros**: Loose coupling, platform-independent, flexible
- **Cons**: Development required, latency, versioning
- **Use Case**: Cross-vendor systems, cloud integrations
- **Implementation**: REST APIs, SOAP web services, GraphQL endpoints

**Middleware Integration**:
- **Description**: Integration via middleware or ESB (Enterprise Service Bus)
- **Pros**: Decoupled, scalable, reliable, protocol-agnostic
- **Cons**: Complexity, middleware dependency, additional layer
- **Use Case**: Complex integrations, multiple systems, enterprise architectures
- **Implementation**: ESB, message brokers, integration platforms

**File-Based Integration**:
- **Description**: Integration via file exchange (CSV, XML, JSON, IDoc)
- **Pros**: Simple, universal, batch-oriented
- **Cons**: Latency, file management overhead, error handling
- **Use Case**: Batch data exchange, legacy systems, non-real-time data
- **Implementation**: File drop folders, SFTP, cloud storage, email

**Message-Based Integration**:
- **Description**: Integration via messaging (MQTT, AMQP, JMS, Kafka)
- **Pros**: Decoupled, scalable, reliable, real-time
- **Cons**: Complexity, message broker dependency, ordering
- **Use Case**: Event-driven architectures, IoT integrations, real-time data
- **Implementation**: Message brokers, queues, topics

### Protocol-Specific Integration

**SAP Integration**:
- **BAPI (Business API)**: SAP's standard API for integration
  - **Description**: Object-oriented API for business processes
  - **Pros**: Standard, well-documented, widely used
  - **Cons**: Complex, requires SAP knowledge
  - **Use Case**: Real-time integrations with SAP systems

- **IDoc (Intermediate Document)**: Document-based integration
  - **Description**: Standardized document format for data exchange
  - **Pros**: Standard, reliable, batch-oriented
  - **Cons**: Complex, requires mapping
  - **Use Case**: Batch data exchange with SAP

- **OData**: RESTful data access
  - **Description**: Open standard for querying and updating data
  - **Pros**: Standard, REST-based, easy to use
  - **Cons**: Limited to exposed entities
  - **Use Case**: Modern integrations, cloud access

- **RFC (Remote Function Call)**: Direct function calls
  - **Description**: Call SAP functions directly
  - **Pros**: Powerful, direct access
  - **Cons**: SAP-specific, complex
  - **Use Case**: Custom integrations with specific SAP functions

- **SAP Cloud Platform Integration**: Cloud-based integration
  - **Description**: Integration via SAP Cloud Platform services
  - **Pros**: Cloud-native, scalable
  - **Cons**: Requires cloud connectivity
  - **Use Case**: Cloud integrations, hybrid architectures

**Oracle Integration**:
- **PL/SQL APIs**: Database stored procedures and packages
  - **Description**: Direct database access via PL/SQL
  - **Pros**: Powerful, efficient, real-time
  - **Cons**: Oracle-specific, requires database access
  - **Use Case**: Database-intensive integrations

- **REST Services**: RESTful web services
  - **Description**: Oracle's RESTful APIs
  - **Pros**: Standard, platform-independent, easy to use
  - **Cons**: Requires REST service configuration
  - **Use Case**: Modern integrations, web-based access

- **SOAP Services**: SOAP-based web services
  - **Description**: Oracle's SOAP-based web services
  - **Pros**: Standard, reliable, well-documented
  - **Cons**: Complex, XML-based
  - **Use Case**: Enterprise integrations, legacy systems

- **Java APIs**: Java-based integration
  - **Description**: Oracle's Java APIs
  - **Pros**: Powerful, object-oriented
  - **Cons**: Java-specific, requires Java development
  - **Use Case**: Custom Java-based integrations

- **Oracle Integration Cloud**: Cloud-based integration
  - **Description**: Cloud-based integration platform
  - **Pros**: Cloud-native, scalable, pre-built adapters
  - **Cons**: Requires cloud connectivity
  - **Use Case**: Cloud integrations, SaaS applications

**Microsoft Dynamics 365 Integration**:
- **OData**: Standard OData endpoints
  - **Description**: RESTful access to Dynamics 365 data
  - **Pros**: Standard, easy to use, widely supported
  - **Cons**: Limited to exposed entities
  - **Use Case**: Modern integrations, external applications

- **Web APIs**: Custom web APIs
  - **Description**: Custom APIs built on Dynamics 365
  - **Pros**: Flexible, customizable
  - **Cons**: Development required
  - **Use Case**: Custom integrations, specialized requirements

- **Azure Integration**: Integration via Azure services
  - **Description**: Use Azure Logic Apps, Service Bus, Event Grid
  - **Pros**: Cloud-native, scalable, event-driven
  - **Cons**: Requires Azure knowledge
  - **Use Case**: Cloud integrations, serverless architectures

- **Power Platform**: Integration via Power Automate, Power Apps
  - **Description**: Low-code integration with Power Platform
  - **Pros**: Low-code, rapid development, user-friendly
  - **Cons**: Limited to Power Platform capabilities
  - **Use Case**: Business user integrations, rapid prototyping

- **Dynamics 365 Connector**: Pre-built connectors
  - **Description**: Pre-built connectors for common systems
  - **Pros**: Quick implementation, pre-tested
  - **Cons**: Limited to available connectors
  - **Use Case**: Common integrations with well-known systems

### Data Mapping Patterns

**Master Data Synchronization**:
- **Products**: Map between ERP product masters and MES product definitions
- **BOMs**: Map between ERP BOMs and MES BOMs
- **Materials**: Map between ERP material masters and MES material definitions
- **Resources**: Map between ERP work centers and MES resources
- **Employees**: Map between ERP employees and MES operators

**Transaction Data Flow**:
- **Production Orders**: Map ERP production orders to MES work orders
- **Material Movements**: Map ERP material movements to MES material transactions
- **Production Confirmations**: Map MES production confirmations to ERP goods receipts
- **Quality Data**: Map MES quality data to ERP quality records
- **Time Data**: Map MES time data to ERP labor transactions

**Financial Data Flow**:
- **Standard Costs**: Map ERP standard costs to MES cost data
- **Actual Costs**: Calculate actual costs from MES data and map to ERP
- **Variances**: Calculate variances in MES and report to ERP
- **Inventory Valuation**: Map MES inventory data to ERP financial data

**Common Data Transformations**:

**Unit Conversion**:
- **Pattern**: Convert between different units of measure
- **Implementation**: Use conversion factors, libraries, or services
- **Considerations**: Precision, rounding, unit systems (metric, imperial)
- **Example**: Convert between ERP units (each) and MES units (kg, meters, etc.)

**Quantity Scaling**:
- **Pattern**: Scale quantities between ERP and MES
- **Implementation**: Use scaling factors, BOM explosions
- **Considerations**: Rounding, precision, lot sizes
- **Example**: Scale MES production quantities to ERP inventory quantities

**Date/Time Conversion**:
- **Pattern**: Convert between different date/time formats and time zones
- **Implementation**: Use date/time libraries, consider time zones
- **Considerations**: Time zone differences, daylight saving time
- **Example**: Convert MES timestamps to ERP date/time formats

**Aggregation**:
- **Pattern**: Aggregate MES data to ERP-level granularity
- **Implementation**: Time-based, order-based, batch-based
- **Considerations**: Aggregation periods, business rules
- **Example**: Aggregate MES hourly production to ERP daily production

**Validation**:
- **Pattern**: Validate data before transmission
- **Implementation**: Range checks, format validation, cross-field validation
- **Considerations**: Validation rules, error handling, default values
- **Example**: Validate MES production data against ERP order quantities

## Performance Optimization Patterns

### Data Volume Management

**Selective Synchronization**:
- **Pattern**: Synchronize only necessary data
- **Implementation**: Filter data based on relevance, change detection
- **Considerations**: Business rules, data dependencies, user requirements
- **Example**: Only synchronize active production orders, not all orders

**Incremental Updates**:
- **Pattern**: Send only changed data
- **Implementation**: Change detection, delta updates, version tracking
- **Considerations**: Change tracking overhead, conflict resolution
- **Example**: Send only changed BOM components, not entire BOM

**Batch Processing**:
- **Pattern**: Process data in batches
- **Implementation**: Accumulate data and process periodically
- **Considerations**: Batch size, timing, resource requirements
- **Example**: Batch production confirmations for end-of-shift processing

### Latency Management

**Real-Time vs Batch**:
- **Pattern**: Choose appropriate timing for data exchange
- **Implementation**: Real-time for critical data, batch for non-critical
- **Considerations**: Data criticality, business requirements, system capabilities
- **Example**: Real-time for production confirmations, batch for inventory updates

**Asynchronous Processing**:
- **Pattern**: Process data asynchronously
- **Implementation**: Message queues, background jobs, event-driven processing
- **Considerations**: Ordering, error handling, retry logic
- **Example**: Queue production confirmations for asynchronous ERP processing

**Caching**:
- **Pattern**: Cache frequently accessed data
- **Implementation**: Local cache, distributed cache, database cache
- **Considerations**: Cache consistency, invalidation, memory usage
- **Example**: Cache ERP master data locally in MES for faster access

### Error Handling and Recovery

**Idempotency**:
- **Pattern**: Ensure operations are idempotent
- **Implementation**: Use unique identifiers, idempotency keys, state tracking
- **Considerations**: Retry logic, duplicate detection, error recovery
- **Example**: Use production confirmation ID to prevent duplicate processing

**Transaction Management**:
- **Pattern**: Manage data consistency across systems
- **Implementation**: Two-phase commit, compensating transactions, sagas
- **Considerations**: Atomicity, consistency, isolation, durability
- **Example**: Roll back MES transactions if ERP update fails

**Retry Logic**:
- **Pattern**: Automatically retry failed operations
- **Implementation**: Exponential backoff, maximum retry limits, circuit breakers
- **Considerations**: Retry conditions, timing, logging
- **Example**: Retry failed API calls with exponential backoff

## Common Integration Defects and Mitigations

| Defect | Impact | Detection | Mitigation |
|--------|--------|-----------|------------|
| Data Not Synchronized | Inconsistent data | Synchronization monitoring, gap detection | Check connections, verify data flow, test synchronization |
| Duplicate Data | Data integrity issues | Duplicate detection, validation | Implement idempotency, use unique identifiers, deduplicate |
| Data Mismatch | Incorrect values | Data validation, comparison | Align data models, validate mappings, implement transformations |
| Version Conflict | Compatibility issues | Version checking, error logging | Align versions, implement compatibility layer, update systems |
| Authentication Error | Access denied | Authentication error logging | Verify credentials, check permissions, test authentication |
| Authorization Error | Operation denied | Authorization error logging | Verify roles, check permissions, test authorization |
| Timeout Error | Operation failure | Timeout monitoring, error logging | Increase timeouts, optimize processing, check network |
| Network Error | Communication failure | Network monitoring, error logging | Check network connectivity, verify firewalls, test communication |
| Database Error | Data access failure | Database monitoring, error logging | Verify database, check connections, test queries |
| Performance Issue | Slow processing | Performance monitoring, resource utilization | Optimize queries, tune batch sizes, improve data models |
| Memory Leak | System instability | Memory monitoring, performance degradation | Restart services, update software, check for known issues |
| License Error | Functionality limited | License monitoring, error logging | Verify licenses, check license servers, renew licenses |
| Master Data Out of Sync | Inconsistent references | Data validation, comparison | Implement synchronization, validate references, reconcile data |
| Transaction Conflict | Data integrity issues | Conflict detection, validation | Implement conflict resolution, use locking, sequence operations |

## Platform-Specific Patterns

### SAP ERP Integration

**Production Integration**:
- **Order to Cash**: Production order -> MES -> Goods receipt -> Invoice
- **Procure to Pay**: Purchase requisition -> PO -> Receipt -> Invoice -> Payment
- **Record to Report**: Transaction recording -> Period-end close -> Financial reporting

**Manufacturing Integration Points**:
- **CO (Production Planning)**: Production orders, confirmations
- **PP (Production Execution)**: Shop floor control, capacity planning
- **MM (Materials Management)**: Material masters, inventory, movements
- **FI (Financial Accounting)**: Cost centers, accounts, postings
- **CO (Controlling)**: Cost objects, overhead allocation
- **QM (Quality Management)**: Inspection results, certificates

**Best Practices**:
- Use BAPI for real-time integrations
- Use IDoc for batch data exchange
- Implement proper authorization using SAP roles
- Use SAP's Application Link Enabling (ALE) for distributed systems
- Leverage SAP's manufacturing industry solutions

### Oracle ERP Integration

**Manufacturing Integration Points**:
- **WIP (Work in Process)**: Production orders, discrete jobs
- **BOM (Bill of Materials)**: Product structures, components
- **INV (Inventory)**: Inventory tracking, movements
- **MTL (Material)**: Material transactions, on-hand quantities
- **PO (Purchase Orders)**: Procurement, receiving
- **GL (General Ledger)**: Financial transactions, accounting

**Best Practices**:
- Use PL/SQL for database-intensive operations
- Leverage Oracle Workflow for approval processes
- Use Oracle Advanced Supply Chain Planning (ASCP) for planning
- Implement proper data validation and error handling
- Use Oracle's Manufacturing Operations Center for shop floor integration

### Microsoft Dynamics 365 Integration

**Manufacturing Integration Points**:
- **Production Control**: Production orders, jobs, operations
- **Inventory Management**: Inventory tracking, warehouse management
- **Procurement and Sourcing**: Purchase requisitions, orders, receiving
- **Cost Management**: Standard costs, actual costs, variances
- **General Ledger**: Financial transactions, accounting
- **Project Management**: Project-based manufacturing

**Best Practices**:
- Use OData for standard data access
- Leverage Azure services for cloud integrations
- Use Power Platform for low-code integrations
- Implement proper security using Azure Active Directory
- Use Dynamics 365 Supply Chain Management for manufacturing

### Infor ERP Integration

**Manufacturing Integration Points**:
- **Shop Floor**: Production orders, operations, confirmations
- **Product Data**: BOMs, routings, work centers
- **Inventory**: Inventory tracking, warehouse management
- **Procurement**: Purchase orders, receiving
- **Financials**: General ledger, cost accounting

**Best Practices**:
- Use Infor's ION middleware for integrations
- Leverage Infor MES for shop floor execution
- Use Infor's industry-specific solutions
- Implement proper data validation and business rules
- Use Infor OS for cloud deployments

## Standing Rules

1. **Single Source of Truth**: Each piece of master data should have a single, authoritative source. ERP is typically the system of record for financial and commercial data.

2. **Data Ownership**: Clearly define which system owns which data. ERP typically owns financial, commercial, and master data; MES owns shop floor execution data.

3. **Synchronization Strategy**: Define clear synchronization strategies for each data type - real-time, batch, or on-demand. Document synchronization frequencies and methods.

4. **Idempotency**: Design all integrations to be idempotent. The same transaction processed multiple times should have the same result as processed once.

5. **Error Handling**: Implement comprehensive error handling and recovery mechanisms. All errors should be logged, monitored, and handled appropriately.

6. **Data Validation**: Validate all data before and after transmission. Implement validation at the source, during transmission, and at the destination.

7. **Performance by Design**: Design for performance from the beginning. Consider data volumes, frequencies, and the capabilities of all systems involved.

8. **Security by Design**: Implement appropriate security measures for all integrations - encryption, authentication, authorization, and audit logging.

9. **Monitor Everything**: Monitor all critical aspects of the integration - data flow, data quality, performance, security, and system availability.

10. **Document Everything**: Document all integration designs, configurations, mappings, and procedures for maintenance, troubleshooting, and compliance.
