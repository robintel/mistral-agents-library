# SafeRTOS platform contract

Attaches alongside `patterns/rtos.md`, `patterns/embedded.md`, and
`platforms/rtos/freertos.md`. SafeRTOS is a safety-certified variant of
FreeRTOS designed for safety-critical applications. The era is the
SafeRTOS version plus the certification profile; both are named by
the project's configuration.

## Overview

SafeRTOS is a derivative of FreeRTOS that adds safety mechanisms and
certifications for use in safety-critical applications. It maintains the
same API as FreeRTOS but adds additional features and restrictions to
meet the requirements of various safety standards.

- **Base**: FreeRTOS kernel with safety enhancements
- **License**: Commercial (paid license required for certified use)
- **Source**: https://www.safertos.com/ (formerly from WITTENSTEIN)
- **Maintainer**: WITTENSTEIN high integrity systems (acquired from FreeRTOS
  contributors)
- **Architectures**: All architectures supported by FreeRTOS
- **Certifications**: IEC 61508 (SIL 3), ISO 26262 (ASIL D), EN 50128,
  IEC 62304, DO-178C (Level A)

## Eras

SafeRTOS versions track FreeRTOS versions with additional safety
enhancements:

- **SafeRTOS V7.x**: Based on FreeRTOS V7.x with safety enhancements
- **SafeRTOS V8.x**: Based on FreeRTOS V8.x with additional features
- **SafeRTOS V9.x**: Based on FreeRTOS V9.x
- **SafeRTOS V10.x**: Based on FreeRTOS V10.x (current)

**Certification eras**:
- **SIL 3 (IEC 61508)**: Safety Integrity Level 3 for industrial applications
- **ASIL D (ISO 26262)**: Automotive Safety Integrity Level D
- **EN 50128**: Railway applications
- **IEC 62304**: Medical device software
- **DO-178C Level A**: Avionics software

**Configuration era**: Like FreeRTOS, `FreeRTOSConfig.h` defines the
configuration. SafeRTOS adds additional safety-related configuration
options.

## Relationship to FreeRTOS

SafeRTOS is **source-code compatible** with FreeRTOS for most applications:

- **Same API**: Function names, parameters, and behavior are the same
- **Same configuration**: Uses `FreeRTOSConfig.h` with additional options
- **Additional features**: Memory protection, task isolation, monitoring
- **Restrictions**: Some FreeRTOS features are restricted or disabled
  in SafeRTOS for safety reasons
- **Additional checks**: Runtime checks for safety violations

**Migration path**: Most FreeRTOS applications can be migrated to SafeRTOS
with minimal changes, primarily related to additional configuration and
the safety features.

## Safety mechanisms

SafeRTOS adds several safety mechanisms on top of FreeRTOS:

### Memory Protection Unit (MPU) support

- **Per-task MPU regions**: Each task can have its own MPU configuration
- **Memory isolation**: Tasks can be isolated from each other via MPU
- **MPU fault handling**: SafeRTOS provides MPU fault handlers that
  can be customized
- **Stack protection**: MPU can be configured to protect task stacks
- **Memory region access control**: Control access to memory regions
  (RAM, flash, peripherals) per task

### Task isolation

- **Isolated tasks**: Tasks can be configured as isolated, preventing
  them from accessing memory outside their allowed regions
- **Isolation levels**: Different levels of isolation depending on
  safety requirements
- **Safe task creation**: Additional checks when creating isolated tasks
- **Isolation verification**: SafeRTOS verifies isolation at runtime

### Monitoring and checking

- **Runtime monitoring**: Monitors for safety violations (stack overflow,
  MPU faults, illegal API calls)
- **Error detection**: Detects errors that FreeRTOS might not (e.g.,
  using API from wrong context)
- **Error reporting**: Reports errors to a configurable error handler
- **Watchdog integration**: Enhanced watchdog support with safety monitoring

### Deterministic timing

