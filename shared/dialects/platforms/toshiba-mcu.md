---
type: platform
family: mcu
region: japan
manufacturer: Toshiba
---

# Toshiba Microcontroller Platform

**Toshiba MCU families**: Comprehensive portfolio of microcontrollers from
the Japanese semiconductor manufacturer, a global leader in industrial, automotive,
and consumer applications. This contract defines the architecture families,
development ecosystems, peripheral modules, toolchain support, and best
practices for Toshiba-based embedded development.

## Overview

Toshiba Corporation is a Japanese multinational conglomerate headquartered
in Tokyo, Japan. Founded in 1875, Toshiba has been a major player in the
semiconductor industry for decades, with a strong focus on industrial and
automotive microcontrollers, as well as consumer electronics.

Toshiba MCUs are widely used in:
- Industrial automation (PLCs, motor control, inverters)
- Automotive applications (body control, powertrain, ADAS)
- Consumer electronics (appliances, AV equipment)
- IoT and connectivity
- Motor control and power management

## Architecture Families

### TXZ Family (ARM Cortex-R)

**TXZ4 Series** (Cortex-R4):
- **Core**: ARM Cortex-R4
- **Performance**: 120-200 MHz
- **Flash**: 512 KB - 4 MB
- **RAM**: 64-512 KB
- **Target**: High-performance industrial and automotive applications
- **Package**: LQFP, BGA, QFP
- **Key Features**:
  - ARM Cortex-R4 with FPU
  - Memory protection unit (MPU)
  - CAN FD, Ethernet MAC, USB, ADC (12-bit), PWM
  - Industrial temperature range (-40°C to +105°C)
  - Automotive qualified (AEC-Q100)
- **Notable**: Highest performance Toshiba MCU, ARM Cortex-R
- **Standing Rules**: Use for real-time applications requiring high performance

**TXZ4A Series** (Cortex-R4 for Automotive):
- **Core**: ARM Cortex-R4 with FPU
- **Performance**: 160-200 MHz
- **Flash**: 1-4 MB
- **RAM**: 128-512 KB
- **Target**: Automotive powertrain and chassis applications
- **Package**: LQFP, BGA
- **Key Features**:
  - CAN FD, Ethernet AVB, LIN, FlexRay
  - ADC (12-bit, up to 2 MSPS)
  - PWM with dead-time generation
  - Automotive temperature range (-40°C to +125°C)
  - AEC-Q100 qualified
  - ISO 26262 (ASIL-D) support
- **Notable**: Automotive-focused, real-time performance

**TXZ5 Series** (Cortex-R5):
- **Core**: ARM Cortex-R5 with FPU
- **Performance**: 200-400 MHz
- **Flash**: 1-8 MB
- **RAM**: 256 KB - 2 MB
- **Target**: Ultimate performance for industrial and automotive
- **Package**: BGA, TFBGA
- **Key Features**:
  - ARM Cortex-R5 with FPU and NEON
  - TrustZone support
  - CAN FD, Ethernet AVB/TSN, USB 3.0
  - ADC (12/16-bit, up to 4 MSPS)
  - Advanced PWM
  - Memory protection
- **Notable**: Highest performance Toshiba MCU, Cortex-R5 architecture

### TMPM Family (ARM Cortex-M)

**TMPM0 Series** (Cortex-M0):
- **Core**: ARM Cortex-M0
- **Performance**: 20-50 MHz
- **Flash**: 8-128 KB
- **RAM**: 4-16 KB
- **Target**: Cost-sensitive, low-power applications
- **Package**: LQFP, QFN, TSSOP
- **Key Features**:
  - Basic peripherals: UART, SPI, I2C, ADC (10/12-bit), timers, PWM
  - Low-power modes
  - Industrial temperature range (-40°C to +85°C or +105°C)
- **Notable**: Entry-level Cortex-M from Toshiba

**TMPM3 Series** (Cortex-M3):
- **Core**: ARM Cortex-M3
- **Performance**: 50-100 MHz
- **Flash**: 64-512 KB
- **RAM**: 16-64 KB
- **Target**: General-purpose industrial applications
- **Package**: LQFP, QFN, BGA
- **Key Features**:
  - CAN, USB, Ethernet MAC (on some)
  - ADC (12-bit, up to 1 MSPS)
  - DAC (12-bit on some)
  - Advanced PWM
  - Industrial temperature range
- **Notable**: Most popular Toshiba Cortex-M family

**TMPM4 Series** (Cortex-M4 with FPU):
- **Core**: ARM Cortex-M4 with FPU
- **Performance**: 80-180 MHz
- **Flash**: 256 KB - 2 MB
- **RAM**: 64-256 KB
- **Target**: High-performance applications with FPU
- **Package**: LQFP, BGA, QFN
- **Key Features**:
  - Ethernet MAC, CAN FD, USB OTG
  - ADC (12-bit, up to 2.4 MSPS)
  - DAC (12-bit)
  - Advanced PWM
  - TrustZone (on some variants)
  - Industrial temperature range
- **Notable**: FPU support, high performance

**TMPM4G Series** (Cortex-M4 with Graphics):
- **Core**: ARM Cortex-M4 with FPU
- **Performance**: 100-150 MHz
- **Flash**: 512 KB - 1 MB
- **RAM**: 128-256 KB
- **Target**: Graphics and display applications
- **Package**: LQFP, BGA
- **Key Features**:
  - LCD-TFT controller
  - 2D graphics accelerator
  - Touch controller interface
  - Ethernet MAC, USB OTG
  - ADC (12-bit), DAC (12-bit)
- **Notable**: Graphics focus, display applications

**TMPM4F Series** (Cortex-M4 for Automotive):
- **Core**: ARM Cortex-M4 with FPU
- **Performance**: 100-150 MHz
- **Flash**: 512 KB - 2 MB
- **RAM**: 128-256 KB
- **Target**: Automotive body and comfort applications
- **Package**: LQFP, QFN
- **Key Features**:
  - CAN FD, LIN
  - ADC (12-bit)
  - Advanced PWM
  - Automotive qualified (AEC-Q100)
- **Notable**: Automotive-focused Cortex-M4

