---
type: protocol
family: industrial
---

# Modbus

The de facto standard industrial protocol: **simple, robust, and
universal**. A request-response protocol that works over serial lines
(Modbus RTU) or Ethernet (Modbus TCP). Device-agnostic, vendor-neutral,
and proven for over 40 years.

## Eras

The era is declared by the **transport** and **specification version**.

**Modbus RTU (1979)**: Serial communication (RS-232/RS-485), binary
format, CRC error checking. The original and most common.

**Modbus ASCII (1979)**: Serial communication using ASCII characters
(LRC checksum). Rarely used today.

**Modbus TCP (1999)**: Ethernet communication (TCP/IP), big-endian
format, no checksum (reliant on TCP). Also called Modbus/TCP.

**Modbus RTU over TCP**: Encapsulated Modbus RTU frames in TCP packets.
Combines RTU reliability with TCP convenience.

**Modbus Security (2018)**: TLS/SSL encryption for Modbus TCP.
Addressing security concerns in industrial networks.

## Transport Layers

### Modbus RTU (Serial)

**Physical layers**:
- **RS-232**: Point-to-point, full-duplex, ±15V signaling
- **RS-485**: Multi-drop, half-duplex, differential signaling
- **RS-422**: Point-to-point, differential, full-duplex

**RS-485 characteristics**:
- **Topology**: Multi-drop bus (up to 32 devices typically, 247 max)
- **Distance**: Up to 1200m at 9600 baud, 100m at 115200 baud
- **Signaling**: Differential (A/B or +/-, A=-B)
- **Termination**: 120Ω resistor at each end
- **Biasing**: Pull-up/pull-down resistors for idle state

**Baud rates**: 9600, 19200, 38400, 57600, 115200 (most common)

### Modbus TCP (Ethernet)

**Network layer**: TCP/IP (port 502 by default)

**Connection**:
- **Single connection**: One TCP connection per Modbus transaction
- **Persistent connection**: Multiple transactions on same connection
- **Port**: 502 (default), can be configured

**Performance**:
- **Latency**: ~1-10ms (network dependent)
- **Throughput**: Limited by network and device
- **Parallel requests**: Multiple clients can connect simultaneously

**Comparison with RTU**:
- **Pros**: No distance limit, no wiring complexity, higher speed
- **Cons**: No checksum (reliant on TCP), more complex setup

## Addressing

### Device Addressing

- **RTU**: 1-247 (0 is broadcast, 248-255 reserved)
- **TCP**: IP address (device address can be 0 for TCP, or used for unit identifier)
- **Broadcast**: Address 0 (RTU: broadcast to all devices, TCP: unit identifier 0)

**Special addresses**:
- **0**: Broadcast address (all devices receive but only broadcast-capable devices respond)
- **248-255**: Reserved for special functions

### Data Addressing

Modbus uses a **unified addressing scheme** across all data types:

| Data Type | Address Range | Access | Description |
|-----------|---------------|--------|-------------|
| **Coils** | 00001-65536 | R/W | Single-bit output (discrete output) |
| **Discrete Inputs** | 10001-65536 | R | Single-bit input (read-only) |
| **Holding Registers** | 40001-65536 | R/W | 16-bit output (analog output, configuration) |
| **Input Registers** | 30001-65536 | R | 16-bit input (analog input, read-only) |

**Note**: Addresses can be specified in different formats:
- **Reference number**: 40001 (Holding Register 1)
- **Zero-based**: 0 (same as 40001)
- **Reference + offset**: 4x for Holding Registers, 3x for Input Registers, 0x for Coils, 1x for Discrete Inputs

**Address mapping**:
- Coil 1 = Address 0 = Reference 00001
- Discrete Input 1 = Address 10000 = Reference 10001
- Holding Register 1 = Address 0 = Reference 40001
- Input Register 1 = Address 0 = Reference 30001

## PDU (Protocol Data Unit)