- **Bounded execution**: Ensures operations have bounded execution times
- **Timing analysis**: SafeRTOS is designed to support timing analysis
- **Interrupt latency**: Bounded interrupt latency for predictable behavior
- **Context switch time**: Deterministic context switch times

### Safety certification artifacts

- **Certification reports**: Full certification reports for each standard
- **Safety manuals**: Comprehensive safety manuals
- **Test reports**: Test reports demonstrating compliance
- **Tool qualification**: Qualified development tools

## Configuration

SafeRTOS uses the same `FreeRTOSConfig.h` as FreeRTOS but adds
additional safety-related configuration options.

### Core safety configuration

```c
// Enable SafeRTOS safety features
#define configENABLE_SAFERTOS                    1

// Enable MPU support
#define configENABLE_MPU                        1

// Enable task isolation
#define configENABLE_TASK_ISOLATION             1

// Maximum number of isolated tasks
#define configMAX_ISOLATED_TASKS               8

// Enable runtime monitoring
#define configENABLE_MONITORING                 1

// Enable error detection
#define configENABLE_ERROR_DETECTION             1

// Enable memory protection
#define configENABLE_MEMORY_PROTECTION          1
```

### MPU configuration

```c
// MPU region definitions for each task
#define configMPU_REGION_0_BASE                 0x20000000
#define configMPU_REGION_0_SIZE                 0x00010000
#define configMPU_REGION_0_ACCESS               (portMPU_REGION_ACCESS_RW)

// Task-specific MPU configurations
#define configTASK_1_MPU_REGIONS               { \
    { configMPU_REGION_0_BASE, configMPU_REGION_0_SIZE, configMPU_REGION_0_ACCESS }, \
    { configMPU_REGION_1_BASE, configMPU_REGION_1_SIZE, configMPU_REGION_1_ACCESS } \
}
```

### Task isolation configuration

```c
// Define isolated task properties
#define configISOLATED_TASK_1_PRIORITY          3
#define configISOLATED_TASK_1_STACK_SIZE        1024
#define configISOLATED_TASK_1_MPU_REGIONS       configTASK_1_MPU_REGIONS

// Number of MPU regions per task
#define configMAX_MPU_REGIONS_PER_TASK         8
```

### Monitoring configuration

```c
// Enable stack overflow detection
#define configCHECK_FOR_STACK_OVERFLOW         2

// Enable MPU fault detection
#define configENABLE_MPU_FAULT_HANDLER           1

// Enable API usage checking
#define configENABLE_API_USAGE_CHECKING          1

// Error handler configuration
#define configSAFERTOS_ERROR_HANDLER            vSafeRTOSErrorHandler
```

### Memory configuration

```c
// Memory protection for critical sections
#define configENABLE_MPU_IN_CRITICAL_SECTIONS    1

// Heap protection
#define configENABLE_HEAP_PROTECTION             1
```

## Core API (SafeRTOS-specific)

SafeRTOS maintains the same API as FreeRTOS but adds some safety-specific
functions and modifies the behavior of some existing functions.

### Task management (enhanced)

```c
// Create an isolated task (SafeRTOS extension)
BaseType_t xSafeTaskCreateIsolated(
    TaskFunction_t pxTaskCode,
    const char * const pcName,
    configSTACK_DEPTH_TYPE usStackDepth,
    void *pvParameters,
    UBaseType_t uxPriority,
    TaskHandle_t *pxCreatedTask,
    const xMPU_SETTINGS *pxMPUSettings,
    const struct xMemoryRegion * const pxRegions
);

// Set task isolation level (SafeRTOS extension)
BaseType_t xTaskSetIsolationLevel(TaskHandle_t xTask, uint32_t ulIsolationLevel);

// Get task isolation level (SafeRTOS extension)
UBaseType_t uxTaskGetIsolationLevel(TaskHandle_t xTask);
```

### MPU management

