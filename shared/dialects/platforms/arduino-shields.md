---
type: platform
family: embedded
---

# Arduino Shields and Extension Boards

Attaches alongside `arduino.md` and `embedded.md`. Shields are the
modular expansion system that turns an Arduino into a domain-specific
controller. The shield is the contract; the stacking order is the
architecture.

## Eras

The board/shield combination declares the era. Three eras are named
by the substrate:

**Classic AVR**: Uno, Mega, Nano — 5V logic, limited SRAM, the original
shield ecosystem. Shims and level-shifting may be required for 3.3V
peripherals.

**ARM/SAMD**: Due, Zero, MKR family — 3.3V logic, native USB, Cortex-M
cores. Shields need 3.3V compatibility; some Classic shields are
incompatible.

**ESP32-based**: ESP32 boards under Arduino layer — 3.3V logic, WiFi/BT
built-in, dual-core. Most shields work, but WiFi/Bluetooth shields are
redundant.

## Shield Categories

### Communication Shields

| Shield | Protocol | Era | Pitfalls |
|--------|----------|-----|----------|
| **Ethernet** (W5100/W5500) | Ethernet | AVR | W5100: single socket, limited buffer; W5500: better throughput |
| **WiFi** (ESP8266) | WiFi | AVR | AT command set, needs proper power, baud rate sensitive |
| **LoRa** (RadioHead) | LoRa | All | SPI bus, frequency band configuration, antenna requirements |
| **NFC/RFID** (PN532, RC522) | RFID/NFC | All | SPI/I2C/UART variants, tag type compatibility |
| **Bluetooth** (HC-05/HC-06) | Bluetooth | All | AT command mode, pairing, baud rate matching |
| **Bluetooth LE** (nRF8001, Bluefruit) | BLE | All | Complex protocol, library-specific |
| **XBee** | Zigbee/802.15.4 | All | Configuration via X-CTU, firmware variants |
| **CAN Bus** (MCP2515, MCP2510) | CAN | All | SPI interface, bus termination, bit rate matching |
| **RS-485** (MAX485) | RS-485 | All | Half-duplex, direction control, termination resistors |

### Sensor Shields

| Shield | Sensors | Interface | Pitfalls |
|--------|---------|-----------|----------|
| **Sensor Shield** (generic) | Multiple sensors | Analog/Digital | Pin multiplexing required, no built-in calibration |
| **IMU** (MPU6050/9250) | Accelerometer, Gyro, Magnetometer | I2C/SPI | Axis alignment, calibration, drift compensation |
| **GPS** (NEO-6M/7M/8M) | GPS/GNSS | UART/I2C | Cold start time, antenna placement, baud rate |
| **Environmental** (BME280) | Temp, Humidity, Pressure | I2C/SPI | I2C address configurable, compensation formulas |
| **Gas** (MQ-x series) | CO, CO2, Alcohol, etc. | Analog | Heater required, warm-up time, non-linear response |
| **Light/Color** (TCS34725) | RGB, Color, Lux | I2C | Integration time affects accuracy |
| **Sound** (MAX4466, MAX9814) | Microphone | Analog | Amplification, sampling rate, ADC resolution |
| **Touch** (Capacitive) | Capacitive touch | Digital | Sensitivity tuning, EMI susceptibility |

### Display Shields

| Shield | Type | Interface | Pitfalls |
|--------|------|-----------|----------|
| **LCD 16x2** (HD44780) | Character LCD | 4-bit/8-bit parallel | Pin count, contrast adjustment, backlight control |
| **LCD 20x4** (HD44780) | Character LCD | 4-bit/8-bit parallel | Same as 16x2, more rows |
| **OLED** (SSD1306) | Monochrome OLED | I2C/SPI | I2C address 0x3C/0x3D, memory layout, page addressing |
| **OLED** (SH1106) | Monochrome OLED | I2C/SPI | Similar to SSD1306, different controller commands |
| **TFT** (ILI9341/ST7789) | Color TFT | SPI | High SPI speed required, frame buffer size |
| **ePaper** (e-Ink) | ePaper display | SPI | Slow refresh rate, partial update support varies |
| **7-Segment** (MAX7219) | LED 7-segment | SPI | Cascadable, brightness control, digit scanning |

### Motor & Actuator Shields

| Shield | Actuators | Interface | Pitfalls |
|--------|-----------|-----------|----------|
| **L298N** | DC motors, 2 channels | PWM + Digital | Heat dissipation, current draw, flyback diodes needed |
| **L293D** | DC motors, 4 channels (half H-bridge) | PWM + Digital | Lower current, same heat concerns |
| **TB6612FNG** | DC motors, 2 channels | PWM + Digital | Higher current, better for larger motors |
| **Stepper** (A4988/DRV8825) | Stepper motors | PWM + Digital | Microstepping configuration, heat sinks required |
| **Servo** | RC servos | PWM | Power requirements, jitter in digitalWrite |
| **Relay** | High-current devices | Digital | Coil current, contact rating, EMI from switching |
| **Solid State Relay** | AC loads | Digital | Zero-cross vs random turn-on, heat sinking |
| **Motor Shield** (Adafruit) | Multiple motor types | I2C/PWM | Current sensing, fault detection |