The core of Modbus communication. All Modbus variants share the same PDU format.

### PDU Structure

```
┌────────┬────────┬─────────────────────────┬──────────┐
│ Function│ Starting│ Quantity of             │ Byte     │
│ Code    │ Address │ Registers/Data Items    │ Count    │
├────────┴────────┴─────────────────────────┴──────────┤
│ Data (for read/write functions)                        │
└──────────────────────────────────────────────────────┘
```

**Function Code**: 1 byte, defines the operation
**Starting Address**: 2 bytes, address of first item
**Quantity**: 2 bytes, number of items to read/write
**Byte Count**: 1 byte (for read functions), number of data bytes
**Data**: Variable length, the actual data

### Function Codes

| Code | Name | Description | Data Type |
|------|------|-------------|-----------|
| 0x01 | Read Coils | Read multiple coil statuses | Coils |
| 0x02 | Read Discrete Inputs | Read multiple discrete input statuses | Discrete Inputs |
| 0x03 | Read Holding Registers | Read multiple holding registers | Holding Registers |
| 0x04 | Read Input Registers | Read multiple input registers | Input Registers |
| 0x05 | Write Single Coil | Write single coil | Coils |
| 0x06 | Write Single Register | Write single holding register | Holding Registers |
| 0x07 | Read Exception Status | Read communication error status | - |
| 0x08 | Diagnostics | Run diagnostic tests | - |
| 0x0B | Get Comm Event Counter | Get communication event counter | - |
| 0x0C | Get Comm Event Log | Get communication event log | - |
| 0x0F | Write Multiple Coils | Write multiple coil statuses | Coils |
| 0x10 | Write Multiple Registers | Write multiple holding registers | Holding Registers |
| 0x11 | Report Slave ID | Report slave ID and additional information | - |
| 0x14 | Read File Record | Read file records | - |
| 0x15 | Write File Record | Write file records | - |
| 0x16 | Mask Write Register | Write holding register with mask | Holding Registers |
| 0x17 | Read/Write Multiple Registers | Read and write multiple registers | Holding Registers |
| 0x18 | Read FIFO Queue | Read FIFO queue | - |

**Most common function codes**: 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x0F, 0x10

### ADU (Application Data Unit)

The ADU wraps the PDU with transport-specific information.

**Modbus RTU ADU**:
```
┌────────┬───────────────┬───────────────┬────────┐
│ Slave   │ PDU           │ CRC           │
│ Address │ (Function +   │ (16-bit       │
│ (1)     │ Data)         │ checksum)     │
└────────┴───────────────┴───────────────┴────────┘
```

**Modbus TCP ADU**:
```
┌────────┬───────────────┬────────┐
│ MBAP    │ PDU           │
│ Header  │ (Function +   │
│ (7)     │ Data)         │
└────────┴───────────────┴────────┘
```

**MBAP Header** (Modbus TCP Application Protocol):
- **Transaction ID**: 2 bytes, used to match request/response
- **Protocol ID**: 2 bytes, always 0 for Modbus
- **Length**: 2 bytes, number of remaining bytes (PDU length + 1 for unit ID)
- **Unit ID**: 1 byte, device address (same as slave address in RTU)

## Data Representation

### Coils and Discrete Inputs

- **Type**: Boolean (1 bit)
- **Value**: 0 = OFF/False, 1 = ON/True
- **Packing**: 8 coils per byte, LSB first
- **Byte order**: Big-endian (MSB of byte is first coil)

**Example**: Reading 8 coils with values [1,0,1,1,0,0,1,0]
- Byte value: 0x92 (binary: 10010010, but stored LSB first)

### Holding Registers and Input Registers

- **Type**: 16-bit integer (unsigned)
- **Byte order**: Big-endian (most significant byte first)
- **Value range**: 0-65535

