# QNX platform contract

Attaches alongside `patterns/rtos.md` and `patterns/embedded.md`.
A microkernel-based, POSIX-compliant RTOS from BlackBerry (formerly
QNX Software Systems) designed for reliability, scalability, and
real-time performance. The era is the QNX version plus the board
support package; both are named by the project's configuration.

## Overview

QNX is a Unix-like real-time operating system based on a microkernel
architecture. It provides a full-featured operating system with
POSIX compliance, making it familiar to Unix/Linux developers while
providing real-time capabilities.

- **Architecture**: Microkernel (separate address spaces for kernel and processes)
- **License**: Commercial (free for non-commercial use)
- **Source**: https://www.qnx.com/
- **Maintainer**: BlackBerry Limited
- **Architectures**: ARM (Cortex-A/R), x86 (32-bit and 64-bit), PowerPC,
  MIPS, SH, and more
- **Certifications**: ISO 26262 (ASIL D), IEC 61508 (SIL 3/4), DO-178C
  (Level A), EN 50128, IEC 62304, Common Criteria EAL4+

## Eras

QNX versions are the era markers. The versioning scheme has evolved:

- **QNX 4**: Classic era (1990s-early 2000s), still in use in legacy systems
- **QNX 6.0 - 6.3**: "Neutrino" era, major architectural changes
- **QNX 6.4 - 6.5**: Maturity era, widespread adoption
- **QNX 6.6**: Current LTS (Long-Term Support) version (as of 2024)
- **QNX 7.0**: Next major version with new features (in development)

**Board Support Package (BSP) era**: The BSP provides the interface
between QNX and the specific hardware. BSP versions are often tied to
QNX versions but can be updated independently.

**Kernel variants**:
- **Standard kernel**: For most applications
- **SMP (Symmetric Multi-Processing) kernel**: For multi-core systems
- **Safety kernel**: For safety-critical applications
- **Secure kernel**: For security-critical applications with additional
  security features

## Architecture

### Microkernel design

QNX uses a **microkernel architecture** where the kernel provides only
core functions and all other services run as separate processes:

- **Kernel**: Memory management, scheduling, interprocess communication,
  interrupt handling
- **Process manager**: Creates and manages processes
- **File system manager**: Manages file systems (native, ext2, FAT, etc.)
- **Device managers**: Manage hardware devices
- **Network manager**: Network stack
- **I/O manager**: Input/output subsystem

This design provides:
- **Fault isolation**: A crash in one component doesn't crash the system
- **Scalability**: Only needed components are included
- **Reliability**: Reduced kernel size means fewer bugs
- **Real-time performance**: Minimal kernel overhead

### Key features

- **POSIX compliance**: Most POSIX APIs are supported
- **Message passing**: Primary interprocess communication mechanism
- **Resource managers**: Servers that manage resources (files, devices, etc.)
- **Path space**: Namespace for resources
- **Process groups**: Collection of processes with shared properties
- **Signal handling**: Unix-style signals with real-time extensions
- **Threads**: Lightweight execution units within processes
- **Synchronization**: Mutexes, semaphores, condition variables, barriers
- **Timers**: Software timers with various timer types

## Idiom and best practices

- **Everything is a file**: Unix philosophy - devices, pipes, sockets
  are all accessed via file system interface
- **Message passing is king**: Primary IPC mechanism between processes
- **Resource managers are servers**: File systems, devices, etc. are
  implemented as resource manager servers
- **Path space is the namespace**: All resources are accessed via paths
  in the path space
- **Small processes**: Each process should do one thing well
- **Error handling**: Always check return values from system calls
- **Signals for events**: Use signals for event notification and handling
- **Resource managers for hardware**: Implement hardware drivers as
  resource managers

## Core concepts

### Message passing

Message passing is the primary IPC mechanism in QNX:

- **Client-server model**: Clients send messages to servers (resource
  managers) to request services
- **Synchronous**: Client blocks until server responds (default)
- **Asynchronous**: Client can continue while server processes
- **Message types**: Each resource manager defines its own message types
- **Message structure**: Typically a header (type, subtype) + data

