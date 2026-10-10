---
type: protocol
family: bus
---

# SPI (Serial Peripheral Interface)

The synchronous, full-duplex, multi-device bus. Master-driven clock,
individual chip selects. Every byte sent is a byte received —
simultaneously.

## Eras

The era is declared by the **controller capabilities** and **clock
speed**.

**Basic SPI**: Master-only, single slave, basic mode (0,0)
**Full SPI**: Master/slave capable, all 4 modes supported
**Dual SPI**: Dual data lines (MOSI2/MISO2) for higher throughput
**Quad SPI**: Quad data lines (IO2/IO3) for even higher throughput
**High-speed SPI**: Clock rates > 10MHz, often with FIFO buffers

Microcontroller support:
- AVR (Uno/Mega): Master-only, up to 8MHz, no dual/quad
- ARM Cortex-M: Master/slave, up to 24MHz+, dual/quad support varies
- ESP32: 4 SPI buses (SPI, HSPI, VSPI, DSPI), master/slave, up to 40MHz

## Bus Topology

```
MOSI (Master Out Slave In) ────┬─ Slave 1 CS ──►
                            ├─ Slave 2 CS ──►
                            ├─ Slave 3 CS ──►
                            └─ ...
MISO (Master In Slave Out) ────┘

SCK (Serial Clock) ──────────────┬─ Slave 1 CS ──►
                            ├─ Slave 2 CS ──►
                            └─ ...

CS/SS (Chip Select/Slave Select) ─┼─ Slave 1
                                ├─ Slave 2
                                └─ Slave 3
```

- **MOSI**: Master → Slave data (output from master)
- **MISO**: Slave → Master data (input to master)
- **SCK**: Clock signal (driven by master)
- **CS/SS**: Chip Select (active LOW for most devices)

**Key property**: Full-duplex — data flows in both directions simultaneously

## Clock Modes

Clock polarity (CPOL) and clock phase (CPHA) define the mode:

| Mode | CPOL | CPHA | Clock Edge | Data Capture |
|------|------|------|------------|---------------|
| 0,0  | 0    | 0    | Rising     | Falling      |
| 0,1  | 0    | 1    | Rising     | Rising       |
| 1,0  | 1    | 0    | Falling    | Falling      |
| 1,1  | 1    | 1    | Falling    | Rising       |

**Visual mode reference**:
```
Mode 0: ▄──▀───▄──▀─── (sample on falling edge)
Mode 1: ▄──▀───▄──▀─── (sample on rising edge)  
Mode 2: ─▄───▀──▄───▀ (sample on falling edge)
Mode 3: ─▄───▀──▄───▀ (sample on rising edge)
```

**Most common**: Mode 0 and Mode 3
- Mode 0: CPOL=0, CPHA=0 (most common for simple devices)
- Mode 3: CPOL=1, CPHA=1 (common for many sensors)

## Transfer Format

### Single Device Transfer
```
Master: CS LOW → [Byte 1] → [Byte 2] → ... → [Byte N] → CS HIGH
Slave:         [Byte 1] ← [Byte 2] ← ... ← [Byte N]
```

**Note**: While master sends byte 1, it receives byte 1 from slave (simultaneously)

### Multi-Device Transfer
- Each slave has its own CS line
- Only the device with CS LOW responds
- Master can communicate with one slave at a time

### Transaction Types
- **Write**: Master sends data, slave responds (often ignored or status)
- **Read**: Master sends dummy bytes, slave sends data
- **Register access**: Send register address, then read/write data

## Electrical Characteristics

| Parameter | Typical Value | Notes |
|-----------|---------------|-------|
| Clock rate | 100kHz - 40MHz | Device-dependent, microcontroller-dependent |
| Voltage levels | 3.3V or 5V | Must match device requirements |
| Clock polarity | 0 or 1 | CPOL setting |
| Clock phase | 0 or 1 | CPHA setting |
| Bit order | MSB-first or LSB-first | Typically MSB-first |
| CS polarity | Active LOW or HIGH | Most devices use active LOW |

**Clock rate limits by device**:
- Slow devices (EEPROM): 1-5MHz
- Fast devices (Flash memory): 10-20MHz
- High-speed devices (RAM): 20-40MHz

## Chip Select Management

### Individual CS Lines
- **Pros**: Simple, reliable, full control
- **Cons**: Uses many GPIO pins
- **Usage**: Up to ~10 slaves (limited by available GPIO)

### CS Decoding
- **Address decoding**: Use address lines to select slave
- **Pros**: Saves GPIO pins
- **Cons**: More complex wiring, limited to power-of-2 slaves
- **Usage**: 4, 8, or 16 slaves with 2, 3, or 4 address lines

### SPI Mux/Demux
- **Hardware demultiplexer**: Dedicated IC to manage CS lines
- **Pros**: Clean design, scales to many slaves
- **Cons**: Additional hardware cost
- **Usage**: >10 slaves