**Data types in registers**:
- **16-bit integer**: Single register (1 word)
- **32-bit integer**: Two registers (2 words), high word first
- **32-bit float**: Two registers, IEEE 754 format
- **64-bit integer**: Four registers (4 words), high word first
- **64-bit float**: Four registers, IEEE 754 double precision

**Example**: 32-bit integer 0x12345678
- Register 0: 0x1234 (high word)
- Register 1: 0x5678 (low word)

## Error Handling

### Exception Responses

When an error occurs, the device responds with an exception instead of normal data.

**Exception PDU**:
```
┌────────┬────────┬────────┐
│ Function│ Error   │
│ Code +  │ Code    │
│ 0x80    │ (1)     │
└────────┴────────┴────────┘
```

**Error codes**:
| Code | Name | Description |
|------|------|-------------|
| 0x01 | Illegal Function | Function code not supported |
| 0x02 | Illegal Data Address | Address outside valid range |
| 0x03 | Illegal Data Value | Value outside valid range |
| 0x04 | Slave Device Failure | Device failure (retry may work) |
| 0x05 | Acknowledge | Request accepted but long time to process |
| 0x06 | Slave Device Busy | Device busy, try later |
| 0x07 | Negative Acknowledge | Device cannot perform request |
| 0x08 | Memory Parity Error | Memory parity error (for devices with parity) |
| 0x0A | Gateway Path Unavailable | Gateway cannot route request |
| 0x0B | Gateway Target Device Failed | Target device on gateway failed |

### Timeout Handling

- **RTU**: Timeout typically 1-3 seconds (configurable)
- **TCP**: TCP timeout applies, typically 30-60 seconds
- **Retry**: Implement retry logic with exponential backoff

## Timing and Performance

### Modbus RTU Timing

**Character timeout (T1.5)**:
- **Definition**: 1.5 character times
- **Purpose**: Detect end of frame (silent period on bus)
- **Calculation**: T1.5 = 1.5 × (11 bits / baud rate) for 10-bit characters
- **Example**: At 9600 baud, T1.5 = 1.5 × 11/9600 ≈ 1.77ms

**Frame timeout (T3.5)**:
- **Definition**: 3.5 character times
- **Purpose**: Detect end of transmission (for master to start new request)
- **Calculation**: T3.5 = 3.5 × (11 bits / baud rate)

**Inter-frame delay**:
- **Minimum**: T3.5 (3.5 character times)
- **Recommended**: At least 4 character times between frames

**Baud rate vs maximum devices**:
| Baud Rate | Max Devices | Max Distance |
|-----------|-------------|--------------|
| 9600 | 247 | 1200m |
| 19200 | 247 | 1200m |
| 38400 | 247 | 1000m |
| 57600 | 247 | 500m |
| 115200 | 32 | 100m |

### Modbus TCP Timing

- **Connection timeout**: Typically 5-30 seconds
- **Read timeout**: Typically 1-5 seconds
- **Keep-alive**: Can be enabled for persistent connections
- **Nagle's algorithm**: Can cause delays; disable for real-time applications

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| No response | Communication failure | Check wiring, verify device address, check baud rate |
| CRC error | Data corruption | Verify wiring, check for noise, reduce baud rate |
| Timeout | Slow or no response | Increase timeout, check device load, verify bus health |
| Illegal function | Function not supported | Check device documentation, use supported functions |
| Illegal address | Address out of range | Verify address range, check device documentation |
| Illegal value | Value out of range | Verify value range, check device documentation |
| Slave busy | Device cannot respond | Retry with backoff, check device load |
| Parity error | Data corruption (RTU) | Verify parity settings, check wiring |
| Framing error | Serial framing issue | Check baud rate, verify stop bits and parity |
| RS-485 collision | Communication errors | Check termination, verify only one master active |
| Ground loop | Noise, erratic behavior | Use isolated RS-485 transceiver, proper grounding |
| Missing termination | Signal reflection | Add 120Ω termination resistors at both ends |

## Best Practices

