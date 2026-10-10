---
type: protocol
family: bus
---

# I2C (Inter-Integrated Circuit)

The two-wire, multi-device, multi-master synchronous bus. Address-first,
then data. Every byte on the bus is either an address or payload — and
the contract is that the address byte always comes first.

## Eras

The era is declared by the **electrical standard** and **speed grade**.

**Original (1982)**: 100kHz standard mode, 7-bit addressing
**Fast mode (1992)**: 400kHz, backward compatible
**Fast mode Plus (1998)**: 1MHz, same signaling as Fast mode
**High-speed mode (2000)**: 3.4MHz, different signaling, requires hub
**Ultra Fast mode (2012)**: 5MHz, unidirectional, not widely adopted

Microcontroller support varies: AVR supports 100kHz/400kHz; ARM
Cortex-M often supports 1MHz; ESP32 supports up to 5MHz.

## Bus Topology

```
SDA (Serial Data) ────┬─ Device 1 (Master/Slave)
                     ├─ Device 2 (Master/Slave)
                     ├─ Device 3 (Slave)
                     └─ Pull-up resistors (4.7kΩ typical)

SCL (Serial Clock) ──┴─ Device 1
                     ├─ Device 2
                     └─ Pull-up resistors (4.7kΩ typical)
```

- **SDA**: Bidirectional data line
- **SCL**: Clock line driven by master(s)
- **Pull-ups**: Required on both lines; typically 4.7kΩ to VCC
- **Capacitance**: Total bus capacitance must be < 400pF for Standard mode

## Address Space

### 7-bit Addressing (Standard)
- **Range**: 0x00 - 0x7F (128 possible addresses)
- **Reserved**: 0x00-0x07, 0x78-0x7F (special purposes)
- **Usage**: Most common; each device has unique 7-bit address

### 10-bit Addressing (Extended)
- **Range**: 0x000 - 0x3FF (1024 possible addresses)
- **Format**: First byte = 0xF0-0xF7 (indicates 10-bit), next 2 bytes = address
- **Usage**: Less common; requires both master and slave support

### Address Assignment
- **Hardware**: Fixed by device (e.g., EEPROMs often 0x50-0x57)
- **Configurable**: Via jumpers, DIP switches, or software
- **Dynamic**: Some devices allow runtime address change

**Common device addresses**:
- EEPROM (24LCxx): 0x50-0x57 (A0-A2 pins selectable)
- RTC (DS1307): 0x68
- RTC (DS3231): 0x68
- Temperature (LM75): 0x48-0x4F
- IMU (MPU6050): 0x68 or 0x69 (AD0 pin selectable)
- OLED (SSD1306): 0x3C or 0x3D (SA0 pin selectable)
- ADC (ADS1115): 0x48-0x4B (ADDR pin selectable)

## Transfer Format

### Single Byte Write
```
Master: START → [Address + W] → [Data] → STOP
```

### Single Byte Read
```
Master: START → [Address + R] → [NACK] → STOP
Slave:                          [Data]
```

### Multi-Byte Write
```
Master: START → [Address + W] → [Data1] → [Data2] → ... → [DataN] → STOP
```

### Multi-Byte Read
```
Master: START → [Address + R] → [ACK] → [ACK] → ... → [NACK] → STOP
Slave:                                 [Data1]→[Data2]→...→[DataN]
```

### Combined Format (Write then Read)
```
Master: START → [Address + W] → [Register] → START → [Address + R] → [Data] → STOP
```

## Electrical Characteristics

| Parameter | Standard Mode | Fast Mode | Fast Mode Plus | High-Speed Mode |
|-----------|---------------|-----------|----------------|------------------|
| Max clock | 100kHz | 400kHz | 1MHz | 3.4MHz |
| Min SCL low | 4.7µs | 1.3µs | 0.5µs | 0.16µs |
| Min SCL high | 4.0µs | 0.6µs | 0.26µs | 0.08µs |
| Min SDA setup | 250ns | 100ns | 50ns | 10ns |
| Min SDA hold | 0ns (min) | 0ns (min) | 0ns (min) | 0ns (min) |
| Max bus capacitance | 400pF | 400pF | 550pF | 400pF |
| Pull-up value | 2-10kΩ | 1-3kΩ | 1-2kΩ | 1kΩ |