### Daisy Chain
- **Shared CS**: Multiple devices on same CS line
- **Pros**: Minimal wiring
- **Cons**: Complex protocol, limited to specific devices
- **Usage**: Shift registers, some memory devices

## Common Device Categories

### Memory Devices
- **Flash memory**: W25Qxx, SST25VF series — typically Mode 0 or 3
- **EEPROM**: 25xx series — typically Mode 0 or 3
- **FRAM**: FM24Vxx — fast write, unlimited endurance

### Sensors
- **IMU**: MPU6050, MPU9250, BNO055 — various modes
- **Temperature**: MAX31855, DS18B20 (via SPI adapter) — Mode 0
- **Pressure**: MS5611, BMP280 (I2C/SPI) — Mode 0 or 1
- **ADC/DAC**: MCP3008, MCP4921, ADS1256 — various modes

### Displays
- **TFT LCD**: ILI9341, ST7789, SSD1351 — Mode 0, high clock rates
- **OLED**: SSD1306, SH1106 (SPI mode) — Mode 0 or 3
- **ePaper**: Various controllers — Mode 0, slow refresh

### Communication
- **Ethernet**: W5500, ENC28J60 — Mode 0
- **WiFi**: ESP8266 (SPI mode) — Mode 0
- **CAN**: MCP2515 — Mode 0

### Other
- **RTC**: DS3234 — Mode 1
- **SD Card**: MicroSD — Mode 0

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| CS line floating | Slave intermittently responds | Pull CS HIGH when not in use |
| CS glitch | Mode change, unexpected behavior | Add RC filter or use dedicated CS pin |
| Mode mismatch | Garbage data | Verify mode match between master and slave |
| Clock rate too high | Data corruption, communication errors | Reduce clock rate to device's maximum |
| Clock rate too low | Slow performance | Increase clock rate if device supports it |
| No MISO pull-up | Weak signal on MISO | Add pull-up resistor on MISO (if needed) |
| Bidirectional level shifting | Signal corruption | Use bidirectional level shifter for 3.3V/5V mixing |
| SPI bus interference | Erratic behavior | Isolate SPI bus, use dedicated pins, avoid crossing signals |
| CS timing violation | Slave doesn't respond | Ensure CS setup time before clock, hold time after clock |
| First byte not sent properly | Corrupted transfer | Send dummy byte before actual data if needed |

## Performance Considerations

- **Throughput**: Bytes per second = clock_rate / (8 + overhead)
- **Overhead**: CS setup/hold time, inter-byte delay
- **FIFO buffers**: Use if available to reduce CPU overhead
- **DMA**: Direct Memory Access for zero-CPU overhead transfers
- **Bottleneck**: Slowest device determines maximum practical clock rate

**Typical throughput**:
- 1MHz clock: ~125KB/s (1 byte per 8 clock cycles)
- 10MHz clock: ~1.25MB/s
- 40MHz clock: ~5MB/s

## Best Practices

- **Always pull CS HIGH when inactive**: Prevents floating CS from causing issues
- **Use dedicated CS per device**: Avoids conflicts and simplifies debugging
- **Start with low clock rate**: Test at low speed, then increase
- **Verify mode compatibility**: Check device datasheet for supported modes
- **Match voltage levels**: Use level shifters for 3.3V/5V mixing
- **Add decoupling capacitors**: Near each slave device for power stability
- **Keep traces short**: Reduce capacitance and improve signal integrity
- **Group devices by speed**: Put fast and slow devices on separate buses
- **Use interrupts for efficiency**: Interrupt-driven transfers reduce CPU overhead
- **Implement error recovery**: Retry failed transfers with backoff

## Debugging Tips

- **Oscilloscope**: Check MOSI, MISO, SCK, CS waveforms
- **Logic analyzer**: Capture full SPI transactions
- **Bus isolation**: Test with one slave at a time to identify problematic device
- **Signal integrity**: Check for rounding on clock edges, proper setup/hold times
- **Voltage levels**: Verify all devices see proper voltage levels
- **CS verification**: Confirm CS is LOW during transfer and HIGH between transfers

## Standing Rules

- **CS LOW means selected** — active LOW is the contract for most
  devices; verify the datasheet, but assume LOW until proven otherwise.
- **Each slave needs its own CS** — or a demultiplexer in the middle.
  A shared CS is a shared problem.
- **Mode 0 is the default assumption** — but check the datasheet; mode
  mismatch is the most common cause of garbage data.
- **Clock rate starts low** — 1MHz is a safe starting point; increase
  only after verification at lower speeds.
- **MISO needs a pull-up only if the slave requires it** — some slaves
  drive MISO actively, others are open-drain; read the datasheet.
- **The first byte is often the command** — many SPI devices use the
  first byte to select a register or command; send it deliberately.
- **SPI is full-duplex by design** — the master always receives a byte
  while sending one; ignoring the received byte is often a mistake.
- **Level shifting is explicit** — 3.3V and 5V do not mix; if the bus
  spans voltages, the level shifter is part of the design.
