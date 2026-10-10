# VxWorks platform contract

Attaches alongside `patterns/rtos.md` and `patterns/embedded.md`.
A commercial, high-performance RTOS from Wind River designed for
demanding embedded applications in industrial, aerospace, defense,
and medical markets. The era is the VxWorks version plus the BSP;
both are named by the project's configuration.

## Overview

VxWorks is a deterministic, priority-based preemptive RTOS with a
comprehensive set of features for embedded systems. It was originally
developed by Wind River Systems (founded 1981) and acquired by Intel
in 2009, then by TPG Capital in 2018. Wind River is now an independent
company again.

- **Architecture**: Monolithic kernel with loadable modules
- **License**: Commercial (proprietary)
- **Source**: https://www.windriver.com/
- **Maintainer**: Wind River Systems
- **Architectures**: ARM (Cortex-A/R/M), x86 (32-bit and 64-bit), PowerPC,
  MIPS, SPARC, RISC-V, and more
- **Certifications**: DO-178C Level A, IEC 61508 SIL 4, ISO 26262 ASIL D,
  EN 50128, IEC 62304, Common Criteria EAL6+

## Eras

VxWorks has a long history with several major versions:

- **VxWorks 5.x**: Classic era (1990s-early 2000s), widely used in
  aerospace and defense
- **VxWorks 6.x**: Major redesign with Workbench IDE, modular
  architecture (2000s-2010s)
- **VxWorks 7**: Modern era with enhanced security, virtualization,
  and multi-core support (2012+)
- **VxWorks 22.03**: Current LTS (Long-Term Support) version (as of 2024)
- **VxWorks 23.x**: Latest versions with new features

**BSP (Board Support Package) era**: The BSP provides the interface
between VxWorks and specific hardware. BSP versions often track
VxWorks versions but can be updated independently.

**Kernel variants**:
- **Standard kernel**: For most applications
- **VxWorks 653**: Multi-partition OS for ARINC 653 compliance (aviation)
- **VxWorks Cert**: Certified version for safety-critical applications
- **VxWorks MILS**: Multiple Independent Levels of Security for
  high-security applications
- **VxWorks SBC**: Small Binary Component for resource-constrained systems

## Architecture

### Kernel design

VxWorks uses a **monolithic kernel** design with the following components:

- **Kernel**: Scheduling, memory management, intertask communication,
  interrupt handling
- **I/O system**: Device drivers, file systems
- **Networking**: TCP/IP stack, protocols
- **Loadable modules**: Dynamic loading of kernel modules
- **Real-time extensions**: Additional real-time capabilities

The kernel provides:
- **Deterministic behavior**: Predictable timing for real-time operations
- **Priority-based scheduling**: Preemptive scheduling with 256 priority
  levels (0-255)
- **Fast interrupt handling**: Efficient interrupt response
- **Memory protection**: Optional memory management unit (MMU) support
- **Task isolation**: Separation between tasks for reliability

### Key features

- **Wind Microkernel**: Core real-time kernel
- **Real-Time Process (RTP)**: User-space processes with real-time
  capabilities
- **Kernel modules**: Dynamically loadable kernel modules
- **Device drivers**: Extensive library of device drivers
- **File systems**: Multiple file system options
- **Networking**: Full TCP/IP stack with advanced features
- **Synchronization**: Rich set of synchronization primitives
- **Timers**: Software and hardware timers
- **Interrupt handling**: Comprehensive interrupt management
- **Memory management**: Various memory allocation schemes
- **Error handling**: Comprehensive error detection and handling

## Idiom and best practices

- **Tasks are the unit of execution**: Each task has its own stack,
  priority, and entry function
- **Everything is a task**: Even system services run as tasks
- **Kernel extensions**: VxWorks can be extended with custom kernel
  modules
- **RTPs for user space**: Real-Time Processes provide user-space
  execution with real-time capabilities
- **Loadable modules**: Kernel functionality can be added dynamically
- **Interrupts are tasks**: Interrupt Service Routines (ISRs) are
  special tasks
- **Message queues are primary IPC**: Message queues are the primary
  mechanism for intertask communication
- **Error handlers**: Comprehensive error detection and handling

## Core concepts

### Task management

- **Task**: Basic execution unit with its own context
- **Task states**: READY, RUNNING, PENDING, SUSPENDED, DELETED
- **Task priority**: 0 (highest) to 255 (lowest). Lower number = higher
  priority
- **Task options**: Various options for task creation (stack size,
  priority, floating point usage, etc.)
- **Task ID**: Unique identifier for each task
- **Task name**: Human-readable name for debugging