Example message structure:
```c
typedef struct {
    uint16_t    type;   // Message type
    uint16_t    subtype; // Message subtype
    // Data follows
} my_message_t;
```

### Resource managers

Resource managers manage resources (files, devices, etc.):

- **File system resource managers**: Manage file systems
- **Device resource managers**: Manage hardware devices
- **Custom resource managers**: Can be created for any resource type
- **Path prefix**: Each resource manager registers a path prefix
  (e.g., "/dev/serial" for serial port driver)

Resource managers implement standard handlers:
- **open()**: Open a resource
- **close()**: Close a resource
- **read()**: Read from a resource
- **write()**: Write to a resource
- **ioctl()**: Device-specific operations
- **devctl()**: Device control operations
- **stat()**: Get status information

### Path space

The path space is QNX's namespace for resources:

- **Hierarchical**: Paths are hierarchical (e.g., "/dev/serial0")
- **Dynamic**: Paths can be added/removed at runtime
- **Virtual**: Paths can be virtual (not corresponding to actual files)
- **Mounting**: File systems and resource managers are "mounted" at
  specific path prefixes

Common path prefixes:
- `/`: Root of the entire path space
- `/dev`: Device files
- `/proc`: Process information
- `/fs`: File systems
- `/net`: Network-related resources
- `/tmp`: Temporary files
- `/usr`: User files

### Processes and threads

- **Process**: Execution environment with its own address space
- **Thread**: Lightweight execution unit within a process
- **Process creation**: `spawn()` or `fork()` (POSIX)
- **Thread creation**: `pthread_create()` (POSIX)
- **Process groups**: Collection of processes with shared properties
- **Process environment**: Each process has its own environment variables

### Scheduling

- **Priority-based preemptive scheduling**: Default scheduling algorithm
- **Round-robin**: Within same priority level
- **Sporadic**: For aperiodic threads
- **FIFO**: First-in-first-out scheduling
- **SMP**: Symmetric Multi-Processing for multi-core systems
- **Priority inheritance**: For mutexes to prevent priority inversion

Priority ranges:
- **0**: Lowest priority
- **255**: Highest priority (real-time)
- **10-15**: Default range for normal processes
- **20+**: Typically used for real-time processes

### Synchronization

- **Mutexes**: `pthread_mutex_t` (POSIX)
- **Semaphores**: `sem_t` (POSIX)
- **Condition variables**: `pthread_cond_t` (POSIX)
- **Barriers**: `pthread_barrier_t` (POSIX)
- **Message queues**: `mqd_t` (POSIX)
- **QNX-specific**: Additional synchronization primitives

### Signals

- **Standard POSIX signals**: SIGINT, SIGTERM, SIGKILL, etc.
- **Real-time signals**: SIGRTMIN to SIGRTMAX
- **Signal handlers**: `signal()` or `sigaction()` (POSIX)
- **Signal sets**: `sigset_t` for managing sets of signals
- **Signal waiting**: `sigsuspend()`, `sigwait()`, `sigwaitinfo()`

### Timers

- **Software timers**: `timer_create()` (POSIX)
- **Timer types**: CLOCK_REALTIME, CLOCK_MONOTONIC, etc.
- **Timer notification**: Via signals or thread creation
- **Cyclic timers**: Timers that fire periodically
- **One-shot timers**: Timers that fire once

## Development ecosystem

### Supported platforms

QNX supports a wide range of platforms through BSPs:

- **ARM Cortex-A**: ARMv7-A, ARMv8-A (32-bit and 64-bit)
  - NXP i.MX 6/8, Texas Instruments OMAP, Qualcomm Snapdragon, etc.
- **ARM Cortex-R**: For real-time applications
- **x86**: 32-bit and 64-bit processors
  - Intel, AMD, VIA, and others
- **PowerPC**: Various PowerPC processors
- **MIPS**: MIPS32 and MIPS64
- **SH**: Renesas SH processors
- **Custom**: Any platform with a BSP