```c
// Set MPU regions for a task
void vTaskSetMPURegions(TaskHandle_t xTask, const xMPU_SETTINGS *pxMPUSettings, const struct xMemoryRegion * const pxRegions);

// Get MPU regions for a task
void vTaskGetMPURegions(TaskHandle_t xTask, xMPU_SETTINGS *pxMPUSettings, struct xMemoryRegion *pxRegions);

// Enable MPU
void vMPUEnable(void);

// Disable MPU
void vMPUDisable(void);
```

### Error handling

```c
// SafeRTOS error handler type
typedef void (*SafeRTOSErrorHandler_t)(SafeRTOSError_t *pxError);

// Default error handler (can be overridden)
void vSafeRTOSErrorHandler(SafeRTOSError_t *pxError);

// Set custom error handler
void vSafeRTOSSetErrorHandler(SafeRTOSErrorHandler_t pxHandler);

// Error types
typedef enum {
    eSafeRTOSErrorNone = 0,
    eSafeRTOSErrorMPUFault,
    eSafeRTOSErrorStackOverflow,
    eSafeRTOSErrorIllegalAPICall,
    eSafeRTOSErrorMemoryAccessViolation,
    eSafeRTOSErrorTaskIsolationViolation,
    eSafeRTOSErrorConfigError
} eSafeRTOSErrorType;

// Error information structure
typedef struct SafeRTOSError {
    eSafeRTOSErrorType eErrorType;
    TaskHandle_t xTaskHandle;
    uint32_t ulErrorValue;
    const char *pcMessage;
} SafeRTOSError_t;
```

### Monitoring functions

```c
// Check for stack overflow (enhanced)
BaseType_t xTaskCheckForStackOverflow(TaskHandle_t xTask, uint32_t *pulOverflowedBy);

// Get MPU fault information
BaseType_t xMPUGetFaultInformation(xMPU_FaultInfo_t *pxFaultInfo);

// Check API usage validity
BaseType_t xSafeRTOSCheckAPIUsage(uint32_t ulAPI, uint32_t ulContext);
```

## Safety features in detail

### Memory Protection Unit (MPU) support

SafeRTOS provides comprehensive MPU support:

- **Per-task MPU regions**: Each task can have its own MPU configuration
- **Region definitions**: MPU regions define base address, size, and
  access permissions (read, write, execute)
- **Region overlap**: SafeRTOS checks for region overlaps and reports
  errors if found
- **Dynamic MPU updates**: MPU regions can be updated at runtime
- **MPU fault handlers**: Customizable handlers for MPU faults

Example MPU region definition:
```c
const struct xMemoryRegion xTask1Regions[] = {
    { 0x20000000, 0x00010000, portMPU_REGION_ACCESS_RW },  // RAM for task 1
    { 0x08000000, 0x00020000, portMPU_REGION_ACCESS_RX },  // Flash for task 1
    { 0x40000000, 0x00001000, portMPU_REGION_ACCESS_RW }   // Peripheral registers
};
```

### Task isolation levels

SafeRTOS defines several levels of task isolation:

- **Level 0 - No isolation**: Standard FreeRTOS task, no MPU protection
- **Level 1 - Basic isolation**: MPU protection enabled, basic checks
- **Level 2 - Medium isolation**: Level 1 + restricted API access
- **Level 3 - Full isolation**: Level 2 + complete memory isolation,
  no access to other tasks' memory

Isolation level affects:
- Which APIs the task can call
- Memory access permissions
- Whether the task can be preempted
- Whether the task can access shared resources

### Runtime monitoring

SafeRTOS monitors for various safety violations:

- **Stack overflow**: Detects when a task's stack pointer exceeds
  the stack boundary
- **MPU faults**: Detects memory protection violations
- **Illegal API calls**: Detects API calls from wrong context (e.g.,
  blocking call from ISR)
- **Memory access violations**: Detects attempts to access protected
  memory regions