### General
- **Use consistent addressing**: Define and document address ranges
- **Minimize polling**: Only poll when necessary, use appropriate intervals
- **Implement error recovery**: Retry failed requests with exponential backoff
- **Validate data**: Check for reasonable values, handle exceptions
- **Log communication**: Log requests and responses for debugging

### Modbus RTU
- **Always use termination**: 120Ω resistor at each end of bus
- **Match baud rate**: All devices must use same baud rate
- **Match parity**: All devices must use same parity setting
- **Limit bus length**: Stay within recommended distance for baud rate
- **Use proper wiring**: Twisted pair for RS-485, shielded cable
- **Add bias resistors**: Pull-up/pull-down for idle state on RS-485
- **Isolate ground**: Use isolated RS-485 transceiver to avoid ground loops

### Modbus TCP
- **Use persistent connections**: Reduces connection overhead
- **Set appropriate timeouts**: Balance responsiveness and reliability
- **Handle disconnections**: Detect and reconnect when connection drops
- **Use multiple connections**: For high-throughput applications, use multiple TCP connections
- **Secure connections**: Use TLS/SSL for sensitive data
- **Use unit ID**: Even on TCP, use unit ID to address specific devices

### Addressing
- **Group by function**: Coils for digital outputs, Holding Registers for configuration, Input Registers for sensor data
- **Use contiguous addresses**: Minimize gaps in address space
- **Document all addresses**: Maintain address map for all devices
- **Avoid address 0**: Unless using broadcast (not all devices support it)
- **Reserve addresses**: Reserve addresses for future devices

### Performance
- **Batch requests**: Read/write multiple registers in single request
- **Use function 0x03/0x10**: Prefer read/write multiple registers over single
- **Prioritize important data**: Poll critical data more frequently
- **Use appropriate baud rate**: Higher baud rate = shorter cycle time but shorter distance
- **Optimize poll rate**: Balance data freshness with bus load

## Debugging Tips

### Serial Debugging (RTU)
- **Check baud rate**: Verify all devices use same baud rate
- **Verify wiring**: Check for shorts, opens, or reversed connections
- **Test with loopback**: Connect TX to RX, send data and verify reception
- **Use serial monitor**: Monitor traffic with serial monitor tool
- **Check termination**: Measure resistance between A and B (should be ~60Ω)
- **Verify signal levels**: Use oscilloscope to check RS-485 signals
- **Test with one device**: Verify basic communication before adding more

### Network Debugging (TCP)
- **Check IP connectivity**: Ping device IP address
- **Verify port**: Check if port 502 is open (or configured port)
- **Test with telnet**: Connect with telnet to verify Modbus TCP response
- **Use Wireshark**: Capture Modbus TCP traffic for analysis
- **Check firewall**: Verify firewall allows traffic on Modbus port
- **Test with known-good device**: Verify network and Modbus TCP stack

### Modbus Tools
- **Modbus Poll**: GUI tool for testing Modbus devices
- **QModMaster**: Open-source Modbus master/simulator
- **mbpoll**: Command-line Modbus polling tool
- **Modbus Pal**: Modbus master/simulator with logging
- **Wireshark**: Network protocol analyzer (with Modbus dissector)
- **Serial oscilloscope**: For RTU signal analysis

## Implementation Examples

### Python (pymodbus)

```python
from pymodbus.client import ModbusTcpClient
from pymodbus.client import ModbusSerialClient

# Modbus TCP
client = ModbusTcpClient('192.168.1.100', port=502)
client.connect()

# Read holding registers
response = client.read_holding_registers(address=0, count=10, slave=1)
if response.isError():
    print(f"Error: {response}")
else:
    print(response.registers)

# Write single register
response = client.write_register(address=0, value=1234, slave=1)

client.close()

# Modbus RTU
client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyUSB0',
    baudrate=9600,
    timeout=1,
    parity='N',
    stopbits=1,
    bytesize=8
)
client.connect()

# Same API as TCP
response = client.read_coils(address=0, count=8, slave=1)

client.close()
```

