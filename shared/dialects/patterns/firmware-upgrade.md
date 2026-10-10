# Firmware Upgrade pattern contract

Attaches by the shape of the work — MCU firmware updates, OTA (Over-The-Air)
upgrades, bootloader integration — alongside the language contract (c, cpp),
the platform contract (specific MCU families), and optionally the RTOS
contract for systems running an operating system. Firmware upgrade is
**platform-specific in mechanism, but universal in pattern** — the challenges
and solutions repeat across vendors, even as the details differ.

## The discipline

Firmware upgrades on resource-constrained devices are **not just deployment**
— they are **safety-critical operations** that must be atomic, verifiable,
and recoverable. A failed upgrade can brick a device in the field, and a
compromised upgrade can open security vulnerabilities that persist beyond
the upgrade itself.

- **Atomicity is mandatory**: The device must either complete the upgrade
  or remain in a known-good state; partial upgrades are not acceptable.
- **Recovery is designed in**: Rollback, bootloader fallback, and factory
  restore must be considered from the start, not added as an afterthought.
- **Verification is mandatory**: Every byte must be verified before
  activation — CRC, hash, or cryptographic signature.
- **Security is non-negotiable**: Upgrades must be authenticated and
  authorized; unauthorized firmware must not be installable.
- **Power-loss resilience**: The system must survive power loss at any
  point during the upgrade process and recover to a safe state.
- **Minimal downtime**: For many systems, availability is critical;
  upgrades should minimize the window during which the device is
  non-functional.
- **Version compatibility**: New firmware must be compatible with
  persistent data structures and external interfaces.

## Upgrade strategies

### 1. Dual-Bank / A-B Partition Scheme

**Pattern**: Maintain two identical firmware banks (A and B). The active
firmware runs from one bank while the upgrade writes to the other. On
successful verification, the bootloader switches to the new bank.

**Mechanism**:
- Bootloader checks a flag or partition table to determine active bank
- Active bank: read-only during operation, contains running firmware
- Inactive bank: writable, receives new firmware image
- Verification: CRC/hash check on inactive bank before switch
- Switch: Bootloader updates active bank pointer and resets

**Pros**:
- Atomic: Switch happens in a single operation (pointer update)
- Fast rollback: Switch back to previous bank if new firmware fails
- No external storage needed
- Power-loss safe: Each bank is independently verifiable

**Cons**:
- Requires 2x flash space for firmware
- Bootloader must support bank switching
- More complex bootloader logic

**Vendor examples**:
- STM32: Dual-bank flash (STM32F4, STM32F7, STM32H7)
- ESP32: OTA partitions with partition table
- Nordic nRF5: Multiple slot support in bootloader
- NXP: Flexible memory partitioning

**Platform-specific considerations**:
- STM32: Bank swapping via option bytes, requires mass erase for switch
- ESP32: Partition table defines OTA slots, uses MD5 for verification
- Nordic: SoftDevice handles bank switching for some Series
- Microchip PIC32: Bootloader must implement dual-bank logic

---

### 2. Single-Bank with External Storage

**Pattern**: Store new firmware in external storage (SPI flash, SD card,
EEPROM), then copy and verify before switching. Used when internal
flash is too small for dual-bank.

**Mechanism**:
- Download firmware to external storage
- Bootloader copies from external to internal flash
- Verify copy before activation
- Optional: Keep external copy for recovery

**Pros**:
- Works with limited internal flash
- External storage can be larger and cheaper
- Can support multiple firmware versions

**Cons**:
- Slower upgrade process (copy operation)
- Requires external storage interface
- More failure points (external storage, copy operation)
- Higher power consumption during copy

**Platform-specific considerations**:
- STM32: Use external SPI flash or SD card
- ESP32: Can use external SPIRAM or SD card
- PIC: External EEPROM or flash via I2C/SPI
- Arduino: SD card library for storage

---

### 3. Delta Updates

**Pattern**: Transmit only the differences between current and new firmware
to reduce transmission size and upgrade time.