- **Task isolation violations**: Detects attempts by isolated tasks
  to access restricted resources
- **Timing violations**: Detects when tasks miss their deadlines

### Error reporting

When SafeRTOS detects a safety violation:

1. **Error information captured**: Type, task, error value, message
2. **Error handler called**: Customizable error handler function
3. **System action**: Based on configuration, can:
   - Log the error
   - Suspend the offending task
   - Trigger a system reset
   - Enter a safe state
4. **Error recovery**: Application can implement recovery logic in
   the error handler

Example error handler:
```c
void vApplicationErrorHandler(SafeRTOSError_t *pxError)
{
    switch(pxError->eErrorType)
    {
        case eSafeRTOSErrorMPUFault:
            // Log MPU fault
            vLogError("MPU Fault in task %s", pxTaskGetName(pxError->xTaskHandle));
            // Suspend the task
            vTaskSuspend(pxError->xTaskHandle);
            break;
            
        case eSafeRTOSErrorStackOverflow:
            // Log stack overflow
            vLogError("Stack overflow in task %s", pxTaskGetName(pxError->xTaskHandle));
            // Enter safe state
            vEnterSafeState();
            break;
            
        default:
            // Handle other errors
            break;
    }
}
```

### Memory protection

SafeRTOS provides several layers of memory protection:

- **MPU-based protection**: Hardware-enforced memory protection
- **Software checks**: Runtime checks for memory access violations
- **Heap protection**: Protection of heap memory from corruption
- **Stack protection**: Protection of task stacks from overflow and
  from access by other tasks
- **Critical section protection**: Protection during critical sections

## Development ecosystem

### Supported platforms

SafeRTOS supports all platforms that FreeRTOS supports, with additional
safety certification for specific platforms:

- **ARM Cortex-M**: Most common, with comprehensive MPU support
  - Cortex-M0/M0+: Basic MPU support
  - Cortex-M3/M4/M7: Full MPU support with up to 16 regions
  - Cortex-M23/M33: TrustZone support for enhanced security
- **ARM Cortex-R**: For high-reliability applications
- **x86**: For PC/104 and other x86 platforms
- **MIPS**: For MIPS-based safety-critical systems
- **PowerPC**: For PowerPC-based safety-critical systems
- **RISC-V**: Growing support for RISC-V with MPU

### Certification packages

SafeRTOS provides certification packages for various standards:

- **IEC 61508 SIL 3**: Industrial functional safety
- **ISO 26262 ASIL D**: Automotive functional safety
- **EN 50128**: Railway applications
- **IEC 62304**: Medical device software
- **DO-178C Level A**: Avionics software

Each package includes:
- **Certification report**: Detailed report from certification body
- **Safety manual**: Comprehensive safety manual for developers
- **Test reports**: Reports demonstrating compliance with requirements
- **Tool qualification**: Documentation for tool qualification

### IDE support

- **SafeRTOS for IAR Embedded Workbench**: Full integration
- **SafeRTOS for Keil MDK**: Full integration
- **SafeRTOS for Tasking**: Eclipse-based IDE
- **SafeRTOS for VS Code**: Extensions available
- **SafeRTOS for Segger Embedded Studio**: Full integration

### Debugging tools

- **TraceX**: Runtime analysis with SafeRTOS awareness
- **SafeRTOS View**: Safety-specific visualization tool
- **J-Link**: Full support with SafeRTOS awareness
- **Lauterbach Trace32**: Professional debugging with SafeRTOS support
- **SEGGER SystemView**: RTOS-aware debugging

### Testing

- **SafeRTOS test suite**: Comprehensive test suite for safety verification
- **Back-to-back testing**: FreeRTOS vs SafeRTOS behavior comparison
- **Fault injection**: Inject faults to verify error detection
- **Stress testing**: Heavy load testing to verify stability
- **Certification testing**: Testing required for safety certification

## Migration from FreeRTOS

### Migration path

