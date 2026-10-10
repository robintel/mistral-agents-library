# Zephyr platform contract

Attaches alongside `patterns/rtos.md` and `patterns/embedded.md`.
A modern, open-source RTOS from the Linux Foundation designed for
security, modularity, and broad hardware support. The era is the
Zephyr version plus the Kconfig configuration; both are named by the
project's configuration.

## Overview

Zephyr is a scalable, secure, and modular RTOS optimized for resource-
constrained embedded systems. It supports multiple architectures and
provides a rich set of subsystems including device drivers, networking
stacks, file systems, and more.

- **License**: Apache 2.0
- **Source**: https://zephyrproject.org/
- **Maintainer**: Linux Foundation
- **Architectures**: ARM Cortex-M/R/A, x86, ARC, RISC-V, NIOS II,XTENSA, and more

## Eras

Zephyr follows semantic versioning with periodic LTS (Long-Term Support)
releases.

- **V1.x series**: Early development (2016-2017)
- **V2.x series**: Major improvements, new architectures (2018-2020)
- **V3.x series**: Significant API changes, improved subsystems (2021-2023)
- **V4.x series**: Current major version (2024+)

**LTS Releases** (recommended for production):
- **v2.7.0 LTS** (2022-2025): "Cinnabar Cod"
- **v3.2.0 LTS** (2023-2026): "Dactyl Dragon"
- **v4.0.0 LTS** (2024-2027): expected

**Kconfig era**: Zephyr uses the Linux kernel's Kconfig system for
configuration. The `.config` file (generated from Kconfig) defines
the build configuration and effectively creates a project-specific era.

**Application era**: The application version and West (Zephyr's build
system/meta-tool) version also affect behavior.

## Idiom and best practices

- **Everything is a device driver**: consistent driver API across
  all hardware peripherals
- **Kconfig-based configuration**: all build options configured via
  menuconfig (GUI) or direct .config editing
- **DTS (Devicetree)**: hardware description using devicetree
  bindings. Defines device instances, properties, and connections.
- **Subsystems**: modular architecture with well-defined interfaces
  between subsystems
- **West build system**: Zephyr's meta-build system that handles
  multiple repositories, boards, and configurations
- **Synchronous by default**: most APIs are synchronous. Asynchronous
  patterns use callbacks, workqueues, or threads
- **Thread-based concurrency**: threads (not tasks) are the primary
  execution unit

## Architecture

### Kernel subsystems

- **Scheduling**: Preemptive priority-based with optional round-robin
  within priority levels
- **Thread management**: k_thread API for thread creation, management,
  and synchronization
- **Memory management**: Multiple allocators (k_malloc, k_calloc,
  k_free), memory pools, slabs
- **Synchronization**: Semaphores, mutexes, FIFOs (queues), lifos,
  message queues, event objects
- **Timers**: Software timers, system clock, uptime
- **Workqueues**: Deferred work execution in thread context
- **Interrupt handling**: ISRs with proper context management

### Device model

- **Device drivers**: uniform API across all device types
- **Driver instances**: each physical device is an instance of a driver
- **Devicetree**: hardware description separate from drivers
- **Driver configuration**: via Kconfig and devicetree

### Subsystems

- **Networking**: Full TCP/IP stack (IPv4/IPv6), BLE, 802.15.4, etc.
- **File systems**: LittleFS, FAT, NFS, RAM disk, etc.
- **Bluetooth**: Host and controller support, multiple profiles
- **USB**: Device and host mode, multiple classes
- **CAN**: CAN FD support, multiple controllers
- **I2C/SPI/UART**: Standard peripheral support
- **GPIO**: General Purpose I/O with interrupt support
- **ADC/DAC**: Analog interfaces
- **PWM**: Pulse Width Modulation
- **DMA**: Direct Memory Access
- **Watchdog**: Hardware watchdog timer support
- **RTC**: Real-Time Clock
- **Logging**: Flexible logging subsystem
- **Shell**: Interactive command-line interface
- **Settings**: Non-volatile configuration storage
- **Power management**: System power state management

## Kconfig configuration

Zephyr's configuration system is based on Linux's Kconfig. Configuration
is hierarchical and can be set at multiple levels.