### Node.js (modbus-serial)

```javascript
const ModbusRTU = require("modbus-serial");

// Modbus RTU
const client = new ModbusRTU();
client.connectRTU("/dev/ttyUSB0", { baudRate: 9600 });
client.setID(1);

// Read holding registers
client.readHoldingRegisters(0, 10)
    .then(data => {
        console.log(data.data);
    })
    .catch(err => {
        console.error(err);
    });

// Write single register
client.writeRegister(0, 1234)
    .then(() => {
        console.log("Write successful");
    });

// Close connection
setTimeout(() => { client.close(); }, 1000);
```

### C (libmodbus)

```c
#include <modbus.h>
#include <stdio.h>

// Modbus TCP
modbus_t *ctx = modbus_new_tcp("192.168.1.100", 502);
modbus_connect(ctx);

uint16_t tab_reg[10];
int rc = modbus_read_registers(ctx, 0, 10, tab_reg);
if (rc == -1) {
    fprintf(stderr, "Error: %s\n", modbus_strerror(errno));
} else {
    for (int i = 0; i < rc; i++) {
        printf("Register %d: %d\n", i, tab_reg[i]);
    }
}

modbus_close(ctx);
modbus_free(ctx);

// Modbus RTU
ctx = modbus_new_rtu("/dev/ttyUSB0", 9600, 'N', 8, 1);
modbus_set_slave(ctx, 1);
modbus_connect(ctx);

// Same API as TCP
rc = modbus_read_bits(ctx, 0, 8, tab_reg);

modbus_close(ctx);
modbus_free(ctx);
```

## Integration Patterns

### Master-Slave Architecture

```
Master (SCADA/HMI/PLC) ↔ Modbus Network ↔ Slave 1 (PLC)
                                              ↔ Slave 2 (Sensor)
                                              ↔ Slave 3 (Motor Drive)
```

- **Master**: Initiates requests, collects data
- **Slaves**: Respond to requests, provide data
- **Network**: RS-485 bus or Ethernet network

### Gateway Pattern

```
External System ↔ Gateway ↔ Modbus Network ↔ Devices
```

- **Gateway**: Translates between protocols (e.g., Modbus ↔ MQTT, Modbus ↔ OPC UA)
- **Functions**: Protocol translation, data concentration, buffering
- **Use cases**: Connect Modbus devices to cloud, integrate with other systems

### Polling Pattern

```
Master: [Poll Slave 1] → [Wait] → [Poll Slave 2] → [Wait] → ...
```

- **Polling interval**: Balance data freshness and bus load
- **Optimization**: Poll critical data more frequently, less critical data less often
- **Burst polling**: Poll multiple registers in single request

### Event-Driven Pattern (via Gateway)

```
Modbus Device → Gateway → MQTT Broker → Subscribers
```

- **Gateway**: Monitors Modbus devices, publishes changes via MQTT
- **Trigger**: On change of value, threshold crossing, or timer
- **Advantage**: Reduces polling, more efficient

## Device Profiles

### Common Modbus Device Types

| Device Type | Typical Functions | Address Ranges |
|-------------|-------------------|----------------|
| **PLC** | 0x01, 0x03, 0x05, 0x06, 0x0F, 0x10 | 0-65535 (all types) |
| **Temperature Sensor** | 0x03, 0x04 | Holding/Input Registers for temperature |
| **Pressure Sensor** | 0x03, 0x04 | Holding/Input Registers for pressure |
| **Flow Meter** | 0x03, 0x04 | Holding/Input Registers for flow rate, total |
| **Level Sensor** | 0x03, 0x04 | Holding/Input Registers for level |
| **Motor Drive** | 0x03, 0x05, 0x06, 0x0F, 0x10 | Holding Registers for speed, Coils for start/stop |
| **VFD (Variable Frequency Drive)** | 0x03, 0x05, 0x06, 0x0F, 0x10 | Holding Registers for frequency, Coils for run/stop |
| **Power Meter** | 0x03, 0x04 | Input Registers for voltage, current, power, energy |
| **I/O Module** | 0x01, 0x02, 0x05, 0x0F | Coils/Discrete Inputs for digital I/O |
| **Analog I/O Module** | 0x03, 0x04, 0x06, 0x10 | Holding/Input Registers for analog I/O |