### Board Support Packages (BSPs)

BSPs provide the interface between QNX and specific hardware:

- **Start-up code**: Bootloader and early initialization
- **Hardware abstraction**: Access to hardware-specific features
- **Interrupt handling**: Configuration and handling of interrupts
- **Memory mapping**: Memory layout configuration
- **Clock configuration**: System clock setup
- **Device drivers**: Drivers for on-board peripherals

BSPs can be:
- **Generic**: For a family of processors (e.g., ARMv7)
- **Specific**: For a specific board (e.g., Raspberry Pi)
- **Custom**: Created for custom hardware

### IDE support

- **QNX Momentics IDE**: Official IDE from QNX (Eclipse-based)
- **Visual Studio**: With QNX plugins
- **VS Code**: With QNX extensions
- **Eclipse**: With QNX plugins
- **Command-line tools**: Full development possible via command line

### Build system

- **Makefiles**: Traditional make-based build system
- **QNX Recursive Make (qcc)**: QNX's own build tool
- **CMake**: Supported via toolchain files
- **QNX Build Files (.mk)**: Special makefiles for QNX projects

Example build command:
```bash
# Compile and link
qcc -Vgcc_ntoaarch64 -lang-c -o myapp myapp.c

# Create image for target
mkifs -v myapp myapp.ifs
```

### Debugging tools

- **QNX Momentics IDE Debugger**: Full-featured debugger
- **GDB**: GNU Debugger with QNX support
- **pdebug**: QNX-specific debugger
- **pidin**: Process information utility (shows all processes and threads)
- **sin**: Signal injection utility
- **dumpmem**: Memory dump utility
- **tracelogger**: System tracing utility
- **slogger**: System logger for debugging

### Profiling tools

- **tracelogger**: Kernel-level tracing with microsecond precision
- **procntime**: Process and thread CPU time profiling
- **pm**: Performance monitoring tool
- **mem**: Memory usage monitoring
- ** Valgrind**: Memory leak detection (modified for QNX)

### Networking

- **Full TCP/IP stack**: IPv4 and IPv6 support
- **Socket API**: Standard BSD socket API
- **Network managers**: Various network managers available
- **Routing**: Advanced routing capabilities
- **Firewall**: Built-in packet filtering
- **VPN**: Virtual Private Network support
- **QoS**: Quality of Service support
- **Multicast**: IP multicast support

### File systems

QNX supports multiple file systems:

- **QNX4FS**: Native QNX file system (power-fail safe)
- **Ext2/3/4**: Linux extended file systems
- **FAT16/32**: FAT file systems
- **NTFS**: NT File System (read-only)
- **CDFS**: CD-ROM File System
- **NFS**: Network File System
- **CIFS**: Common Internet File System (SMB)
- **RAM disk**: In-memory file system
- **Flash file systems**: For flash memory devices

### Graphics

- **Photon microGUI**: Native QNX GUI system
- **Screen graphics**: Library for graphics applications
- **OpenGL ES**: Embedded OpenGL support
- **Wayland**: Wayland display server protocol support
- **X11**: X Window System support (legacy)

## Configuration

### System configuration

QNX system configuration is done through various files:

- **Build files**: `.mk` files for project configuration
- **Image files**: `.ifs` files for system image configuration
- **BSP configuration**: Board-specific configuration
- **Kernel configuration**: Kernel build configuration

### Build file (.mk) example

```makefile
# Project build file
APP_NAME = myapp
APP_CFLAGS = -lang-c -O2
APP_SRCS = main.c utils.c

# Include paths
APP_INCLUDES = . include

# Libraries
APP_LIBS = socket c

# Target architecture
TARGET_ARCH = aarch64le

include $(MKFILES_PATH)/qtarget.mk
```

### Image file (.ifs) example

