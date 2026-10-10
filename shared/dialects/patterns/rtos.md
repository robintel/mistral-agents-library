# RTOS pattern contract

Attaches to embedded/firmware work when the target uses a real-time
operating system. The pattern is concurrency discipline plus timing
guarantees; the RTOS is the means, never the goal. Attaches alongside
`patterns/embedded.md` and the platform/language contracts.

## The discipline

- **Tasks/threads are the unit of concurrency**: each owns a stack, a
  priority, and a state. The design names them, the code does not
  multiply them.
- **Priorities are a contract**: the scheduler runs the highest-priority
  ready task. Priority inversion is a finding; priority inheritance
  and ceiling protocols are the fixes.
- **Synchronization is explicit**: semaphores, mutexes, queues, event
  flags — the discipline is "lock the minimal scope," and the design
  names which primitive and why.
- **Timing is a budget**: task periods, deadlines, worst-case execution
  time (WCET) measured. The scheduler model (rate-monotonic,
  earliest-deadline-first, or simple preemptive) is stated; silence
  implies preemptive priority-based.
- **Memory is partitioned**: each task has its stack; global/heap
  access requires synchronization. Stack overflow is a defect the
  design prevents, not the runtime detects.
- **ISRs are special tasks**: they run at interrupt priority, cannot
  block (except on special primitives with FromISR variants),
  and must be short. Defer work to a task via queue or semaphore.

## Scheduling models

- **Preemptive priority-based**: default for most RTOS. Highest
  priority ready task runs. Classic pitfall: priority inversion
  (low-priority task holds a resource needed by high-priority task).
- **Round-robin / time-sliced**: tasks at same priority share CPU
  via time slices. Starvation is the pitfall.
- **Cooperative / non-preemptive**: tasks yield explicitly. Simpler
  but requires discipline; long-running tasks block everything.
- **Hybrid**: e.g., preemptive with priority ceiling, or
  preemptive + round-robin within priority bands.

## Synchronization primitives

- **Semaphore (binary)**: signal mechanism. Take waits, give
  signals. Use for signaling, not for mutual exclusion.
  Pitfall: giving from ISR without FromISR variant.
- **Semaphore (counting)**: allows multiple takes before blocking.
  Use for resource pools. Pitfall: unbounded count leading to
  memory exhaustion.
- **Mutex**: mutual exclusion with priority inheritance (prevents
  priority inversion). Recursive mutex allows same task to take
  multiple times. Pitfall: taking in ISR (usually disallowed).
- **Queue**: message passing. Fixed-size buffer. Pitfall: blocking
  on full queue; design the size.
- **Event flags / groups**: multiple event bits in one object.
  Tasks can wait for specific bits. Pitfall: missing events due
  to read-clear vs. wait-clear semantics.
- **Message mailbox**: single message. Simpler than queue but
  limited to one message.

## Memory management

- **Static allocation**: preferred for embedded. All objects
  (tasks, queues, semaphores) created at startup with fixed sizes.
- **Dynamic allocation**: heap-based object creation. Pitfalls:
  fragmentation, deterministic timing compromised, memory exhaustion.
- **Memory pools**: pre-allocated blocks. Middle ground between
  static and dynamic.
- **Stack management**: each task has its stack. Stack overflow
  causes undefined behavior. Use stack guards, fill patterns, or
  runtime checking where available.

## Timing and timeouts

- **Tick interval**: the RTOS heartbeat (typically 1ms to 10ms).
  Shorter ticks improve timing resolution but increase overhead.
- **Tickless idle**: CPU stops in idle to save power. Affects
  timing accuracy for sleep/delay operations.
- **Timeouts**: always specify on blocking calls. INFINITE/portMAX_DELAY
  is a code smell. Use timeout values that align with design budgets.
- **Timers**: software timers for delayed execution. One-shot vs
  periodic. Pitfall: timer callback running in ISR context
  (depends on RTOS implementation).
- **Delays**: vTaskDelay / equivalent. Yields CPU to other tasks.
  Not for precise timing; use timers instead.

## ISR constraints

- **Cannot block**: ISRs cannot use blocking primitives.
  Use FromISR variants (give from ISR, send from ISR) which have
  special behavior.
- **Must be short**: long ISRs delay task execution and affect
  system responsiveness. Defer work to a task.
- **No floating point**: often disabled in ISR context. Use
  fixed-point.
- **Context switch may occur on exit**: depending on RTOS and
  priority. Assumes this in design.
- **Nested interrupts**: may or may not be supported. Design
  accordingly.

## Inter-task communication patterns

- **Producer-consumer via queue**: classic pattern. Producer sends
  to queue, consumer receives. Queue size designed for worst-case
  burst.
- **Notification via semaphore/event**: signal-based. Lower
  overhead than queue but no data payload.
- **Shared buffer with mutex**: direct memory sharing. Mutex
  protects access. Pitfall: priority inversion if mutex held
  across different priority tasks.
- **Message passing**: tasks send messages directly. Coupling
  is the trade-off.
- **Stream buffer**: continuous data stream. Efficient for
  byte-stream protocols.

## Common pitfalls

- **Priority inversion**: low-priority task holds resource needed
  by high-priority task, medium-priority task runs and blocks high.
  Fix: priority inheritance protocol (mutex) or priority ceiling.
- **Stack overflow**: task uses more stack than allocated. Prevent
  with analysis, stack fill patterns, or runtime checks.
- **Blocking in ISR**: using blocking primitive in ISR causes
  system hang. Use FromISR variants or defer to task.
- **Unbounded queue growth**: queue fills and blocks producer.
  Design queue size for worst-case scenario.