**TMPM5 Series** (Cortex-M7):
- **Core**: ARM Cortex-M7 with FPU
- **Performance**: 200-300 MHz
- **Flash**: 1-4 MB
- **RAM**: 256 KB - 1 MB
- **Target**: Highest-performance Cortex-M applications
- **Package**: BGA, LQFP
- **Key Features**:
  - Cache (I-cache, D-cache)
  - Ethernet MAC, CAN FD, USB OTG HS
  - ADC (12/16-bit, up to 4 MSPS)
  - Advanced PWM
  - TrustZone
- **Notable**: Cortex-M7 architecture, highest performance

### TLX Family (Toshiba Original Cores)

**TLX9 Series**:
- **Core**: Toshiba TLX9 (proprietary 32-bit)
- **Performance**: 80-160 MHz
- **Flash**: 256 KB - 2 MB
- **RAM**: 32-256 KB
- **Target**: Industrial automation, motor control
- **Package**: LQFP, QFP, BGA
- **Key Features**:
  - Proprietary 32-bit architecture
  - Advanced PWM for motor control
  - ADC (12-bit, up to 1 MSPS)
  - CAN, USB, UART, SPI, I2C
  - Industrial temperature range
- **Notable**: Toshiba's proprietary architecture, strong in motor control

**TLX4 Series**:
- **Core**: Toshiba TLX4 (proprietary 16-bit/32-bit)
- **Performance**: 40-80 MHz
- **Flash**: 128-512 KB
- **RAM**: 16-64 KB
- **Target**: Cost-sensitive industrial applications
- **Package**: LQFP, QFP
- **Key Features**:
  - Proprietary architecture
  - Basic peripherals: UART, SPI, I2C, ADC (10-bit), PWM
  - Industrial temperature range
- **Notable**: Cost-optimized Toshiba MCU

### M32C Family (Legacy 32-bit)

**M32C/80 Series**:
- **Core**: Toshiba M32C (proprietary 32-bit)
- **Performance**: 10-40 MHz
- **Flash**: 64-256 KB
- **RAM**: 8-32 KB
- **Target**: Legacy applications, 16-bit migration
- **Package**: LQFP, QFP
- **Key Features**:
  - Proprietary 32-bit architecture
  - CAN, UART, SPI, I2C, ADC (10-bit)
  - Industrial temperature range
- **Notable**: Legacy architecture, still supported
- **Status**: Mature, not recommended for new designs

### 8-bit/16-bit Families

**TMP86 Series** (8-bit):
- **Core**: Toshiba TLCS-870 (proprietary 8-bit)
- **Performance**: 5-20 MHz
- **Flash**: 4-64 KB
- **RAM**: 128-2048 bytes
- **Target**: Cost-sensitive, low-complexity applications
- **Package**: DIP, SOP, QFP
- **Key Features**:
  - Basic peripherals: UART, timers, ADC (8-bit), PWM
  - Low cost
  - Industrial temperature range
- **Notable**: Entry-level Toshiba MCU

**TMP87 Series** (8-bit):
- **Core**: Toshiba TLCS-870 (proprietary 8-bit)
- **Performance**: 10-20 MHz
- **Flash**: 8-64 KB
- **RAM**: 256-2048 bytes
- **Target**: General-purpose 8-bit applications
- **Package**: DIP, SOP, QFP
- **Key Features**:
  - Enhanced peripherals: UART, SPI, I2C, ADC (10-bit), PWM
  - Industrial temperature range
- **Notable**: Most popular Toshiba 8-bit family

**TMP90 Series** (16-bit):
- **Core**: Toshiba TLCS-900 (proprietary 16-bit)
- **Performance**: 10-40 MHz
- **Flash**: 32-256 KB
- **RAM**: 2-16 KB
- **Target**: 16-bit applications, 8-bit migration
- **Package**: LQFP, QFP
- **Key Features**:
  - Enhanced peripherals: CAN, USB, UART, SPI, I2C, ADC (10/12-bit)
  - Industrial temperature range
- **Notable**: 16-bit workhorse, still popular in industrial

## Development Ecosystem

### Official IDEs

**CS+ for TX**:
- **Description**: Toshiba's IDE for TX family
- **Features**:
  - Support for TXZ and TLX families
  - Graphical configuration tools
  - Debugging with Toshiba probes
  - Compiler integration
- **Platform**: Windows
- **Pros**: Official Toshiba tool, comprehensive for TX families
- **Cons**: Windows only, proprietary

**CS+ for M32C/TMP**:
- **Description**: Toshiba's IDE for M32C and TMP families
- **Features**:
  - Support for M32C, TMPM, TLX families
  - Configuration tools
  - Debugging support
- **Platform**: Windows
- **Pros**: Official Toshiba tool, comprehensive
- **Cons**: Windows only

**e2 studio with Toshiba Plugin**:
- **Description**: Eclipse-based IDE with Toshiba support
- **Features**:
  - Cross-platform support
  - Toshiba device support
  - Configuration tools
  - Debugging support
- **Platform**: Windows, Linux, macOS
- **Pros**: Cross-platform, modern
- **Cons**: Requires plugin installation

**IAR Embedded Workbench**:
- **Description**: Third-party IDE with Toshiba support
- **Features**:
  - IAR C/C++ Compiler
  - Advanced optimization
  - Debugging support
- **Platform**: Windows, Linux, macOS
- **Pros**: Excellent optimization, industry standard
- **Cons**: Commercial license
- **Toshiba Support**: All Toshiba Cortex-M families

**Keil MDK**:
- **Description**: Third-party IDE with Toshiba Cortex-M support
- **Features**:
  - ARM Compiler (ARMCC)
  - µVision IDE
  - Debugging support
- **Platform**: Windows
- **Pros**: Industry standard for ARM, excellent debugger
- **Cons**: Commercial license, Windows only
- **Toshiba Support**: TMPM families (Cortex-M)

### Configuration Tools

**CS+ Configurator**:
- **Description**: Graphical configuration tool in CS+
- **Features**:
  - Pin configuration
  - Clock configuration
  - Peripheral configuration
  - Code generation
- **Pros**: Visual, intuitive, official Toshiba tool
- **Cons**: Windows only, CS+ integration required

**Toshiba Peripheral Configuration Tool**:
- **Description**: Standalone configuration tool
- **Features**:
  - Visual peripheral configuration
  - Code generation
  - Register-level configuration
- **Pros**: Standalone, flexible
- **Cons**: Less integrated than IDE tools

### Toolchains