```ifs
[virtual=x86,bios +compress] .bootstrap = {
    startup -n `/usr/bin/startup`
    PATH=/proc/boot:/bin:/usr/bin LD_LIBRARY_PATH=/proc/boot:/lib:/usr/lib:/lib procnto
}

[+script] startup-script = {
    # Start necessary drivers
    devc-ser8250 -e -b115200 /dev/ser1 &
    
    # Start application
    myapp &
}

[perms] .script = 777
[perms] .bin = 555
[perms] .text = 555

# File systems
[+session] tmp=devf-mqueue
[+session] fs-qnx4.so
[+session] fs-ext2.so

# Networking
[+session] io-pkt-v4-hc -dne2000
[+session] io-pkt-v6-hc -dne2000
```

### Kernel configuration

Kernel configuration is typically done through command-line options
when building the kernel:

```bash
# Build a custom kernel
qnx-build kernel -v -n -o /path/to/output /path/to/bsp
```

Common kernel options:
- **SMP**: Enable Symmetric Multi-Processing
- **Memory**: Configure physical memory
- **Interrupts**: Configure interrupt controllers
- **Timers**: Configure timer sources
- **Scheduling**: Configure scheduling algorithms
- **Features**: Enable/disable various kernel features

## Core API

### Process management

```c
// Process creation (POSIX)
pid_t fork(void);
pid_t vfork(void);

// Process creation with attributes (POSIX)
int posix_spawn(pid_t *pid, const char *path, const posix_spawn_file_actions_t *file_actions, 
               const posix_spawnattr_t *attrp, char *const argv[], char *const envp[]);

// Process creation (QNX-specific)
pid_t spawn(const char *path, int argc, char *const argv[], char *const envp[]);
pid_t spawnl(const char *path, const char *arg0, ...);

// Process termination
void exit(int status);
void _exit(int status);

// Process information
pid_t getpid(void);
pid_t getppid(void);
int getpriority(int which, id_t who);
int setpriority(int which, id_t who, int prio);

// Process control
int kill(pid_t pid, int sig);
int sigsend(pid_t pid, int sig);
int raise(int sig);
```

### Thread management

```c
// Thread creation (POSIX)
int pthread_create(pthread_t *thread, const pthread_attr_t *attr, 
                   void *(*start_routine)(void *), void *arg);

// Thread attributes
int pthread_attr_init(pthread_attr_t *attr);
int pthread_attr_destroy(pthread_attr_t *attr);
int pthread_attr_setdetachstate(pthread_attr_t *attr, int detachstate);
int pthread_attr_setstack(pthread_attr_t *attr, void *stackaddr, size_t stacksize);
int pthread_attr_setschedparam(pthread_attr_t *attr, const struct sched_param *param);

// Thread management
int pthread_join(pthread_t thread, void **value_ptr);
int pthread_detach(pthread_t thread);
int pthread_cancel(pthread_t thread);

// Thread synchronization
int pthread_equal(pthread_t t1, pthread_t t2);
pthread_t pthread_self(void);

// Thread scheduling
int pthread_setschedparam(pthread_t thread, int policy, const struct sched_param *param);
int pthread_getschedparam(pthread_t thread, int *policy, struct sched_param *param);

// Thread-specific data
int pthread_key_create(pthread_key_t *key, void (*destr_function)(void *));
int pthread_key_delete(pthread_key_t key);
void *pthread_getspecific(pthread_key_t key);
int pthread_setspecific(pthread_key_t key, const void *value);
```

### Message passing

```c
// Open a connection to a resource manager
int open(const char *path, int oflag, ...);

// Close a connection
int close(int fd);

// Read from a resource manager
ssize_t read(int fd, void *buf, size_t nbytes);

// Write to a resource manager
ssize_t write(int fd, const void *buf, size_t nbytes);

// Device control operations
int devctl(int fd, int dcmd, void *data, size_t nbytes, int *info);

// IO control operations (POSIX)
int ioctl(int fd, int request, ...);

// Status operations
int fstat(int fd, struct stat *buf);
int stat(const char *path, struct stat *buf);

// Select (POSIX)
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, 
           struct timeval *timeout);

// Poll (POSIX)
int poll(struct pollfd *fds, nfds_t nfds, int timeout);
```

