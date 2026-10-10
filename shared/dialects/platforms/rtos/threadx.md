# ThreadX (Azure RTOS) platform contract

Attaches alongside `patterns/rtos.md` and `patterns/embedded.md`.
A high-performance, industrial-grade RTOS from Microsoft (formerly
Express Logic) optimized for deeply embedded applications. The era
is the ThreadX version plus the platform; both are named by the
project's configuration.

## Overview

ThreadX is a preemptive priority-based RTOS with a small footprint,
fast execution, and deterministic behavior. It was acquired by
Microsoft in 2019 and is now part of Azure RTOS, a family of embedded
software components.

- **License**: Apache 2.0 (since acquisition by Microsoft)
- **Source**: https://github.com/azure-rtos/threadx
- **Maintainer**: Microsoft
- **Architectures**: ARM Cortex-M/R/A, x86, MIPS, PowerPC, RISC-V, and more
- **Certifications**: IEC 61508 (SIL 3/4), ISO 26262 (ASIL D), ISO 13849,
  IEC 62304, DO-178C (Level A), EN 50128, MISRA C compliant

## Eras

ThreadX versions are the era markers. Azure RTOS continues the
versioning from Express Logic.

- **V5.x series**: Classic Express Logic era (pre-2019)
- **V6.x series**: First Microsoft-branded releases (2019-2021)
- **Current**: V6.3.x (as of 2024)

**Platform-specific eras**:
- **ARM Cortex-M**: most common, optimized for Cortex-M0/M0+/M3/M4/M7/M33/M35P
- **ARM Cortex-R**: for real-time applications requiring higher performance
- **ARM Cortex-A**: for applications requiring MMU and more advanced features
- **x86**: for PC/104, COM Express, and other x86 embedded platforms
- **MIPS**: for MIPS-based embedded systems
- **PowerPC**: for PowerPC-based embedded systems
- **RISC-V**: growing support for RISC-V architectures

**Azure RTOS era**: ThreadX is now part of Azure RTOS which also
includes FileX, GUIX, NetX, USBX, and others. Using ThreadX with
other Azure RTOS components is common.

## Idiom and best practices

- **Everything is a thread**: the primary execution unit
- **Preemption threshold**: unique feature that allows non-preemptible
  sections within a thread
- **Event-driven**: rich event signaling system with 32 event flags
- **Fast and deterministic**: optimized for performance and determinism
- **Block pool memory management**: flexible memory allocation system
- **Error checking**: optional error checking build configuration
- **Tick-based scheduling**: typically 100-1000 Hz tick rate

## Core concepts

### Thread management

- **Thread**: basic execution unit with stack, priority, and entry function
- **Preemption threshold**: prevents threads below threshold from
  preempting the current thread
- **Thread states**: Ready, Suspended, Completed, Terminated, Error
- **Run states**: Executing, Ready, Blocked, Waiting

### Memory management

- **Block pool**: memory divided into fixed-size blocks
- **Byte pool**: variable-size memory allocation
- **Static allocation**: preferred for deterministic behavior
- **Dynamic allocation**: from block or byte pools

### Synchronization

- **Mutex**: mutual exclusion with priority inheritance
- **Semaphore**: counting semaphore
- **Event flags**: 32-bit event signaling within a thread
- **Message queue**: FIFO message passing
- **Timer**: software timer
- **Application timers**: up to 64 application timers

### Preemption threshold

Unique to ThreadX, preemption threshold provides a mechanism to
create non-preemptible sections of code:

- **Threshold levels**: 0 (fully preemptible) to 31 (non-preemptible)
- **Set threshold**: `tx_thread_preemption_change()`
- **Get threshold**: `tx_thread_preemption_get()`
- **Preemption disable**: `tx_thread_preemption_change(tx_thread_get_current(), 32, &old_threshold)`
- **Preemption enable**: `tx_thread_preemption_change(tx_thread_get_current(), old_threshold, NULL)`

This allows fine-grained control over preemption without disabling
interrupts, which is safer and more flexible than critical sections.

## Configuration

ThreadX is configured through `tx_user.h` header file. This file is
included by all ThreadX source files and must be provided by the
application.

### Core configuration