### Configuration hierarchy

1. **Default configuration**: from subsystems and drivers
2. **Board configuration**: board-specific defaults
3. **Application configuration**: project-specific configuration
4. **Command-line overrides**: via `west build -DCONFIG_xxx=y`

### Common configuration options

```kconfig
# Kernel configuration
CONFIG_SCHEDULER=y
CONFIG_PREEMPT_ENABLED=y
CONFIG_COOP_ENABLED=y
CONFIG_TIMESLICING=y
CONFIG_TIMESLICE_SIZE=10
CONFIG_NUM_PREEMPT_PRIORITIES=15
CONFIG_NUM_COOP_PRIORITIES=8
CONFIG_MAIN_THREAD_PRIORITY=10

# Thread configuration
CONFIG_THREAD_STACK_INFO=y
CONFIG_THREAD_MONITOR=y
CONFIG_THREAD_NAME=y
CONFIG_MAX_THREAD_NAME_LEN=32
CONFIG_THREAD_CUSTOM_DATA=y

# Memory configuration
CONFIG_HEAP_MEM_POOL_SIZE=8192
CONFIG_HEAP_MEM_POOL_MIN_SIZE=16
CONFIG_MPSL livestock=

# Interrupt configuration
CONFIG_IRQ_OFFLOAD=y
CONFIG_GEN_IRQ_START_VECTOR=0
CONFIG_GEN_SWI_START_VECTOR=0

# Logging configuration
CONFIG_LOG=y
CONFIG_LOGinherit _FUNCTION_NAME=y
CONFIG_LOG_BASE_TIMESTAMP=y
CONFIG_LOG_PROCESS_THREAD=y

# Power management
CONFIG_PM=y
CONFIG_PM_DEVICE=y
CONFIG_PM_POLICY_RESIDENCY=y
```

### Viewing and editing configuration

- `west build -t menuconfig`: Interactive GUI configuration
- `west build -t guiconfig`: Alternative GUI (qt based)
- Edit `.config` directly
- `west build -DCONFIG_xxx=y`: Set configuration from command line

## Devicetree

Zephyr uses devicetree to describe hardware. This allows board
configuration to be separate from driver code.

### Devicetree basics

- `.dts` files: human-readable devicetree source
- `.dtb` files: compiled binary devicetree
- Bindings: define properties for each device type

### Example devicetree

```dts
/dts-v1/;

/ {
    model = "Custom Board";
    compatible = "vendor,custom-board";
    
    aliases {
        led0 = &led0;
        serial0 = &uart0;
    };
    
    cpus {
        cpu0: cpu@0 {
            compatible = "arm,cortex-m4";
            reg = <0>;
        };
    };
    
    memory {
        reg = <0x20000000 0x40000>;
    };
    
    soc {
        uart0: serial@40000000 {
            compatible = "vendor,uart";
            reg = <0x40000000 0x1000>;
            interrupts = <20 IRQ_TYPE_LEVEL_HIGH>;
            clocks = <&clk0>;
            status = "okay";
            current-speed = <115200>;
        };
        
        led0: led@50000000 {
            compatible = "gpio-leds";
            gpios = <&gpio0 13 GPIO_ACTIVE_HIGH>;
            label = "LED 0";
        };
    };
};
```

### Devicetree bindings

Each driver type has a binding that defines its properties:

```yaml
# Example binding for a GPIO LED
description: GPIO connected LED

compatible: "gpio-leds"

properties:
  gpios:
    type: phandle-array
    required: true
    description: |
      GPIO specifiers for the LED GPIOs. The first cell is the
      phandle to the GPIO controller, and the subsequent cells
      are the pin number and flags.
  label:
    type: string
    description: Human readable string describing the LED.
```

## Core API

### Thread management