### Memory management

- **Partition allocation**: Fixed-size memory partitions for
  deterministic allocation
- **Heap allocation**: Variable-size allocation from heap
- **MMU support**: Memory Management Unit for memory protection
  and virtual memory
- **Shared memory**: Memory shared between tasks or processes
- **Memory mapping**: Mapping of memory regions

### Synchronization

- **Semaphores**: Binary and counting semaphores
- **Mutexes**: Mutual exclusion with priority inheritance
- **Message queues**: FIFO message passing between tasks
- **Event flags**: 32-bit event signaling within a task
- **Barriers**: Synchronization point for multiple tasks
- **Watchdogs**: Software watchdog timers

### Intertask communication

- **Message queues**: Primary mechanism for intertask communication
- **Pipes**: Stream-based communication
- **Sockets**: Network-based communication
- **Shared memory**: Direct memory sharing
- **Signals**: Event notification (VxWorks 7+)

### Interrupt handling

- **Interrupt Service Routines (ISRs)**: Special tasks that run in
  response to hardware interrupts
- **Interrupt vectors**: Mapping of hardware interrupts to ISRs
- **Interrupt nesting**: Support for nested interrupts
- **Interrupt masking**: Disabling/enabling specific interrupts
- **Interrupt latency**: Measured and optimized for real-time performance

### Timing

- **System clock**: Global system time
- **Hardware timers**: Various timer sources
- **Software timers**: Kernel-managed timers
- **Watchdog timers**: Hardware and software watchdogs
- **Tick timing**: System tick (typically 60-1000 Hz)

## Configuration

VxWorks is configured through several mechanisms:

### Kernel configuration

The kernel is configured through the **VxWorks Image Configuration**
(VSB - VxWorks System Builder):

```c
// Example kernel configuration in VSB
// Kernel Components
INCLUDE_KERNEL
INCLUDE_TASK_LIB
INCLUDE_SEM_LIB
INCLUDE_MSG_Q_LIB
INCLUDE_INT_LIB
INCLUDE_TIMER_LIB

// Memory Configuration
NUM_MEMORY_PARTITIONS = 3
MEM_PARTITION_SIZE_1 = 0x100000  // 1MB
MEM_PARTITION_SIZE_2 = 0x200000  // 2MB
MEM_PARTITION_SIZE_3 = 0x400000  // 4MB

// Task Configuration
MAX_TASKS = 128
MAX_PRIORITIES = 256
MAX_TASK_NAME_LEN = 32

// Synchronization Configuration
MAX_SEM_ID = 256
MAX_MSG_Q_ID = 256
MAX_EVENT_POINTS = 256
```

### Project configuration

Project-specific configuration in **config.h** or via VSB:

```c
// Task configuration
#define MAX_TASKS          128
#define MAX_PRIORITIES      256
#define MAX_TASK_NAME_LEN   32

// Memory configuration
#define NUM_MEMORY_PARTITIONS  5
#define MEM_PARTITION_SIZE_1  0x100000

// Semaphore configuration
#define MAX_SEM_ID          256

// Message queue configuration
#define MAX_MSG_Q_ID        256
#define MAX_MSG_Q_MESSAGES  1024

// Timer configuration
#define MAX_TIMERS          64

// Interrupt configuration
#define MAX_INT_SRC        256
#define MAX_INT_CONNECT    256
```

### BSP configuration

Board Support Package configuration:

```c
// Memory layout
#define RAM_LOW_ADRS      0x80000000
#define RAM_HIGH_ADRS      0x81FFFFFFF
#define ROM_BASE_ADRS      0x00000000
#define ROM_END_ADRS       0x007FFFFF

// Interrupt controller
#define INT_CTRL_TYPE      INTC_TYPE_VIC
#define INT_CTRL_BASE       0xFFFFF000

// System clock
#define SYS_CLK_RATE       100000000  // 100 MHz
```

## Core API

### Task management