### Resource manager API

```c
// Resource manager context structure
typedef struct {
    // Various fields for resource manager state
} resource_manager_context_t;

// Resource manager open handler
int my_open(resource_manager_context_t *ctp, io_open_t *msg);

// Resource manager close handler
int my_close(resource_manager_context_t *ctp, io_close_t *msg);

// Resource manager read handler
int my_read(resource_manager_context_t *ctp, io_read_t *msg, RESMGR_OCB_T *ocb);

// Resource manager write handler
int my_write(resource_manager_context_t *ctp, io_write_t *msg, RESMGR_OCB_T *ocb);

// Resource manager devctl handler
int my_devctl(resource_manager_context_t *ctp, io_devctl_t *msg, RESMGR_OCB_T *ocb);

// Register a resource manager
int resmgr_attach(dispatch_t *dpp, resource_manager_context_t **ctpp, 
                 resmgr_attr_t *attr, resmgr_connect_funcs_t *connect_funcs, 
                 resmgr_io_funcs_t *io_funcs, char *device_name);
```

### Synchronization

```c
// Mutex (POSIX)
int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr);
int pthread_mutex_destroy(pthread_mutex_t *mutex);
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);
int pthread_mutex_timedlock(pthread_mutex_t *mutex, const struct timespec *abstime);
int pthread_mutex_unlock(pthread_mutex_t *mutex);

// Semaphore (POSIX)
int sem_init(sem_t *sem, int pshared, unsigned int value);
int sem_destroy(sem_t *sem);
int sem_wait(sem_t *sem);
int sem_trywait(sem_t *sem);
int sem_timedwait(sem_t *sem, const struct timespec *abstime);
int sem_post(sem_t *sem);

// Condition variable (POSIX)
int pthread_cond_init(pthread_cond_t *cond, const pthread_condattr_t *attr);
int pthread_cond_destroy(pthread_cond_t *cond);
int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);
int pthread_cond_timedwait(pthread_cond_t *cond, pthread_mutex_t *mutex, 
                           const struct timespec *abstime);
int pthread_cond_signal(pthread_cond_t *cond);
int pthread_cond_broadcast(pthread_cond_t *cond);

// Barrier (POSIX)
int pthread_barrier_init(pthread_barrier_t *barrier, const pthread_barrierattr_t *attr, 
                          unsigned count);
int pthread_barrier_destroy(pthread_barrier_t *barrier);
int pthread_barrier_wait(pthread_barrier_t *barrier);
```

### Signals

```c
// Signal handling (POSIX)
int signal(int sig, void (*func)(int));
int sigaction(int sig, const struct sigaction *act, struct sigaction *oact);

// Signal sets
int sigemptyset(sigset_t *set);
int sigfillset(sigset_t *set);
int sigaddset(sigset_t *set, int signo);
int sigdelset(sigset_t *set, int signo);
int sigismember(const sigset_t *set, int signo);

// Signal masking
int sigprocmask(int how, const sigset_t *set, sigset_t *oset);
int pthread_sigmask(int how, const sigset_t *set, sigset_t *oset);

// Signal waiting
int sigsuspend(const sigset_t *mask);
int sigwait(const sigset_t *set, int *sig);
int sigwaitinfo(const sigset_t *set, siginfo_t *info);

// Signal sending
int kill(pid_t pid, int sig);
int sigsend(pid_t pid, int sig);
int raise(int sig);

// Signal queue (real-time signals)
int sigqueue(pid_t pid, int sig, const union sigval value);
```

### Timers

