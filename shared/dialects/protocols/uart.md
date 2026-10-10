---
type: protocol
family: bus
---

# UART (Universal Asynchronous Receiver/Transmitter)

The asynchronous serial protocol: no clock line, just two signals and
timing discipline. Data flows as frames, self-clocked by the baud rate.

## Eras

The era is declared by the **hardware support** and **features**.

**Basic UART**: RX/TX only, no FIFO, no hardware flow control
**Enhanced UART**: RX/TX + FIFO buffers (typically 4-16 bytes)
**Full UART**: RX/TX + FIFO + RTS/CTS flow control
**IrDA UART**: Infrared mode, supports IrDA encoding
**DMA UART**: Direct Memory Access support for zero-CPU transfers

Microcontroller support:
- AVR (Uno): 1 Hardware UART (UDR0), SoftwareSerial library
- AVR (Mega): 4 Hardware UARTs (UDR0-UDR3)
- ARM Cortex-M: Multiple UARTs (UART0-UARTn), often with FIFO
- ESP32: 3 Hardware UARTs (UART0-UART2), all with FIFO

## Signal Lines

```
TX (Transmit) ──────────────────────► RX (Receive)
        Device A                              Device B

Optional flow control:
RTS (Request To Send) ────────────► CTS (Clear To Send)
CTS (Clear To Send) ◄──────────────── RTS (Request To Send)
```

- **TX**: Output from device, sends data
- **RX**: Input to device, receives data
- **RTS**: Output from device, indicates ready to send
- **CTS**: Input to device, indicates other device ready to receive
- **DTR**: Data Terminal Ready (less common)
- **DSR**: Data Set Ready (less common)
- **DCD**: Data Carrier Detect (less common)
- **RI**: Ring Indicator (less common)

## Frame Format

Each byte is transmitted as a **frame**:

```
┌─────────┬────────┬────────┬────────┬────────┐
│ Start   │ Data 0  │ Data 1  │ ...    │ Stop   │
│ (LSB)   │         │         │         │ (MSB)  │
└─────────┴────────┴────────┴────────┴────────┘
```

**Components**:
- **Start bit**: Always LOW (0), 1 bit
- **Data bits**: 5-9 bits (typically 8), LSB first
- **Parity bit**: Optional (None, Even, Odd, Mark, Space)
- **Stop bit(s)**: Always HIGH (1), 1 or 2 bits

**Example** (8-N-1: 8 data bits, No parity, 1 stop bit):
```
Start: 0, Data: D0-D7 (LSB to MSB), Stop: 1
Total: 10 bits per byte
```

## Baud Rate

The symbol rate — bits per second. Both devices must agree.

**Standard baud rates**:
- 300, 600, 1200, 2400, 4800, 9600, 14400
- 19200, 28800, 38400, 57600, 76800
- 115200, 230400, 250000, 460800, 500000, 921600, 1000000

**Common usage**:
- Debug/Console: 9600, 19200, 115200
- GPS modules: 9600, 38400, 57600
- Bluetooth modules: 9600, 115200, 230400
- WiFi modules (ESP8266): 115200
- Industrial devices: 19200, 38400

**Baud rate calculation**:
```
Baud rate = Clock frequency / (16 × (UBRR + 1))  [Normal mode]
Baud rate = Clock frequency / (8 × (UBRR + 1))   [Double speed mode]
```

**Typical clock frequencies**:
- AVR: 16MHz (Uno/Nano), 8MHz (internal)
- ARM: 48MHz, 64MHz, 72MHz, 84MHz, 96MHz, 120MHz+
- ESP32: 40MHz, 80MHz, 160MHz, 240MHz

## Data Configuration

### Data Bits
- **5 bits**: Rare, used for Baudot code
- **6 bits**: Rare, used for some teleprinters
- **7 bits**: Common for ASCII (0-127)
- **8 bits**: Most common (0-255)
- **9 bits**: Used for address/byte multiplexing or parity

### Parity
- **None**: No parity bit
- **Even**: Parity bit set to make total 1s even
- **Odd**: Parity bit set to make total 1s odd
- **Mark**: Parity bit always HIGH (1)
- **Space**: Parity bit always LOW (0)

**Parity check**:
- Count number of 1s in data bits
- For Even parity: parity bit = 1 if odd number of 1s
- For Odd parity: parity bit = 1 if even number of 1s

### Stop Bits
- **1 stop bit**: Most common
- **2 stop bits**: Used at low baud rates for reliability
- **1.5 stop bits**: Rare, used for some teleprinters

## Flow Control

### Hardware Flow Control (RTS/CTS)
- **RTS (Request To Send)**: Device ready to send data
- **CTS (Clear To Send)**: Other device ready to receive data
- **Usage**: Prevents buffer overflow at high baud rates
- **Wiring**: RTS from Device A → CTS on Device B, CTS from Device A → RTS on Device B

### Software Flow Control (XON/XOFF)
- **XON**: ASCII 17 (DC1, 0x11) - Resume transmission
- **XOFF**: ASCII 19 (DC3, 0x13) - Pause transmission
- **Usage**: In-band flow control, no extra wires
- **Pitfall**: XON/XOFF bytes can appear in binary data

## Electrical Characteristics

| Parameter | Typical Value | Notes |
|-----------|---------------|-------|
| Voltage levels | 0V (LOW), 3.3V or 5V (HIGH) | Must match device requirements |
| Input threshold | 0.3×VCC (LOW), 0.7×VCC (HIGH) | Logic level thresholds |
| Idle state | HIGH (1) | Mark condition |
| Start bit | LOW (0) | Space condition |
| Stop bit | HIGH (1) | Mark condition |

