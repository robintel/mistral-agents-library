# Embedded pattern contract

Attaches by the shape of the work — firmware, bare-metal, maker
boards — alongside the language contract (c, cpp) and the platform
contract (arduino, esp32). The discipline is shared; the board is
not.

## The discipline

- Hardware registers are volatile: every MMIO access is a side
  effect; the optimizer is not your friend here, and the barrier
  goes where the datasheet says.
- No heap in interrupt contexts: allocation in an ISR is a finding;
  keep ISRs short — set a flag, defer the work to the loop or task.
- Timing is a budget in cycles, not a vibe: busy-waits measured,
  deadlines counted, the watchdog a designed safety net rather than
  a bandage for hangs.
- Atomicity is architecture-dependent: on 8-bit MCUs a 16- or 32-bit
  read can tear mid-instruction — shared ISR/loop state gets a
  critical section or a copy-and-compare discipline.
- The datasheet's register map is the contract: read it like the
  lineage tour reads a schema — what the hardware promises, what it
  silently doesn't.
- Power is a requirement: sleep modes change the timing model, ADC
  references have tolerances, flash and EEPROM have write-endurance
  budgets spent deliberately.

## Pitfalls (shared)

- delay() where a state machine belongs: blocking code that makes
  the system unresponsive to everything but itself.
- Floating point on FPU-less cores: fixed-point is the idiom, and
  the scaling decision belongs in the design.
- Uninitialized peripherals assumed at reset: the boot state is
  per-family and per-datasheet.
- Debug output priced in baud: the debug interface (UART, SWD,
  JTAG) is part of the design, not an afterthought.