**Mechanism**:
- Generate delta between current and target firmware
- Transmit delta (typically 10-30% of full size)
- Apply delta to current firmware in place
- Verify result

**Pros**:
- Significantly smaller transmission size
- Faster upgrades over slow connections
- Lower power consumption (less data to transmit)

**Cons**:
- Complex delta generation and application
- Requires knowledge of current firmware version
- Delta application can be slow on resource-constrained devices
- Risk of corruption if delta application fails mid-way

**Vendor examples**:
- ESP32: ESP-IDF supports delta updates via `spiffs_delta`
- Nordic: nRF5 SDK includes delta update support
- Custom implementations using bsdiff or similar algorithms

---

### 4. Direct Programming (Debug Interface)

**Pattern**: Use debug interface (SWD, JTAG, UART bootloader) to program
firmware directly. Typically used for development or manufacturing, not
field upgrades.

**Mechanism**:
- Connect via debug interface
- Erase and program entire flash
- Verify firmware
- Reset device

**Pros**:
- Full control over programming process
- Can recover from any state (including bricked)
- Fastest programming method
- Supports all memory regions

**Cons**:
- Requires physical access
- Not suitable for field upgrades
- Debug interface may be disabled in production
- Security risk if debug interface remains accessible

**Vendor examples**:
- All platforms: SWD (ARM), JTAG (universal)
- STM32: STM32CubeProgrammer via UART, SWD, JTAG
- ESP32: esptool via UART
- Arduino: Serial bootloader (STM32, AVR, etc.)

---

## Bootloader requirements

### Minimal bootloader capabilities

1. **Firmware verification**: CRC32, SHA-256, or cryptographic signature
2. **Upgrade state management**: Track upgrade progress and status
3. **Watchdog feeding**: Prevent watchdog timeout during long upgrade operations
4. **Rollback mechanism**: Restore previous firmware if upgrade fails
5. **Communication interface**: UART, USB, SPI, I2C, or wireless for receiving firmware
6. **Memory protection**: Prevent application from overwriting bootloader
7. **Error recovery**: Handle verification failures, power loss, corruption

### Advanced bootloader features

1. **Secure boot**: Cryptographic verification of firmware signature
2. **A/B partition support**: Dual-bank switching
3. **Encrypted firmware**: Decrypt firmware before installation
4. **Compression support**: Decompress firmware on-the-fly
5. **Multi-stage boot**: Bootloader → recovery bootloader → application
6. **Firmware metadata**: Version, timestamp, compatibility info
7. **Remote attestation**: Prove current firmware state to remote server

---

## Platform-specific implementation patterns

### STM32 (STMicroelectronics)

**Flash organization**:
- Single-bank or dual-bank depending on model
- Option bytes control read/write protection
- Bootloader typically in System memory (ROM) or first flash sector

**Upgrade methods**:
- **Internal bootloader**: Factory bootloader via UART/USB
  - Limited functionality, no dual-bank support
  - Use STM32CubeProgrammer for production
- **Custom bootloader**: User-implemented in first flash sectors
  - Full control over upgrade process
  - Can implement dual-bank, secure boot, etc.
- **Dual-bank**: Available on STM32F4, F7, H7, L4+ models
  - Bank 1 and Bank 2, each 256KB-1MB depending on model
  - Switch via option bytes (requires mass erase)

**Flash operations**:
- HAL_FLASH_Program() for word/half-word programming
- FLASH_ErasePage() for sector erasure
- Must disable interrupts during flash operations
- Watchdog must be fed during long operations

**Bootloader location**:
- Typically at 0x08000000 (start of Flash)
- Must be < 32KB to fit in first sector (STM32F4)
- Can use separate bank for bootloader (STM32H7)

**Verification**:
- CRC32 built into hardware (CRC peripheral)
- Can use STM32 Cube HAL CRC functions

**Example upgrade process**:
1. Application receives firmware via UART/SPI
2. Writes to inactive bank (or external storage)
3. Verifies CRC
4. Sets option byte to switch active bank
5. Resets device

---

### ESP32 (Espressif)