### Popular Modbus Device Vendors

| Vendor | Device Types | Notes |
|--------|--------------|-------|
| **Siemens** | S7-200, S7-1200 (via Modbus TCP), ET200 | Requires communication modules |
| **Allen-Bradley** | Micro800, CompactLogix (via Modbus TCP) | Requires communication modules |
| **Schneider** | Zelio, M221, M241, M251, M262 | Native Modbus support |
| **Mitsubishi** | FX, Q, iQ-R (via Modbus TCP) | Requires communication modules |
| **Omron** | CP1E, CP1H, CJ, CS (via Modbus TCP) | Requires communication modules |
| **ABB** | AC500, AC800M | Native Modbus support |
| **WEG** | CFW, W22 | Motor drives with Modbus |
| **Danfoss** | VLT, VACON | VFD with Modbus |
| **Sick** | Sensors (distance, photoelectric) | Sensor manufacturer |
| **ifm** | Sensors (pressure, temperature, flow) | Sensor manufacturer |
| **Pepperl+Fuchs** | Sensors (proximity, photoelectric) | Sensor manufacturer |
| **Honeywell** | Sensors, controllers | Process automation |
| **Yokogawa** | Meters, recorders | Measurement instruments |

## Security Considerations

### Modbus RTU Security

- **Physical access**: RS-485 bus can be tapped; use isolated transceivers
- **No authentication**: Modbus RTU has no built-in authentication
- **Access control**: Control physical access to devices and bus
- **Encryption**: Not available; use separate network for sensitive data
- **Network isolation**: Use dedicated RS-485 network, avoid sharing with other systems

### Modbus TCP Security

- **Port security**: Change default port (502) to non-standard port
- **Firewall**: Restrict access to Modbus port
- **Network segmentation**: Isolate Modbus network from other networks
- **Authentication**: Use IP-based access control, VPN for remote access
- **Encryption**: Use TLS/SSL for Modbus TCP Security
- **Disable unused services**: Close unused TCP ports

### General Security

- **Device hardening**: Disable unused services, change default passwords
- **Network monitoring**: Monitor for unusual Modbus traffic
- **Access logging**: Log all Modbus access attempts
- **Regular audits**: Periodically review device configurations
- **Firmware updates**: Keep device firmware up to date

## Standing Rules

- **Address 0 is for broadcast** — use it to send to all devices, but
  remember that not all devices support broadcast and not all
  functions work with broadcast.
- **The master always initiates** — Modbus is strictly master-slave;
  a slave never sends unsolicited data (except in special cases like
  Modbus over MQTT).
- **CRC is mandatory on RTU** — a frame without a valid CRC is a
  frame to discard; the checksum is the contract.
- **The slave address is the first byte** — on RTU, it is always the
  first byte of the ADU; on TCP, it is the last byte of the MBAP header.
- **Function codes define the contract** — a device that does not
  support a function code returns an exception; a device that
  pretends to support it is a device to distrust.
- **Big-endian is the byte order** — high byte first, low byte
  second, for both registers and multi-byte data types.
- **Registers are 16-bit** — a 32-bit value is two registers, a
  64-bit value is four; the order is high-word-first.
- **Timeout is a design decision** — a short timeout catches
  failures fast, a long timeout tolerates slow devices; pick based
  on the application.
- **Retries are expected** — networks and buses fail; design for
  retries with backoff, and document the retry policy.