- **Deadlock**: circular wait between tasks. Prevent with
  consistent lock ordering, timeout on all blocking calls.
- **Livelock**: tasks keep yielding to each other, no progress.
  Detect via watchdog or design review.
- **Priority starvation**: high-priority task keeps running, low
  never gets CPU. Ensure all priorities get CPU time via design
  or time-slicing.
- **Race conditions on shared data**: concurrent access without
  synchronization. Always protect shared data.
- **Tick timing inaccuracies**: assuming tick-based timing is
  precise. Account for tick interval in design.
- **Missing yield points**: long code paths without yielding.
  Break into smaller functions, add explicit yields, or redesign
  as state machines.
- **Incorrect task priority assignment**: critical tasks at
  wrong priority. Analyze real-time requirements carefully.
- **Returning from ISR without context switch hint**: if ISR
  makes a higher-priority task ready, must trigger context switch.
  Most RTOS do this automatically for FromISR calls.

## Timing analysis

- **WCET (Worst-Case Execution Time)**: measure or estimate for
  each task. Critical for meeting deadlines.
- **Response time analysis**: calculate worst-case response time
  for each task considering interference from higher-priority tasks.
- **Utilization test**: sum of (Ci / Pi) for all tasks must be <= n(2^(1/n) - 1)
  for rate-monotonic scheduling (Liu & Layland bound), where Ci is
  WCET and Pi is period. For n=1, utilization <= 100%. For n=2,
  <= 82.8%. For n=>infinity, <= 69.3%.
- **Deadline monotonic**: deadlines equal to periods. Simplifies
  analysis.
- **Sporadic vs periodic**: sporadic tasks have minimum inter-arrival
  time. Analysis must account for worst-case arrival pattern.

## Power management

- **Tickless idle**: CPU can stop clock in idle to save power.
  Affects timing granularity.
- **Sleep modes**: RTOS may support low-power modes. Tasks must
  be designed to allow system to enter sleep (no busy-wait).
- **Wakeup sources**: external interrupts, timers. Design wakeup
  latency budget.
- **Dynamic voltage/frequency scaling**: if supported, affects timing
  analysis. WCET measured at lowest voltage/frequency.

## Debugging and testing

- **Task state inspection**: most RTOS provide API to check task
  states (running, ready, blocked, suspended). Useful for debugging.
- **Stack usage analysis**: tools or APIs to check stack high-water
  mark. Critical for stack sizing.
- **Timing measurement**: use RTOS timestamps or external logic
  analyzer to measure task execution times and identify bottlenecks.
- **Queue monitoring**: check queue usage, number of messages.
- **ISR profiling**: measure ISR execution times, identify long
  ISRs.
- **Deadlock detection**: some RTOS provide deadlock detection.
  Otherwise, implement via timeout on mutex acquisition.
- **Watchdog**: hardware watchdog should be fed by a dedicated
  task. Never feed from ISR.

## Integration with hardware

- **Peripheral drivers**: most RTOS provide driver layers or
  patterns for integrating peripheral drivers. Drivers may run in
  task context or ISR context.
- **DMA**: direct memory access for efficient data transfer.
  Synchronization between CPU and DMA required.
- **Interrupts**: peripheral interrupts mapped to ISRs. ISR
  design follows RTOS constraints.
- **Memory-mapped I/O**: volatile access, memory barriers
  required on some architectures.

## RTOS selection considerations

- **Footprint**: memory requirements (code, data, stack).
- **Determinism**: worst-case interrupt latency, context switch time.
- **Certifications**: safety (IEC 61508, ISO 26262), security, medical.
- **Tooling**: debugger integration, trace tools, IDE support.
- **Community**: size, activity, commercial support available.
- **Licensing**: open source vs commercial, restrictions on use.
- **Portability**: ease of porting to new hardware.
- **Features**: required synchronization primitives, file systems,
  networking stack, etc.

## Best practices

- **Task design**: each task has single responsibility. Avoid
  "god tasks" that do everything.
- **Priority assignment**: assign based on timing requirements,
  not importance. Critical deadline tasks get highest priority.
- **Minimize shared state**: use message passing instead where
  possible to reduce synchronization complexity.
- **Always use timeouts**: never block forever. Use reasonable
  timeout values.
- **Design for testability**: tasks should be testable in
  isolation. Consider mocking dependencies.
- **Document timing requirements**: specify deadlines, periods,
  WCET for each task in design documentation.
- **Use static allocation**: for deterministic behavior and to
  avoid fragmentation.
- **Implement watchdog feeding**: dedicated task feeds hardware
  watchdog. Watchdog timeout set to detect hung system.
- **Handle errors**: tasks should handle errors gracefully and
  report them. Consider error reporting mechanism.
- **Resource cleanup**: ensure resources (memory, file handles,
  etc.) are released when no longer needed.

## Common RTOS families

The individual RTOS dialect files document the specifics:

- **FreeRTOS** (`platforms/rtos/freertos.md`): most popular open-source RTOS
- **Zephyr** (`platforms/rtos/zephyr.md`): Linux Foundation, highly configurable
- **ThreadX** (`platforms/rtos/threadx.md`): Azure RTOS, industrial-grade
- **SafeRTOS** (`platforms/rtos/safertos.md`): safety-certified FreeRTOS variant
- **QNX** (`platforms/rtos/qnx.md`): microkernel, POSIX-compliant
- **VxWorks** (`platforms/rtos/vxworks.md`): Wind River, industrial/defense

See the respective dialect files for API specifics, eras, and
platform-specific considerations.