**Voltage compatibility**:
- **5V UART**: Uno, Mega, most AVR boards
- **3.3V UART**: ARM boards, ESP32, most modern devices
- **Level shifting**: Required for 3.3V/5V mixing

## Common Device Categories

### Debug & Console
- **FTDI chips**: FT232R, FT232H — USB to UART bridge
- **CP210x**: CP2102, CP2104 — USB to UART
- **CH340**: USB to UART, low cost
- **PL2303**: USB to UART, older

### Wireless Modules
- **ESP8266**: WiFi module, UART for configuration and data
- **ESP32**: WiFi/Bluetooth, multiple UARTs
- **HC-05/HC-06**: Bluetooth modules, UART interface
- **nRF24L01**: 2.4GHz radio, SPI (not UART) — but some use UART
- **XBee**: Zigbee/802.15.4, UART interface
- **LoRa modules**: SX1278, RFM95W — UART or SPI

### GPS Modules
- **NEO-6M/7M/8M**: UBlox GPS, UART interface
- **MTK3339**: MediaTek GPS, UART interface
- **PA1010D**: GPS with dead reckoning, UART

### Cellular Modules
- **SIM800/900**: GSM/GPRS, UART interface
- **ESP32 with SIM7600**: Cellular add-on, UART
- **NB-IoT modules**: Various, UART interface

### Industrial Devices
- **Modbus RTU**: RS-485 transceivers, UART interface
- **HMI displays**: Nextion, UART interface
- **Barcode scanners**: Various, UART interface
- **Printers**: Thermal, label, UART interface

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Baud rate mismatch | Garbage data | Verify baud rate on both ends, check clock configuration |
| Parity error | Data corruption | Match parity settings, check for noise |
| Framing error | Byte boundary lost | Check stop bits, verify baud rate accuracy |
| Buffer overflow | Data loss | Use FIFO buffers, implement flow control, increase buffer size |
| Flow control mismatch | Data loss | Match flow control settings, verify wiring for RTS/CTS |
| Inverted logic | All bits flipped | Check if device uses inverted logic, verify voltage levels |
| Ground loop | Noise, erratic behavior | Use common ground, isolate power supplies |
| Long cable length | Signal degradation | Use proper cable, add line drivers, reduce baud rate |
| SoftwareSerial timing | Data loss at high baud rates | Use HardwareSerial when possible, reduce baud rate for SoftwareSerial |
| XON/XOFF in binary data | Premature flow control | Use hardware flow control or escape XON/XOFF bytes |

## Performance Considerations

- **Maximum baud rate**: Limited by microcontroller clock and UART implementation
- **SoftwareSerial limits**: Typically < 38400 on AVR, varies by platform
- **FIFO buffer benefit**: Reduces CPU overhead, prevents data loss
- **DMA benefit**: Zero-CPU overhead for large transfers
- **Interrupt overhead**: Can impact timing at high baud rates

**Typical maximum baud rates**:
- AVR SoftwareSerial: 38400 (reliable), 57600 (marginal), 115200 (unreliable)
- AVR HardwareSerial: 115200 (16MHz clock), 230400 (8MHz clock)
- ARM HardwareSerial: 1-10Mbps (depending on clock and implementation)
- ESP32 HardwareSerial: Up to 5Mbps

## Best Practices

- **Use HardwareSerial when available**: More reliable, supports higher baud rates
- **Match baud rate exactly**: Small differences can cause framing errors
- **Use parity for reliability**: Even or Odd parity catches single-bit errors
- **Implement flow control**: Prevents buffer overflow at high baud rates
- **Verify voltage compatibility**: Use level shifters for 3.3V/5V mixing
- **Keep cable length short**: < 3m for reliable operation at high baud rates
- **Use proper cable**: Twisted pair for long distances, shielded cable for noisy environments
- **Add buffer management**: Check for data before reading, handle overflows
- **Handle errors gracefully**: Detect framing/parity errors, implement recovery
- **Use circular buffers**: For software implementations to avoid data loss
- **Flush buffers**: Before switching between read/write modes or changing configurations

## Debugging Tips

- **Loopback test**: Connect TX to RX, send data and verify reception
- **External logic analyzer**: Capture UART signals for analysis
- **Check baud rate accuracy**: Use oscilloscope to measure actual baud rate
- **Verify signal levels**: Check TX/RX voltage levels with oscilloscope
- **Test with known-good device**: Verify UART works with simple echo test
- **Check flow control wiring**: Verify RTS/CTS connections are correct
- **Monitor buffer status**: Check buffer full/empty flags
- **Verify clock configuration**: Check UART clock source and divider values

## Standing Rules

- **Baud rate is a contract** — both ends must agree exactly; a 1% error
  can cause framing errors at high speeds.
- **8-N-1 is the default assumption** — but check the device datasheet;
  parity and stop bit mismatches are common defects.
- **Start bit is always 0** — the idle state is 1; a 0 bit starts the frame.
- **FIFO buffers prevent overflow** — but they must be drained; a full
  FIFO with no flow control is a data loss waiting to happen.
- **SoftwareSerial is for convenience, not performance** — use it for
  debugging and low-speed peripherals, not for reliable high-speed
  communication.
- **Hardware flow control solves real problems** — at high baud rates or
  with bursty traffic, RTS/CTS prevents buffer overflow.
- **Level shifting is explicit** — 3.3V and 5V UARTs do not mix; if the
  connection spans voltages, the level shifter is part of the contract.