```c
// Task entry function
typedef void (*FUNCPTR)(int arg1, int arg2, ..., int arg10);

// Task ID type
typedef int STATUS;
typedef int TASK_ID;

// Create a task
TASK_ID taskSpawn(
    const char *name,      // Task name
    int priority,          // Priority (0-255, lower is higher)
    int options,           // Task options (VX_FP_TASK, VX_PRIVATE_MEM, etc.)
    int stackSize,         // Stack size in bytes
    FUNCPTR entryPt,       // Entry function
    int arg1, int arg2, ..., int arg10  // Arguments (up to 10)
);

// Task options
#define VX_FP_TASK          0x01    // Task uses floating point
#define VX_PRIVATE_MEM      0x02    // Task has private memory
#define VX_UNBREAKABLE      0x04    // Task cannot be deleted
#define VX_NO_STACK_FILL    0x08    // Don't fill stack with pattern

// Task services
STATUS taskDelete(TASK_ID taskId);
STATUS taskSuspend(TASK_ID taskId);
STATUS taskResume(TASK_ID taskId);
STATUS taskPrioritySet(TASK_ID taskId, int newPriority);
STATUS taskPriorityGet(TASK_ID taskId, int *pPriority);
STATUS taskNameGet(TASK_ID taskId, char *pName, int maxLen);
STATUS taskIdSelf(void);
STATUS taskIdVerify(TASK_ID taskId);

// Task delay
STATUS taskDelay(int ticks);
STATUS taskDelaySys(int ticks);  // System delay (not affected by time slice)

// Task information
STATUS taskInfoGet(TASK_ID taskId, TASK_DESC *pTaskDesc);
```

### Synchronization primitives

```c
// Semaphore
SEM_ID semBinaryCreate(int options, int initialState);
SEM_ID semCountingCreate(int options, int initialCount);
STATUS semTake(SEM_ID semId, int timeout);
STATUS semGive(SEM_ID semId);
STATUS semDelete(SEM_ID semId);

// Semaphore options
#define SEM_Q_PRIORITY     0x00    // Priority queuing
#define SEM_Q_FIFO         0x01    // FIFO queuing
#define SEM_DELETE_SAFE    0x02    // Safe delete (wait for all tasks)
#define SEM_INVERSION_SAFE 0x04    // Prevent priority inversion

// Mutex
SEM_ID mutexCreate(int options);
STATUS mutexTake(SEM_ID mutexId, int timeout);
STATUS mutexGive(SEM_ID mutexId);
STATUS mutexDelete(SEM_ID mutexId);

// Message queue
MSG_Q_ID msgQCreate(int maxMsgs, int maxMsgLength, int options);
STATUS msgQSend(MSG_Q_ID queueId, char *buffer, int nBytes, int timeout, int priority);
STATUS msgQReceive(MSG_Q_ID queueId, char *buffer, int maxNBytes, int timeout);
STATUS msgQNumMsgsGet(MSG_Q_ID queueId, int *pNumMsgs);
STATUS msgQDelete(MSG_Q_ID queueId);

// Message queue options
#define MSG_Q_PRIORITY     0x00    // Priority message queue
#define MSG_Q_FIFO         0x01    // FIFO message queue
#define MSG_Q_Q_PRIORITY   0x02    // Priority queuing

// Event flags
EVENT_GROUP_ID eventGroupCreate(int options);
STATUS eventGroupSignal(EVENT_GROUP_ID groupId, int eventMask);
STATUS eventGroupWait(EVENT_GROUP_ID groupId, int eventMask, int options, int timeout);
STATUS eventGroupClear(EVENT_GROUP_ID groupId, int eventMask);
STATUS eventGroupDelete(EVENT_GROUP_ID groupId);

// Event options
#define EVENT_WAIT_OR      0x00    // Wait for any event in mask
#define EVENT_WAIT_AND     0x01    // Wait for all events in mask
```

### Memory management

```c
// Memory partition allocation
PART_ID partCreate(void *memStart, unsigned memSize, unsigned objSize, int options);
void *partAlloc(PART_ID partId);
STATUS partFree(PART_ID partId, void *memBlock);
STATUS partDelete(PART_ID partId);

// Memory partition options
#define PART_FREE_BEST_FIT 0x00    // Best-fit allocation
#define PART_FREE_FIRST_FIT 0x01   // First-fit allocation

// Heap allocation (malloc/free)
void *malloc(unsigned size);
void free(void *ptr);
void *calloc(unsigned num, unsigned size);
void *realloc(void *ptr, unsigned newSize);

// Memory mapping
STATUS mmap(void *addr, unsigned size, int prot);
STATUS munmap(void *addr, unsigned size);
```

### Timers