```c
// Timer creation (POSIX)
int timer_create(clockid_t clockid, struct sigevent *evp, timer_t *timerid);
int timer_delete(timer_t timerid);

// Timer setting
int timer_settime(timer_t timerid, int flags, const struct itimerspec *value, 
                  struct itimerspec *ovalue);
int timer_gettime(timer_t timerid, struct itimerspec *value);

// Timer notification via signal
struct sigevent evp;
evp.sigev_notify = SIGEV_SIGNAL;
evp.sigev_signo = SIGALRM;
evp.sigev_value.sival_ptr = &timerid;

// Timer notification via thread creation
evp.sigev_notify = SIGEV_THREAD;
evp.sigev_notify_function = timer_thread;
evp.sigev_notify_attributes = &attr;

// High-resolution timers
int clock_getres(clockid_t clockid, struct timespec *res);
int clock_gettime(clockid_t clockid, struct timespec *tp);
int clock_settime(clockid_t clockid, const struct timespec *tp);

// QNX-specific timers
int TimerCreate(int clock_id, struct sigevent *event);
int TimerDestroy(int timer_id);
```

### Interrupt handling

```c
// Interrupt attachment
int InterruptAttach(int intr, const struct sigevent *(*handler)(void *, int), 
                    const void *area, int size, unsigned flags);

// Interrupt wait
int InterruptWait(int intr, struct _msg_info *info);

// Interrupt mask
int InterruptMask(int intr, int id);
int InterruptUnmask(int intr, int id);

// Interrupt disable/enable
int InterruptDisable(void);
void InterruptEnable(void);

// Interrupt handler (QNX-style)
const struct sigevent *interrupt_handler(void *area, int id);

// Signal-based interrupt handling
int ConnectAttach(int chid, pid_t pid, int signo, _Uint32t code, int flags);
```

## Common pitfalls

- **Resource leaks**: Not closing file descriptors or releasing
  resources. Always close what you open.
- **Memory leaks**: Not freeing allocated memory. Use `malloc_g()`
  and `free()` for tracked memory.
- **Incorrect error handling**: Not checking return values from system
  calls. Most QNX calls return -1 on error with errno set.
- **Blocking in signal handlers**: Signal handlers should be short
  and not block. Use `SA_SIGINFO` for async-signal-safe functions.
- **Priority inversion**: Not using priority inheritance mutexes for
  shared resources. Use `PTHREAD_MUTEX_RECURSIVE_NP` or
  `PTHREAD_MUTEX_ERRORCHECK_NP`.
- **Message passing deadlocks**: Circular dependencies in message
  passing. Design carefully to avoid deadlocks.
- **Path space issues**: Incorrect path configurations. Verify all
  paths with `ls` or `ls -R`.
- **BSP issues**: Hardware-specific issues due to incorrect BSP
  configuration. Verify BSP for your hardware.
- **Memory exhaustion**: Not checking for memory allocation failures.
  Always check return values from malloc.
- **Thread stack overflow**: Not sizing thread stacks correctly.
  Use `pthread_attr_setstacksize()` with adequate sizes.
- **Interrupt handling issues**: Not handling interrupts correctly.
  Use InterruptAttach/InterruptWait or signal-based handling.
- **Process vs thread confusion**: Not understanding the difference.
  Processes have separate address spaces; threads share address space.
- **Scheduling issues**: Not setting priorities correctly. Remember
  that real-time priorities (20+) preempt all lower priorities.
- **Resource manager issues**: Not implementing resource manager
  handlers correctly. Follow the resource manager template.
- **Not using QNX utilities**: Not using QNX-specific utilities like
  `pidin`, `sin`, `slogger`, etc. for debugging.

## Best practices

- **Use QNX utilities**: Use `pidin`, `sin`, `slogger`, `use`, `mem`,
  etc. for system monitoring and debugging.
- **Check return values**: Always check return values and errno for
  errors. Use `strerror()` or `perror()` for error messages.
- **Use resource managers**: Implement device drivers and services as
  resource managers for consistency.
- **Design for fault isolation**: Use separate processes for separate
  functions to achieve fault isolation.
- **Use message passing**: Prefer message passing over shared memory
  for interprocess communication.
- **Manage resources**: Always close file descriptors, free memory,
  and release other resources when done.
- **Use path space effectively**: Organize resources in a logical
  path space hierarchy.
- **Configure priorities**: Set process and thread priorities based on
  real-time requirements.