**Toshiba C/C++ Compiler**:
- **Description**: Toshiba's official compiler
- **Features**:
  - Highly optimized for Toshiba architectures
  - C and C++ support
  - Excellent code efficiency
- **Platform**: Windows
- **Pros**: Official Toshiba tool, excellent optimization
- **Cons**: Commercial license, Windows only
- **Version**: TX Compiler v1.x, M32C Compiler v2.x

**GNU Toolchain for ARM (arm-none-eabi-gcc)**:
- **Description**: GCC compiler for Toshiba Cortex-M/R MCUs
- **Features**:
  - C and C++ compilers
  - ARM-specific optimizations
  - Newlib support
- **Pros**: Free, open-source, industry standard
- **Cons**: Less optimized than Toshiba compiler
- **Version**: arm-none-eabi-gcc 13.x (as of 2026)
- **Toshiba Support**: All Cortex-M/R families

**ARM Compiler 6 (ARMCC)**:
- **Description**: ARM's official compiler
- **Features**:
  - Highly optimized for ARM Cortex-M/R
  - C and C++ support
  - Keil MDK integration
- **Platform**: Windows
- **Pros**: Excellent optimization, industry standard
- **Cons**: Commercial license, Windows only
- **Toshiba Support**: All Cortex-M/R families

**IAR C/C++ Compiler**:
- **Description**: IAR's C/C++ compiler for ARM
- **Features**:
  - Highly optimized for ARM
  - C and C++ support
  - Excellent debugging support
- **Platform**: Windows, Linux, macOS
- **Pros**: Excellent optimization, industry standard
- **Cons**: Commercial license
- **Toshiba Support**: All Cortex-M/R families

### SDKs and Libraries

**Toshiba TMPM Software Library**:
- **Description**: Official SDK for TMPM families
- **Features**:
  - Hardware Abstraction Layer (HAL)
  - Peripheral drivers
  - Example projects
  - Middleware (USB, File System, etc.)
- **Pros**: Official Toshiba support, comprehensive
- **Cons**: Less modern than some competitors
- **Supported Families**: TMPM families (Cortex-M)

**Toshiba TXZ Software Library**:
- **Description**: Official SDK for TXZ families
- **Features**:
  - Peripheral drivers
  - Example projects
  - RTOS support (FreeRTOS, etc.)
  - AUTOSAR support (for automotive)
- **Pros**: Official Toshiba support, automotive focus
- **Cons**: Complex, automotive-specific
- **Supported Families**: TXZ families (Cortex-R)

**Toshiba TLX Software Library**:
- **Description**: Official SDK for TLX families
- **Features**:
  - Peripheral drivers
  - Example projects
  - Motor control libraries
- **Pros**: Official Toshiba support, motor control focus
- **Cons**: TLX-specific
- **Supported Families**: TLX families

**Third-Party RTOS Support**:
- **FreeRTOS**: Open-source RTOS with Toshiba ports
- **ThreadX**: Azure RTOS with Toshiba support
- **SafeRTOS**: Safety-certified RTOS for industrial/medical
- **embOS**: Segger RTOS with Toshiba support
- **VxWorks**: Wind River RTOS with Toshiba support

**Third-Party Libraries**:
- **Mbed OS**: ARM Mbed OS with Toshiba Cortex-M support
- **LwIP**: Lightweight IP TCP/IP stack
- **FatFS**: File system library
- **LittleFS**: Wear-leveling file system for Flash
- **mbed TLS**: SSL/TLS library

**AUTOSAR Support**:
- **Description**: AUTOSAR-compliant software for automotive MCUs
- **Features**:
  - AUTOSAR RTE
  - BSW modules
  - MCAL (Microcontroller Abstraction Layer)
  - Safety-certified components
- **Pros**: AUTOSAR compliant, automotive industry standard
- **Cons**: Complex, requires AUTOSAR knowledge
- **Supported Families**: TXZ4A, TXZ5 (automotive variants)

### Debugging and Programming

### Debug Probes

**Toshiba T-Engine**:
- **Description**: Toshiba's official debug probe
- **Features**:
  - Full debug capabilities
  - High-speed operation
  - Programming
  - Trace capabilities
- **Pros**: Official Toshiba tool, excellent support
- **Cons**: Expensive, Windows-focused
- **Supported Families**: All Toshiba MCUs

**Toshiba Emulator**:
- **Description**: High-end debug and trace system
- **Features**:
  - Full debug capabilities
  - Instruction trace
  - Data trace
  - High-speed operation
- **Pros**: Industry standard, excellent trace capabilities
- **Cons**: Very expensive
- **Supported Families**: All Toshiba MCUs

**SEGGER J-Link**:
- **Description**: Third-party debug probe
- **Features**:
  - High-speed debugging
  - Unlimited Flash breakpoints
  - RTT (Real-Time Transfer)
  - Programming
- **Pros**: Excellent performance, cross-platform, wide support
- **Cons**: Expensive (commercial)
- **Toshiba Support**: All Toshiba Cortex-M/R families

**SEGGER J-Trace**:
- **Description**: Debug probe with trace capability
- **Features**:
  - High-speed debugging
  - Instruction trace
  - Limited data trace
  - Programming
- **Pros**: Trace capability, excellent performance
- **Cons**: Very expensive
- **Toshiba Support**: Cortex-M/R with trace support

**Lauterbach Trace32**:
- **Description**: Professional debug and trace system
- **Features**:
  - Instruction trace
  - Data trace
  - High-speed debugging
  - Multi-core support
- **Pros**: Industry standard for professional development, excellent trace capabilities
- **Cons**: Very expensive, complex
- **Toshiba Support**: All Toshiba MCUs

**OpenOCD**:
- **Description**: Open-source on-chip debugging
- **Features**:
  - GDB server for debugging
  - Flash programming
  - Support for multiple probes (J-Link, etc.)
- **Platform**: Windows, Linux, macOS
- **Pros**: Free, open-source, flexible
- **Cons**: Complex setup, requires configuration
- **Toshiba Support**: Cortex-M/R families (with proper configuration)

### Programming Tools

**Toshiba Flash Programmer**:
- **Description**: Official Toshiba programming tool
- **Features**:
  - Programming via Toshiba probes
  - Mass erase, sector erase, program, verify
  - Option byte configuration
  - Multi-device programming
- **Platform**: Windows
- **Pros**: Official Toshiba tool, comprehensive features
- **Cons**: Windows only
- **Supported Families**: All Toshiba MCUs