1. **Replace FreeRTOS source files**: Replace FreeRTOS source files
   with SafeRTOS source files
2. **Update FreeRTOSConfig.h**: Add SafeRTOS-specific configuration
   options
3. **Review API usage**: Check for any API usage that might be
   restricted in SafeRTOS
4. **Add safety features**: Configure MPU, task isolation, monitoring
5. **Implement error handler**: Provide error handler for safety violations
6. **Test thoroughly**: Verify all functionality and safety features
7. **Certify**: Work with certification body for final certification

### Compatibility matrix

| FreeRTOS Feature | SafeRTOS Support | Notes |
|-----------------|-----------------|-------|
| Basic scheduling | Full | Same behavior |
| Tasks | Full | With isolation options |
| Queues | Full | With monitoring |
| Semaphores | Full | With monitoring |
| Mutexes | Full | With priority inheritance |
| Timers | Full | With monitoring |
| Memory management | Full | With heap protection |
| ISR functions | Full | With additional checks |
| MPU | Enhanced | Per-task MPU regions |
| Task isolation | New | SafeRTOS-specific |
| Runtime monitoring | New | SafeRTOS-specific |
| Error handling | Enhanced | Customizable handlers |

### Breaking changes

SafeRTOS introduces minimal breaking changes:

- **Additional configuration**: Some configuration options are required
- **API restrictions**: Some API calls may be restricted based on context
- **Behavior differences**: Some functions may have additional checks
  that affect behavior
- **Error reporting**: Errors that FreeRTOS might ignore are reported
  in SafeRTOS

## Common pitfalls

- **Insufficient MPU regions**: not enough MPU regions to implement
  required isolation. Cortex-M3/M4 have 8-16 regions depending on
  variant. Plan carefully.
- **Overlapping MPU regions**: MPU regions that overlap can cause
  unexpected behavior. SafeRTOS checks for overlaps but application
  must design regions correctly.
- **Incorrect isolation level**: setting isolation level too high
  can cause application to fail. Start with lower levels and increase
  as needed.
- **Missing error handler**: not providing an error handler causes
  default behavior (typically system halt). Always provide an error
  handler for production systems.
- **Ignoring error reports**: SafeRTOS reports many errors that
  FreeRTOS might not. Application must handle these errors appropriately.
- **Stack size too small**: SafeRTOS monitoring uses some stack space.
  Increase stack sizes from FreeRTOS sizes.
- **MPU fault handler not implemented**: MPU faults can cause system
  reset if not handled. Always implement MPU fault handler.
- **Incorrect MPU permissions**: setting wrong permissions can cause
  application to fail. Verify permissions for each region.
- **Task priorities not matching safety requirements**: safety-critical
  tasks must have appropriate priorities. Design carefully.
- **Not testing safety features**: Safety features must be tested
  thoroughly. Include fault injection testing.

## Best practices

- **Start with minimal isolation**: Begin with Level 0 (no isolation)
  and increase isolation levels as needed for safety requirements.
- **Design MPU regions carefully**: Plan memory layout to fit within
  available MPU regions. Group related memory together.
- **Use isolation for safety-critical tasks**: Isolate safety-critical
  tasks from non-critical tasks to prevent interference.
- **Implement comprehensive error handling**: Handle all error types
  appropriately. Log errors, take corrective action, enter safe state.
- **Test fault conditions**: Inject faults (MPU violations, stack
  overflows) to verify error detection and handling.
- **Document safety design**: Document all safety-related design
  decisions, including isolation levels, MPU regions, error handling.
- **Use SafeRTOS monitoring**: Enable all monitoring features during
  development and testing. Consider which to enable in production.
- **Validate configuration**: Use SafeRTOS configuration tools to
  validate configuration for target certification level.
- **Work with certification body**: Engage certification body early
  in development process to ensure compliance.
- **Maintain traceability**: Maintain traceability between requirements,
  design, implementation, and testing for certification.