### Power & Management Shields

| Shield | Purpose | Interface | Pitfalls |
|--------|---------|-----------|----------|
| **Power Shield** | Voltage regulation | None | Input voltage range, current limits, heat |
| **Battery Shield** | Battery charging | I2C | Charger IC configuration, battery type matching |
| **RTC** (DS1307/DS3231) | Real-time clock | I2C | Battery backup required, I2C address conflicts |
| **Data Logging** | SD card logging | SPI | File system, FAT16/32, wear leveling |
| **Watchdog** | System reset | Digital | Trigger conditions, timeout configuration |

### Utility Shields

| Shield | Purpose | Interface | Pitfalls |
|--------|---------|-----------|----------|
| **Proto Shield** | Prototyping | None | Soldering required, no built-in functionality |
| **Motor Proto Shield** | Motor + Proto | Stackable | Combines motor driver and proto area |
| **Wireless Proto Shield** | Proto + Wireless | Stackable | RF interference from poor layout |
| **Screw Terminal** | Easy wiring | None | Connection integrity, current limits |
| **LED Matrix** (MAX7219) | LED matrix | SPI | Cascadable, brightness, power consumption |

## Communication Interface Contracts

### I2C Bus

**Era mapping**: AVR (Wire library), ARM (Wire library), ESP32 (Wire
library with dual bus support).

**The contract**:
- **Addressing**: 7-bit (0x00-0x7F) and 10-bit (0x000-0x3FF) addressing
- **Pull-ups**: External pull-up resistors required on SDA and SCL
  (typical 4.7kΩ - 10kΩ)
- **Speed limits**: Standard mode (100kHz), Fast mode (400kHz), Fast mode
  Plus (1MHz), High-speed mode (3.4MHz) — most shields support 100kHz or
  400kHz
- **Clock stretching**: Some devices (EEPROMs) use clock stretching
- **Repeated start**: Required for some complex transactions

**Pitfalls**:
- Address conflicts between multiple shields on same bus
- Insufficient pull-up resistance for long buses
- Clock stretching not supported on all microcontrollers
- Bus capacitance limits (400pF for 100kHz, 200pF for 400kHz)

**Best practices**:
- Use a dedicated I2C bus for each set of incompatible devices
- Place pull-ups near the master, not at the device
- Keep bus length short (< 1m for 100kHz)
- Use bus capacitors for long runs

### SPI Bus

**Era mapping**: AVR (SPI library), ARM (SPI library), ESP32 (SPI
library with multiple buses).

**The contract**:
- **Modes**: 4 modes (CPOL, CPHA combinations)
- **Clock rates**: Typically up to 8MHz on AVR, higher on ARM/ESP32
- **Chip Select (CS/SS)**: Active-low, must be controlled by master
- **Full-duplex**: Simultaneous send and receive
- **Bit order**: MSB first (standard) or LSB first

**Pitfalls**:
- CS glitches (floating CS pins can cause mode changes)
- Clock rate too high for device
- Mode mismatch between master and slave
- Multiple slaves sharing SPI bus need individual CS lines

**Best practices**:
- Always pull CS high when not in use
- Use dedicated CS for each device
- Start with low clock rate, increase as needed
- Use level-shifters for 3.3V/5V compatibility

### UART/Serial

**Era mapping**: AVR (Serial library, HardwareSerial), ARM (Serial
library, Serial1+), ESP32 (Serial library, multiple UARTS).

**The contract**:
- **Baud rates**: Standard rates (300, 1200, 2400, 4800, 9600, 19200,
  38400, 57600, 115200, 230400, 250000, 500000, 1000000)
- **Data bits**: 5-9 (typically 8)
- **Parity**: None, Even, Odd, Mark, Space
- **Stop bits**: 1 or 2
- **Flow control**: None, RTS/CTS, XON/XOFF

**Pitfalls**:
- Baud rate mismatch between devices
- Insufficient buffer size for incoming data
- Parity errors from noise
- SoftwareSerial conflicts with other libraries

**Best practices**:
- Use HardwareSerial when available (more reliable)
- Match baud rate to device's maximum reliable rate
- Use SoftwareSerial for additional ports on AVR
- Implement buffer management for high-speed data

### 1-Wire

**Era mapping**: All eras (OneWire library).

**The contract**:
- **Single wire**: Data + power (parasite power possible)
- **Timing critical**: Strict timing requirements
- **Device enumeration**: Each device has unique 64-bit ROM code
- **CRC**: 8-bit CRC for data integrity
- **Pull-up**: Strong pull-up required (typically 4.7kΩ)

**Pitfalls**:
- Bus capacitance limits (< 400pF total)
- Long bus lengths require active pull-up
- Parasite power limits number of devices
- Bus reset timing critical