**Toshiba T-Engine Programmer**:
- **Description**: Programming tool for T-Engine probes
- **Features**:
  - Fast programming
  - Batch programming
  - Production support
- **Platform**: Windows
- **Pros**: Fast, reliable
- **Cons**: Windows only, T-Engine specific
- **Supported Families**: All Toshiba MCUs

**J-Flash**:
- **Description**: SEGGER programming tool
- **Features**:
  - Programming via J-Link
  - Batch programming
  - Production programming
- **Platform**: Windows
- **Pros**: Fast, reliable, cross-platform
- **Cons**: Commercial license
- **Toshiba Support**: All Toshiba Cortex-M/R families

**OpenOCD**:
- **Description**: Open-source programming tool
- **Features**:
  - Programming via OpenOCD
  - Support for multiple probes
  - Scriptable
- **Platform**: Windows, Linux, macOS
- **Pros**: Free, open-source, flexible
- **Cons**: Complex setup
- **Toshiba Support**: Cortex-M/R families (with proper configuration)

**Bootloader Support**:
- **Description**: Toshiba bootloader
- **Features**:
  - UART bootloader
  - USB bootloader (on some families)
  - CAN bootloader (on some families)
- **Pros**: No debug probe required for updates
- **Cons**: Slower than debug probe programming
- **Supported Families**: Most Toshiba Cortex-M families

## Peripheral Modules

### Core Peripherals (Common across families)

**Clock System**:
- **Sources**:
  - Internal oscillators: IRC (8 MHz), LRC (32 kHz)
  - External oscillators: Xtal (4-24 MHz), external clock
  - PLL: Phase-Locked Loop for clock multiplication
  - Clock monitoring: Clock failure detection
- **Features**:
  - Multiple clock domains
  - Clock switching
  - Power management clocks
- **Configuration**: Use CS+ or Toshiba configurator tools

**General Purpose I/O (GPIO)**:
- **Ports**: Multiple GPIO ports (P0-Pn depending on family)
- **Modes**: Input, Output, Alternate Function, Analog
- **Drive Strength**: Configurable (low, standard, high)
- **Pull-Up/Down**: Configurable resistors
- **Interrupts**: External interrupt support
- **Alternate Functions**: Multiple functions per pin
- **Special Features**:
  - 5V tolerant I/O (on some families)
  - High-current drive (up to 20 mA on some)
  - Open-drain output

**Interrupt Controller**:
- **TXZ/TMPM (Cortex-R/M)**: ARM NVIC with configurable priority
- **TLX/M32C**: Proprietary interrupt controller
- **Features**:
  - Priority levels: 4-16 configurable levels
  - Interrupt vector table: Located in Flash or RAM
  - Exception handling: System exceptions
  - Wakeup sources: Configurable wakeup from low-power modes

**Timers**:
- **Types**:
  - 16-bit timers: General-purpose, input capture, output compare
  - 32-bit timers: High-resolution timing
  - PWM timers: Advanced PWM generation
  - Watchdog timers: Independent and windowed
- **Features**:
  - Input capture: Measure external signal periods/frequencies
  - Output compare: Generate output signals at specific times
  - PWM: Pulse Width Modulation with dead-time generation
  - Quadrature decoder: For encoder interfaces
  - Synchronization: Timer synchronization
  - DMA support: Direct Memory Access support
- **Use Cases**: Timing, PWM generation, input capture, output compare

**Watchdog Timers**:
- **Independent Watchdog**: Free-running watchdog timer
- **Windowed Watchdog**: Watchdog with time window for reset
- **Features**:
  - Configurable timeout period
  - Can generate reset or interrupt
  - Can be disabled via configuration
- **Use Cases**: System recovery from hangs, software errors
- **Best Practice**: Always enable WDT in production for reliability

### Communication Peripherals

**UART (Universal Asynchronous Receiver/Transmitter)**:
- **Features**:
  - Full-duplex, asynchronous communication
  - Baud rates: 1200-3 Mbps (depending on family)
  - Data formats: 5-9 bits, parity (even, odd, none), 1-2 stop bits
  - Hardware flow control: RTS/CTS
  - FIFO: Hardware FIFO (typically 4-16 bytes)
  - DMA support: Direct Memory Access support
  - IrDA mode: On some families
  - LIN support: Local Interconnect Network support
- **Number of Instances**: 1-8 (depending on family)

**SPI (Serial Peripheral Interface)**:
- **Features**:
  - Full-duplex, synchronous serial communication
  - Modes: Master and Slave modes
  - Clock modes: CPOL and CPHA configuration (4 modes)
  - Data sizes: 8-16 bits (depending on family)
  - Clock rates: Up to 24-50 MHz (depending on family)
  - FIFO: Hardware FIFO
  - DMA support: Direct Memory Access support
  - Multiple chip selects
- **Number of Instances**: 1-6 (depending on family)

**I2C (Inter-Integrated Circuit)**:
- **Features**:
  - Multi-master, multi-slave bus
  - Speeds: Standard Mode (100 kHz), Fast Mode (400 kHz), Fast Mode Plus (1 MHz)
  - Addressing: 7-bit and 10-bit addressing
  - Clock synchronization: Clock stretching support
  - DMA support: Direct Memory Access support
  - FIFO: Hardware FIFO on some families
- **Number of Instances**: 1-4 (depending on family)

**CAN (Controller Area Network)**:
- **Features**:
  - Industrial communication protocol
  - Standards: CAN 2.0A (11-bit ID), CAN 2.0B (29-bit ID)
  - CAN FD support on newer families
  - Speeds: Up to 1 Mbps (CAN), up to 5 Mbps (CAN FD)
  - Message filtering: Hardware filtering
  - DMA support: Direct Memory Access support
  - Time stamping: Hardware time stamping
- **Number of Instances**: 1-4 (depending on family)

**Ethernet MAC**:
- **Features**:
  - Ethernet communication
  - Interfaces: MII (Media Independent Interface), RMII (Reduced MII)
  - DMA: Integrated DMA controller
  - PHY Interface: Requires external PHY
  - Wake-on-LAN: Support for wake-up from Ethernet
  - Time-stamping: IEEE 1588 (PTP) support on some families
- **Number of Instances**: 1-2 (depending on family)