- **Use certified tools**: Ensure all development tools are certified
  for the target safety level.
- **Perform safety analysis**: Perform FMEA (Failure Modes and Effects
  Analysis), FTA (Fault Tree Analysis), and other safety analyses.

## Safety design patterns

### Partitioning

- **Temporal partitioning**: Separate safety-critical and non-critical
  tasks into different time slices or priorities
- **Spatial partitioning**: Use MPU to separate memory access between
  tasks
- **Functional partitioning**: Separate functions into different tasks
  based on safety requirements

### Monitor task

- **Dedicated monitor task**: Separate task that monitors system
  health and safety
- **Periodic checks**: Monitor task runs periodically to check
  system state
- **Error collection**: Collect and log errors from various sources
- **Safe state entry**: Trigger safe state when errors detected

### Watchdog

- **Hardware watchdog**: External hardware watchdog for system-level
  monitoring
- **Software watchdog**: Internal watchdog for task-level monitoring
- **Dual watchdog**: Both hardware and software watchdogs for
  redundancy
- **Watchdog feeding**: Dedicated task feeds watchdog. Never feed from
  ISR or critical sections.

### Graceful degradation

- **Error recovery**: Implement recovery mechanisms for detected errors
- **Safe state**: Define and implement safe state for system to enter
  on critical errors
- **Redundancy**: Implement redundant functions for critical operations
- **Fallback modes**: Implement fallback modes when primary functions
  fail

## Integration patterns

### With safety-critical applications

- **Mixed-criticality**: Run safety-critical and non-critical tasks on
  same processor with appropriate isolation
- **Safety monitor**: Dedicated core or processor running safety
  monitor that watches over application processor
- **Lockstep processors**: Run same code on two processors in
  lockstep for error detection
- **Diverse redundancy**: Run different implementations of same
  function for comparison

### With FreeRTOS applications

- **Gradual migration**: Migrate tasks one at a time to SafeRTOS
- **Hybrid systems**: Run some tasks under FreeRTOS and some under
  SafeRTOS (not typical, requires careful design)
- **Configuration inheritance**: Start with FreeRTOS configuration and
  add SafeRTOS features

### With hardware safety features

- **MPU integration**: Configure MPU to work with SafeRTOS isolation
- **TrustZone**: On Cortex-M33/M35P, use TrustZone for additional
  security and safety
- **Error Correction Code (ECC)**: Use memory with ECC for detecting
  and correcting memory errors
- **Hardware watchdog**: Integrate with SafeRTOS error handling

## Testing strategies

### Safety testing

- **Fault injection**: Inject hardware faults (MPU violations, bus
  errors) to verify detection and handling
- **Software fault injection**: Inject software faults (stack overflow,
  illegal API calls) to verify detection
- **Stress testing**: Run system under heavy load to verify stability
- **Boundary testing**: Test at boundaries of configuration (maximum
  tasks, maximum priorities, etc.)
- **Timing testing**: Verify timing requirements are met under all
  conditions

### Certification testing

- **Requirements-based testing**: Test all requirements from safety
  standard
- **Back-to-back testing**: Compare SafeRTOS behavior with FreeRTOS
  to ensure compatibility
- **Regression testing**: Run full test suite after any changes
- **Integration testing**: Test integration with other system components
- **System testing**: Test complete system under various conditions

### Performance testing

- **WCET testing**: Measure worst-case execution times
- **Interrupt latency testing**: Measure interrupt latency under
  various conditions
- **Context switch testing**: Measure context switch times
- **Memory usage testing**: Measure and verify memory usage
- **Timing analysis**: Perform timing analysis to verify real-time
  requirements

## Performance optimization

- **Minimize isolation overhead**: Use lowest isolation level that
  meets safety requirements
- **Optimize MPU regions**: Design MPU regions to minimize overhead
  and maximize coverage
- **Static allocation**: Use static allocation for all objects to avoid
  dynamic allocation overhead
