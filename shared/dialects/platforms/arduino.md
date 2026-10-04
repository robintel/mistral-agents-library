# Arduino platform contract

Attaches alongside `patterns/embedded.md` and the language contract
(c, cpp). The framework is constant; the substrate is the era.

## Eras

The board menu is the era declaration: classic AVR (Uno, Mega —
16MHz, 2-8KB SRAM, PROGMEM territory, cycle-countable timing) versus
SAMD/ARM boards (Nano 33, Due — Cortex-M0+, real FPU-free
fixed-point discipline) versus ESP32-based boards under the Arduino
layer. Same API, different physics: write the substrate the board
names.

## Idiom

- setup()/loop() is cooperative: no scheduler underneath — blocking
  in loop() starves everything except interrupts. The millis()
  state machine over delay() is the difference between a sketch and
  a program.
- Direct port manipulation over digitalWrite where speed matters:
  the AVR port registers are one cycle; the API is comfort.
- Interrupt handlers attach cleanly; shared state gets volatile and
  the embedded contract's atomicity discipline — on AVR, a 16-bit
  millis() read can tear against an ISR.

## Structure

- PROGMEM and F() for constants on AVR: RAM is the scarce resource;
  the heap fragments under String — static buffers are the idiom.
- Stack and heap collide on 2KB SRAM: recursion and String are the
  classic offenders.

## Pitfalls

- String as the heap-fragmenter: the single most common AVR
  stability bug.
- The watchdog resetting mid-write: EEPROM/flash writes designed
  against it, or corrupted on schedule.
- I2C addresses and pull-ups: the bus problems that read as code
  problems.
- analogRead accuracy: the reference voltage is part of the
  measurement, and its tolerance is part of the error budget.