**USB (Universal Serial Bus)**:
- **Modes**: Device, Host, OTG (On-The-Go)
- **Speeds**: FS (12 Mbps), HS (480 Mbps)
- **Interfaces**:
  - USB Device: Device mode only
  - USB Host: Host mode only
  - USB OTG: Both Device and Host modes
- **PHY**: Integrated PHY on most families
- **DMA support**: Direct Memory Access support
- **Number of Instances**: 1-2 (depending on family)

**LIN (Local Interconnect Network)**:
- **Features**: Single-wire communication protocol
- **Speeds**: Up to 20 kbps
- **Use Cases**: Automotive body control, sensor networks
- **Supported Families**: TXZ4A, TMPM4F, some TMPM families

**FlexRay**:
- **Features**: High-speed automotive network
- **Speeds**: Up to 10 Mbps
- **Use Cases**: Automotive powertrain, chassis applications
- **Supported Families**: TXZ4A, TXZ5 (automotive variants)

**Ethernet AVB/TSN**:
- **Features**: Automotive Ethernet with AVB/TSN
- **Speeds**: 100 Mbps
- **Use Cases**: Automotive infotainment, ADAS
- **Supported Families**: TXZ4A, TXZ5 (automotive variants)

### Analog Peripherals

**ADC (Analog-to-Digital Converter)**:
- **Resolution**: 8-bit, 10-bit, 12-bit (most common), 16-bit (on some families)
- **Channels**: 4-32 channels (depending on family)
- **Sampling Rates**: 20 ksps - 4 MSPS (depending on family)
- **Modes**:
  - Single scan
  - Continuous scan
  - Group scan
  - Differential mode (on some families)
- **Trigger Sources**:
  - Timer
  - External
  - Software
  - PWM
  - Compare events
- **DMA support**: Direct Memory Access support
- **Special Features**:
  - Window comparator
  - Limit check
  - Temperature sensor (internal)
  - VBat monitoring
- **Use Cases**: Sensor interfacing, analog measurement, signal acquisition

**DAC (Digital-to-Analog Converter)**:
- **Resolution**: 8-bit, 10-bit, 12-bit (most common)
- **Channels**: 1-4 channels (depending on family)
- **Output Range**: 0-VREF or 0-VDD
- **DMA support**: Direct Memory Access support
- **Trigger Sources**: Timer, external, software
- **Buffer**: Internal or external buffer
- **Use Cases**: Waveform generation, analog output

**Analog Comparators**:
- **Number**: 1-8 (depending on family)
- **Features**:
  - Fast comparators
  - Programmable reference voltage
  - Hysteresis control
  - Interrupt generation
- **Use Cases**: Threshold detection, zero-crossing detection, signal monitoring

**Operational Amplifiers**:
- **Number**: 1-4 (depending on family)
- **Configuration**: Programmable gain, input selection
- **Characteristics**: Rail-to-rail input/output on some families
- **Use Cases**: Signal conditioning, filtering, sensor interfacing

### Advanced Timers and PWM

**PWM (Pulse Width Modulation)**:
- **Features**:
  - Multiple PWM channels (4-16 depending on family)
  - Dead-time generation
  - Complementary output
  - Synchronization
  - Fault detection
  - Multiple PWM modes (Edge-aligned, Center-aligned)
- **Resolution**: 16-bit or 32-bit (depending on family)
- **DMA support**: Direct Memory Access support
- **Use Cases**: Motor control, power conversion, LED control

**Motor Control PWM**:
- **Description**: Advanced PWM for motor control
- **Features**:
  - Multiple PWM channels (3-8 for 3-phase motors)
  - Dead-time generation
  - Current sensing interface
  - Fault detection
  - Synchronization
  - Space Vector Modulation (SVM) support
- **Supported Families**: TLX, TXZ, TMPM families
- **Use Cases**: AC/DC motor control, inverter control, power conversion

**Quadrature Encoder Interface**:
- **Features**:
  - Decode quadrature encoder signals
  - A/B inputs
  - Position counter
  - Interrupt on position change
- **Number of Instances**: 1-4 (depending on family)
- **Use Cases**: Rotary encoder, position sensing, motion detection

**Capture/Compare**:
- **Features**:
  - Input capture: Measure external signal periods/frequencies
  - Output compare: Generate output signals at specific times
  - Multiple channels per timer
- **Resolution**: 16-bit or 32-bit
- **DMA support**: Direct Memory Access support
- **Use Cases**: Timing, input capture, output compare

### Special Peripherals

**RTC (Real-Time Clock)**:
- **Features**:
  - Real-time clock with calendar
  - Power: Runs in low-power modes
  - Wakeup: Wakeup from low-power modes
  - Backup Registers: Non-volatile backup registers
  - Tamper Detection: Tamper detection on some families
  - Alarm: Multiple alarm sources
- **Use Cases**: Timekeeping, logging, scheduling
- **Number of Instances**: 1-2 (depending on family)

**CRC (Cyclic Redundancy Check)**:
- **Features**: Hardware CRC computation
- **Polynomials**: Multiple CRC polynomials (CRC-8, CRC-16, CRC-32)
- **Use Cases**: Data integrity verification, communication protocols
- **Number of Instances**: 1 on most families

**DMA Controller**:
- **Features**: Transfer data between peripherals and memory without CPU intervention
- **Channels**: 4-16 channels (depending on family)
- **Transfer Types**:
  - Memory-to-memory
  - Peripheral-to-memory
  - Memory-to-peripheral
- **Priority Levels**: Configurable priority for DMA channels
- **Interrupts**: DMA transfer complete interrupts
- **Use Cases**: High-speed data transfer, efficient memory operations

**Memory Controllers**:
- **External Memory Interface**: NAND Flash, NOR Flash, SRAM
- **Addresses**: Up to 256 MB address space
- **Timing**: Configurable timing for read/write operations
- **Multiplexing**: Multiple chip selects
- **Use Cases**: External memory, LCD displays, FPGA interfaces
- **Supported Families**: TXZ, TMPM (32-bit families)

**Graphics Accelerator**:
- **Description**: 2D graphics acceleration
- **Features**:
  - Drawing primitives (line, rectangle, circle, etc.)
  - Image scaling
  - Color conversion
  - Bit-BLT (Bit Block Transfer)
- **Use Cases**: HMI, graphical displays, user interfaces
- **Supported Families**: TMPM4G