```c
// Timer creation
TIMER_ID timerCreate(int options, FUNCPTR routine, int arg);
STATUS timerStart(TIMER_ID timerId, int delay, int interval);
STATUS timerStop(TIMER_ID timerId);
STATUS timerDelete(TIMER_ID timerId);

// Timer options
#define TIMER_ONESHOT       0x00    // One-shot timer
#define TIMER_PERIODIC      0x01    // Periodic timer

// Watchdog timer
WDOG_ID wdCreate(int options, FUNCPTR routine, int arg);
STATUS wdStart(WDOG_ID wdId, int delay, int arg);
STATUS wdCancel(WDOG_ID wdId, int *pArg);
STATUS wdDelete(WDOG_ID wdId);

// System clock
ULONG tickGet(void);
ULONG sysClkRateGet(void);
void sysClkRateSet(ULONG rate);

// High-resolution timer (VxWorks 7+)
HR_TIMER_ID hrTimerCreate(int options);
STATUS hrTimerStart(HR_TIMER_ID timerId, ULONG delay, ULONG interval, FUNCPTR routine, int arg);
STATUS hrTimerStop(HR_TIMER_ID timerId);
STATUS hrTimerDelete(HR_TIMER_ID timerId);
```

### Interrupt handling

```c
// Interrupt Service Routine (ISR)
typedef void (*ISR)(void);

// Connect ISR to interrupt vector
STATUS intConnect(INUM intNum, ISR isr, int arg);

// Enable/disable interrupt
STATUS intEnable(INUM intNum);
STATUS intDisable(INUM intNum);

// Interrupt masking
STATUS intMaskSet(INUM intNum);
STATUS intMaskClear(INUM intNum);

// Interrupt nesting
STATUS intNestedSet(INUM intNum, int nested);
STATUS intNestedGet(INUM intNum, int *pNested);

// Interrupt controller
STATUS intCtlrInit(void);
STATUS intCtlrVectorSet(INUM intNum, ISR isr, int arg);

// Software interrupt
STATUS intSwiTrigger(INUM intNum);
```

### I/O system

```c
// Open/close
int open(const char *path, int oflag, ...);
int close(int fd);

// Read/write
int read(int fd, char *buffer, int nBytes);
int write(int fd, const char *buffer, int nBytes);

// IO control
int ioctl(int fd, int request, int arg);

// Device control
STATUS devCreate(const char *name, int type, int baseAddr, int numEntries);
STATUS devDelete(const char *name);
STATUS devOpen(const char *name, int oflag);
STATUS devClose(int fd);
STATUS devRead(int fd, char *buffer, int nBytes);
STATUS devWrite(int fd, const char *buffer, int nBytes);
STATUS devIoctl(int fd, int request, int arg);

// File system
int fsMount(const char *path, const char *type, int flags, const char *dev);
int fsUnmount(const char *path);

// File operations
int creat(const char *path, int mode);
int unlink(const char *path);
int rename(const char *oldPath, const char *newPath);
int stat(const char *path, struct stat *buf);
```

### Networking

```c
// Socket API (POSIX-like)
int socket(int domain, int type, int protocol);
int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
int listen(int sockfd, int backlog);
int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
ssize_t send(int sockfd, const void *buf, size_t len, int flags);
ssize_t recv(int sockfd, void *buf, size_t len, int flags);

// Host and service resolution
struct hostent *gethostbyname(const char *name);
struct hostent *gethostbyaddr(const char *addr, int len, int type);
struct servent *getservbyname(const char *name, const char *proto);
struct servent *getservbyport(int port, const char *proto);

// Network configuration
STATUS ifAddrGet(char *ifName, struct ifreq *ifr);
STATUS ifAddrSet(char *ifName, struct ifreq *ifr);
```

## Development ecosystem

### Supported platforms

VxWorks supports a wide range of platforms through BSPs:

- **ARM Cortex-A**: ARMv7-A, ARMv8-A (32-bit and 64-bit)
  - NXP i.MX 6/8, Texas Instruments, Qualcomm, etc.
- **ARM Cortex-R**: For real-time applications requiring high performance
- **ARM Cortex-M**: For microcontroller applications (VxWorks MILS)
- **x86**: 32-bit and 64-bit processors
  - Intel, AMD, and others
- **PowerPC**: Various PowerPC processors (historically strong for VxWorks)
- **MIPS**: MIPS32 and MIPS64
- **SPARC**: SPARC V8 and V9
- **RISC-V**: Growing support for RISC-V architectures
- **Custom**: Any platform with a BSP

### Board Support Packages (BSPs)

BSPs provide the interface between VxWorks and specific hardware:

- **Start-up code**: Bootloader and early initialization
- **Hardware abstraction**: Access to hardware-specific features
- **Interrupt handling**: Configuration and handling of interrupts
- **Memory mapping**: Memory layout configuration
- **Clock configuration**: System clock setup
- **Device drivers**: Drivers for on-board peripherals
- **Flash file system**: Support for flash memory

