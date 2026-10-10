# FreeRTOS platform contract

Attaches alongside `patterns/rtos.md` and `patterns/embedded.md`.
The de facto standard open-source RTOS for microcontrollers — lightweight,
portable, and widely supported across architectures. The era is the
FreeRTOS version plus the port layer; both are named by the project's
configuration.

## Overview

FreeRTOS is a preemptive priority-based real-time kernel with optional
components (TCP/IP, FAT filesystem, CLI, etc.). It provides the core
scheduler, task management, synchronization primitives, and memory
allocation schemes. The kernel is written primarily in C for maximum
portability.

- **License**: MIT (formerly modified GPL with exception)
- **Source**: https://www.freertos.org/
- **Maintainer**: Amazon Web Services (since 2017)
- **Architectures**: ARM Cortex-M/R/A, x86, MIPS, RISC-V, AVR, PIC, and many more

## Eras

FreeRTOS versions are the era markers. Major versions with notable
changes:

- **V7.x - V8.x**: Classic series, widely deployed
- **V9.x**: Added SMP (Symmetric Multi-Processing) support
- **V10.x**: Major overhaul, improved portability, new features
- **V10.3.x**: Current stable series (as of 2024)
- **V10.4.x - V10.6.x**: Latest releases with bug fixes and enhancements
- **Long-term support (LTS)**: Amazon provides LTS branches with extended
  support windows (e.g., 202012.00 LTS, 202112.00 LTS)