**Flash organization**:
- External SPI flash (typically 4MB-16MB)
- Partition table defines layout
- OTA partitions for A/B updates
- NVS partition for non-volatile storage

**Upgrade methods**:
- **OTA via WiFi/BLE**: Most common for IoT devices
  - Uses HTTP, MQTT, or custom protocol
  - Firmware encrypted and signed
- **Serial (UART)**: Via esptool or custom protocol
- **External storage**: SPI flash partition management

**Partition table**:
```
# Example partition table for OTA
nvs,      data, nvs,    , 0x9000,  0x5000
phy_init, data, phy,    , 0xe000,  0x1000
factory,  app,  factory, , 0x10000, 1M
storage,  data, 0x99,   , 0x110000, 1M
ota_0,    app,  ota_0,  , 0x210000, 1M
ota_1,    app,  ota_1,  , 0x310000, 1M
```

**Bootloader**:
- First-stage bootloader in ROM (immutable)
- Second-stage bootloader in partition (customizable)
- Can implement custom OTA logic in second-stage

**ESP-IDF OTA support**:
- Built-in OTA partition switching
- MD5 verification of firmware
- Rollback on boot failure (configurable)
- Status tracking in NVS

**Secure boot**:
- RSA or ECDSA signature verification
- Bootloader verifies firmware before boot
- Custom keys via efuse

**Example upgrade process**:
1. Device receives OTA update via WiFi
2. Writes to inactive OTA partition
3. Sets ota_seq in NVS
4. Verifies MD5
5. Resets device
6. Second-stage bootloader checks ota_seq and boots from OTA partition
7. If boot fails 3 times, rolls back to previous partition

---

### Nordic nRF5 Series

**Flash organization**:
- Internal flash (typically 256KB-1MB)
- SoftDevice (Bluetooth stack) occupies upper region
- Application and bootloader in lower region
- External flash optional via QSPI

**Upgrade methods**:
- **DFU (Device Firmware Update)**: Nordic's proprietary protocol
  - Over BLE or UART
  - Secure DFU with signed firmware
  - Buttonless DFU for seamless upgrades
- **Bootloader**: Custom bootloader with DFU support
- **External storage**: QSPI flash for larger firmware

**DFU protocol**:
- Transfer protocol: Reliable data transfer
- Control protocol: Commands for start, stop, verify
- Packet-based with CRC
- Can be encrypted

**Memory layout**:
- Bootloader: First 16KB-32KB
- SoftDevice: Upper region (fixed for each SoftDevice version)
- Application: Middle region
- Storage: NVMC for flash operations

**Secure DFU**:
- Firmware signed with ECDSA or Ed25519
- Bootloader verifies signature before installation
- Can use Nordic's nRF5 SDK DFU library

**Example upgrade process**:
1. Host sends DFU start command
2. Device enters DFU mode
3. Host sends firmware in packets
4. Bootloader writes to flash
5. Bootloader verifies signature
6. Bootloader updates SoftDevice if needed
7. Device resets to new firmware

---

### NXP (Kinetis, i.MX RT, LPC)

**Flash organization**:
- Internal flash (varies by model: 128KB-4MB)
- Flexible memory partitioning
- Some models support dual-bank

**Upgrade methods**:
- **MCUboot**: Open-source bootloader from NXP
  - Supports A/B updates
  - Secure boot
  - Multiple image slots
- **Custom bootloader**: User-implemented
- **External storage**: SPI flash, SD card

**MCUboot features**:
- Image signing and verification
- Swap status for A/B updates
- Boot status tracking
- Upgrade state machine
- Watchdog integration

**Flash operations**:
- FlexRAM for EEPROM emulation
- Flash configuration field (FCF) for protection
- Can use NXP's flash driver libraries

**Example upgrade process (MCUboot)**:
1. Application receives firmware via UART/SPI/WiFi
2. Writes to secondary slot
3. Sets image version and swap state
4. Verifies signature
5. Resets device
6. MCUboot checks swap state and boots from new slot
7. If boot fails, rolls back to primary slot

---

### Microchip (PIC32, SAM, AVR)