BSP types:
- **Full BSP**: Complete BSP with all features
- **Minimal BSP**: Minimal BSP for resource-constrained systems
- **Custom BSP**: Created for custom hardware

### IDE support

- **Wind River Workbench**: Official IDE (Eclipse-based)
- **Visual Studio**: With Wind River plugins
- **VS Code**: With Wind River extensions
- **Eclipse**: With Wind River plugins
- **Command-line tools**: Full development possible via command line

### Build system

- **VxWorks System Builder (VSB)**: Graphical tool for kernel
  configuration
- **Makefiles**: Traditional make-based build system
- **Project files**: For Workbench IDE
- **Command-line build**: `make` with various options

Example build commands:
```bash
# Build kernel
make -f kernel.mk

# Build VxWorks image
make -f vxWorks.mk

# Build application
make -f myapp.mk
```

### Debugging tools

- **Wind River Workbench Debugger**: Full-featured debugger
- **GDB**: GNU Debugger with VxWorks support
- **CrossWind**: Debugging and profiling tools
- **WDB**: VxWorks-specific debugger
- **pidin**: Process information utility
- **sp**: Task spawn and control
- **ld**: Module load and unload
- **si**: System information
- **m**: Memory examination and modification

### Profiling tools

- **Wind River Workbench Profiler**: Performance profiling
- **CrossWind Analyzer**: Advanced profiling and analysis
- **sysProbe**: System-level profiling
- **taskProbe**: Task-level profiling
- **memProbe**: Memory usage profiling

### Networking

- **Full TCP/IP stack**: IPv4 and IPv6 support
- **Socket API**: Standard BSD socket API
- **Protocols**: TCP, UDP, ICMP, IGMP, etc.
- **Routing**: Advanced routing capabilities
- **Firewall**: Built-in packet filtering
- **QoS**: Quality of Service support
- **Multicast**: IP multicast support
- **Security**: IPsec, SSL/TLS support

### File systems

VxWorks supports multiple file systems:

- **VxWorks file system**: Native trueFFS (True Flash File System)
- **DOSFS**: DOS-compatible file system
- **HDDFS**: High-density DOS file system
- **HRFS**: High-reliability file system
- **TFFS**: True Flash File System (power-fail safe)
- **NFS**: Network File System
- **CIFS**: Common Internet File System (SMB)
- **JFFS2**: Journalling Flash File System v2
- **YAFFS**: Yet Another Flash File System
- **FAT**: FAT16/32 file systems
- **RAM disk**: In-memory file system

### Real-Time Processes (RTPs)

VxWorks 6.x+ introduced RTPs which allow user-space processes with
real-time capabilities:

- **User-space execution**: Processes run in user space
- **Real-time capabilities**: RTPs can have real-time priorities and
  capabilities
- **Memory protection**: MMU provides memory protection between RTPs
- **Kernel modules**: RTPs can load kernel modules
- **POSIX compliance**: RTPs provide more POSIX-like environment

## Common pitfalls

- **Memory leaks**: Not freeing allocated memory. Use `malloc()` and
  `free()` carefully. Consider using partitions for deterministic allocation.
- **Resource leaks**: Not closing file descriptors or releasing resources.
  Always close what you open.
- **Incorrect error handling**: Not checking return values from system
  calls. Most VxWorks calls return STATUS (OK or ERROR) or int (-1 on error).
- **Priority inversion**: Not using priority inheritance mutexes for
  shared resources. Use semMLib with SEM_INVERSION_SAFE option.
- **Blocking in ISRs**: ISRs cannot block. Use interrupt-safe functions
  or defer work to a task.
- **Stack overflow**: Not sizing task stacks correctly. Use larger
  stacks for tasks with complex functions.
- **Message queue overflow**: Not sizing message queues correctly.
  Design queue sizes for worst-case scenarios.
- **Memory fragmentation**: With heap allocation. Use partitions for
  fixed-size allocations to avoid fragmentation.
- **BSP issues**: Hardware-specific issues due to incorrect BSP
  configuration. Verify BSP for your hardware.
- **Interrupt handling issues**: Not handling interrupts correctly.
  Use intConnect/intEnable/intDisable properly.
- **Task priority confusion**: Remember that lower number = higher
  priority (0 is highest, 255 is lowest).
- **Kernel module issues**: Not loading/unloading modules correctly.
  Use ld() and unld() properly.
- **Not using VxWorks utilities**: Not using VxWorks-specific utilities
  like sp, ld, si, etc. for debugging and monitoring.

## Best practices

- **Use partitions for deterministic memory**: For real-time applications,
  use partition allocation (partCreate/partAlloc/partFree) instead of
  malloc/free.