```c
// Define ThreadX constants
#define TX_MAX_PRIORITIES           32
#define TX_MINIMUM_STACK            256
#define TX_MAX_THREADS              64
#define TX_MAX_SEMAPHORES           32
#define TX_MAX_MUTEXES              32
#define TX_MAX_QUEUES               32
#define TX_MAX_EVENT_FLAGS_GROUPS   32
#define TX_MAX_TIMERS               16
#define TX_MAX_BLOCK_POOLS          8
#define TX_MAX_BYTE_POOLS           8

// Tick configuration
#define TX_TIMER_TICKS_PER_SECOND   100

// Preemption threshold
#define TX_MAX_PREEMPTION_THRESHOLD 31

// Memory alignment
#define TX_BYTE_POOL_ALIGNMENT      8
```

### Memory configuration

```c
// Block pool sizes
#define TX_BLOCK_POOL_SIZE_1       1024
#define TX_BLOCK_POOL_SIZE_2       2048

// Byte pool sizes
#define TX_BYTE_POOL_SIZE_1        8192
#define TX_BYTE_POOL_SIZE_2        16384
```

### Error checking

```c
// Enable error checking (increases code size but helps debugging)
#define TX_ENABLE_EVENT_TRACE       // Enable event tracing
#define TX_DISABLE_ERROR_CHECKING   // Disable error checking for production
// #define TX_ENABLE_ERROR_CHECKING // Enable error checking for development
```

### Platform-specific configuration

```c
// Interrupt configuration
#define TX_lowest_interrupt_priority  255
#define TX_highest_interrupt_priority 0

// Stack configuration
#define TX_STACK_FILL                0xEFEFEFEF
#define TX_STACK_GROWTH              TX_STACK_GROWTH_DOWN
```

## Core API

### Thread management

```c
// Thread entry function
typedef VOID (*TX_THREAD_ENTRY)(ULONG thread_input);

// Thread control block
TX_THREAD thread_0;

// Create a thread
UINT tx_thread_create(
    TX_THREAD *thread_ptr,
    CHAR *name,
    TX_THREAD_ENTRY entry_function,
    ULONG entry_parameter,
    VOID *stack_start,
    ULONG stack_size,
    UINT priority,
    UINT preempt_threshold,
    ULONG time_slice,
    UINT auto_start
);

// Static thread definition
#define TX_THREAD_STACK_BUILD(stack_ptr, stack_size, thread_ptr) \
    memset(stack_ptr, 0xEF, stack_size); \
    thread_ptr->tx_thread_stack_ptr = stack_ptr; \
    thread_ptr->tx_thread_stack_size = stack_size;

// Thread services
UINT tx_thread_delete(TX_THREAD *thread_ptr);
UINT tx_thread_suspend(TX_THREAD *thread_ptr);
UINT tx_thread_resume(TX_THREAD *thread_ptr);
UINT tx_thread_set_priority(TX_THREAD *thread_ptr, UINT new_priority);
UINT tx_thread_get_priority(TX_THREAD *thread_ptr, UINT *current_priority);
UINT tx_thread_preemption_change(TX_THREAD *thread_ptr, UINT new_threshold, UINT *old_threshold);
UINT tx_thread_relinquish(void);
UINT tx_thread_sleep(ULONG ticks);
UINT tx_thread_time_slice_change(TX_THREAD *thread_ptr, ULONG new_time_slice, ULONG *old_time_slice);
UINT tx_thread_wait_abort(TX_THREAD *thread_ptr);

// Get current thread
TX_THREAD *tx_thread_get_current(void);

// Get thread info
UINT tx_thread_info_get(TX_THREAD *thread_ptr, CHAR **name, UINT *priority, UINT *preempt_threshold, ULONG *time_slice, UINT *state);
```

### Synchronization primitives