- **Minimize monitoring overhead**: Enable only necessary monitoring
  features in production
- **Preemptibility**: Design tasks to minimize unnecessary preemption
- **Use appropriate priorities**: Don't use too many priority levels
- **Optimize error handler**: Keep error handler fast and minimal

## Certification process

### Steps to certification

1. **Define safety requirements**: Identify safety goals and
   requirements from applicable standard
2. **Perform hazard analysis**: Identify hazards and assign Safety
   Integrity Levels (SIL) or Automotive Safety Integrity Levels (ASIL)
3. **Design safety architecture**: Design system architecture to
   meet safety requirements
4. **Implement SafeRTOS**: Configure and integrate SafeRTOS with
   appropriate safety features
5. **Develop application**: Implement application with safety
   considerations
6. **Perform testing**: Execute comprehensive test suite
7. **Perform safety analysis**: Perform FMEA, FTA, and other analyses
8. **Prepare documentation**: Prepare all documentation required for
   certification
9. **Work with certification body**: Submit evidence to certification
   body for review
10. **Address findings**: Address any findings from certification body
11. **Receive certification**: Receive final certification

### Documentation required

- **Safety manual**: Document all safety-related aspects of SafeRTOS
- **Safety requirements specification**: Document all safety requirements
- **Safety design description**: Document safety design
- **Safety verification report**: Document verification activities and results
- **Safety case**: Overall argument for safety
- **Configuration management**: Document all configuration items
- **Test reports**: Detailed test reports
- **Analysis reports**: Reports from safety analyses

### Working with certification body

- **Early engagement**: Engage certification body early in process
- **Regular reviews**: Schedule regular reviews to catch issues early
- **Evidence collection**: Collect and organize all evidence required
  for certification
- **Traceability**: Maintain traceability between requirements, design,
  implementation, and testing
- **Address findings**: Address all findings from certification body
  promptly and thoroughly

## Common use cases

- **Industrial automation**: PLCs, motor controllers, HMIs in
  safety-critical industrial applications
- **Medical devices**: Patient monitors, infusion pumps, ventilators,
  surgical robots
- **Automotive**: ECUs for powertrain, chassis, ADAS, autonomous driving
  (ASIL D applications)
- **Aviation**: Flight control, avionics systems (DO-178C Level A)
- **Railway**: Signaling, train control systems (EN 50128)
- **Energy**: Nuclear power plant control, smart grid applications
- **Transportation**: Railway signaling, marine control systems
- **Defense**: Military applications requiring high reliability

## Alternatives and when to use them

- **FreeRTOS**: When safety certification is not required. FreeRTOS
  provides the same core functionality without safety overhead.
- **SafeRTOS**: When safety certification is required. SafeRTOS adds
  safety features and provides certification packages.
- **ThreadX**: When need commercial support, industrial features, or
  other Azure RTOS components. ThreadX has its own safety-certified
  versions.
- **QNX**: When need POSIX compliance, microkernel architecture,
  or comprehensive safety ecosystem. QNX is certified for various
  standards.
- **VxWorks**: When need comprehensive safety ecosystem, extensive
  certifications, or defense/aerospace applications.
- **Bare metal with MPU**: When RTOS overhead unacceptable but need
  memory protection. Requires implementing all safety features manually.

## Resources

- **Official website**: https://www.safertos.com/
- **Documentation**: Available from WITTENSTEIN
- **FreeRTOS compatibility**: https://www.freertos.org/
- **Certification reports**: Available from WITTENSTEIN (under NDA)
- **Safety manuals**: Available from WITTENSTEIN (under NDA)
- **API reference**: Same as FreeRTOS plus SafeRTOS extensions
- **Support**: Commercial support available from WITTENSTEIN
- **Training**: Training available from WITTENSTEIN
- **Community**: Limited community due to commercial nature
- **GitHub**: Some open-source projects use SafeRTOS (check licenses)