## Protocol Features

### Clock Stretching
- **What**: Slave holds SCL low to pause communication
- **When**: Slave needs more time to process data
- **Signaling**: SCL held low by slave; master must wait
- **Support**: Not all microcontrollers support clock stretching
- **Pitfall**: Master timeout if clock stretching not supported

### Repeated Start
- **What**: START condition without STOP between transfers
- **When**: Master wants to send multiple messages without releasing bus
- **Usage**: Combined write-read transactions, addressing different slaves
- **Signaling**: SDA transitions while SCL is high

### General Call Address
- **Address**: 0x00 (reserved)
- **Purpose**: Broadcast to all devices
- **Usage**: Rare; typically used for bus reset or global commands
- **Pitfall**: Most devices don't respond to General Call

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| No pull-ups | Bus hangs, no communication | Add 4.7kΩ pull-ups on SDA and SCL |
| Address conflict | Bus lockup, NACK on all transfers | Scan bus, use I2C scanner, reconfigure addresses |
| Insufficient pull-up current | Signal degradation on long buses | Use lower resistance (2-3kΩ) or active pull-ups |
| Excessive bus capacitance | Signal rounding, communication errors | Reduce bus length, reduce device count, use bus repeaters |
| Clock stretching not supported | Slave times out, data loss | Use master that supports clock stretching or avoid slow slaves |
| Missing ACK | Transfer fails at specific byte | Check device ready status, verify address, check for bus errors |
| Bus not released | Next transfer fails | Ensure STOP condition sent, check for stuck slave |
| Interference from other buses | Erratic behavior | Isolate I2C bus from other signals, use dedicated pins |
| 7-bit vs 10-bit address mismatch | Address not found | Verify all devices support same addressing mode |

## Performance Considerations

- **Maximum data rate**: Limited by slowest device on bus
- **Transaction overhead**: Each byte = 9 clock pulses (1 start bit, 8 data bits, 1 ACK bit)
- **Efficiency**: Bulk transfers amortize START/STOP overhead
- **Bottleneck**: Slowest slave determines bus speed

## Best Practices

- **Pull-ups**: Always use pull-ups; place them near the master for best results
- **Address scanning**: Implement I2C bus scanner in code to detect devices
- **Bus length**: Keep under 1m for 100kHz, under 0.5m for 400kHz+ 
- **Capacitance**: Total bus capacitance < 400pF for Standard mode
- **Address assignment**: Assign addresses to avoid conflicts; document all addresses
- **Error recovery**: Implement retry logic with reasonable timeout
- **Clock stretching**: Design for it; test with slowest slave
- **Bus isolation**: Use separate buses for incompatible devices or speed requirements
- **Level shifting**: Use bidirectional level shifters for 3.3V/5V mixing

## Debugging Tips

- **Oscilloscope**: Check SDA and SCL waveforms for proper edges
- **Logic analyzer**: Capture full bus transactions for analysis
- **Bus scanner**: Run I2C scanner to detect all devices on bus
- **Signal integrity**: Check for rounding on clock/data edges
- **Voltage levels**: Verify pull-up voltage matches device requirements

## Standing Rules

- **Pull-ups are mandatory** — no pull-ups, no bus; the datasheet
  specifies the range, the design picks a value within it.
- **Address 0x00 is reserved** — never use it for a device; use it only
  for General Call when the contract explicitly allows it.
- **A START without a STOP is still on the bus** — always send STOP
  or Repeated START to release the bus properly.
- **The master owns the clock** — but the slave can stretch it; design
  for both the fast path and the stretched path.
- **Each byte is ACKed or NACKed** — a missing ACK is a defect to
  investigate, not to ignore.
- **Bus capacitance is a budget** — count it, and design the pull-ups
  and the topology to stay under the limit.