**Flash organization**:
- Internal flash (varies: 8KB-2MB)
- Bootloader section (typically first 8KB-16KB)
- Application section

**Upgrade methods**:
- **PIC32**: Custom bootloader via UART/USB
  - Can use Microchip's Harmony bootloader
  - Supports external storage
- **SAM**: SAM-BA bootloader via USB
  - Factory bootloader
  - Custom bootloader for more features
- **AVR**: Optiboot or custom bootloader via UART

**AVR specific**:
- Bootloader in upper memory (via BOOTRST fuse)
- Typically 512B-4KB size
- Uses page erase (128-256 bytes)
- Slow write operations

**PIC32 specific**:
- Fast flash programming via NVM module
- Can program while executing from flash
- Cache management required

**SAM specific**:
- SAM-BA bootloader via USB native port
- Can be disabled via fuses
- Supports external memory

---

### Renesas (RX, RL78, RH850)

**Flash organization**:
- Internal flash (varies by family)
- RX: Single-bank or dual-bank options
- RL78: Bank switching support
- RH850: Automotive-grade with ECC

**Upgrade methods**:
- **Renesas Flash Programmer**: Via debug interface
- **Custom bootloader**: UART or CAN-based
- **Dual-bank**: Available on some models

**RX specific**:
- Flash programming via FACI (Flash Access Control Interface)
- Can be programmed from user code
- Bank switching via option bytes

**RL78 specific**:
- Bank switching for code and data
- Can switch banks at runtime
- Requires careful timing management

---

### Infineon (XMC, AURIX, PSoC)

**Flash organization**:
- XMC: Internal flash with sector protection
- AURIX: Large flash (up to 16MB) with ECC
- PSoC: Multiple flash regions

**Upgrade methods**:
- **XMC**: Custom bootloader via UART/SPI
  - Can use Infineon's XMC Lib for flash operations
- **AURIX**: Multi-bank with ECC
  - Automotive-grade requirements
  - Secure boot support
  - Can use DAS (Debug Access Server)
- **PSoC**: Bootloader via I2C/SPI/UART
  - CyBootloader component

**AURIX specific**:
- Memory Protection Unit (MPU) for security
- ECC (Error Correction Code) for reliability
- HSM (Hardware Security Module) for secure boot
- Supports multiple CAN interfaces for updates

---

## OTA (Over-The-Air) patterns

### 1. Pull-based OTA

**Pattern**: Device periodically checks for updates and downloads if available.

**Mechanism**:
- Device connects to server via WiFi/BLE/Cellular
- Sends current version and device info
- Server responds with update availability
- Device downloads and installs firmware

**Pros**:
- Device controls upgrade timing
- Can check for updates when convenient (power, network available)
- Scales well to many devices

**Cons**:
- Requires device to initiate
- May miss critical security updates
- Needs reliable connectivity

**Example**:
- ESP32 IoT devices checking update server
- Nordic nRF5 devices via BLE

---

### 2. Push-based OTA

**Pattern**: Server initiates upgrade and pushes firmware to device.

**Mechanism**:
- Server maintains device registry
- Server pushes update notification to specific devices
- Device acknowledges and downloads firmware
- Server tracks upgrade progress

**Pros**:
- Immediate deployment of critical updates
- Server controls upgrade rollout
- Can target specific devices

**Cons**:
- Requires device to be online and reachable
- More complex server infrastructure
- May interrupt device operation

**Example**:
- Enterprise devices with centralized management
- Automotive ECUs via OBD-II

---

### 3. Hybrid OTA

**Pattern**: Combine pull and push approaches.

**Mechanism**:
- Server pushes notification of critical updates
- Device periodically checks for non-critical updates
- Device can defer non-critical updates

**Pros**:
- Best of both worlds
- Critical updates deployed immediately
- Non-critical updates when convenient

**Cons**:
- More complex implementation
- Requires both server and device logic

---

## Security patterns

### 1. Firmware Signing

**Pattern**: Cryptographically sign firmware to ensure authenticity.