- **Use signals for events**: Use signals for event notification and
  handling. Real-time signals for urgent events.
- **Implement proper error handling**: Handle errors gracefully and
  provide meaningful error messages.
- **Use QNX persistence**: Use `persistent` attribute for resource
  managers to survive restarts.
- **Design for startup**: Create proper startup scripts in `.ifs` files
  to start required services.
- **Use Build files**: Use `.mk` build files for reproducible builds.
- **Test on target**: Always test on actual target hardware, not just
  simulation.
- **Use tracing**: Use `tracelogger` for kernel-level tracing of
  performance issues.
- **Profile memory**: Use `mem` utility to monitor memory usage.

## Integration patterns

### With hardware

- **Device resource managers**: Implement hardware drivers as device
  resource managers
- **Direct register access**: Use `mmap_device_memory()` for direct
  hardware register access
- **Interrupt handling**: Use InterruptAttach/InterruptWait or
  signal-based handling
- **DMA**: Use DMA resource managers for efficient data transfer
- **Hardware watchdog**: Integrate with QNX watchdog facilities

### With middleware

- **File systems**: Mount file systems at appropriate path prefixes
- **Networking**: Configure network interfaces and managers
- **Graphics**: Use Photon or other graphics subsystems
- **Audio**: Use audio resource managers
- **USB**: Use USB resource managers
- **CAN**: Use CAN resource managers

### With safety features

- **Safety kernel**: Use safety-certified kernel for safety-critical
  applications
- **Process isolation**: Use separate processes for safety-critical
  and non-critical functions
- **Resource monitoring**: Monitor system resources and take action
  when thresholds are exceeded
- **Watchdog**: Use hardware watchdog with QNX watchdog facilities
- **Error handling**: Implement comprehensive error handling and
  recovery

### With multi-core

- **SMP (Symmetric Multi-Processing)**: Use SMP kernel for multi-core
  systems. Threads can run on any core.
- **Bound threads**: Bind threads to specific cores using
  `pthread_setaffinity_np()`
- **Core isolation**: Reserve cores for specific purposes (e.g.,
  real-time on core 0, non-real-time on core 1)
- **IPC**: Use message passing or shared memory for inter-core
  communication

### With real-time extensions

- **Priority inheritance**: Use priority inheritance mutexes to
  prevent priority inversion
- **Real-time signals**: Use SIGRTMIN to SIGRTMAX for real-time
  signal handling
- **Timers**: Use high-resolution timers for precise timing
- **Scheduling**: Use appropriate scheduling policies (SCHED_FIFO,
  SCHED_RR, SCHED_SPORADIC)

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
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <errno.h>
#include <string.h>

void *test_thread(void *arg) {
    // Test code
    return NULL;
}

