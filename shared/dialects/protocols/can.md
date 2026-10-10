---
type: protocol
family: bus
---

# CAN (Controller Area Network)

The multi-master, multi-device, message-oriented bus. Priority-based
arbitration, error detection, and fault tolerance. Designed for
automotive and industrial applications.

## Eras

The era is declared by the **protocol version** and **speed grade**.

**CAN 2.0A**: Standard 11-bit identifiers (1980s)
**CAN 2.0B**: Extended 29-bit identifiers (1991)
**CAN FD**: CAN with Flexible Data Rate (2012) — faster data rates
**CAN XL**: Next generation, higher data rates, longer payloads

Microcontroller support:
- AVR: Via MCP2515/MCP2510 transceiver (SPI interface)
- ARM Cortex-M: Native CAN controller (CAN, FlexCAN, BXCAN)
- ESP32: Via external transceiver (SPI or dedicated peripheral on some chips)

Transceiver support:
- **MCP2515**: CAN 2.0A/B, SPI interface, 1Mbps max
- **MCP2510**: CAN 2.0A/B, SPI interface
- **TJA1050**: CAN FD, up to 5Mbps
- **TJA1040**: High-speed CAN, up to 1Mbps
- **SNR65HVD234**: Industrial CAN, ±60V fault protection

## Bus Topology

```
CAN_H ─────────────────────────────┬─ Node 1
                                  ├─ Node 2
                                  ├─ Node 3
                                  └─ Termination resistor (120Ω)

CAN_L ─────────────────────────────┴─ Node 1
                                  ├─ Node 2
                                  └─ Node 3
                                  └─ Termination resistor (120Ω)
```

- **CAN_H**: High signal line (dominant = LOW, recessive = HIGH)
- **CAN_L**: Low signal line (dominant = HIGH, recessive = LOW)
- **Differential signaling**: CAN_H - CAN_L = bus state
- **Termination**: 120Ω resistor at each end of bus
- **Bus length**: Up to 40m at 1Mbps, up to 1km at lower speeds

**Logical states**:
- **Dominant**: Both CAN_H LOW and CAN_L HIGH (logical 0)
- **Recessive**: Both CAN_H HIGH and CAN_L HIGH (logical 1)

## Message Format

### CAN 2.0 Frame Types

#### Data Frame (CAN 2.0A - 11-bit ID)
```
┌────────┬────────┬─────┬─────┬─────┬─────────────┬──────┐
│ Start  │ ID     │ RTR │ IDE │ r1  │ Data        │ CRC  │
│ (1)    │ (11)   │ (1) │ (1) │ (1) │ (0-8 bytes) │ (15) │
└────────┴────────┴─────┴─────┴─────┴─────────────┴──────┘
                           └───────────┬─────────────┘
                               Stop (1) + Intermission (3)
```

#### Data Frame (CAN 2.0B - 29-bit ID)
```
┌────────┬────────┬─────┬────────────┬─────┬─────┬─────────────┬──────┐
│ Start  │ ID     │ SRR │ IDE=0      │ RTR │ r1  │ Data        │ CRC  │
│ (1)    │ (11)   │ (1) │ (18 bits)  │ (1) │ (1) │ (0-8 bytes) │ (15) │
└────────┴────────┴─────┴────────────┴─────┴─────┴─────────────┴──────┘
                           └──────────────────────┬─────────────┘
                                   Stop (1) + Intermission (3)
```

#### Remote Frame (RTR = 1)
- **Purpose**: Request data from another node
- **Format**: Same as Data Frame but with RTR bit = 1 and no data field
- **Usage**: Rare in modern applications (deprecated in CAN FD)

#### Error Frame
- **Purpose**: Signal bus errors
- **Format**: Superposition of ERROR FLAGS from different nodes
- **Components**: ERROR FLAG (6 dominant bits), ERROR DELIMITER (8 recessive bits)
- **Pitfall**: Multiple nodes sending error flags simultaneously

#### Overload Frame
- **Purpose**: Signal overload condition
- **Format**: Similar to error frame but for overload
- **Usage**: Rare, used when node needs delay

#### Interframe Space
- **Purpose**: Separate consecutive frames
- **Components**: Intermission (3 recessive bits) + Bus Idle

### CAN FD Frame Format

**Enhanced features**:
- **Payload**: Up to 64 bytes (vs 8 bytes in CAN 2.0)
- **Bit rate switching**: Different rates for arbitration and data phases
- **Stuff bit reduction**: Fewer stuff bits for higher efficiency
- **Error detection**: Enhanced CRC (17 or 21 bits)