**Mechanism**:
- Sign firmware with private key (RSA, ECDSA, Ed25519)
- Include signature in firmware image
- Bootloader verifies signature with public key
- Public key stored in secure location (efuse, protected flash)

**Implementation**:
- Use mbed TLS, WolfSSL, or custom crypto
- Sign entire firmware or just header
- Include version, timestamp, and other metadata

**Example**:
- ESP32: Built-in secure boot with RSA/ECDSA
- Nordic: DFU with signed firmware
- STM32: Custom secure bootloader with verification

---

### 2. Encrypted Firmware

**Pattern**: Encrypt firmware to prevent reverse engineering.

**Mechanism**:
- Encrypt firmware with symmetric key (AES)
- Key encrypted with asymmetric key (RSA)
- Bootloader decrypts firmware before installation

**Pros**:
- Prevents firmware extraction
- Protects intellectual property
- Can be combined with signing

**Cons**:
- Adds complexity
- Key management challenge
- Slower upgrade process (decryption overhead)

**Example**:
- ESP32: Firmware encryption via efuse keys
- Custom implementations with AES-256

---

### 3. Secure Communication

**Pattern**: Encrypt upgrade communication channel.

**Mechanism**:
- Use TLS for OTA downloads
- Use BLE Secure Connections
- Verify server certificate
- Prevent man-in-the-middle attacks

**Implementation**:
- mbed TLS for TLS support
- Platform-specific secure protocols
- Certificate pinning for server verification

---

### 4. Anti-Rollback Protection

**Pattern**: Prevent downgrading to vulnerable firmware versions.

**Mechanism**:
- Store current firmware version in secure storage
- Include minimum version in firmware header
- Bootloader checks version before boot
- Reject firmware older than current or minimum

**Implementation**:
- Version number in firmware header
- Secure storage for current version (efuse, protected flash)
- Bootloader version check

---

### 5. Secure Bootloader

**Pattern**: Protect bootloader from modification.

**Mechanism**:
- Bootloader in read-protected flash
- Cryptographic verification of bootloader
- Hardware root of trust (if available)
- Chain of trust: ROM → bootloader → application

**Implementation**:
- Write-protect bootloader region
- Verify bootloader signature
- Use hardware security features

---

## Power-loss resilience patterns

### 1. Atomic Write Operations

**Pattern**: Ensure each write operation is atomic and recoverable.

**Mechanism**:
- Write to temporary location first
- Verify temporary copy
- Atomic switch to new location
- Clean up temporary if successful

**Example**:
- Write firmware to inactive bank
- Verify CRC
- Switch active bank pointer (atomic operation)
- Erase old bank if successful

---

### 2. Power-Loss Detection

**Pattern**: Detect and recover from power loss during upgrade.

**Mechanism**:
- Track upgrade state in non-volatile storage
- Bootloader checks state on startup
- Resume or rollback based on state

**States**:
- IDLE: No upgrade in progress
- RECEIVING: Downloading firmware
- VERIFYING: Verifying firmware
- SWITCHING: Switching to new firmware
- ROLLING_BACK: Rolling back to previous firmware
- COMPLETE: Upgrade successful
- FAILED: Upgrade failed, needs recovery

---

### 3. Watchdog Integration

**Pattern**: Prevent watchdog timeout during long upgrade operations.

**Mechanism**:
- Feed watchdog during flash operations
- Calculate worst-case time for each operation
- Feed watchdog before timeout
- Use separate watchdog for bootloader

**Implementation**:
- Independent watchdog for bootloader
- Feed watchdog in interrupt context
- Watchdog timeout longer than upgrade operation

---

## Verification patterns

### 1. CRC Verification

**Pattern**: Use CRC for fast verification.

**Mechanism**:
- Calculate CRC of firmware during build
- Include CRC in firmware header
- Bootloader calculates CRC of received firmware
- Compare with expected CRC

**Implementation**:
- CRC32 for most platforms
- Hardware-accelerated CRC where available (STM32)
- Software CRC implementation for others

**Pros**:
- Fast calculation
- Low memory overhead
- Good for detecting accidental corruption