**Camera Interface**:
- **Description**: Digital camera interface
- **Features**:
  - Parallel interface
  - MIPI CSI-2 (on some families)
  - Resolution: Up to 2048x2048
  - Data formats: YUV, RGB
  - DMA support
- **Use Cases**: Image capture, computer vision
- **Supported Families**: TXZ5

**TrustZone (on Cortex-M/R families)**:
- **Description**: ARM TrustZone technology
- **Features**:
  - Secure and Non-Secure worlds
  - Memory isolation
  - Peripheral isolation
  - Secure attributes for memory and peripherals
- **Use Cases**: Secure applications, trusted execution, data protection
- **Supported Families**: TMPM4 (some variants), TXZ5

**Cryptographic Acceleration**:
- **Features**: Hardware cryptographic acceleration
- **Algorithms**: AES (128/192/256), SHA (1, 224, 256), RSA, ECC
- **Modes**: ECB, CBC, CTR, GCM, CFB, OFB
- **DMA support**: Direct Memory Access support
- **Use Cases**: Secure communication, data encryption, authentication
- **Supported Families**: TXZ5, TMPM4 (some variants)

**Random Number Generator (TRNG)**:
- **Features**: True random number generation
- **Use Cases**: Cryptographic keys, random values, security
- **Supported Families**: TXZ5, TMPM4 (some variants)

**Temperature Sensor**:
- **Features**: On-chip temperature measurement
- **Range**: -40°C to +125°C
- **Resolution**: 8-12 bits
- **Accuracy**: ±3°C (typical)
- **Use Cases**: System monitoring, thermal management
- **Supported Families**: Most Toshiba MCUs

## Power Management

### Power Modes

**Normal Mode**:
- **Description**: Normal operation
- **Power Consumption**: Highest
- **Wakeup Sources**: Any interrupt or peripheral

**Idle Mode**:
- **Description**: CPU stopped, peripherals running
- **Power Consumption**: Low
- **Wakeup Sources**: Any peripheral interrupt
- **Entry/Exit**: Automatic or via WFI/WFE instructions

**Sleep Mode**:
- **Description**: CPU and some clocks stopped
- **Power Consumption**: Very low
- **Wakeup Sources**: Specific peripheral interrupts
- **Entry/Exit**: Manual via power management

**Deep Sleep Mode**:
- **Description**: Most of the device powered down
- **Power Consumption**: Ultra-low
- **Wakeup Sources**: External interrupts, RTC alarms
- **Entry/Exit**: Manual via power management
- **RAM Retention**: Configurable (partial or full)

**Standby Mode**:
- **Description**: Most of the device powered down with minimal state retention
- **Power Consumption**: Ultra-low
- **Wakeup Sources**: External interrupts, RTC alarms
- **Entry/Exit**: Manual via power management
- **Boot**: Wakes up as from reset

**Hibernate Mode**:
- **Description**: Complete power-down with state retention
- **Power Consumption**: Near zero
- **Wakeup Sources**: External wakeup events
- **Entry/Exit**: Manual via power management
- **Use Cases**: Long-term storage, ultra-low power operation

**Shutdown Mode**:
- **Description**: Complete power-down
- **Power Consumption**: Near zero
- **Wakeup Sources**: External reset
- **Entry/Exit**: Manual or via watchdog

### Power Management Features

**Clock Gating**: Disable clocks to unused peripherals
**Dynamic Voltage Scaling**: Adjust core voltage based on clock frequency
**Low-Power Clocks**: Use low-power oscillators for timing in low-power modes
**Peripheral Power Management**: Put unused peripherals to sleep
**Wakeup Sources**: Configure appropriate wakeup sources for application
**Power Supply Monitoring**: Monitor power supply voltage

### Power Optimization Techniques

**Use Low-Power Modes**: Enter low-power modes when possible
**Disable Unused Peripherals**: Turn off peripherals not in use
**Optimize Clock Configuration**: Use appropriate clock sources
**Use DMA**: Use DMA for memory-intensive operations
**Minimize Active Time**: Reduce CPU active time with efficient code
**Optimize Flash Access**: Place frequently accessed code in fast memory

## Development Best Practices

### Project Structure

**Recommended Structure (CS+)**:
```
project/
├── src/                    # Source files
│   ├── main.c              # Main application
│   ├── app/                # Application code
│   │   ├── tasks/         # RTOS tasks
│   │   ├── drivers/       # Custom drivers
│   │   └── utils/         # Utility functions
│   ├── system/            # System files
│   │   ├── clock.c        # Clock configuration
│   │   ├── gpio.c         # GPIO configuration
│   │   └── interrupts.c   # Interrupt handlers
│   └── config/            # Configuration files
├── include/               # Header files
├── libraries/            # Library files
│   └── toshiba/          # Toshiba provided files
├── toolchain/             # Toolchain files
├── Debug/                # Debug build (generated)
├── Release/              # Release build (generated)
├── project.cspj          # CS+ project file
└── README.md             # Project documentation
```

**Recommended Structure (Keil MDK)**:
```
project/
├── src/
├── inc/
├── libraries/
├── Debug/
├── Release/
├── project.uvprojx      # Keil project file
└── README.md
```

### Build Systems

**CS+ for TX**: Official Toshiba tool, comprehensive for TX families
**CS+ for M32C/TMP**: Official Toshiba tool, comprehensive
**e2 studio**: Cross-platform, modern, Eclipse-based
**IAR Embedded Workbench**: Excellent optimization, cross-platform
**Keil MDK**: Industry standard for ARM, excellent debugger
**Make**: Simple, cross-platform, custom
**CMake**: Cross-platform, modern, flexible

### Coding Standards

**Naming Conventions**:
- **Variables**: snake_case or camelCase
- **Functions**: snake_case or camelCase
- **Constants**: UPPER_CASE or ALL_CAPS
- **Types**: PascalCase or typedef prefixes
- **Files**: lowercase_with_underscores.h/.c
- **Macros**: UPPER_CASE_WITH_UNDERSCORES

**Code Formatting**:
- **Indentation**: 4 spaces
- **Braces**: K&R style
- **Line Length**: 80-120 characters
- **Comments**: // for single-line, /* */ for multi-line, /// for Doxygen
- **Header Guards**: #ifndef FILE_H / #define FILE_H / #endif

**Error Handling**:
- **Error Codes**: Use Toshiba SDK error codes or custom
- **Error Logging**: Implement error logging for debugging
- **Assertions**: Use SDK or compiler-specific assert functions
- **Fault Handlers**: Implement HardFault, BusFault handlers
- **Error Recovery**: Implement proper error recovery mechanisms