- **Name all objects**: Use descriptive names for tasks, semaphores,
  queues, etc. for debugging.
- **Use semMLib with SEM_INVERSION_SAFE**: For mutexes to prevent
  priority inversion.
- **Keep ISRs short**: Set a flag or send to a queue, then return.
  Defer actual work to a task.
- **Always check return values**: Never ignore return values from
  VxWorks API calls. Check for OK or ERROR.
- **Use error handlers**: Implement error handlers for critical errors.
- **Design for determinism**: Use fixed-size allocations, avoid
  dynamic memory where possible, design for bounded execution times.
- **Use VxWorks utilities**: Use sp, ld, si, m, etc. for system
  monitoring and debugging.
- **Configure appropriately**: Use VSB to configure kernel with only
  needed features for your application.
- **Test on target**: Always test on actual target hardware.
- **Profile with CrossWind**: Use CrossWind tools for performance
  profiling and analysis.
- **Use watchdog timers**: Implement watchdog timers for system health
  monitoring.
- **Handle errors**: Implement comprehensive error handling and
  recovery mechanisms.
- **Document configuration**: Document all kernel and BSP configuration
  decisions.
- **Use RTPs**: For complex applications, use Real-Time Processes for
  better isolation and memory protection.

## Integration patterns

### With hardware

- **Device drivers**: Implement hardware drivers using VxWorks
  driver framework
- **Direct register access**: Use memory-mapped I/O for direct hardware
  register access
- **Interrupt handling**: Use intConnect/intEnable/intDisable for
  interrupt handling
- **DMA**: Use DMA drivers for efficient data transfer
- **Hardware watchdog**: Integrate with VxWorks watchdog timer facilities

### With middleware

- **File systems**: Mount file systems at appropriate path prefixes
- **Networking**: Configure network interfaces and protocols
- **Kernel modules**: Load kernel modules dynamically for additional
  functionality
- **RTPs**: Use Real-Time Processes for user-space middleware
- **Custom services**: Implement as tasks or RTPs

### With safety features

- **VxWorks Cert**: Use certified version for safety-critical applications
- **Memory protection**: Use MMU for memory protection between tasks
  or RTPs
- **Error handling**: Implement comprehensive error detection and
  handling
- **Watchdog**: Use hardware and software watchdog timers
- **Safety monitoring**: Implement safety monitoring tasks

### With multi-core

- **SMP (Symmetric Multi-Processing)**: Use SMP kernel for multi-core
  systems (VxWorks 7+). Tasks can run on any core.
- **Bound tasks**: Bind tasks to specific cores using taskOptionsSet()
- **Core isolation**: Reserve cores for specific purposes
- **IPC**: Use message queues or other IPC mechanisms for
  inter-core communication
- **Shared memory**: Use shared memory with proper synchronization

### With real-time extensions

- **Priority inheritance**: Use SEM_INVERSION_SAFE option for mutexes
- **High-resolution timers**: Use hrTimerCreate/hrTimerStart for
  precise timing
- **Preemptibility control**: Use taskOptionsSet() with VX_NO_PREEMPT
  to create non-preemptible sections

## Testing strategies

- **Unit testing**: Test individual functions and modules
- **Integration testing**: Test component interactions
- **System testing**: Test complete system on target hardware
- **Stress testing**: Run system under heavy load
- **Performance testing**: Measure and verify timing requirements
- **Fault injection**: Inject faults to verify error handling
- **Coverage testing**: Achieve high code coverage
- **Regression testing**: Run tests after any changes

Example test framework:
```c
#include "vxWorks.h"
#include "stdio.h"
#include "taskLib.h"
#include "semLib.h"

void testTask(int arg1, int arg2, ..., int arg10)
{
    STATUS status;
    SEM_ID sem;
    
    // Test semaphore
    sem = semBinaryCreate(SEM_Q_PRIORITY, SEM_FULL);
    if (sem == NULL) {
        printf("semBinaryCreate failed\n");
        return;
    }
    
    status = semTake(sem, 10);
    if (status != OK) {
        printf("semTake failed: %d\n", status);
    }
    
    status = semGive(sem);
    if (status != OK) {
        printf("semGive failed: %d\n", status);
    }
    
    status = semDelete(sem);
    if (status != OK) {
        printf("semDelete failed: %d\n", status);
    }
}

int main(void)
{
    TASK_ID taskId;
    
    taskId = taskSpawn("tTest", 100, 0, 4096, testTask, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
    if (taskId == ERROR) {
        printf("taskSpawn failed\n");
        return ERROR;
    }
    
    taskDelay(100);  // Wait for test to complete
    return OK;
}
```