**Cons**:
- Not secure against intentional modification
- Collisions possible (but rare for CRC32)

---

### 2. Hash Verification

**Pattern**: Use cryptographic hash for verification.

**Mechanism**:
- Calculate SHA-256 or SHA-3 of firmware
- Include hash in firmware header
- Bootloader calculates hash and compares

**Implementation**:
- Use mbed TLS or similar for hash calculation
- Software implementation for platforms without hardware support

**Pros**:
- Cryptographically secure
- Detects intentional modifications
- Widely supported

**Cons**:
- Slower than CRC
- Higher memory overhead

---

### 3. Signature Verification

**Pattern**: Cryptographically sign and verify firmware.

**Mechanism**:
- Sign firmware with private key
- Include signature in firmware image
- Bootloader verifies signature with public key

**Pros**:
- Provides authenticity and integrity
- Prevents unauthorized firmware installation
- Tamper-proof

**Cons**:
- Most complex to implement
- Requires key management
- Slower verification

---

## Data compatibility patterns

### 1. Persistent Data Migration

**Pattern**: Handle changes in persistent data structures between firmware versions.

**Mechanism**:
- Version persistent data structure
- Include migration code in firmware
- Run migration on first boot after upgrade
- Rollback data if firmware rollback

**Implementation**:
- Data version in non-volatile storage
- Migration functions for each version transition
- Backward compatibility for older firmware

---

### 2. Configuration Compatibility

**Pattern**: Ensure new firmware is compatible with existing configuration.

**Mechanism**:
- Version configuration format
- Validate configuration on boot
- Provide defaults for missing configuration
- Handle deprecated configuration gracefully

---

### 3. External Interface Stability

**Pattern**: Maintain compatibility with external systems.

**Mechanism**:
- Version communication protocols
- Support multiple protocol versions
- Deprecation warnings for old interfaces
- Graceful handling of protocol errors

---

## Rollback patterns

### 1. Automatic Rollback

**Pattern**: Automatically roll back if new firmware fails to boot.

**Mechanism**:
- Bootloader counts boot attempts
- If new firmware fails to boot N times, roll back
- Track rollback count in non-volatile storage

**Implementation**:
- Boot counter in NVS or protected flash
- Bootloader checks counter on startup
- Reset counter on successful boot

---

### 2. Manual Rollback

**Pattern**: Allow user-initiated rollback.

**Mechanism**:
- Special key combination on boot
- JButton press during boot
- Command via debug interface
- Web interface for networked devices

**Pros**:
- User control over rollback
- Can recover from unexpected issues

**Cons**:
- Requires user intervention
- May not be available on headless devices

---

### 3. Recovery Mode

**Pattern**: Enter recovery mode if upgrade fails.

**Mechanism**:
- Bootloader detects upgrade failure
- Enters recovery mode
- Provides interface for re-programming
- May blink LED or provide other indication

**Implementation**:
- Recovery mode in bootloader
- Limited functionality (only programming)
- Special communication protocol for recovery

---

## Testing patterns

### 1. Factory Test

**Pattern**: Test upgrade process in manufacturing.

**Mechanism**:
- Program initial firmware
- Simulate upgrade process
- Verify upgrade succeeds
- Verify rollback works
- Verify recovery mode

---

### 2. Field Test

**Pattern**: Test upgrade in real-world conditions.

**Mechanism**:
- Test with various network conditions
- Test with power interruptions
- Test with storage limitations
- Test with multiple devices simultaneously

---

### 3. Regression Test

**Pattern**: Ensure upgrades don't break existing functionality.

**Mechanism**:
- Test all features after upgrade
- Test upgrade from multiple previous versions
- Test upgrade sequence (v1 → v2 → v3)
- Test interrupted upgrades

---

## Pitfalls (shared across platforms)

### ❌ No rollback mechanism
- **Finding**: Firmware upgrade fails, device is bricked
- **Fix**: Always implement rollback or recovery mechanism

### ❌ Unverified firmware
- **Finding**: Corrupted firmware installed, device behaves unpredictably
- **Fix**: Always verify firmware before activation (CRC, hash, or signature)