int main(void) {
    pthread_t thread;
    int rc;
    
    rc = pthread_create(&thread, NULL, test_thread, NULL);
    if (rc != 0) {
        fprintf(stderr, "pthread_create failed: %s\n", strerror(rc));
        exit(EXIT_FAILURE);
    }
    
    pthread_join(thread, NULL);
    return EXIT_SUCCESS;
}
```

## Performance optimization

- **Minimize context switches**: Design threads with appropriate
  granularity
- **Use efficient IPC**: Message passing is efficient but has overhead.
  Minimize message size and frequency.
- **Use shared memory**: For high-bandwidth, low-latency communication
  between processes
- **Optimize resource managers**: Keep resource manager handlers
  efficient and non-blocking when possible
- **Use appropriate scheduling**: SCHED_FIFO for real-time threads,
  SCHED_RR for fairness
- **Minimize system calls**: System calls have overhead. Minimize
  frequency where possible.
- **Use direct register access**: For performance-critical hardware
  access, use `mmap_device_memory()`
- **Tune kernel parameters**: Adjust kernel parameters for specific
  application requirements
- **Use trace tools**: Use `tracelogger` to identify performance
  bottlenecks
- **Profile with pm**: Use performance monitoring tools

## Migration and upgrade

- **Version compatibility**: QNX maintains good backward compatibility.
  Most applications can upgrade with minimal changes.
- **BSP updates**: BSPs may need updates for new QNX versions.
  Check BSP compatibility.
- **API changes**: Some API changes between major versions. Check
  release notes and migration guides.
- **Configuration**: Review and update build files and configurations.
- **Testing**: Thoroughly test after upgrade, especially on target
  hardware.
- **Driver updates**: Device drivers may need updates for new QNX
  versions.
- **Tool updates**: Update development tools (compiler, debugger, etc.)
  for new QNX versions.

## Common use cases

- **Automotive**: Infotainment, ADAS, autonomous driving, digital
  instrument clusters
- **Medical devices**: MRI machines, patient monitors, surgical
  robots, infusion pumps
- **Industrial automation**: PLCs, HMIs, robotics, machine control
- **Aerospace**: Avionics, flight control, cabin systems
- **Defense**: Military command and control, radar, sonar
- **Transportation**: Railway signaling, train control, airline
  reservation systems
- **Telecom**: Base stations, telecom switches, network appliances
- **Consumer electronics**: Smart TVs, set-top boxes, gaming consoles
- **Networking equipment**: Routers, switches, firewalls, load balancers
- **Energy**: Smart grid, power plant control, SCADA systems

## Safety and certification

QNX is used in safety-critical applications with various certifications:

### Available certifications

- **ISO 26262**: ASIL D for automotive (highest level)
- **IEC 61508**: SIL 3/4 for industrial functional safety
- **DO-178C**: Level A for avionics (highest level)
- **EN 50128**: Railway applications
- **IEC 62304**: Medical device software
- **Common Criteria**: EAL4+ for security

### Safety-certified versions

- **QNX OS for Safety**: Safety-certified version of QNX
- **Safety manuals**: Comprehensive safety manuals available
- **Certification packages**: Full certification packages for
  various standards
- **Tool qualification**: Qualified development tools

### Using QNX in safety-critical applications

- **Use certified version**: Ensure using a version with the required
  certification
- **Follow safety guidelines**: Follow all guidelines in safety manual
- **Document design**: Document all design decisions related to safety
- **Design for isolation**: Use process isolation for fault containment
- **Use safety kernel**: Use safety-certified kernel for highest
  assurance
- **Perform safety analysis**: Perform FMEA, FTA, and other analyses
- **Test thoroughly**: Perform comprehensive testing required by
  safety standard
- **Maintain traceability**: Maintain traceability between requirements,
  design, implementation, and testing

## Alternatives and when to use them

- **Linux**: When need full OS features, large ecosystem, or
  open-source. Linux can achieve near real-time with PREEMPT_RT
  patch.
- **FreeRTOS**: When need lightweight, minimal overhead RTOS for
  microcontrollers. FreeRTOS is more lightweight but has fewer
  features.
- **Zephyr**: When need open-source, modular RTOS with extensive
  hardware support. Zephyr is more modular but may have less
  POSIX compliance.
- **ThreadX**: When need commercial RTOS with Azure integration or
  specific industrial features.
- **VxWorks**: When need commercial RTOS with extensive safety
  certifications or defense/aerospace features.
- **QNX**: When need full-featured, POSIX-compliant RTOS with
  microkernel architecture and extensive certifications.

## Resources

- **Official website**: https://www.qnx.com/
- **Documentation**: https://www.qnx.com/developers/docs/
- **Developer zone**: https://community.qnx.com/
- **Source code**: Available to customers (not open-source)
- **QNX Momentics IDE**: Official IDE
- **Foundry27**: QNX's project hosting and CI platform
- **GitHub**: Some open-source QNX projects and samples
- **Books**: "QNX Neutralino: An RTOS for the Rest of Us" by Robert Krten
- **Training**: QNX provides training courses
- **Support**: Commercial support available from BlackBerry
- **Blog**: https://www.qnx.com/en/blog
- **Release notes**: Included with each release
- **API reference**: https://www.qnx.com/developers/docs/6.6.0/index.html