**Port-specific eras**: The BSP/port layer often defines additional eras:
- CMSIS-RTOS v1 vs v2 wrapper for ARM Cortex-M
- ESP-IDF integration layer for ESP32
- TI-RTOS (formerly TI-RTOS, now part of TI's SDK)
- SafeRTOS compatibility layer

**Configuration era**: The `FreeRTOSConfig.h` file defines the build
configuration and effectively creates a project-specific era. Key
configuration options are listed below.

## Idiom and best practices

- **Tasks are the primary execution unit**: created with `xTaskCreate()`
  or `xTaskCreateStatic()`. Each task has a name (for debugging),
  priority, stack, and entry function.
- **Use `xTaskCreateStatic()` for deterministic systems**: avoids heap
  allocation, requires pre-allocated task control block and stack.
- **Priority 0 is the idle task**: never create user tasks at priority 0.
  The idle task runs when no other task is ready.
- **Priority `configMAX_PRIORITIES-1` is highest**: used by ISRs and
  critical tasks.
- **ISRs use special primitives**: `xQueueSendFromISR()`,
  `xSemaphoreGiveFromISR()`, etc. These have different semantics than
  their non-ISR counterparts.
- **Context switch on ISR exit**: if an ISR makes a higher-priority
  task ready, a context switch occurs automatically on ISR exit.
- **Critical sections use taskENTER/EXIT_CRITICAL()**: for short
  atomic operations. Long critical sections block the scheduler.
- **Suspend the scheduler with `vTaskSuspendAll()`**: for atomic
  operations that must not be interrupted. Keep suspend periods short.

## Configuration (FreeRTOSConfig.h)

`FreeRTOSConfig.h` is the single most important file. It must be
provided by the application and defines the RTOS behavior.

### Core configuration

- `configMAX_PRIORITIES`: maximum number of priority levels (8-255,
  typically 5-32 for embedded). Higher values increase memory usage.
- `configCPU_CLOCK_HZ`: CPU clock frequency in Hz. Used for timing
  calculations.
- `configTICK_RATE_HZ`: tick interrupt frequency (typically 100-1000Hz).
  Higher values increase timing resolution but overhead.
- `configUSE_PREEMPTION`: must be 1 for preemptive scheduling.
  Set to 0 for cooperative scheduling (rare).
- `configUSE_IDLE_HOOK`: enable idle task hook for power management
  or background processing.
- `configUSE_TICK_HOOK`: enable tick hook for periodic background work.
- `configUSE_MALLOC_FAILED_HOOK`: enable hook called when memory
  allocation fails.

### Memory management

FreeRTOS provides multiple heap (memory allocation) implementations:

- `heap_1.c`: simplest, uses only `pvPortMalloc()` and `vPortFree()`
  that are provided by the port layer. No heap management in FreeRTOS.
- `heap_2.c`: uses a single contiguous block. Fast but fragment-prone.
- `heap_3.c`: uses a block allocation scheme. Each allocation gets
  its own block. No coalescing of adjacent free blocks.
- `heap_4.c`: uses a wrapper around the standard `malloc()` and `free()`.
  Most flexible but requires libc heap.
- `heap_5.c`: allocates memory from a statically allocated array.
  Very predictable, good for safety-critical systems.

Configuration: `configAPPLICATION_ALLOCATED_HEAP` for heap_5.

### Task and stack configuration

- `configMINIMAL_STACK_SIZE`: minimum stack size for idle and timer
  tasks. Application tasks need their own stack sizes.
- `configMAX_TASK_NAME_LEN`: maximum length of task names (default 10).
  Longer names useful for debugging but consume RAM.
- `configCHECK_FOR_STACK_OVERFLOW`: if 1, tasks check their stack
  usage. Can catch stack overflow but has overhead.
- `configRECORD_STACK_HIGH_ADDRESS`: if 1, tracks maximum stack usage.
  Useful for stack sizing analysis.

### Synchronization configuration

- `configUSE_MUTEXES`: enable mutex support (1).
- `configUSE_RECURSIVE_MUTEXES`: enable recursive mutexes (1).
- `configUSE_COUNTING_SEMAPHORES`: enable counting semaphores (1).
- `configQUEUE_REGISTRY_SIZE`: number of queues/semaphores that can
  be registered for debugging. Set to 0 to disable.

### Timer configuration

- `configUSE_TIMERS`: enable software timer support.
- `configTIMER_TASK_PRIORITY`: priority of the timer task (the task
  that manages software timers).
- `configTIMER_QUEUE_LENGTH`: number of active timer command
  messages that can be held in timer command queue.
- `configTIMER_TASK_STACK_DEPTH`: stack size for timer task.

### ISR configuration

- `configKERNEL_INTERRUPT_PRIORITY`: kernel interrupt priority.
  ISRs at or below this priority can make FreeRTOS API calls.
- `configMAX_SYSCALL_INTERRUPT_PRIORITY`: highest interrupt priority
  from which FreeRTOS API calls are made. Must be >= kernel priority.
- `configMAX_API_CALL_INTERRUPT_PRIORITY`: same as above (alias).

### Debug and tracing

- `configUSE_TRACE_FACILITY`: enable trace hooks for debugging.
- `configUSE_STATS_FORMATTING_FUNCTIONS`: enable statistics formatting
  functions for debugging output.
- `configGENERATE_RUN_TIME_STATS`: if 1, generates runtime statistics
  (CPU usage per task). Requires a timer with known frequency.

### SMP (Symmetric Multi-Processing) configuration

- `configNUMBER_OF_CORES`: number of CPU cores (V9+).
- `configRUN_MULTIPLE_PRIORITIES`: if 1, allows multiple tasks at
  same priority to run simultaneously on different cores.
- Various SMP-specific synchronization primitives.

### MPU (Memory Protection Unit) configuration

- `configENABLE_MPU`: enable Memory Protection Unit support.
- `configENABLE_TRUSTZONE`: enable ARM TrustZone support.
- MPU regions configured separately for each task.

### Additional components

- **FreeRTOS+TCP**: TCP/IP stack (separate download)
  - `configUSE_TCP`: enable TCP/IP
  - Network buffer sizes, socket counts, etc.
- **FreeRTOS+FAT**: FAT filesystem (separate download)
  - `configUSE_FATFS`: enable FAT filesystem
- **FreeRTOS+CLI**: Command Line Interface
  - `configUSE_CLI`: enable CLI

## Port-specific considerations

FreeRTOS is highly portable. Each architecture has a port layer that
implements the architecture-specific code.

### ARM Cortex-M port

- Uses CMSIS (ARM's Cortex Microcontroller Software Interface Standard)
- Provides both assembly and C implementations
- `port.c` contains the port implementation
- `portmacro.h` contains architecture-specific macros
- Interrupt priorities: FreeRTOS requires specific interrupt priority
  configuration. Cortex-M uses NVIC with configurable priorities.
- **SVCall for context switch**: Cortex-M uses the SVCall exception for
  context switches (triggered by PendSV interrupt).
- **SysTick for tick**: System tick timer used for RTOS tick.
- **FPU support**: configurable via `configENABLE_FPU` and
  `configENABLE_MVE`. Floating point context saved during context
  switch if enabled.

### ARM Cortex-R and Cortex-A ports

- More complex than Cortex-M due to MMU, caches, etc.
- Often used in asymmetric multiprocessing (AMP) configurations
- May run alongside Linux on Cortex-A (big.LITTLE configurations)

### ESP32 port

- Integrated into ESP-IDF (Espressif IoT Development Framework)
- Uses Xtensa or RISC-V ISA depending on ESP32 variant
- FreeRTOS tickless idle enabled by default for power saving
- Special handling for dual-core (ESP32 dual-core parts)
- WiFi and Bluetooth stacks run as separate tasks
- See `esp32.md` platform contract for ESP32-specific details

### RISC-V port

- Multiple variants based on RISC-V specifications
- Standard port for RV32I and RV64I
- Special ports for specific implementations (SiFive, etc.)
- Uses standard RISC-V exceptions and interrupts

### AVR port

- 8-bit architecture with limited resources
- Special considerations for small stack sizes
- Often used with AVR-GCC compiler
- Limited to smaller FreeRTOS configurations

## Core API

### Task management

```c
// Create a task (dynamic allocation)
BaseType_t xTaskCreate(
    TaskFunction_t pxTaskCode,      // Task entry function
    const char * const pcName,      // Descriptive name
    configSTACK_DEPTH_TYPE usStackDepth, // Stack size in words
    void *pvParameters,             // Parameters passed to task
    UBaseType_t uxPriority,         // Priority
    TaskHandle_t *pxCreatedTask     // Handle to created task
);

// Create a task (static allocation)
TaskHandle_t xTaskCreateStatic(
    TaskFunction_t pxTaskCode,
    const char * const pcName,
    uint32_t ulStackDepth,
    void *pvParameters,
    UBaseType_t uxPriority,
    StackType_t *pxStackBuffer,
    StaticTask_t *pxTaskBuffer
);

// Delete a task
void vTaskDelete(TaskHandle_t xTaskToDelete);

// Suspend/Resume a task
void vTaskSuspend(TaskHandle_t xTaskToSuspend);
void vTaskResume(TaskHandle_t xTaskToResume);

// Delay a task
void vTaskDelay(TickType_t xTicksToDelay);

// Yield to other tasks
void taskYIELD(void);

// Get current task handle
TaskHandle_t xTaskGetCurrentTaskHandle(void);

// Get task state
eTaskState eTaskGetState(TaskHandle_t xTask);
```

### Synchronization primitives

```c
// Semaphore (binary)
SemaphoreHandle_t xSemaphoreCreateBinary(void);
BaseType_t xSemaphoreGive(SemaphoreHandle_t xSemaphore);
BaseType_t xSemaphoreTake(SemaphoreHandle_t xSemaphore, TickType_t xBlockTime);

// Semaphore (counting)
SemaphoreHandle_t xSemaphoreCreateCounting(UBaseType_t uxCount, UBaseType_t uxInitialCount);

// Mutex
SemaphoreHandle_t xSemaphoreCreateMutex(void);
BaseType_t xSemaphoreGiveMutex(SemaphoreHandle_t xMutex);
BaseType_t xSemaphoreTakeMutex(SemaphoreHandle_t xMutex, TickType_t xBlockTime);

// Recursive mutex
SemaphoreHandle_t xSemaphoreCreateRecursiveMutex(void);
BaseType_t xSemaphoreGiveRecursiveMutex(SemaphoreHandle_t xMutex);
BaseType_t xSemaphoreTakeRecursiveMutex(SemaphoreHandle_t xMutex, TickType_t xBlockTime);

// Queue
QueueHandle_t xQueueCreate(UBaseType_t uxQueueLength, UBaseType_t uxItemSize);
BaseType_t xQueueSend(QueueHandle_t xQueue, const void *pvItemToQueue, TickType_t xTicksToWait);
BaseType_t xQueueReceive(QueueHandle_t xQueue, void *pvBuffer, TickType_t xTicksToWait);
BaseType_t xQueueSendToFront(QueueHandle_t xQueue, const void *pvItemToQueue, TickType_t xTicksToWait);
BaseType_t xQueueSendToBack(QueueHandle_t xQueue, const void *pvItemToQueue, TickType_t xTicksToWait);
UBaseType_t uxQueueMessagesWaiting(const QueueHandle_t xQueue);

// Stream buffer
StreamBufferHandle_t xStreamBufferCreate(size_t xBufferSizeBytes, size_t xTriggerLevelBytes);
size_t xStreamBufferSend(StreamBufferHandle_t xStreamBuffer, const void *pvTxData, size_t xDataLengthBytes, TickType_t xTicksToWait);
size_t xStreamBufferReceive(StreamBufferHandle_t xStreamBuffer, void *pvRxData, size_t xBufferLengthBytes, TickType_t xTicksToWait);

// Event groups
EventGroupHandle_t xEventGroupCreate(void);
EventBits_t xEventGroupSetBits(EventGroupHandle_t xEventGroup, const EventBits_t uxBitsToSet);
EventBits_t xEventGroupClearBits(EventGroupHandle_t xEventGroup, const EventBits_t uxBitsToClear);
EventBits_t xEventGroupGetBits(EventGroupHandle_t xEventGroup);
EventBits_t xEventGroupWaitBits(EventGroupHandle_t xEventGroup, const EventBits_t uxBitsToWaitFor, const BaseType_t xClearOnExit, const BaseType_t xWaitForAllBits, TickType_t xTicksToWait);
```

### ISR-safe versions

```c
// These are for use in ISRs only
BaseType_t xQueueSendFromISR(QueueHandle_t xQueue, const void *pvItemToQueue, BaseType_t *pxHigherPriorityTaskWoken);
BaseType_t xQueueOverwriteFromISR(QueueHandle_t xQueue, const void *pvItemToQueue);
BaseType_t xSemaphoreGiveFromISR(SemaphoreHandle_t xSemaphore, BaseType_t *pxHigherPriorityTaskWoken);
BaseType_t xTaskResumeFromISR(TaskHandle_t xTaskToResume);

// Timer callback safe versions
void xQueueSendFromISR(QueueHandle_t xQueue, const void *pvItemToQueue, BaseType_t *pxHigherPriorityTaskWoken);
```

### Timers

```c
// Create a one-shot timer
TimerHandle_t xTimerCreate(const char * const pcTimerName, TickType_t xTimerPeriodInTicks, UBaseType_t uxAutoReload, void *pvTimerID, TimerCallbackFunction_t pxCallbackFunction);

// Create a timer (static allocation)
TimerHandle_t xTimerCreateStatic(const char * const pcTimerName, TickType_t xTimerPeriod, UBaseType_t uxAutoReload, void *pvTimerID, TimerCallbackFunction_t pxCallbackFunction, StaticTimer_t *pxTimerBuffer);

// Start/Stop timer
BaseType_t xTimerStart(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerStop(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerReset(TimerHandle_t xTimer, TickType_t xBlockTime);
BaseType_t xTimerChangePeriod(TimerHandle_t xTimer, TickType_t xNewPeriod, TickType_t xBlockTime);
BaseType_t xTimerIsTimerActive(TimerHandle_t xTimer);

// Get timer task handle
TaskHandle_t xTimerGetTimerTaskHandle(void);
```

### Time and tick functions

```c
// Get current tick count
TickType_t xTaskGetTickCount(void);

// Get tick count from ISR
TickType_t xTaskGetTickCountFromISR(void);

// Convert ticks to milliseconds
portTickType xTaskGetTickCount(void);

// Get tick rate (Hz)
uint32_t configTICK_RATE_HZ; // From FreeRTOSConfig.h

// Delay until specific tick count
void vTaskDelayUntil(TickType_t *pxPreviousWakeTime, const TickType_t xTimeIncrement);
```

### Scheduler control

```c
// Start the scheduler
void vTaskStartScheduler(void);

// Suspend/resume the scheduler
void vTaskSuspendAll(void);
void xTaskResumeAll(void);

// Get scheduler state
eTaskState eTaskGetState(TaskHandle_t xTask);
BaseType_t xTaskGetSchedulerState(void);

// Get RTOS version
uint8_t uxTaskGetSystemState(uint32_t *pulTotalRunTime);
```

### Memory management

```c
// Allocate memory
void *pvPortMalloc(size_t xWantedSize);

// Free memory
void vPortFree(void *pv);

// Heap utilities (depend on selected heap implementation)
size_t xPortGetFreeHeapSize(void);
size_t xPortGetMinimumEverFreeHeapSize(void);
void vPortInitialiseBlocks(void);
```

### MPU (Memory Protection Unit) functions

```c
// Enable/disable MPU
void vPortStoreTaskMPUSettings(xTaskHandle xTaskToSet, const xMPU_SETTINGS *xMPUSettings, const struct xMemoryRegion * const pxRegions);
void vTaskAllocateMPURegions(xTaskHandle xTaskToSet, const struct xMemoryRegion * const pxRegions);

// MPU fault handlers
void vMPUFaultHandler(void);
```

## Development ecosystem

### IDE support

- **Keil MDK**: Official FreeRTOS integration, examples, and debugging
- **IAR Embedded Workbench**: Full support with plugins
- **STM32CubeIDE**: STM32-specific FreeRTOS integration
- **Arduino IDE**: Via FreeRTOS-Arduino library
- **PlatformIO**: FreeRTOS framework support
- **VS Code**: With Cortex-Debug and OpenOCD
- **ESP-IDF**: Full integration for ESP32

### Debugging tools

- **FreeRTOS Trace Hooks**: Built-in hooks for tracing and debugging
- **FreeRTOS+Trace**: Commercial tracing tool from Percepio (now part of Arm)
- **Tracealyzer**: Visual trace analysis tool
- **SEGGER SystemView**: RTOS-aware debugging
- **J-Link**: SEGGER's debugger with FreeRTOS awareness
- **Lauterbach Trace32**: Professional debugging
- **OpenOCD + GDB**: Open-source debugging
- **ITM/SWO**: ARM CoreSight tracing (on supported hardware)

### Static analysis

- **FreeRTOS Config Checker**: Tool to validate FreeRTOSConfig.h
- **Cppcheck**: Static analysis with FreeRTOS awareness
- **Coverity**: Commercial static analysis
- **Clang-Tidy**: Modern static analysis
- **MISRA C**: FreeRTOS can be configured for MISRA compliance

### Memory analysis

- **Heap usage tracking**: `configUSE_MALLOC_FAILED_HOOK` and custom hooks
- **Stack usage analysis**: `configCHECK_FOR_STACK_OVERFLOW` and
  `configRECORD_STACK_HIGH_ADDRESS`
- **FreeRTOS Task Status**: `uxTaskGetSystemState()` returns task
  status including stack high water mark
- **Static stack analysis**: Tools that analyze stack usage statically

### Timing analysis

- **Runtime statistics**: `configGENERATE_RUN_TIME_STATS` provides
  task execution time statistics
- **Timing measurement**: Use hardware timers or external logic analyzers
- **WCET analysis**: Static analysis tools for worst-case execution time

## Common pitfalls

- **Incorrect FreeRTOSConfig.h**: most issues stem from wrong
  configuration. Validate with FreeRTOS Config Checker.
- **Stack overflow**: most common runtime issue. Use stack fill
  patterns and high-water mark tracking. Size stacks generously.
- **Priority inversion without inheritance**: use `xSemaphoreCreateMutex()`
  (not binary semaphore) for mutual exclusion to get priority inheritance.
- **Using binary semaphore as mutex**: binary semaphores don't have
  priority inheritance. Use mutexes for mutual exclusion.
- **Blocking in ISR**: ISRs cannot block. Use FromISR variants or
  defer work to a task.
- **Not checking return values**: most FreeRTOS functions return
  status. Ignoring pdFAIL/pdPASS can hide bugs.
- **Incorrect tick rate**: too high causes overhead, too low causes
  poor timing resolution. 1000Hz is common for 1ms resolution.
- **Not using timeouts**: always specify timeouts on blocking calls.
  Use `portMAX_DELAY` only for tasks that should block indefinitely.
- **Task priorities not matching requirements**: critical deadline
  tasks must have highest priority. Don't assign based on "importance."
- **Queue overflow**: design queue sizes for worst-case burst.
  Use `uxQueueMessagesWaiting()` to monitor.
- **Memory fragmentation**: with dynamic allocation (heap_1, heap_2,
  heap_3). Consider heap_5 for deterministic systems.
- **MPU configuration errors**: incorrect MPU regions cause hard
  faults. Validate MPU configuration carefully.
- **SMP on unsupported hardware**: SMP requires specific hardware
  support. Check hardware documentation.
- **Tickless idle issues**: tickless idle can affect timing accuracy.
  Disable if precise timing required.

## Best practices

- **Always use static allocation** for production systems to ensure
  deterministic behavior and avoid fragmentation.
- **Name all tasks and queues** with descriptive names for debugging.
- **Use mutexes (not binary semaphores)** for mutual exclusion to get
  priority inheritance automatically.
- **Keep ISRs short**: set a flag or send to a queue, then return.
  Defer actual work to a task.
- **Always specify timeouts**: never use INFINITE_DELAY or portMAX_DELAY
  for production code. Use reasonable timeouts based on design.
- **Use vTaskDelayUntil()** for periodic tasks to avoid drift.
- **Monitor stack usage**: enable stack checking and high-water mark
  tracking. Regularly check stack usage during development.
- **Validate FreeRTOSConfig.h**: use FreeRTOS Config Checker tool.
- **Document task priorities**: in design documentation, explain why
  each task has its priority.
- **Use software timers judiciously**: each timer adds overhead.
  Consider task-based timing for complex timing requirements.
- **Implement watchdog feeding**: dedicate a task to feed hardware
  watchdog. Never feed from ISR.
- **Handle errors**: check all FreeRTOS API return values and handle
  errors appropriately.
- **Design for power saving**: use tickless idle, implement idle hook
  to enter low-power modes, use dynamic voltage scaling if available.
- **Use task notifications** (V9+) for efficient task-to-task
  signaling with minimal overhead.
- **Avoid recursive mutexes** unless necessary. Regular mutexes are
  simpler and more efficient.
- **Initialize all variables**: FreeRTOS tasks start with uninitialized
  stack. Don't assume zero-initialization.

## Integration patterns

### With peripheral drivers

- **Interrupt-driven**: ISR signals task via queue or semaphore
- **Polling**: task polls peripheral in loop (less efficient)
- **DMA**: DMA transfers data directly to/from memory, task notified
  on completion
- **Driver as task**: peripheral driver runs as separate task

### With middleware

- **LwIP (Lightweight IP)**: TCP/IP stack, runs as separate task(s)
- **FatFS**: FAT filesystem, typically runs in task context
- **USB stack**: often runs as separate task
- **CAN stack**: CAN protocol handling as task
- **MQTT client**: network protocol as task

### With safety features

- **Watchdog**: separate task feeds watchdog
- **Error handler**: separate task handles errors and recovery
- **Health monitor**: separate task monitors system health
- **Recovery**: separate task handles system recovery

### With multi-core

- **AMP (Asymmetric Multiprocessing)**: each core runs its own
  FreeRTOS instance
- **SMP (Symmetric Multiprocessing)**: single FreeRTOS instance spans
  multiple cores (V9+)
- **IPC (Inter-Processor Communication)**: queues, mailboxes, or
  shared memory for core-to-core communication

## Testing strategies

- **Unit testing**: test individual tasks in isolation with mocked
  FreeRTOS API
- **Integration testing**: test task interactions with real FreeRTOS
- **Timing testing**: measure and verify timing requirements
- **Stress testing**: create heavy load to verify stability
- **Power testing**: measure power consumption in various states
- **Fault injection**: inject faults (e.g., memory allocation failures)
  to test error handling
- **Coverage**: aim for high coverage of all code paths

## Performance optimization

- **Minimize context switches**: reduce unnecessary task switches
  by designing tasks with appropriate granularity
- **Use appropriate queue lengths**: balance memory usage vs
  blocking probability
- **Optimize ISRs**: keep ISRs as short as possible
- **Use task notifications**: lower overhead than queues for simple
  signaling
- **Disable interrupts judiciously**: use critical sections only
  when absolutely necessary
- **Cache optimization**: align data structures to cache lines,
  minimize cache thrashing
- **Minimize MPU regions**: each MPU region adds overhead to context
  switches
- **Use static allocation**: avoids heap fragmentation and
  allocation overhead
- **Optimize tick rate**: balance timing resolution vs. overhead

## Migration and upgrade

- **Version compatibility**: FreeRTOS maintains good backward
  compatibility. Most applications can upgrade with minimal changes.
- **Configuration file**: the biggest effort is typically updating
  FreeRTOSConfig.h for new features
- **Testing**: thoroughly test after upgrade, especially timing-sensitive
  code
- **Port layer**: port layer may need updates for new FreeRTOS
  versions
- **Third-party integrations**: libraries and middleware may need
  updates for new FreeRTOS versions
- **SafeRTOS**: if using SafeRTOS, upgrade requires consideration of
  safety certification implications

## Common use cases

- **IoT devices**: sensors, actuators, network connectivity
- **Industrial control**: PLCs, motor controllers, HMI interfaces
- **Automotive**: ECUs, ADAS, infotainment (with SafeRTOS or QNX)
- **Medical devices**: patient monitors, infusion pumps (with safety
  certification)
- **Consumer electronics**: wearables, smart home devices
- **Aerospace**: avionics, flight control (with safety certification)
- **Robotics**: motor control, sensor fusion, path planning

## Alternatives and when to use them

- **FreeRTOS**: default choice for most microcontroller applications.
  Lightweight, well-supported, battle-tested.
- **Zephyr**: when need extensive hardware support, modular
  configuration, or Linux compatibility
- **ThreadX**: when need industrial-grade, commercial support, or
  Azure integration
- **SafeRTOS**: when FreeRTOS features needed with safety certification
- **QNX**: when need POSIX compliance, microkernel architecture,
  or high-end industrial/automotive
- **VxWorks**: when need commercial support, extensive ecosystem,
  or defense/aerospace certification
- **Bare metal**: when RTOS overhead unacceptable or system very simple
- **Linux**: when need full OS features, not real-time (consider
  PREEMPT_RT patch for real-time)

## Resources

- **Official website**: https://www.freertos.org/
- **Documentation**: https://www.freertos.org/documentation/
- **Source code**: https://github.com/FreeRTOS/FreeRTOS-Kernel
- **Books**: "Mastering the FreeRTOS Real Time Kernel" by Richard Barry
- **Forums**: https://forums.freertos.org/
- **Blog**: https://www.freertos.org/blog/
- **AWS FreeRTOS**: Extended version with AWS IoT integration
- **FreeRTOS+**: Commercial add-ons (TCP, FAT, CLI, etc.)