### ❌ No power-loss protection
- **Finding**: Device loses power during upgrade, left in undefined state
- **Fix**: Design upgrade to be power-loss resilient at every step

### ❌ Insufficient flash space
- **Finding**: New firmware doesn't fit in available flash
- **Fix**: Check available space before starting upgrade; use delta updates or external storage

### ❌ Incompatible data structures
- **Finding**: New firmware fails because persistent data format changed
- **Fix**: Implement data migration; version persistent data structures

### ❌ No version tracking
- **Finding**: Can't determine current firmware version for upgrade decisions
- **Fix**: Store version in non-volatile storage; include in bootloader

### ❌ Slow upgrade process
- **Finding**: Upgrade takes too long, device unavailable for extended period
- **Fix**: Optimize transmission (compression, delta); use faster communication; background downloads

### ❌ Security vulnerabilities in bootloader
- **Finding**: Bootloader has buffer overflow or other vulnerability
- **Fix**: Harden bootloader; minimize attack surface; use secure protocols

### ❌ No authentication
- **Finding**: Anyone can upload firmware to device
- **Fix**: Implement authentication; sign firmware; use secure channels

### ❌ Watchdog timeout during upgrade
- **Finding**: Long upgrade operations cause watchdog reset
- **Fix**: Feed watchdog during upgrade; use longer timeout for bootloader

### ❌ Race conditions in flash operations
- **Finding**: Flash operations interrupted or corrupted
- **Fix**: Disable interrupts during flash operations; use atomic operations

### ❌ No progress tracking
- **Finding**: Can't determine upgrade status or progress
- **Fix**: Track upgrade state; provide status reporting; log progress

---

## Checklist for firmware upgrade implementation

- [ ] Define upgrade strategy (dual-bank, external storage, delta, etc.)
- [ ] Design bootloader with upgrade capabilities
- [ ] Implement firmware verification (CRC/hash/signature)
- [ ] Implement rollback mechanism
- [ ] Handle power-loss scenarios
- [ ] Feed watchdog during long operations
- [ ] Secure communication channel for OTA
- [ ] Firmware signing and encryption (if needed)
- [ ] Version tracking and compatibility checks
- [ ] Data migration for persistent storage
- [ ] Test upgrade from all supported previous versions
- [ ] Test interrupted upgrades
- [ ] Test power-loss during upgrade
- [ ] Test rollback and recovery
- [ ] Document upgrade procedure
- [ ] Define update notification mechanism
- [ ] Implement update server (for OTA)

---

## Vendor-specific tooling

| Vendor | Tool | Description |
|--------|------|-------------|
| STM32 | STM32CubeProgrammer | CLI/GUI for programming STM32 devices |
| STM32 | STM32CubeIDE | IDE with integrated programming |
| ESP32 | esptool | Python-based tool for ESP32 flashing |
| ESP32 | ESP-IDF | Framework with OTA support |
| Nordic | nRF5 SDK | Includes DFU and bootloader support |
| Nordic | nrfutil | Command-line tool for DFU packages |
| NXP | MCUboot | Open-source bootloader |
| NXP | Kinetis Flash Tool | Programming tool for Kinetis MCUs |
| Microchip | MPLAB X | IDE with programming support |
| Microchip | Harmony | Framework with bootloader support |
| Infineon | DAS | Debug Access Server for Infineon MCUs |
| Renesas | Renesas Flash Programmer | Programming tool for Renesas MCUs |

---

## Standards and protocols

- **MCUmgr**: Open-source management protocol for embedded devices
- **MCUboot**: Open-source bootloader for microcontrollers
- **DFU (Device Firmware Update)**: USB DFU protocol
- **SWD (Serial Wire Debug)**: ARM debugging protocol
- **JTAG**: IEEE 1149.1 test access port
- **UART**: Serial bootloader protocol (vendor-specific)
- **I2C/SPI**: For external storage programming
- **BLE**: For wireless firmware updates (Nordic, ESP32)
- **WiFi**: For OTA updates (ESP32, etc.)