```c
// Thread entry function
typedef void (*k_thread_entry_t)(void *arg1, void *arg2, void *arg3);

// Create a thread (dynamic)
int k_thread_create(
    struct k_thread *thread,
    k_thread_stack_t *stack,
    size_t stack_size,
    k_thread_entry_t entry,
    void *arg1, void *arg2, void *arg3,
    int prio,
    u32_t options,
    s32_t delay
);

// Thread definition (static, preferred)
#define K_THREAD_DEFINE(name, stack_size, prio, options, entry, a1, a2, a3) \
    static char __noinit __stack_##name[stack_size]; \
    static struct k_thread name = { \
        .entry = entry, \
        .stack_info = { \
            .stack_ptr = __stack_##name, \
            .stack_size = stack_size, \
        }, \
        .prio = prio, \
        .options = options, \
        .arg1 = a1, \
        .arg2 = a2, \
        .arg3 = a3, \
    };

// Start a thread
k_thread_start(struct k_thread *thread);

// Suspend/resume a thread
k_thread_suspend(struct k_thread *thread);
k_thread_resume(struct k_thread *thread);

// Abort a thread
k_thread_abort(struct k_thread *thread);

// Join a thread (wait for completion)
k_thread_join(struct k_thread *thread, s32_t timeout);

// Get current thread
struct k_thread *k_current_get(void);

// Thread priority
void k_thread_priority_set(struct k_thread *thread, int prio);
int k_thread_priority_get(struct k_thread *thread);

// Thread name
void k_thread_name_set(struct k_thread *thread, const char *name);
const char *k_thread_name_get(struct k_thread *thread);

// Thread states
enum k_thread_state {
    K_THREAD_STATE_RUNNING,
    K_THREAD_STATE_READY,
    K_THREAD_STATE_PENDING,
    K_THREAD_STATE_SUSPENDED,
    K_THREAD_STATE_ABORTED,
    K_THREAD_STATE_DEAD
};
```

### Synchronization primitives

```c
// Semaphore
struct k_sem sem;
k_sem_init(&sem, 1, 1); // Initial count=1, limit=1 (binary)
k_sem_give(&sem);
k_sem_take(&sem, K_FOREVER);
k_sem_take(&sem, K_MSEC(100)); // With timeout

// Mutex
struct k_mutex mutex;
k_mutex_init(&mutex);
k_mutex_lock(&mutex, K_FOREVER);
k_mutex_unlock(&mutex);

// FIFO (Queue)
struct k_fifo fifo;
K_FIFO_DEFINE(fifo, 10); // Queue of 10 items
k_fifo_put(&fifo, &item);
struct my_data *item = k_fifo_get(&fifo, K_FOREVER);

// LIFO
struct k_lifo lifo;
K_LIFO_DEFINE(lifo);
k_lifo_put(&lifo, &item);
item = k_lifo_get(&lifo, K_FOREVER);

// Message queue (variable size items)
struct k_msgq msgq;
K_MSGQ_DEFINE(msgq, sizeof(my_struct), 10, 4); // 10 items, 4-byte aligned
k_msgq_put(&msgq, &my_struct_instance, K_FOREVER);
void *data = k_msgq_get(&msgq, K_FOREVER);

// Event
struct k_event event;
k_event_init(&event);
k_event_post(&event, EVENT_BIT_0);
k_event_wait(&event, EVENT_BIT_0, false, K_FOREVER);

// Mailbox (single message)
struct k_mailbox mailbox;
K_MAILBOX_DEFINE(mailbox);
k_mailbox_put(&mailbox, &msg, K_FOREVER);
k_mailbox_get(&mailbox, &msg, K_FOREVER);
```

### Memory management

```c
// Dynamic memory allocation
void *k_malloc(size_t size);
void *k_calloc(size_t num, size_t size);
void k_free(void *ptr);

// Memory pool (fixed size blocks)
K_MEM_POOL_DEFINE(pool, block_size, num_blocks, alignment);
void *k_mem_pool_alloc(struct k_mem_pool *pool, k_timeout_t timeout);
void k_mem_pool_free(void *block);

// Slab allocator (for kernel objects)
K_MEM_SLAB_DEFINE(slab, block_size, num_blocks);
void *k_mem_slab_alloc(struct k_mem_slab *slab, k_timeout_t timeout);
void k_mem_slab_free(struct k_mem_slab *slab, void *block);
```

### Timers