**Best practices**:
- Use dedicated pull-up resistor
- Limit bus length (< 100m with proper wiring)
- Group devices by distance
- Use separate buses for distant devices

### CAN Bus

**Era mapping**: AVR (CAN library, MCP2515), ARM (FlexCAN), ESP32
(ESP32 CAN).

**The contract**:
- **Message IDs**: Standard (11-bit) and Extended (29-bit)
- **Frame types**: Data frame, Remote frame, Error frame, Overload frame
- **Bit rates**: Common rates 125kbps, 250kbps, 500kbps, 1Mbps
- **Arbitration**: Lower ID = higher priority
- **Termination**: 120Ω resistors at both ends of bus

**Pitfalls**:
- Missing termination resistors
- Bit rate mismatch between nodes
- Bus length vs bit rate relationship
- Error frames can flood bus

**Best practices**:
- Always use termination resistors (120Ω)
- Keep bus length appropriate for bit rate
- Use CAN transceiver with proper voltage levels
- Monitor bus error counters

## Stacking Architecture

### Physical Stacking

- Shields stack via header pins (D0-D13, A0-A5, VCC, GND, RESET)
- **Power pins**: 5V, 3.3V, VIN, GND — must align with board capabilities
- **I/O pins**: Some pins are shared between shields
- **ICSP**: In-Circuit Serial Programming header for programming

### Pin Conflict Resolution

**Conflict matrix** — common pin usage:

| Pin | Common Uses | Conflict Risk |
|-----|-------------|---------------|
| D0/D1 | UART (RX/TX) | HIGH - used by many shields |
| D2/D3 | Interrupts | MEDIUM - external interrupts |
| D4/D5 | SPI (MISO/MOSI) | HIGH - SPI shields |
| D10 | SPI (SS/CS) | HIGH - most SPI slaves |
| D11/D12/D13 | SPI (MOSI/MISO/SCK) | HIGH - SPI bus |
| A4/A5 | I2C (SDA/SCL) | HIGH - I2C shields |

**Resolution strategies**:
- Use jumpers to route signals to alternative pins (where hardware allows)
- Software bit-banging for non-critical interfaces
- Dedicated boards for specific shield combinations
- External multiplexers for high-conflict setups

### Power Budgeting

- **Classic AVR (Uno)**: 500mA total, ~20mA per I/O pin
- **Mega**: 800mA total
- **ARM/SAMD**: 3.3V logic, lower current
- **ESP32**: 3.3V logic, higher current for WiFi/BT

**Budget calculation**:
1. Sum current draw of all shields
2. Add motor/actuator current (peaks and continuous)
3. Account for voltage conversion losses
4. Ensure power supply can provide total current
5. Add margin (20-50% recommended)

### Address Management

- **I2C**: Each device must have unique address; some have configurable
  addresses via jumpers or software
- **SPI**: Each slave needs unique CS line
- **1-Wire**: Each device has unique ROM address
- **CAN**: Each node has unique ID

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| I2C address conflict | Bus lockup, no communication | Scan bus, configure addresses, use bus multiplexers |
| Insufficient power | Reset loops, brownouts | Calculate power budget, use external supply |
| CS line floating | SPI miscommunication | Pull CS high when inactive, use dedicated CS |
| UART buffer overflow | Data loss | Increase buffer size, implement flow control |
| 1-Wire bus capacitance | Communication errors | Shorten bus, reduce device count, use active pull-up |
| CAN bus missing termination | Communication errors | Add 120Ω termination resistors at both ends |
| Pin conflicts | Shield malfunction | Rewire jumpers, use different pins, separate boards |
| Heat buildup | Thermal shutdown | Add heat sinks, improve airflow, derate current |
| EMI/Noise | Erratic behavior | Shield wires, add capacitors, improve grounding |
| SoftwareSerial interference | Timing issues | Use HardwareSerial, avoid pins with PWM/Interrupts |

## Standing Rules

- **Shield first, code second**: The shield defines the hardware contract;
  the code follows. Never assume a shield works until its datasheet is read.
- **Power is a design constraint**: Calculate the budget before stacking;
  a design that exceeds the power supply is a broken design.
- **Pin conflicts are architecture bugs**: Resolve them in the design phase,
  not with hacks on the bench.
- **Level shifting is explicit**: 5V and 3.3V do not play well together;
  if the shield is one and the board is the other, the level shifter is
  part of the design.
- **I2C needs pull-ups, always**: If the shield or board does not provide
  them, the designer does. No pull-ups, no bus.
- **SPI needs chip selects**: One CS per slave, or a demultiplexer in the
  middle. Shared CS is a shared problem.
- **UART needs flow control for reliability**: At high baud rates or
  bursty traffic, hardware flow control (RTS/CTS) prevents buffer
  overflow.
- **Test with minimal stack first**: Verify each shield individually before
  combining; a stacked system with a bad shield is hard to debug.