**Resource Management**:
- **Initialization**: Initialize all peripherals before use
- **Deinitialization**: Clean up resources when no longer needed
- **Memory Management**: Use static or stack allocation, avoid heap in critical paths
- **Interrupts**: Keep ISRs short, use flags to defer work
- **DMA Usage**: Use DMA for memory-intensive operations
- **Power Management**: Use low-power modes when possible
- **Watchdog Timer**: Always enable WDT in production

### Optimization Techniques

**Compiler Optimizations**:
- **Levels**: -O0 (debug), -O1, -O2, -O3, -Os (size), -Ofast
- **Best Practice**: Use -O2 or -O3 for release builds, -O0 for debug builds
- **Link-Time Optimization (LTO)**: Enable for better cross-module optimization
- **Inlining**: Use inline for small, frequently called functions

**Code Optimizations**:
- **Bit Manipulation**: Use bitwise operations instead of division/multiplication
- **Look-up Tables**: Pre-compute values for expensive calculations
- **Memory Alignment**: Align data structures for optimal access
- **Loop Unrolling**: Manual or automatic unrolling for critical loops
- **Function Placement**: Place frequently called functions in fast memory

**Peripheral Optimizations**:
- **Clock Configuration**: Optimize clock tree for performance/power trade-off
- **DMA Usage**: Use DMA for memory-intensive operations (ADC, SPI, UART, etc.)
- **Interrupt Coalescing**: Combine multiple interrupts to reduce overhead
- **FIFO Thresholds**: Configure FIFO thresholds for optimal throughput
- **Burst Transfers**: Use burst transfers for DMA operations

**Motor Control Optimizations**:
- **PWM Configuration**: Optimize PWM for motor control
- **Dead-Time Generation**: Use dead-time generation for complementary outputs
- **Current Sensing**: Implement current sensing for protection
- **Fault Detection**: Implement fault detection for safety
- **Synchronization**: Synchronize PWM with ADC for precise control

### Debugging Techniques

**Debug Probes**:
- **Toshiba T-Engine**: Best for Toshiba development, official tool
- **Toshiba Emulator**: Best for professional development, trace capabilities
- **SEGGER J-Link**: Best performance, cross-platform, excellent features
- **SEGGER J-Trace**: Best for trace capabilities
- **Lauterbach Trace32**: Professional trace system, excellent features
- **OpenOCD**: Open-source, flexible, cross-platform

**Debugging Methods**:
- **printf Debugging**: Simple but effective
- **RTT (Real-Time Transfer)**: SEGGER J-Link RTT for printf debugging without stopping
- **SWO (Serial Wire Output)**: ARM SWO for trace output
- **ITM (Instrumentation Trace Macrocell)**: For data trace
- **Logic Analyzer**: Use for signal analysis

**Breakpoints**:
- **Hardware Breakpoints**: Use for critical locations (limited number)
- **Software Breakpoints**: Use for less critical locations
- **Watchpoints**: Use for data access breakpoints

**Profiling**:
- **Cycle Counter**: Use DWT cycle counter for timing measurements
- **Performance Counters**: Use for performance analysis
- **Memory Usage**: Monitor stack and heap usage
- **Code Coverage**: Use coverage tools for test analysis

**Common Pitfalls and Solutions**:
- **Clock Configuration**: Always verify clock configuration
- **Pin Muxing**: Double-check pin multiplexing to avoid conflicts
- **Power Supply**: Ensure stable power supply, especially for high-speed operation
- **Interrupt Priorities**: Carefully configure interrupt priorities
- **Endianness**: Be aware of endianness (little-endian for ARM)
- **Alignment**: Ensure proper data alignment for DMA and memory access
- **Watchdog Timer**: Always enable WDT in production
- **Low-Power Modes**: Test wakeup from all low-power modes

### Security Best Practices

**Secure Coding**:
- **Input Validation**: Always validate inputs from untrusted sources
- **Buffer Overflow**: Use safe string and memory functions
- **Stack Protection**: Use stack protection mechanisms (MPU)
- **Memory Protection**: Configure MPU/TrustZone to protect critical memory

**Cryptography**:
- **Use Hardware Acceleration**: Use hardware crypto modules when available
- **Standard Algorithms**: Use industry-standard cryptographic algorithms
- **Key Management**: Securely store and manage cryptographic keys
- **Random Numbers**: Use TRNG for cryptographic random number generation

**Secure Boot**:
- **Implement Secure Boot**: Use secure bootloader to verify firmware integrity
- **Digital Signatures**: Use digital signatures for firmware verification
- **Rollback Protection**: Implement rollback protection mechanisms

**Secure Firmware Update**:
- **Use Secure Protocols**: Use secure firmware update protocols
- **Encryption**: Encrypt firmware updates in transit and at rest
- **Authentication**: Authenticate firmware updates before installation
- **Integrity Check**: Verify firmware integrity before and after update

**TrustZone (if available)**:
- **Implement TrustZone**: Use TrustZone for security isolation
- **Memory Partitioning**: Partition memory into Secure and Non-Secure
- **Peripheral Partitioning**: Partition peripherals between Secure and Non-Secure
- **Secure Services**: Implement secure services in Secure world

## Standing Rules

1. **Always verify clock configuration**: Clock settings affect all peripheral behavior
2. **Check pin multiplexing**: Pin conflicts are a common source of issues
3. **Initialize peripherals before use**: Uninitialized peripherals can cause undefined behavior
4. **Use SDK libraries when available**: Toshiba SDK drivers are tested
5. **Keep ISRs short**: Long ISRs can cause timing issues
6. **Handle errors gracefully**: Always implement proper error handling
7. **Consider power consumption**: Optimize for application requirements
8. **Test on real hardware**: Simulators may not catch all issues
9. **Verify timing constraints**: Check timing requirements for all interfaces
10. **Enable watchdog timer**: Always enable WDT in production
11. **Test low-power modes**: Thoroughly test wakeup from all low-power modes
12. **Document assumptions**: Clearly document all assumptions
13. **Use version control**: Always use version control for firmware development
14. **Follow automotive standards**: For automotive applications, follow ISO 26262, AEC-Q100
15. **Optimize for industrial**: For industrial applications, optimize for reliability and temperature range