```c
// Software timer
typedef void (*k_timer_expired_t)(struct k_timer *timer);

K_TIMER_DEFINE(timer, k_timer_expired_t, NULL);
k_timer_start(&timer, K_SECONDS(1), K_SECONDS(1)); // Periodic, 1s
k_timer_start(&timer, K_MSEC(500), K_NO_WAIT); // One-shot, 500ms
k_timer_stop(&timer);

// System clock (uptime since boot)
u64_t k_uptime_get(void);
u64_t k_uptime_get_32(void);

// High-resolution timer
s64_t k_cyc_get_32(void);
```

### Workqueues

```c
// Workqueue definition
K_WORK_DEFINE(work, work_handler);

// Work item
typedef void (*k_work_handler_t)(struct k_work *work);
struct k_work work_item;
k_work_init(&work_item, work_handler);

// Submit work to default workqueue
k_work_submit(&work_item);

// Delayed work
k_delayed_work_init(&delayed_work, work_handler);
k_delayed_work_submit(&delayed_work, K_SECONDS(1));

// Workqueue with custom thread
struct k_work_q workq;
k_work_q_start(&workq, workq_stack, stack_size, prio);
k_work_q_submit(&workq, &work_item);
```

### Interrupt handling

```c
// ISR definition
void isr_handler(const struct device *dev);

// ISR with IRQ number
IRQ_CONNECT(DT_IRQN(...), priority, isr_handler, 0, 0);
irq_enable(DT_IRQN(...));

// In ISR context
k_is_in_isr(); // Check if in ISR
k_irq_lock();  // Disable interrupts
k_irq_unlock(key); // Restore interrupt state
k_sched_lock(); // Lock scheduler
k_sched_unlock(key); // Unlock scheduler

// ISR-safe functions ( *_irq suffix)
k_fifo_put_irq(&fifo, &item);
item = k_fifo_get_irq(&fifo);
```

### Device driver API

```c
// Get device
const struct device *device_get_binding(const char *name);

// Device configuration from devicetree
#define DT_DRV_COMPAT vendor_model

// GPIO API
const struct device *gpio_dev = device_get_binding(DT_GPIO_CTLR labels);
gpio_pin_configure(gpio_dev, pin, GPIO_OUTPUT);
gpio_pin_set(gpio_dev, pin, 1);

// UART API
const struct device *uart_dev = device_get_binding(DT_UART_0_LABEL);
uart_config_t cfg = {
    .baudrate = 115200,
    .parity = UART_CFG_PARITY_NONE,
    .stop_bits = UART_CFG_STOP_BITS_1,
    .data_bits = UART_CFG_DATA_BITS_8,
};
uart_configure(uart_dev, &cfg);
uart_tx(uart_dev, tx_data, tx_len, SYS_FOREVER_MS);

// I2C API
const struct device *i2c_dev = device_get_binding(DT_I2C_0_LABEL);
u8_t tx_buf[2] = {reg, value};
i2c_write(i2c_dev, tx_buf, 2, addr);

// SPI API
const struct device *spi_dev = device_get_binding(DT_SPI_0_LABEL);
struct spi_config cfg = {.frequency = 1000000, .operation = SPI_OP_MODE_MASTER};
spi_configure(spi_dev, &cfg);
spi_write(spi_dev, tx_buf, tx_len);
```

### Logging

```c
// Logging macros
LOG_MODULE_REGISTER(my_module, LOG_LEVEL_DBG);

LOG_INF("System initialized");
LOG_DBG("Debug value: %d", value);
LOG_ERR("Error occurred");
LOG_WRN("Warning condition");

// Custom log level
LOG_LEVEL_SET(my_module, LOG_LEVEL_DBG);

// Hex dump
LOG_HEXDUMP_INF(data, len, "Data:");
```

## Development ecosystem

### Build system (West)

West is Zephyr's meta-tool that provides a consistent interface across
multiple repositories and build systems.

```bash
# Initialize workspace
west init
west update

# Build for a specific board
west build -b <board_name>

# Build with custom configuration
west build -b <board_name> -DCONFIG_xxx=y

# Flash
west flash

# Debug
west debug

# Run tests
west test
west twister -p <platform>
```

### Supported boards

Zephyr supports hundreds of boards from various vendors:

