# ESP32 platform contract

Attaches alongside `patterns/embedded.md` and the language contract.
A SoC with an RTOS underneath and radios on top: the discipline is
concurrency, and the era is the ISA.

## Eras

The ISA is the era marker: Xtensa LX6/LX7 (classic ESP32, S2, S3 —
dual-core on the original) versus the RISC-V era (C3, C6, P4). The
API era runs alongside it: ESP-IDF (the native framework, FreeRTOS
underneath) versus the Arduino layer on top. Both eras are named by
the project's configuration; write them.

## Idiom

- FreeRTOS is not optional knowledge: tasks with priorities, queues
  and semaphores — and the messaging core's rules apply, with the
  FromISR variants in interrupt context.
- The watchdog is standard equipment: long loops feed it
  deliberately or explain themselves in resets.
- Core pinning (PRO_CPU/APP_CPU) is a design decision on dual-core
  parts, not a detail: the shared-state discipline follows the
  answer.

## Structure

- Memory: internal SRAM, PSRAM on some parts, DMA-capable regions
  with constraints; task stack sizes configured, not assumed.
- WiFi and BLE stacks run with their own priorities and memory
  footprint: the application budgets around them.

## Pitfalls

- Brownout resets from weak power supply: the classic that reads as
  a software mystery.
- SPI flash writes disabling the cache: the window where
  interrupt code can fault — the datasheet names it, the bug report
  rediscovers it.
- Dual-core races without the portMUX: shared state between cores
  needs it.
- Deep sleep and the RTC domain: wakeup sources designed, state
  persisted deliberately, and the timing model changes with the
  mode.