```c
// Mutex
TX_MUTEX mutex;
UINT tx_mutex_create(TX_MUTEX *mutex_ptr, CHAR *name, UINT inherit_priority);
UINT tx_mutex_delete(TX_MUTEX *mutex_ptr);
UINT tx_mutex_get(TX_MUTEX *mutex_ptr, ULONG wait_option);
UINT tx_mutex_put(TX_MUTEX *mutex_ptr);

// Semaphore
TX_SEMAPHORE semaphore;
UINT tx_semaphore_create(TX_SEMAPHORE *semaphore_ptr, CHAR *name, ULONG initial_count);
UINT tx_semaphore_delete(TX_SEMAPHORE *semaphore_ptr);
UINT tx_semaphore_get(TX_SEMAPHORE *semaphore_ptr, ULONG wait_option);
UINT tx_semaphore_put(TX_SEMAPHORE *semaphore_ptr);

// Event flags
TX_EVENT_FLAGS_GROUP event_group;
UINT tx_event_flags_create(TX_EVENT_FLAGS_GROUP *group_ptr, CHAR *name);
UINT tx_event_flags_delete(TX_EVENT_FLAGS_GROUP *group_ptr);
UINT tx_event_flags_get(TX_EVENT_FLAGS_GROUP *group_ptr, ULONG requested_flags, UINT get_option, ULONG *actual_flags_ptr, ULONG wait_option);
UINT tx_event_flags_set(TX_EVENT_FLAGS_GROUP *group_ptr, ULONG flags_to_set, UINT set_option);

// Message queue
TX_QUEUE queue;
UINT tx_queue_create(TX_QUEUE *queue_ptr, CHAR *name, UINT message_size, VOID *queue_start, ULONG queue_size);
UINT tx_queue_delete(TX_QUEUE *queue_ptr);
UINT tx_queue_send(TX_QUEUE *queue_ptr, VOID *source_ptr, ULONG wait_option);
UINT tx_queue_receive(TX_QUEUE *queue_ptr, VOID *destination_ptr, ULONG wait_option);
UINT tx_queue_flush(TX_QUEUE *queue_ptr);
UINT tx_queue_info_get(TX_QUEUE *queue_ptr, UINT *enqueued, UINT *available_storage, TX_THREAD **first_suspended, ULONG *suspended_count);
```

### Memory management

```c
// Block pool
TX_BLOCK_POOL block_pool;
UINT tx_block_pool_create(TX_BLOCK_POOL *pool_ptr, CHAR *name, ULONG block_size, VOID *pool_start, ULONG pool_size);
UINT tx_block_pool_delete(TX_BLOCK_POOL *pool_ptr);
VOID *tx_block_allocate(TX_BLOCK_POOL *pool_ptr, ULONG wait_option);
UINT tx_block_release(VOID *block_ptr);
UINT tx_block_pool_info_get(TX_BLOCK_POOL *pool_ptr, UINT *available_blocks, UINT *total_blocks, TX_THREAD **first_suspended, ULONG *suspended_count);

// Byte pool
TX_BYTE_POOL byte_pool;
UINT tx_byte_pool_create(TX_BYTE_POOL *pool_ptr, CHAR *name, VOID *pool_start, ULONG pool_size);
UINT tx_byte_pool_delete(TX_BYTE_POOL *pool_ptr);
VOID *tx_byte_allocate(TX_BYTE_POOL *pool_ptr, ULONG memory_size, ULONG wait_option);
UINT tx_byte_release(VOID *memory_ptr);
UINT tx_byte_pool_info_get(TX_BYTE_POOL *pool_ptr, UINT *available_bytes, UINT *fragment_size, VOID **first_available_block, TX_THREAD **first_suspended, ULONG *suspended_count);
```

### Timers

```c
// Application timer
typedef VOID (*TX_TIMER_CALLBACK)(ULONG timer_input);

TX_TIMER timer;
UINT tx_timer_create(TX_TIMER *timer_ptr, CHAR *name, TX_TIMER_CALLBACK activation_function, ULONG activation_input, ULONG initial_ticks, ULONG reschedule_ticks, UINT auto_activate);
UINT tx_timer_delete(TX_TIMER *timer_ptr);
UINT tx_timer_activate(TX_TIMER *timer_ptr);
UINT tx_timer_deactivate(TX_TIMER *timer_ptr);
UINT tx_timer_change(TX_TIMER *timer_ptr, ULONG new_initial_ticks, ULONG new_reschedule_ticks);
UINT tx_timer_info_get(TX_TIMER *timer_ptr, CHAR **name, UINT *active, ULONG *remaining_ticks, ULONG *reschedule_ticks, UINT *auto_activate);
```

### Time functions

```c
// Get system clock (ticks since start)
ULONG tx_time_get(void);

// Convert ticks to milliseconds/seconds
#define TX_TICKS_PER_SECOND    100
#define TX_TICKS_MS(t)         ((t) * (TX_TICKS_PER_SECOND / 1000))
#define TX_MS_TO_TICKS(t)      ((t) * (TX_TICKS_PER_SECOND / 1000))

// System clock utilities
VOID tx_time_set(ULONG new_time);
```

### Interrupt handling

- ThreadX provides interrupt-safe versions of API functions with `_irq` suffix
- ThreadX also provides macros for saving/restoring interrupt state