**Frame types**:
- **Classic CAN FD**: Compatible with CAN 2.0
- **CAN FD with BRS**: Bit Rate Switch enabled

## Addressing (Message IDs)

### 11-bit ID (CAN 2.0A)
- **Range**: 0x000 - 0x7FF (2048 possible IDs)
- **Priority**: Lower ID = higher priority
- **Usage**: Most common, sufficient for most applications

### 29-bit ID (CAN 2.0B)
- **Range**: 0x00000000 - 0x1FFFFFFF (~536 million possible IDs)
- **Priority**: Lower 11 bits determine priority (for arbitration)
- **Usage**: Extended addressing for complex systems

**Special IDs**:
- **0x000**: Highest priority (reserved for emergency messages)
- **0x7FF**: Lowest priority in 11-bit
- **0x00000000 - 0x000007FF**: Compatible with 11-bit IDs

## Arbitration

### Non-Destructive Arbitration
- **Principle**: Multiple nodes can start transmitting simultaneously
- **Mechanism**: Each node monitors bus while transmitting
- **Outcome**: Node with lower ID (higher priority) wins, others back off
- **Bit-wise**: Dominant bits (0) overwrite recessive bits (1)

**Example**:
```
Node A sends: 0x100 (0001 0000 0000)
Node B sends: 0x200 (0010 0000 0000)

Bit 10: A sends 0 (dominant), B sends 0 → Bus = 0
Bit 9:  A sends 0 (dominant), B sends 1 → Bus = 0 (A wins)
... Node B detects it lost arbitration and stops transmitting
```

### Arbitration Process
1. All nodes start transmitting START OF FRAME (dominant)
2. Each node transmits its ID bit by bit
3. Each node monitors bus state
4. If node transmits recessive (1) but sees dominant (0), it loses arbitration
5. Winning node continues transmission
6. Losing nodes switch to receive mode

## Bit Timing

### Nominal Bit Time (CAN 2.0)
Divided into segments:

```
┌──────────┬──────────┬──────────┬──────────┐
│ Sync     │ Prop     │ Phase 1   │ Phase 2   │
│ Segment  │ Segment  │ Segment   │ Segment   │
└──────────┴──────────┴──────────┴──────────┘
```

- **Sync Segment**: 1 time quantum (tq) - Synchronization edge
- **Propagation Segment**: 1-8 tq - Compensates for physical delay
- **Phase Segment 1**: 1-8 tq - Position of sample point
- **Phase Segment 2**: 2-8 tq - Compensates for phase errors
- **Sample Point**: Between Phase Segment 1 and 2

**Sample point**: Must be at same position for all nodes (typically 60-85% of bit time)

### CAN FD Bit Timing
- **Arbitration Phase**: Uses nominal bit rate (same as CAN 2.0)
- **Data Phase**: Uses faster bit rate (configurable)
- **Bit Rate Switch (BRS)**: Enabled in frame to switch rates

**Typical bit rates**:
- **1Mbps**: 100ns bit time, high-speed automotive
- **500kbps**: 200ns bit time, common industrial
- **250kbps**: 400ns bit time, long distance
- **125kbps**: 800ns bit time, very long distance
- **100kbps**: 1000ns bit time, maximum distance
- **50kbps**: 2000ns bit time, very long distance
- **20kbps**: 5000ns bit time, extreme distance

**Bit rate vs bus length**:
- 1Mbps: ≤ 40m
- 500kbps: ≤ 100m
- 250kbps: ≤ 200m
- 125kbps: ≤ 500m
- 100kbps: ≤ 1000m
- 50kbps: ≤ 1500m

## Error Detection & Handling

### Error Types

| Error Type | Detection Mechanism | Error Flag |
|------------|---------------------|------------|
| **Bit Error** | Bit sent ≠ bit received | Error flag from detector |
| **Stuff Error** | >5 consecutive same bits | Error flag from detector |
| **CRC Error** | Calculated CRC ≠ received CRC | Error flag from detector |
| **Form Error** | Invalid fixed bit fields | Error flag from detector |
| **Acknowledgment Error** | No ACK received | Error flag from transmitter |

### Error Flags
- **Active Error Flag**: 6 dominant bits
- **Passive Error Flag**: 6 recessive bits (node in error passive state)

### Error Counters
Each node maintains two counters:
- **Transmit Error Counter (TEC)**: Increases on transmission errors
- **Receive Error Counter (REC)**: Increases on reception errors

**Error states**:
- **Error Active**: TEC/REC < 128 - Node can send active error flags
- **Error Passive**: TEC/REC ≥ 128 - Node can only send passive error flags
- **Bus Off**: TEC ≥ 256 - Node is disconnected from bus

