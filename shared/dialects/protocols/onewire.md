---
type: protocol
family: bus
---

# 1-Wire

The single-wire, half-duplex, device-identified bus. Power and data
on the same wire — or two wires with dedicated power. Every device
self-identifies with a unique 64-bit ROM code.

## Eras

The era is declared by the **device family** and **communication mode**.

**Parasite power**: Power derived from data line, no separate VCC
**External power**: Dedicated VCC, data on separate wire
**Overdrive mode**: Higher drive strength for long buses or many devices
**1-Wire XS**: Extended speed mode for newer devices

Microcontroller support:
- AVR: Software implementation (OneWire library)
- ARM: Software implementation
- ESP32: Software implementation, can use dedicated GPIO

## Bus Topology

```
Data/Power (when parasite power) ────┬─ Device 1 (Sensor)
                                          ├─ Device 2 (Sensor)
                                          ├─ Device 3 (RTC)
                                          └─ Pull-up resistor (4.7kΩ)

OR (with external power):

Data ──────────────────────────────┬─ Device 1
                                   ├─ Device 2
                                   └─ Pull-up resistor
VCC ──────────────────────────────┴─ All devices
```

- **Single wire**: Data + power (parasite mode) or data only (external power)
- **Pull-up resistor**: Required, typically 4.7kΩ to VCC (3.3V-5V)
- **Pull-up strength**: Strong pull-up for reliable communication
- **Bus length**: Up to 100m with proper wiring

## Device Identification

### 64-bit ROM Code Structure

```
┌────────────┬────────────┬────────────┬────────────┐
│ 8-bit Family │ 48-bit ID   │ 8-bit CRC   │
└────────────┴────────────┴────────────┴────────────┘
```

- **Family code**: Identifies device type (0x10 = DS18B20 temperature sensor, 0x22 = DS1822, etc.)
- **48-bit ID**: Unique serial number
- **8-bit CRC**: Cyclic Redundancy Check for data integrity

**Common family codes**:
- 0x01: DS1990A (iButton, 1KB ROM)
- 0x02: DS1991 (iButton, 4KB ROM)
- 0x04: DS1994 (iButton, 4KB RAM)
- 0x08: DS1920 (Temperature logger)
- 0x10: DS18B20 (Temperature sensor)
- 0x1D: DS1822 (Temperature sensor)
- 0x22: DS1822 (Alternate family code)
- 0x26: DS2438 (Smart battery monitor)
- 0x2D: DS2406 (SHA-1 coprocessor)
- 0x3A: DS1922 (Temperature logger)
- 0x3B: DS1923 (Hygrochron temperature/humidity logger)

### Device Discovery
1. Master sends **Reset pulse** (480µs low)
2. Master releases bus, waits for **Presence pulse** (15-60µs low from slave)
3. Master sends **ROM commands** to identify devices
4. Each device responds with its unique 64-bit ROM code

## ROM Commands

| Command | Code | Description | Use Case |
|---------|------|-------------|----------|
| **Search ROM** | 0xF0 | Discover all devices on bus | Initial discovery |
| **Read ROM** | 0x33 | Read ROM of single device | Single device bus |
| **Match ROM** | 0x55 | Address specific device | Targeted communication |
| **Skip ROM** | 0xCC | Skip ROM, address all devices | Single device bus or broadcast |
| **Resume** | 0xA5 | Resume after alarm search | Alarm handling |
| **Alarm Search** | 0xEC | Find devices with alarm flag | Temperature alarm, etc. |

## Function Commands

Commands vary by device family. Common commands for DS18B20 (temperature sensor):

| Command | Code | Description |
|---------|------|-------------|
| **Convert T** | 0x44 | Start temperature conversion |
| **Write Scratchpad** | 0x4E | Write to scratchpad memory |
| **Read Scratchpad** | 0xBE | Read scratchpad (includes temperature) |
| **Copy Scratchpad** | 0x48 | Copy scratchpad to EEPROM |
| **Recall EEPROM** | 0xB8 | Recall EEPROM to scratchpad |
| **Read Power Supply** | 0xB4 | Check if device uses parasite power |

## Timing Requirements

All timing is critical and measured from the master's perspective.

### Reset Timing
- **Reset pulse (T_RSTL)**: 480µs ± 40µs LOW
- **Presence pulse (T_PDLO)**: 15-60µs LOW from slave
- **Presence high (T_PDHI)**: 60-240µs HIGH from slave

### Bit Timing (Standard Speed)
- **Write 0 (T_SLOT)**: 60-120µs LOW
- **Write 1 (T_SLOT)**: 1-15µs LOW, then HIGH for remainder
- **Read 0**: Master pulls LOW for 1-15µs, slave pulls LOW for remainder
- **Read 1**: Master pulls LOW for 1-15µs, slave leaves HIGH

### Timing Slots
- **Standard speed**: 60µs per bit slot
- **Overdrive speed**: 7.5µs per bit slot (requires support from all devices)

## Power Requirements

### Parasite Power Mode
- **Power source**: Data line (via pull-up resistor)
- **Power consumption**: 4µA per device (typical)
- **Current draw**: Varies by device and operation
- **Limitations**: 
  - Limited number of devices (depends on power budget)
  - Cannot perform operations that require > 4mA
  - DS18B20 temperature conversion requires 4mA

### External Power Mode
- **Power source**: Dedicated VCC (3.3V-5V)
- **Advantages**: More devices, higher current operations
- **Wiring**: Separate VCC and data lines
- **Pull-up**: Still required on data line