## Performance optimization

- **Use partitions**: For deterministic memory allocation and to avoid
  fragmentation
- **Minimize context switches**: Design tasks with appropriate
  granularity
- **Use message queues efficiently**: Optimize message sizes and
  queue depths
- **Keep ISRs short**: Minimize ISR execution time
- **Use static allocation**: For critical data structures to avoid
  dynamic allocation overhead
- **Disable interrupts judiciously**: Only when absolutely necessary
- **Use appropriate priorities**: Don't use too many priority levels
- **Tune kernel parameters**: Adjust kernel parameters for specific
  application requirements
- **Profile with CrossWind**: Use CrossWind tools for performance
  profiling
- **Use cache optimization**: Align data structures, minimize cache
  thrashing

## Migration and upgrade

- **Version compatibility**: VxWorks maintains backward compatibility
  within major versions. Most applications can upgrade with changes
  primarily to BSP.
- **BSP updates**: BSPs may need updates for new VxWorks versions.
  Check BSP compatibility.
- **API changes**: Some API changes between major versions. Check
  release notes and migration guides.
- **Configuration**: Review and update kernel configuration using VSB.
- **Testing**: Thoroughly test after upgrade, especially on target
  hardware.
- **Driver updates**: Device drivers may need updates for new VxWorks
  versions.
- **Tool updates**: Update development tools (compiler, debugger, etc.)
  for new VxWorks versions.

## Common use cases

- **Aerospace**: Flight control, avionics, navigation, communication
  (DO-178C Level A)
- **Defense**: Military command and control, radar, sonar, electronic
  warfare
- **Medical devices**: MRI machines, CT scanners, patient monitors,
  surgical robots (IEC 62304)
- **Industrial automation**: PLCs, HMIs, robotics, process control
  (IEC 61508 SIL 3/4)
- **Automotive**: ADAS, autonomous driving, infotainment, powertrain
  control (ISO 26262 ASIL D)
- **Railway**: Signaling, train control, passenger information
  (EN 50128)
- **Telecom**: Base stations, telecom switches, network appliances
- **Networking equipment**: Routers, switches, firewalls, load balancers
- **Space**: Satellite control, spacecraft systems
- **Energy**: Power plant control, smart grid, SCADA systems

## Safety and certification

VxWorks is used in safety-critical applications with various
certifications:

### Available certifications

- **DO-178C**: Level A, B, C, D for avionics
- **IEC 61508**: SIL 1, 2, 3, 4 for industrial functional safety
- **ISO 26262**: ASIL A, B, C, D for automotive
- **EN 50128**: Railway applications
- **IEC 62304**: Medical device software
- **Common Criteria**: EAL1 to EAL6+ for security

### Safety-certified versions

- **VxWorks 653**: ARINC 653 compliant multi-partition OS for aviation
- **VxWorks Cert**: Certified version for safety-critical applications
- **VxWorks MILS**: Multiple Independent Levels of Security for
  high-security applications
- **Safety manuals**: Comprehensive safety manuals available
- **Certification packages**: Full certification packages for
  various standards
- **Tool qualification**: Qualified development tools

### Using VxWorks in safety-critical applications

- **Use certified version**: Ensure using a version with the required
  certification
- **Follow safety guidelines**: Follow all guidelines in safety manual
- **Document design**: Document all design decisions related to safety
- **Use VxWorks 653**: For ARINC 653 compliance in aviation applications
- **Design for isolation**: Use partitions (VxWorks 653) or RTPs for
  fault isolation
- **Perform safety analysis**: Perform FMEA, FTA, and other analyses
- **Test thoroughly**: Perform comprehensive testing required by
  safety standard
- **Maintain traceability**: Maintain traceability between requirements,
  design, implementation, and testing

## VxWorks 653 (ARINC 653)

VxWorks 653 is a special version of VxWorks that implements the ARINC
653 standard for space and time partitioning in safety-critical avionics
applications:

### Key features

- **Space partitioning**: Separate address spaces for each partition
- **Time partitioning**: Guaranteed CPU time for each partition
- **Communication**: Well-defined communication between partitions
- **Health monitoring**: System-level health monitoring
- **Error handling**: Comprehensive error detection and handling

### ARINC 653 concepts

- **Partition**: Independent unit of execution with its own resources
- **Module**: Loadable unit of code and data
- **Process**: Execution unit within a partition
- **Port**: Communication endpoint between partitions
- **Channel**: Communication path between ports
- **Sampling port**: For asynchronous message passing
- **Queuing port**: For synchronous message passing
- **Buffer**: Memory buffer for message data