```c
// Interrupt-safe functions
UINT _txe_mutex_get(TX_MUTEX *mutex_ptr);
UINT _txe_semaphore_get(TX_SEMAPHORE *semaphore_ptr);
UINT _txe_queue_send(TX_QUEUE *queue_ptr, VOID *source_ptr);

// Interrupt handling macros
#define TX_DISABLE               tx_kernel_enter()
#define TX_ENABLE                tx_kernel_exit(old_posture)
#define TX_RESTORE               tx_kernel_exit(old_posture)
```

## Azure RTOS ecosystem

ThreadX is part of Azure RTOS, which provides a complete embedded
software ecosystem:

### Azure RTOS components

- **ThreadX**: Real-time operating system (this document)
- **FileX**: FAT-compatible file system
- **GUIX**: Advanced graphical user interface
- **NetX**: TCP/IP network stack
- **USBX**: USB host and device stack
- **NetX Duo**: Next-generation TCP/IP stack with IPv6 support
- **USBX Duo**: Next-generation USB stack
- **TraceX**: Runtime analysis and visualization tool

### Integration

Azure RTOS components are designed to work together seamlessly:

- **FileX + ThreadX**: File system runs in ThreadX threads
- **NetX + ThreadX**: Network stack runs in ThreadX threads
- **GUIX + ThreadX**: GUI runs in ThreadX threads with graphics drivers
- **USBX + ThreadX**: USB stack runs in ThreadX threads

### TraceX

TraceX is a powerful runtime analysis tool for ThreadX:

- **Event tracing**: captures all ThreadX events (thread switches,
  mutex operations, queue operations, etc.)
- **Performance analysis**: identifies bottlenecks and performance issues
- **Memory analysis**: tracks memory usage and fragmentation
- **Timing analysis**: measures execution times and identifies timing issues
- **Visualization**: graphical display of system behavior

TraceX integrates with ThreadX by enabling `TX_ENABLE_EVENT_TRACE` in
`tx_user.h`. It captures events with minimal overhead (typically < 2%)
and provides detailed insights into system behavior.

## Development ecosystem

### Supported platforms

ThreadX supports a wide range of platforms through BSPs (Board Support
Packages):

- **ARM Cortex-M**: STM32, NXP LPC/Kinetis/i.MX, Nordic nRF, TI MSP432/CC32xx, etc.
- **ARM Cortex-R**: Various ARM Cortex-R platforms
- **ARM Cortex-A**: ARM Cortex-A processors with MMU
- **x86**: Various x86 embedded platforms
- **MIPS**: MIPS-based embedded systems
- **PowerPC**: PowerPC-based embedded systems
- **RISC-V**: Growing support for RISC-V architectures
- **C166/ST10**: Infineon C166 and ST10 architectures
- **SH**: Renesas SH architectures
- **V850**: Renesas V850 architecture

### IDE support

- **Azure RTOS ThreadX for Visual Studio**: Full integration with VS
- **IAR Embedded Workbench**: Full support with plugins
- **Keil MDK**: Full support with RTX (Real-Time eXtension)
- **Segger Embedded Studio**: Full support
- **Eclipse**: With custom configuration
- **VS Code**: With extensions
- **Code Composer Studio**: TI's IDE with ThreadX support
- **MPLAB X**: Microchip's IDE with ThreadX support

### Debugging tools

- **TraceX**: Runtime analysis and visualization (part of Azure RTOS)
- **J-Link**: Full support with ThreadX awareness
- **OpenOCD**: Open-source debugging
- **Lauterbach Trace32**: Professional debugging with ThreadX support
- **SEGGER SystemView**: RTOS-aware debugging
- **QEMU**: Emulation for various architectures

### Static analysis

- **ThreadX Error Checking**: Built-in error checking (when enabled)
- **MISRA C**: ThreadX is MISRA C compliant
- **Cppcheck**: Static analysis with ThreadX awareness
- **Coverity**: Commercial static analysis
- **PC-lint**: Static analysis with ThreadX configurations

## Common pitfalls

- **Incorrect stack size**: most common issue. ThreadX doesn't detect
  stack overflow. Use stack fill patterns and size stacks generously.
- **Priority inversion without inheritance**: ThreadX mutexes support
  priority inheritance, but semaphores don't. Use mutexes for mutual
  exclusion.
- **Blocking in ISR**: ISRs cannot block. Use interrupt-safe functions
  or defer work to a thread.
- **Not checking return values**: most ThreadX functions return status
  codes. Ignoring them hides bugs. TX_SUCCESS is 0, others are error codes.
- **Incorrect preemption threshold**: setting threshold too high can
  cause priority inversion or make system unresponsive.