## Common Use Cases

### Motor Control
- **Recommended Families**: TLX9, TXZ4, TXZ5, TMPM4
- **Key Peripherals**: Advanced PWM, ADC (high-speed), encoders, timers
- **Tools**: Toshiba Motor Control SDK, CS+ IDE
- **Algorithms**: FOC (Field-Oriented Control), trapezoidal control, V/f control
- **Use Cases**: AC/DC motor control, inverter control, servo motors, industrial drives

### Industrial Automation
- **Recommended Families**: TXZ4, TXZ5, TLX9, TMPM4
- **Key Peripherals**: Ethernet, CAN FD, USB, timers, PWM, ADC
- **Tools**: Industrial communication stacks, HMI libraries
- **Protocols**: Modbus, Profibus, EtherCAT, Ethernet/IP, OPC UA, CANopen
- **Use Cases**: PLCs, motor drives, HMIs, industrial sensors, factory automation

### Automotive
- **Recommended Families**: TXZ4A, TXZ5, TMPM4F
- **Key Peripherals**: CAN FD, LIN, FlexRay, Ethernet AVB/TSN, ADC, PWM
- **Tools**: AUTOSAR, ISO 26262 certified software
- **Standards**: AEC-Q100, ISO 26262 (ASIL)
- **Use Cases**: Body control, powertrain, chassis, ADAS, infotainment

### Consumer Electronics
- **Recommended Families**: TMPM0, TMPM3, TMPM4G
- **Key Peripherals**: Graphics, touch, USB, ADC, PWM
- **Tools**: Graphics libraries, touch driver stacks
- **Use Cases**: Home appliances, AV equipment, gaming, smart home devices

### IoT and Connectivity
- **Recommended Families**: TMPM4, TXZ4
- **Key Peripherals**: Ethernet, USB, CAN, ADC, PWM
- **Tools**: IoT libraries, cloud connectivity SDKs
- **Protocols**: MQTT, CoAP, HTTP, HTTPS, CAN, Ethernet
- **Use Cases**: Industrial IoT, sensor nodes, gateways, edge computing

### Power Conversion
- **Recommended Families**: TLX9, TXZ4, TMPM4
- **Key Peripherals**: Advanced PWM, ADC (high-speed), comparators, timers
- **Tools**: Power conversion libraries, digital power tools
- **Topologies**: Buck, Boost, Buck-Boost, Flyback, Half-Bridge, Full-Bridge
- **Use Cases**: DC-DC converters, inverters, battery chargers, power supplies

### Graphics and HMI
- **Recommended Families**: TMPM4G, TXZ5
- **Key Peripherals**: LCD-TFT controller, graphics accelerator, touch interface
- **Tools**: Graphics libraries, HMI frameworks
- **Libraries**: Toshiba Graphics Library, emWin, LVGL
- **Use Cases**: HMIs, graphical displays, user interfaces, industrial panels

### Security Applications
- **Recommended Families**: TXZ5, TMPM4 (with crypto)
- **Key Peripherals**: TrustZone, crypto acceleration, TRNG, secure storage
- **Tools**: Security libraries, secure boot tools
- **Certifications**: Common Criteria, FIPS, automotive certifications
- **Use Cases**: Secure connectivity, data protection, authentication

## Era Notes

### TXZ Era (2010s-Present)
- **Era 1 (2010-2015)**: TXZ4 - First ARM Cortex-R MCUs
- **Era 2 (2015-2020)**: TXZ4A - Automotive focus
- **Era 3 (2020-Present)**: TXZ5 - Cortex-R5, highest performance

### TMPM Era (2000s-Present)
- **Era 1 (2000-2010)**: TMPM0 - First Cortex-M0
- **Era 2 (2010-2015)**: TMPM3 - Cortex-M3, general-purpose
- **Era 3 (2015-2020)**: TMPM4 - Cortex-M4 with FPU
- **Era 4 (2020-Present)**: TMPM4G/4F/5 - Graphics, automotive, Cortex-M7

### TLX Era (1990s-Present)
- **Era 1 (1990-2000)**: TLX4 - First proprietary 32-bit
- **Era 2 (2000-2010)**: TLX9 - Enhanced for industrial
- **Era 3 (2010-Present)**: TLX9 (enhanced) - High-performance industrial

### Legacy Era (1980s-2010s)
- **M32C Era (1980s-2010s)**: M32C/80 - Proprietary 32-bit
- **16-bit Era (1980s-2000s)**: TMP90 - Proprietary 16-bit
- **8-bit Era (1970s-2000s)**: TMP86/87 - Proprietary 8-bit

## Additional Resources

### Documentation
- **Reference Manuals**: Comprehensive peripheral documentation
- **Data Sheets**: Electrical characteristics and specifications
- **User Manuals**: SDK and tool usage documentation
- **Application Notes**: Design examples and best practices
- **Hardware Design Guides**: PCB layout and design recommendations
- **Migration Guides**: Migration paths between MCU families

### Community
- **Toshiba Semiconductor Website**: https://toshiba.semicon-storage.com/
- **Toshiba Support**: https://www.toshiba.eu/semiconductors/
- **Toshiba Contact**: Contact form and support portal
- **Distributor Support**: Digi-Key, Mouser, Avnet, etc.

### Training and Certification
- **Toshiba Training**: https://www.toshiba.eu/semiconductors/training/
- **Webinars**: Regular webinars on Toshiba technologies
- **Technical Workshops**: Hands-on training sessions
- **Certification Programs**: Various certification programs

### Tools and Utilities
- **CS+ IDE**: https://www.toshiba.eu/semiconductors/design-development-tools/
- **Toshiba Peripheral Configuration Tool**: Standalone configuration
- **Toshiba Flash Programmer**: Flash programming tool
- **Toshiba Simulator**: Instruction set simulator

### Partners and Ecosystem
- **Authorized Distributors**: Digi-Key, Mouser, Newark, Farnell, Avnet, etc.
- **Third-Party Tools**: Multiple third-party tools and services
- **Design Partners**: Certified design and consulting partners
- **Training Partners**: Authorized training partners

### Certification Programs
- **Automotive Certifications**: AEC-Q100, ISO 26262
- **Industrial Certifications**: IEC 61508, ISO 9001
- **Medical Certifications**: IEC 62304 (for medical applications)
- **Security Certifications**: Common Criteria (for secure MCUs)