### API

```c
// Partition management
STATUS APEX_Partition_Ident(APEX_PARTITION_ID_TYPE *Partition_Id);
STATUS APEX_Partition_Get_Status(APEX_PARTITION_STATUS_TYPE *Partition_Status);

// Process management
STATUS APEX_Process_Create(
    APEX_PROCESS_NAME_TYPE *Process_Name,
    APEX_PROCESS_ATTRIBUTE_TYPE *Process_Attributes,
    SYSTEM_ADDRESS_TYPE Entry_Point,
    STACK_SIZE_TYPE Stack_Size,
    APEX_PARTITION_ID_TYPE Partition_Id,
    PRIORITY_TYPE Priority,
    SYSTEM_TIME_TYPE Deadline,
    APEX_PROCESS_ID_TYPE *Process_Id
);

// Sampling port
STATUS APEX_Sampling_Port_Create(
    APEX_SAMPLING_PORT_NAME_TYPE *Sampling_Port_Name,
    MESSAGE_SIZE_TYPE Max_Message_Size,
    MESSAGE_RANGE_TYPE Max_Nb_Message,
    PORT_DIRECTION_TYPE Port_Direction,
    SYSTEM_TIME_TYPE Refresh_Period,
    APEX_SAMPLING_PORT_ID_TYPE *Sampling_Port_Id
);
STATUS APEX_Sampling_Port_Send(
    APEX_SAMPLING_PORT_ID_TYPE Sampling_Port_Id,
    MESSAGE_ADDR_TYPE Message_Addr,
    MESSAGE_SIZE_TYPE Message_Size
);
STATUS APEX_Sampling_Port_Receive(
    APEX_SAMPLING_PORT_ID_TYPE Sampling_Port_Id,
    SYSTEM_TIME_TYPE Timeout,
    MESSAGE_ADDR_TYPE Message_Addr,
    MESSAGE_SIZE_TYPE *Message_Size
);

// Queuing port
STATUS APEX_Queuing_Port_Create(
    APEX_QUEUING_PORT_NAME_TYPE *Queuing_Port_Name,
    MESSAGE_SIZE_TYPE Max_Message_Size,
    MESSAGE_RANGE_TYPE Max_Nb_Message,
    PORT_DIRECTION_TYPE Port_Direction,
    APEX_QUEUING_PORT_ID_TYPE *Queuing_Port_Id
);
STATUS APEX_Queuing_Port_Send(
    APEX_QUEUING_PORT_ID_TYPE Queuing_Port_Id,
    MESSAGE_ADDR_TYPE Message_Addr,
    MESSAGE_SIZE_TYPE Message_Size,
    SYSTEM_TIME_TYPE Timeout
);
STATUS APEX_Queuing_Port_Receive(
    APEX_QUEUING_PORT_ID_TYPE Queuing_Port_Id,
    SYSTEM_TIME_TYPE Timeout,
    MESSAGE_ADDR_TYPE Message_Addr,
    MESSAGE_SIZE_TYPE *Message_Size
);
```

## Alternatives and when to use them

- **VxWorks**: When need commercial RTOS with extensive certifications,
  comprehensive features, and support for demanding applications in
  aerospace, defense, industrial, and medical markets.
- **QNX**: When need POSIX compliance, microkernel architecture,
  or real-time extensions to Linux-like environment.
- **FreeRTOS**: When need lightweight, open-source RTOS for
  microcontrollers. More lightweight but fewer features.
- **Zephyr**: When need open-source, modular RTOS with extensive
  hardware support. More modular but may have less POSIX compliance.
- **ThreadX**: When need commercial RTOS with Azure integration or
  specific industrial features.
- **Linux**: When need full OS features, large ecosystem, or
  open-source. Can achieve near real-time with PREEMPT_RT patch.

## Resources

- **Official website**: https://www.windriver.com/
- **Documentation**: https://docs.windriver.com/
- **Wind River University**: Training and certification
- **Support**: https://support.windriver.com/
- **Community**: https://community.windriver.com/
- **GitHub**: Some open-source VxWorks projects and samples
- **Books**: "VxWorks Programming Guide" by various authors
- **Release notes**: Included with each release
- **API reference**: https://docs.windriver.com/bundle/VxWorks_7_Core_OS_API_Reference
- **VxWorks 653 documentation**: https://docs.windriver.com/bundle/VxWorks_653_API_Reference
- **White papers**: Various white papers on safety, security, and real-time
- **Case studies**: Customer case studies for various industries