- **Memory fragmentation**: with byte pools. Use block pools for
  fixed-size allocations when possible.
- **Not using error checking**: for development, always enable
  TX_ENABLE_ERROR_CHECKING to catch issues early.
- **Incorrect tick rate**: too high causes overhead, too low causes
  poor timing resolution. 100-1000 Hz is typical.
- **ThreadX not entered**: forgetting to call `tx_kernel_enter()` and
  `tx_kernel_exit()` around critical sections in ISRs.
- **Not using static allocation**: for production systems, use static
  allocation to ensure deterministic behavior.
- **ISR nesting issues**: not properly handling nested interrupts.
- **Thread priorities not matching requirements**: assign priorities
  based on timing requirements, not importance.

## Best practices

- **Use static allocation**: for production systems to ensure
  deterministic behavior and avoid fragmentation.
- **Name all objects**: use descriptive names for threads, mutexes,
  queues, etc. for debugging. Names are limited to 31 characters.
- **Use mutexes (not semaphores)** for mutual exclusion to get
  priority inheritance automatically.
- **Keep ISRs short**: set a flag or send to a queue, then return.
  Defer actual work to a thread.
- **Always specify timeouts**: never use TX_WAIT_FOREVER for production
  code. Use reasonable timeout values (TX_WAIT_FOREVER = 0xFFFFFFFF).
- **Use preemption threshold wisely**: create non-preemptible sections
  only when absolutely necessary. Keep threshold periods short.
- **Enable error checking**: during development to catch issues early.
  Disable for production to save code space.
- **Use TraceX**: for runtime analysis and debugging. Minimal overhead
  and provides valuable insights.
- **Validate tx_user.h**: review configuration carefully for each project.
  Many issues stem from incorrect configuration.
- **Document thread priorities**: in design documentation, explain why
  each thread has its priority.
- **Handle errors**: check all ThreadX API return values and handle
  errors appropriately.
- **Design for portability**: use ThreadX abstractions to maximize
  code portability across platforms.
- **Use time slicing**: for threads at the same priority to ensure
  fairness and prevent starvation.
- **Implement watchdog feeding**: dedicate a thread to feed hardware
  watchdog. Never feed from ISR.
- **Use block pools**: for fixed-size memory allocations to avoid
  fragmentation.

## Integration patterns

### With peripheral drivers

- **Interrupt-driven**: ISR signals thread via queue or event flags
- **Polling**: thread polls peripheral (less efficient)
- **Driver as thread**: peripheral driver runs as separate thread
- **Callback**: driver calls callback on event

### With middleware

- **FileX**: file system runs in ThreadX threads
- **NetX**: network stack runs in ThreadX threads
- **GUIX**: GUI runs in ThreadX threads with graphics drivers
- **USBX**: USB stack runs in ThreadX threads
- **Custom middleware**: integrate as threads

### With safety features

- **Watchdog**: separate thread feeds watchdog
- **Error handler**: separate thread handles system errors
- **Health monitor**: separate thread monitors system health
- **Recovery**: implement system recovery in error handler

### With multi-core

- **AMP (Asymmetric Multiprocessing)**: each core runs its own
  ThreadX instance
- **SMP (Symmetric Multiprocessing)**: ThreadX can be configured for
  SMP on supported platforms
- **IPC**: use queues, mailboxes, or shared memory for
  inter-processor communication

## Testing strategies

- **Unit testing**: test individual threads and functions in isolation
- **Integration testing**: test thread interactions with real ThreadX
- **Timing testing**: measure and verify timing requirements
- **Stress testing**: create heavy load to verify stability
- **Memory testing**: test with various memory configurations
- **Error injection**: inject errors (e.g., out of memory) to test
  error handling
- **Coverage**: aim for high coverage of all code paths

Example test framework:
```c
#include "tx_api.h"
#include "tx_user.h"

void test_thread_entry(ULONG input)
{
    // Test code here
    while(1)
    {
        tx_thread_sleep(10);
    }
}

int main(void)
{
    tx_kernel_enter();
    
    // Create test thread
    CHAR *stack_ptr = malloc(2048);
    tx_thread_create(&test_thread, "Test Thread", test_thread_entry, 0,
                     stack_ptr, 2048, 5, 5, TX_DONT_START, TX_AUTO_START);
    
    tx_kernel_exit(0);
    return 0;
}
```

## Performance optimization

- **Minimize context switches**: reduce unnecessary thread switches
  by designing threads with appropriate granularity