**Recovery**:
- Node in Bus Off state monitors bus
- After detecting 128 occurrences of 11 consecutive recessive bits, it resets TEC and enters Error Passive
- After successful transmission/reception, it resets REC and enters Error Active

### Error Frame
- **Format**: Superposition of error flags from multiple nodes
- **Components**:
  - Error Flag field (6-12 bits, depending on error state)
  - Error Delimiter (8 recessive bits)
- **Pitfall**: Error frames can be corrupted by simultaneous transmissions

## Message Filtering

### Acceptance Filters
- **Purpose**: Filter which messages a node receives
- **Implementation**: Hardware filters in CAN controller
- **Types**:
  - **Single ID filter**: Match specific ID
  - **Range filter**: Match range of IDs
  - **Mask filter**: Match ID with bitmask

**Example filters**:
- Accept ID 0x100 exactly
- Accept IDs 0x100-0x1FF
- Accept IDs with bits 10-15 = 0x10

### Filter Configuration
- **Number of filters**: Varies by controller (typically 2-16)
- **Filter banks**: Each filter can be configured independently
- **FIFO assignment**: Messages matching filter go to specific FIFO

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Missing termination | Communication errors, reflections | Add 120Ω resistors at both ends of bus |
| Incorrect termination value | Signal reflection, errors | Use exactly 120Ω termination |
| Bus length too long | Signal degradation, timing errors | Reduce bus length or use lower bit rate |
| Bit rate mismatch | No communication | Verify bit rate configuration on all nodes |
| ID conflict | Message collision, arbitration failure | Use unique IDs, verify with bus analyzer |
| No acknowledgment | Transmission fails | Check ACK slot, verify other nodes are present |
| Error passive node | Degraded error detection | Investigate node errors, check error counters |
| Bus off node | Node disconnected | Reset node, investigate cause of bus off |
| Wrong sample point | Communication errors | Verify sample point configuration on all nodes |
| Stuff bit violation | Spurious error frames | Check data patterns, use CAN FD for high data rates |
| Ground loop | Noise, erratic behavior | Use common ground reference, isolate power |
| EMI/RFI | Data corruption | Use shielded twisted pair, proper grounding |

## Best Practices

- **Always use termination**: 120Ω at each end of bus
- **Match bit rate**: All nodes must use same nominal bit rate
- **Match sample point**: Sample point must be at same position for all nodes
- **Use unique IDs**: Each message type should have unique ID
- **Prioritize important messages**: Lower ID = higher priority
- **Limit bus length**: Stay within recommended length for bit rate
- **Use shielded twisted pair**: For noise immunity
- **Verify grounding**: All nodes should share common ground reference
- **Monitor error counters**: Detect bus issues early
- **Implement error recovery**: Handle bus off and error passive states
- **Test with bus analyzer**: Verify bus signals before full deployment
- **Use CAN FD for high throughput**: When payload > 8 bytes or higher speed needed
- **Group messages by priority**: Critical messages get lower IDs

## Debugging Tips

- **Bus analyzer**: Capture CAN frames for analysis
- **Check termination**: Measure resistance between CAN_H and CAN_L (should be ~60Ω)
- **Verify bit rate**: Use oscilloscope to measure actual bit rate
- **Check signal levels**: CAN_H and CAN_L should be ~2.5V when recessive, differential ~2V when dominant
- **Monitor error counters**: Use CAN controller registers to check TEC/REC
- **Test with known-good node**: Verify bus works with simple echo test
- **Check message IDs**: Verify IDs are unique and within expected range
- **Verify sample point**: Use oscilloscope to check sample point position
- **Test with one node**: Verify basic communication before adding more nodes

## Standing Rules

- **120Ω termination is mandatory** — at both ends; a bus without
  proper termination is a bus that does not work at speed.
- **Lower ID wins arbitration** — the priority is the ID; design the
  ID space so critical messages have the lowest IDs.
- **Every message needs an ACK** — if no node ACKs, the transmitter
  knows something is wrong; investigate why.
- **Error counters are the health monitor** — a TEC that climbs to
  256 disconnects the node; that is protection, not punishment.
- **CAN FD is backward compatible until it switches** — arbitration
  uses the same rules as CAN 2.0; only the data phase can be faster.
- **The physical layer matters** — differential signaling, proper
  grounding, and twisted pair are not optional for reliable operation.
- **Stuff bits are automatic** — every five consecutive same bits
  gets a stuff bit of the opposite; the protocol handles it, but
  the designer must account for the overhead.