- **ARM**: STM32 (Nucleo, Discovery, etc.), Nordic (nRF52, nRF91),
  NXP (i.MX, LPC, Kinetis), TI (MSP432, CC32xx), Raspberry Pi Pico
- **x86**: Intel (Galileo, Quark), various x86 emulation (QEMU)
- **RISC-V**: SiFive, GD32V, ESP32-C3/C6
- **ARC**: Synopsys DesignWare
- **XTENSA**: ESP32
- **SPARC**: LEON
- **NIOS II**: Intel
- **Custom**: Any board with devicetree support

### IDE support

- **VS Code**: Official Zephyr extension with IntelliSense
- **Eclipse**: Via Zephyr plugin
- **Segger Embedded Studio**: Full support
- **IAR Embedded Workbench**: Full support
- **Keil MDK**: Full support
- **CLion**: With custom configuration
- **Zephyr Studio**: Standalone IDE from Antmicro

### Debugging tools

- **J-Link**: Full support with Zephyr awareness
- **OpenOCD**: Open-source debugging
- **SEGGER SystemView**: RTOS-aware debugging
- **Lauterbach Trace32**: Professional debugging
- **QEMU**: Emulation for x86, ARM, RISC-V, and more
- **Twister**: Zephyr's test framework

### Testing

- **Unit testing**: `ztest` framework for unit tests
- **Integration testing**: Test applications in `tests/` directory
- **Sample applications**: Examples in `samples/` directory
- **CI testing**: GitHub Actions, Azure Pipelines, GitLab CI
- **Test coverage**: Using various tools (gcov, lcov)

## Common pitfalls

- **Incorrect devicetree**: most hardware-related issues stem from
  incorrect or incomplete devicetree. Validate with `west build -t devicetree`.
- **Missing Kconfig options**: required features not enabled in
  configuration. Check `.config` file.
- **Stack overflow**: common issue. Use `CONFIG_THREAD_STACK_INFO`
  and check stack usage. Size stacks generously.
- **Priority inversion**: use mutexes (not semaphores) for mutual
  exclusion to get priority inheritance.
- **Blocking in ISR**: ISRs cannot block. Use `_irq` variants or defer
  work to a workqueue/thread.
- **Not checking return values**: many Zephyr APIs return error codes.
  Ignoring them hides bugs.
- **Incorrect clock configuration**: system clock not configured
  properly. Check board-specific clock configuration.
- **Memory fragmentation**: with dynamic allocation. Consider
  memory pools or static allocation for critical paths.
- **Driver not enabled**: device driver not enabled for the board.
  Check Kconfig and devicetree.
- **Interrupt priorities**: incorrect interrupt priority configuration.
  Check board-specific interrupt configuration.
- **Power management issues**: not handling power states correctly.
  Check power management configuration and hooks.
- **Networking stack issues**: TCP/IP stack not configured correctly.
  Check networking Kconfig options.
- **Flash vs RAM conflicts**: code placed in RAM when it should be
  in flash. Check linker script and memory configuration.

## Best practices

- **Use devicetree**: describe all hardware in devicetree for
  portability and maintainability.
- **Static allocation**: use `K_THREAD_DEFINE`, `K_SEM_DEFINE`,
  etc. for static object definition when possible.
- **Name all objects**: use descriptive names for threads, semaphores,
  queues, etc. for debugging.
- **Use workqueues**: for deferred work from ISRs. Avoid long ISRs.
- **Always specify timeouts**: never use `K_FOREVER` for production
  code. Use reasonable timeout values.
- **Enable logging**: use `CONFIG_LOG` and appropriate log levels for
  debugging and production.
- **Validate configuration**: use `west build -t menuconfig` to
  review configuration regularly.
- **Document dependencies**: in `CMakeLists.txt` and
  `zephyr/module.yml` for external dependencies.
- **Use Zephyr libraries**: leverage existing subsystems and
  libraries (net, bluetooth, filesystem, etc.) instead of
  reimplementing.
- **Write tests**: use `ztest` framework for unit tests. Aim for
  high coverage.
- **Implement power management**: use power management framework
  for energy-efficient applications.
- **Handle errors**: check all return values and handle errors
  appropriately. Use `LOG_ERR` for error reporting.