- **Use preemption threshold**: create non-preemptible sections only
  when necessary to reduce context switch overhead
- **Optimize ISRs**: keep ISRs as short as possible
- **Use block pools**: for fixed-size memory allocations to avoid
  fragmentation and reduce allocation overhead
- **Static allocation**: avoids dynamic memory allocation overhead
- **Cache optimization**: align data structures, minimize cache thrashing
- **Disable interrupts judiciously**: use preemption threshold instead
  of disabling interrupts when possible
- **Use appropriate priorities**: don't use too many priority levels
- **Thread time slicing**: use time slicing for threads at same priority
  to ensure fairness
- **Profile with TraceX**: identify bottlenecks and performance issues

## Migration and upgrade

- **Version compatibility**: ThreadX maintains good backward
  compatibility. Most applications can upgrade with minimal changes.
- **Configuration file**: the biggest effort is typically updating
  `tx_user.h` for new features
- **API changes**: some API changes between major versions. Check
  release notes.
- **Testing**: thoroughly test after upgrade, especially timing-sensitive
  code
- **Azure RTOS integration**: when upgrading, consider integrating
  other Azure RTOS components (FileX, NetX, etc.)
- **Certification**: if using ThreadX for certified applications, ensure
  the version has the required certifications

## Common use cases

- **Industrial automation**: PLCs, motor controllers, HMIs
- **Medical devices**: patient monitors, infusion pumps, ventilators
- **Automotive**: ECUs, ADAS, body control modules (often with safety
  certifications)
- **Aerospace**: avionics, flight control (with DO-178C certification)
- **Consumer electronics**: smart home, audio, appliances
- **IoT devices**: gateways, sensors, edge devices
- **Networking equipment**: routers, switches, network appliances
- **Telecom**: base stations, telecom equipment
- **Defense**: military applications (with various certifications)
- **Transportation**: railway, automotive, marine applications

## Safety and certification

ThreadX is used in safety-critical applications with various
certifications:

### Available certifications

- **IEC 61508**: SIL 3/4 (Functional Safety for Electrical/Electronic
  Systems)
- **ISO 26262**: ASIL D (Functional Safety for Road Vehicles)
- **IEC 62304**: Medical Device Software
- **DO-178C**: Level A (Software Considerations in Airborne Systems)
- **EN 50128**: Railway Applications (CENELEC)
- **ISO 13849**: Machine Safety
- **MISRA C**: Compliant with MISRA C guidelines

### Safety-certified versions

- **ThreadX-Safe**: Safety-certified version of ThreadX
- **Certification packages**: Available from Microsoft for specific
  use cases and certification levels
- **Documentation**: Comprehensive safety manuals and certification
  reports available

### Using ThreadX in safety-critical applications

- **Use certified version**: ensure using a version with the required
  certification
- **Follow safety guidelines**: follow all guidelines in safety manual
- **Document design**: document all design decisions related to safety
- **Testing**: perform additional testing required by the safety
  standard
- **Code reviews**: perform code reviews as required by the safety
  standard
- **Tool qualification**: ensure all development tools are qualified

## Alternatives and when to use them

- **FreeRTOS**: when need lightweight, open-source RTOS with wide
  community support. FreeRTOS is more lightweight but may have fewer
  features.
- **Zephyr**: when need modularity, extensive hardware support, or
  Linux compatibility. Zephyr is more modular but may have higher overhead.
- **ThreadX**: when need industrial-grade, commercial support, safety
  certifications, or Azure integration. ThreadX is the best choice
  for safety-critical applications.
- **SafeRTOS**: when need FreeRTOS features with safety certification
- **QNX**: when need POSIX compliance, microkernel architecture, or
  high-end industrial/automotive
- **VxWorks**: when need commercial support, extensive ecosystem, or
  defense/aerospace certification
- **Bare metal**: when RTOS overhead unacceptable or system very simple

## Resources

- **Official website**: https://azure.microsoft.com/en-us/products/rtos/
- **Source code**: https://github.com/azure-rtos/threadx
- **Documentation**: https://learn.microsoft.com/en-us/azure/rtos/
- **Azure RTOS**: https://azure.microsoft.com/en-us/products/rtos/
- **ThreadX GitHub**: https://github.com/azure-rtos
- **Release notes**: Included in each release
- **API reference**: Included in documentation
- **Books**: "ThreadX: Real-Time Operating System for Embedded Systems" by
  various authors
- **Training**: Microsoft provides ThreadX training
- **Support**: Commercial support available from Microsoft