**Power budget calculation**:
1. Determine current draw per device (active and idle)
2. Sum current for all devices (worst-case simultaneous operation)
3. Account for voltage drop across pull-up and wiring
4. Ensure power supply can provide total current
5. Add margin (20-50%)

## Communication Modes

### Single Device Bus
- **Pros**: Simple, fast
- **Cons**: Limited to one device
- **Usage**: Read ROM with Skip ROM command

### Multi-Device Bus
- **Pros**: Multiple devices on one wire
- **Cons**: More complex addressing
- **Usage**: Must use Match ROM to address specific device

### Alarm-Based Communication
- **Pros**: Efficient polling for alarm conditions
- **Cons**: Requires alarm-capable devices
- **Usage**: Temperature alarms, threshold violations

## Common Device Families

### Temperature Sensors
- **DS18B20**: 1-Wire digital temperature sensor
  - Range: -55°C to +125°C
  - Accuracy: ±0.5°C (-10°C to +85°C)
  - Resolution: 9-12 bits (0.5°C to 0.0625°C)
  - Conversion time: 750ms (12-bit), 375ms (11-bit), 187.5ms (10-bit), 93.75ms (9-bit)
- **DS1822**: Economy temperature sensor
  - Range: -55°C to +125°C
  - Accuracy: ±2°C
  - Resolution: 9-11 bits
- **DS18S20**: Older temperature sensor
  - Range: -55°C to +125°C
  - Accuracy: ±0.5°C
  - Resolution: 9 bits

### Memory Devices
- **DS2431**: 1024-bit EEPROM
- **DS2433**: 4096-bit EEPROM
- **DS1990A**: iButton, 1KB ROM
- **DS1991**: iButton, 4KB ROM
- **DS1994**: iButton, 4KB RAM + RTC

### RTC (Real-Time Clock)
- **DS1904**: RTC iButton
- **DS1923**: Hygrochron (temperature + RTC)

### A/D Converters
- **DS2450**: 4-channel, 16-bit A/D converter

### Smart Battery Monitors
- **DS2438**: Battery monitor with EEPROM

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| No presence pulse | No devices detected | Check wiring, verify pull-up, check power |
| Presence pulse but no ROM | Device not responding | Check device compatibility, verify ROM commands |
| CRC error | Data corruption | Verify wiring, check for noise, reduce bus length |
| Bus not released | Next transaction fails | Ensure proper reset pulse timing |
| Parasite power insufficient | Device not responding | Use external power, reduce device count |
| Timing violation | Communication errors | Verify timing, use standard speed mode |
| Long bus length | Signal degradation | Use shorter bus, add bus drivers, use twisted pair |
| Noise on bus | Data corruption | Improve grounding, shield cable, add capacitors |
| Multiple devices with same ROM | Address conflicts | Cannot happen with genuine Dallas devices (unique IDs) |
| Pull-up too weak | Communication errors | Use stronger pull-up (2-4.7kΩ) |

## Performance Considerations

- **Bus speed**: Standard mode ~16.3KB/s, Overdrive mode ~130KB/s
- **Device count**: Limited by bus capacitance (< 800pF total) and power
- **Polling overhead**: Each temperature conversion takes 750ms (DS18B20, 12-bit)
- **Bus capacitance**: Total < 800pF for reliable operation
- **Parallel conversion**: DS18B20 supports parallel conversion on all devices

**Typical performance**:
- Temperature read: ~750ms per device (12-bit conversion)
- ROM read: ~5ms per device
- Bus scan: ~10ms per device

## Best Practices

- **Use strong pull-up**: 4.7kΩ for most applications, 2kΩ for long buses
- **Minimize bus length**: Keep under 100m with proper wiring
- **Use twisted pair**: For long distances to reduce noise
- **Add decoupling capacitor**: 0.1µF near each device for power stability
- **Verify power mode**: Check if devices support parasite power
- **Use parasite power judiciously**: Only for low-power devices and small counts
- **Group devices**: By distance and power requirements
- **Use separate buses**: For different device types or speed requirements
- **Implement error recovery**: Retry failed transactions
- **Handle CRC errors**: Detect and report, investigate root cause
- **Use alarm search**: For efficient polling of alarm conditions
- **Cache ROM codes**: Store discovered ROM codes to avoid repeated discovery

## Debugging Tips

- **Check pull-up**: Verify pull-up resistor is present and correct value
- **Verify wiring**: Check for shorts, opens, or reversed connections
- **Test with one device**: Verify basic communication before adding more
- **Check power**: Measure voltage at device with multimeter
- **Use logic analyzer**: Capture 1-Wire transactions for analysis
- **Verify timing**: Check reset pulse and bit timing with oscilloscope
- **Test power modes**: Try both parasite and external power
- **Isolate devices**: Remove devices one at a time to identify problematic one

## Standing Rules

- **The reset pulse is sacred** — 480µs LOW is the contract; a
  shorter or longer pulse breaks the bus.
- **Presence pulse is the handshake** — no presence pulse, no
  device; investigate why.
- **Every device has a unique 64-bit ROM** — use it to address the
  device; a duplicate ROM is a manufacturing error.
- **Parasite power is a budget** — count the current, design the
  pull-up, and stay within the limit.
- **CRC is not optional** — always check the CRC; a device that
  reports a CRC error is a device to investigate.
- **Overdrive mode requires support from all devices** — one device
  that does not support it blocks the entire bus.
- **Bus capacitance is a hard limit** — stay under 800pF; exceeding
  it means redesigning the bus.