- **Design for portability**: use Zephyr APIs and abstractions to
  maximize code portability across boards.
- **Use West**: use West for all build, flash, debug, and test
  operations for consistency.

## Subsystems in detail

### Networking

Zephyr provides a full networking stack with support for:

- **IPv4 and IPv6**: Full dual-stack support
- **TCP and UDP**: Standard transport protocols
- **DHCP**: Dynamic IP address configuration
- **DNS**: Domain name resolution
- **HTTP/HTTPS**: Web server and client
- **MQTT**: Lightweight pub/sub protocol for IoT
- **CoAP**: Constrained Application Protocol
- **LwM2M**: Lightweight M2M protocol
- **6LoWPAN**: IPv6 over Low-Power Wireless Personal Area Networks
- **802.15.4**: IEEE 802.15.4 MAC layer
- **Bluetooth**: Full Bluetooth stack with multiple profiles
- **BLE**: Bluetooth Low Energy
- **Cellular**: LTE-M, NB-IoT (via modem interfaces)
- **WiFi**: WiFi support (station and AP mode)

Configuration options:
```kconfig
CONFIG_NETWORKING=y
CONFIG_NET_IPV4=y
CONFIG_NET_IPV6=y
CONFIG_NET_SOCKETS=y
CONFIG_NET_SOCKETS_POSIX_NAMES=y
```

### Bluetooth

Zephyr has comprehensive Bluetooth support:

- **Bluetooth Classic**: Basic Rate (BR), Enhanced Data Rate (EDR)
- **Bluetooth Low Energy (BLE)**: Full BLE 4.x/5.x support
- **Mesh**: Bluetooth Mesh networking
- **Audio**: Audio profiles and codecs
- **Multiple roles**: Central, Peripheral, Broadcaster, Observer
- **Profiles**: GATT, L2CAP, SMP, ATT, etc.

Configuration:
```kconfig
CONFIG_BT=y
CONFIG_BT_HCI=y
CONFIG_BT_CONN=y
CONFIG_BT_GATT=y
```

### File systems

Zephyr supports multiple file systems:

- **LittleFS**: Wear-leveling, power-fail safe, designed for flash
- **FAT**: Standard FAT filesystem (FAT12/16/32)
- **NFS**: Network File System client
- **RAM disk**: File system in RAM for testing
- **Custom**: Implement custom file system drivers

Configuration:
```kconfig
CONFIG_FS=y
CONFIG_FS_LITTLEFS=y
CONFIG_FS_FAT=y
```

### Power management

Zephyr's power management framework helps minimize power consumption:

- **Power states**: Active, Idle, Sleep, Deep Sleep, Off
- **Device power management**: Per-device power state control
- **System power management**: Coordinate power states across devices
- **Power policies**: Residency, Suspend, Always-on
- **Wakeup sources**: Configure which devices can wake the system
- **Power state constraints**: Prevent system from entering low-power
  states when constraints exist

Configuration:
```kconfig
CONFIG_PM=y
CONFIG_PM_DEVICE=y
CONFIG_PM_POLICY_RESIDENCY=y
```

## Integration patterns

### With peripheral drivers

- **Interrupt-driven**: ISR signals workqueue or thread via
  k_work_submit
- **Polling**: thread polls peripheral (less efficient)
- **Callback**: driver calls callback on event
- **Asynchronous**: driver supports asynchronous operations

### With middleware

- **Networking stack**: runs as separate threads
- **File system**: typically runs in calling thread context
- **Bluetooth stack**: runs as separate threads with dedicated stack
- **USB stack**: runs as separate threads
- **Custom middleware**: integrate as threads or workqueues

### With safety features

- **Watchdog**: separate thread or driver handles watchdog feeding
- **Error handler**: separate thread handles system errors
- **Health monitor**: separate thread monitors system health
- **Recovery**: implement system recovery in error handler

### With multi-core

- **AMP (Asymmetric Multiprocessing)**: each core runs its own
  Zephyr instance with different configurations
- **SMP (Symmetric Multiprocessing)**: single Zephyr instance spans
  multiple cores (experimental)
