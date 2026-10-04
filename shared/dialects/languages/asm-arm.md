# ARM assembly dialect

Attaches for .S files, inline asm, disassembly, and bare-metal work.
One family, three eras, and the profile decides the rules.

## Eras and profiles

- AArch64 (ARM64): servers, phones, Apple Silicon — x0-x31, NEON.
- AArch32 (ARM and Thumb): the embedded elder — conditional
  everything, literal pools, Thumb interworking.
- Cortex-M (Thumb-2 only): the maker profile — RP2040, STM32, nRF,
  SAMD. No A-profile instructions; write the profile the target
  runs, named by the build.

## The ABI (AAPCS and AAPCS64)

- Args in x0-x7 (or r0-r3 in AArch32), return in x0/x1; varargs on
  the stack after the register window.
- Callee-saved: x19-x28 and x29 (FP), x30 (LR) if used; SP stays
  aligned to 16 (AArch64).
- Load/store architecture: no memory operands on ALU operations —
  load, compute, store.

## Idiom

- A64 has no push/pop: stp/ldp pairs, and the link register saved
  by hand — bl overwrites x30.
- Conditional execution is the era split: AArch32's conditional
  instructions versus A64's CSEL/CINC family.
- Barriers matter on multi-core: dmb/dsb where the datasheet and the
  memory model say, not by folklore.

## Pitfalls

- bl clobbering x30 without saving: the classic leaf-function bug.
- Unaligned access on Cortex-M0: hard fault, not a shrug.
- The Thumb bit in addresses: function pointers on AArch32/M carry
  state in bit 0.
- ldr/stp offset ranges: out-of-range displacements assemble wrong
  or not at all.