- **IPC**: Use shared memory, mailboxes, or custom IPC mechanisms
- **OpenAMP**: Framework for AMP communication

## Testing strategies

- **Unit testing**: use `ztest` framework in `tests/unit/`
- **Integration testing**: test subsystems in `tests/integration/`
- **Application testing**: test complete applications in `tests/sample/`
- **Board testing**: test on specific boards in `tests/boards/`
- **Continuous Integration**: run tests on GitHub Actions or other CI
- **Test coverage**: use coverage tools (gcov, lcov) with test runs

Example unit test:
```c
#include <ztest.h>

void test_my_function(void)
{
    int result = my_function(2, 3);
    zassert_equal(result, 5, "2+3 should equal 5");
}

ZTEST_SUITE(test_suite, NULL, NULL, NULL, NULL, NULL);
ZTEST(test_suite, test_my_function);
```

## Performance optimization

- **Minimize context switches**: design threads with appropriate
  granularity, avoid unnecessary wakeups
- **Use workqueues**: for deferred work to avoid blocking
- **Optimize ISRs**: keep ISRs short, use `_irq` variants
- **Use static allocation**: avoid dynamic memory allocation overhead
- **Cache optimization**: align data structures, minimize cache thrashing
- **Disable interrupts judiciously**: use critical sections sparingly
- **Use appropriate priorities**: don't use too many priority levels
- **Optimize devicetree**: ensure hardware description is accurate
  and efficient
- **Profile with tools**: use SystemView, Tracealyzer, or custom
  profiling to identify bottlenecks

## Migration and upgrade

- **Version compatibility**: Zephyr maintains API compatibility
  within major versions. Check release notes for breaking changes.
- **Kconfig changes**: configuration options may change between
  versions. Review `.config` after upgrade.
- **Devicetree changes**: devicetree bindings may change. Review
  devicetree files after upgrade.
- **Driver changes**: device drivers may have changes. Review
  driver API after upgrade.
- **Testing**: thoroughly test after upgrade, especially hardware-specific
  code
- **LTS releases**: for production, use LTS releases with longer
  support windows

## Common use cases

- **IoT devices**: sensors, actuators, network connectivity
- **Wearables**: health monitoring, fitness tracking
- **Industrial control**: PLCs, motor controllers, HMI
- **Medical devices**: patient monitors, infusion pumps
- **Automotive**: ECUs, ADAS, gateways (often with safety extensions)
- **Consumer electronics**: smart home, audio, appliances
- **Aerospace**: avionics, flight control (with safety certification)
- **Robotics**: motor control, sensor fusion
- **Gateways**: protocol translation, data aggregation
- **Edge computing**: local data processing, AI inference

## Alternatives and when to use them

- **FreeRTOS**: when need lightweight, battle-tested RTOS with wide
  industry adoption. Better for very resource-constrained systems.
- **Zephyr**: when need modularity, extensive hardware support,
  multiple subsystems, or Linux compatibility. Better for complex
  applications with many features.
- **ThreadX**: when need industrial-grade, commercial support, or
  Azure integration
- **SafeRTOS**: when need FreeRTOS features with safety certification
- **QNX**: when need POSIX compliance, microkernel architecture, or
  high-end industrial/automotive
- **VxWorks**: when need commercial support, extensive ecosystem, or
  defense/aerospace certification
- **Bare metal**: when RTOS overhead unacceptable or system very simple
- **Linux**: when need full OS features, not hard real-time (consider
  PREEMPT_RT or real-time extensions)

## Resources

- **Official website**: https://zephyrproject.org/
- **Documentation**: https://docs.zephyrproject.org/
- **Source code**: https://github.com/zephyrproject-rtos/zephyr
- **GitHub**: https://github.com/zephyrproject-rtos
- **Slack/Discord**: Community chat channels
- **Mailing lists**: zephyr-devel@lists.zephyrproject.org
- **Books**: "Getting Started with Zephyr RTOS" by Anas Malik
- **Conference**: Zephyr Developer Summit (annual)
- **West documentation**: https://docs.zephyrproject.org/latest/develop/west/index.html
- **API documentation**: https://docs.zephyrproject.org/latest/reference/
