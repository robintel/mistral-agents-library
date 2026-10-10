---
type: platform
family: mcu
region: usa
manufacturer: Microchip
---

# Microchip Technology Microcontroller Platform

**Microchip Technology MCU families**: Comprehensive portfolio of 8-bit, 16-bit,
and 32-bit microcontrollers from the American semiconductor manufacturer. This
contract defines the architecture families, development ecosystems, peripheral
modules, toolchain support, and best practices for Microchip-based embedded
development.

## Overview

Microchip Technology Inc. is headquartered in Chandler, Arizona. Founded in 1989
as a spin-off from General Instrument, Microchip is a pioneer in the MCU industry,
particularly known for its PIC microcontrollers. The company acquired Atmel in 2016,
expanding its portfolio to include AVR, ARM Cortex-M, and ARM Cortex-A MCUs.

Microchip MCUs are widely used in: industrial control, automotive, consumer
electronics, IoT, medical devices, and aerospace.

## Architecture Families

### 8-bit PIC Families

#### PIC10/12/16 Families

**PIC10F Series**: Ultra-low cost, 6-8 I/O, basic peripherals (timers, WDT, comparator)
- **Core**: 8-bit PIC, 12-14 bit instruction word
- **Performance**: 4-16 MHz
- **Flash**: 384-1024 words
- **RAM**: 16-41 bytes

**PIC12F Series**: Low-cost, small package (8-28 pins)
- **Core**: 8-bit PIC, 14-bit instruction word
- **Performance**: 4-20 MHz
- **Flash**: 512-4096 words
- **RAM**: 25-256 bytes
- **Key Features**: CAN, USB, UART, SPI, I2C, ADC (10-bit)

**PIC16F Series** (Most Popular 8-bit):
- **Core**: 8-bit PIC, 14-bit instruction word
- **Performance**: 8-32 MHz
- **Flash**: 1-64 KB
- **RAM**: 64-2048 bytes
- **Sub-families**: F5x (basic), F6x (general), F7x (low-power), F8x (high-end), F1xxx (enhanced), F15xx (XLP)
- **Key Features**: Multiple timers, ADC (10/12-bit), UART, SPI, I2C, PWM, comparators, WDT

**PIC16F15xx Series** (XLP):
- **Performance**: 32 MHz
- **Flash**: 1.75-28 KB
- **RAM**: 256-2048 bytes
- **Key Features**: XLP technology, ADC (10-bit), DAC (8-bit), PWM (10/16-bit), UART, SPI, I2C

**PIC18F Series** (High Performance 8-bit):
- **Core**: 8-bit PIC, 16-bit instruction word
- **Performance**: 40-64 MHz
- **Flash**: 4-128 KB
- **RAM**: 256-4096 bytes
- **Sub-families**: F2x, F4x, FxxJ, FxxK22, FxxK42, FxxQ10, FxxQ43
- **Key Features**: ADC (10-bit), DAC (8/10-bit), CAN, USB, UART, SPI, I2C, PWM, comparators

### 16-bit Families

#### PIC24 Family

**PIC24F Series**:
- **Core**: 16-bit PIC
- **Performance**: 16 MIPS (40 MHz)
- **Flash**: 16-512 KB
- **RAM**: 8-96 KB
- **Sub-families**: FJxx, FJxxGA (graphics), FJxxGB (USB OTG)
- **Key Features**: Multiple 16-bit timers, ADC (10-bit), DAC (10-bit), UART, SPI, I2C, CAN, USB, Ethernet, DMA, RTCC

**PIC24H Series**:
- **Performance**: 16 MIPS (40 MHz)
- **Flash**: 256-1024 KB
- **RAM**: 64-96 KB
- **Key Features**: Advanced PWM, ADC (10-bit, 1.1 MSPS), CAN, USB OTG, Ethernet, DMA

#### dsPIC Family (Digital Signal Controllers)

**dsPIC30F Series**:
- **Core**: 16-bit dsPIC (DSP-enabled)
- **Performance**: 30 MIPS (30 MHz)
- **Flash**: 12-144 KB
- **RAM**: 2-16 KB
- **Key Features**: DSP engine, PWM, ADC (10-bit, 500 ksps), UART, SPI, I2C, CAN

**dsPIC33F Series**:
- **Performance**: 40 MIPS (40 MHz)
- **Flash**: 24-256 KB
- **RAM**: 8-32 KB
- **Key Features**: Enhanced DSP, PWM, ADC (10-bit, 1.1 MSPS), USB

**dsPIC33E Series**:
- **Performance**: 70 MIPS (70 MHz)
- **Flash**: 64-512 KB
- **RAM**: 32-128 KB
- **Key Features**: High-performance DSP, PWM, ADC (12-bit, 2.2 MSPS), DAC (12-bit), CAN FD, USB OTG, Ethernet, DMA

### 32-bit Families

#### PIC32 Family (MIPS-based)

**PIC32MX Series**:
- **Core**: MIPS32 M4K
- **Performance**: 80 MHz
- **Flash**: 64-512 KB
- **RAM**: 32-128 KB
- **Sub-families**: MX1xx/2xx (entry), MX3xx/4xx (general), MX5xx/6xx (high-end), MX7xx (ultimate)
- **Key Features**: Multiple timers, ADC (10-bit), CAN, USB OTG, Ethernet, DMA, RTCC

**PIC32MZ Series**:
- **Core**: MIPS32 microAptiv (DA/EC/MA)
- **Performance**: 200-252 MHz
- **Flash**: 512 KB - 2 MB
- **RAM**: 256-512 KB
- **Sub-families**: DA (200 MHz), EC (252 MHz, crypto, CAN FD, Ethernet), MA (252 MHz, ultimate)
- **Key Features**: FPU, ADC (12-bit), DAC (12-bit), CAN FD, USB OTG HS, Ethernet, DMA, crypto

#### SAM Family (ARM Cortex-M from Atmel)

**SAM D Series** (Cortex-M0+): Low-power, 16-256 KB Flash, 4-32 KB RAM, ADC (12-bit), USB
**SAM L Series** (Cortex-M0+): Ultra-low power, XLP, 8-64 KB Flash, 2-8 KB RAM
**SAM R Series** (Cortex-M0+): Automotive, CAN FD, LIN, 32-256 KB Flash
**SAM C Series** (Cortex-M0+): Capacitive touch, PTC, 16-256 KB Flash
**SAM G Series** (Cortex-M4): High-performance, FPU, 256 KB - 2 MB Flash, CAN FD, USB OTG HS, Ethernet
**SAM E Series** (Cortex-M4): Industrial, CAN FD, Ethernet, 256 KB - 2 MB Flash
**SAM V Series** (Cortex-M7): Ultimate, cache, 512 KB - 4 MB Flash, CAN FD, USB OTG HS, Ethernet
**SAM DA/DB Series** (Cortex-M0+): Cost-sensitive, USB, 16-256 KB Flash
**SAM HA/HC Series** (Cortex-M4): Automotive, AEC-Q100, CAN FD, Ethernet

#### AVR Families (from Atmel)

**AVR Classic**: ATtiny (4-40 pins), AT90S, ATmega (28-100 pins)
- **Core**: 8-bit AVR RISC
- **Performance**: 1-20 MHz
- **Flash**: 0.5-256 KB
- **RAM**: 32 bytes - 8 KB
- **EEPROM**: 64 bytes - 4 KB
- **Key Features**: ISP, DebugWire, BOD, WDT, timers, UART, SPI, I2C (TWI), ADC, comparators

**AVR XMEGA**:
- **Performance**: 32 MHz
- **Flash**: 16-512 KB
- **RAM**: 1-32 KB
- **Key Features**: Event system, DMA, ADC (12-bit), DAC (12-bit), UART, SPI, I2C, CAN, USB, crypto

### Wireless Families

**SAM B11 Series**: BLE 4.2, Cortex-M0+, 48 MHz, 128-256 KB Flash
**SAM D21 + WINC**: Wi-Fi 802.11 b/g/n, Cortex-M0+, 48 MHz
**SAM R30 Series**: Sub-GHz (315-915 MHz), Cortex-M0+, 48 MHz
**SAM L22 + MON09**: LoRaWAN, Cortex-M0+, 32 MHz
**SAM D21 + WINC1500/3400**: Wi-Fi via external module

## Development Ecosystem

### Official IDEs

**MPLAB X IDE**:
- **Description**: Official IDE for all Microchip MCUs
- **Features**: MPLAB Code Configurator (MCC), debugging, compiler integration (XC8/16/32/DSC)
- **Platform**: Windows, Linux, macOS
- **Pros**: Comprehensive, official, free
- **Cons**: Java-based, resource-heavy

**Atmel Studio**:
- **Description**: IDE for AVR and SAM MCUs (legacy)
- **Features**: Atmel START, debugging, AVR/GNU toolchain integration
- **Platform**: Windows
- **Pros**: Excellent for AVR, good for SAM
- **Cons**: Windows only
- **Status**: Replaced by MPLAB X for new projects

**Microchip Studio**:
- **Description**: Unified IDE (Atmel Studio successor)
- **Features**: MCC + START integration, cross-platform support
- **Platform**: Windows, Linux (experimental), macOS (experimental)
- **Status**: Actively developed

### Configuration Tools

**MPLAB Code Configurator (MCC)**:
- **Description**: Graphical configuration tool
- **Features**: Pin config, clock config, peripheral config, code generation, Harmony integration
- **Pros**: Visual, intuitive, comprehensive
- **Cons**: Java-based, can be slow
- **Supported**: All Microchip MCUs

**Atmel START**:
- **Description**: Web-based configuration for AVR/SAM
- **Features**: Visual config, code generation, project generation
- **Pros**: Modern, web-based
- **Cons**: Requires internet
- **Supported**: AVR, SAM

**MPLAB Harmony Configurator**:
- **Description**: Framework configuration for Harmony
- **Features**: Modular config, library selection, RTOS config
- **Pros**: Comprehensive for Harmony
- **Cons**: Complex, learning curve

### Toolchains

**MPLAB XC Compilers**:
- **XC8**: For PIC 8-bit
- **XC16**: For PIC 16-bit and dsPIC
- **XC32**: For PIC32
- **XC-DSC**: For dsPIC
- **Pros**: Official, optimized, good support
- **Cons**: Commercial (free with limitations)

**GNU Toolchains**:
- **avr-gcc**: For AVR MCUs
- **arm-none-eabi-gcc**: For SAM Cortex-M
- **Pros**: Free, open-source
- **Cons**: Less optimized

**Third-Party**:
- **IAR Embedded Workbench**: ICCAVR, ICCARM
- **Keil MDK**: For ARM
- **Pros**: Excellent optimization
- **Cons**: Commercial

### SDKs and Libraries

**MPLAB Harmony**:
- **Description**: Official framework for PIC32/SAM/dsPIC
- **Features**: HAL, peripheral drivers, middleware (FreeRTOS, LwIP, FatFS, etc.), RTOS support
- **Pros**: Modular, comprehensive, official
- **Cons**: Large, learning curve

**MPLAB XC Libraries**: Peripheral drivers for PIC families
**Atmel Software Framework (ASF)**: Legacy framework for AVR/SAM
**MPLAB Harmony Graphics**: Graphics libraries
**Third-Party RTOS**: FreeRTOS, ThreadX, SafeRTOS, embOS, QNX, VxWorks

### Debugging and Programming

**Debug Probes**:
- **MPLAB ICD 4**: Professional, full features, expensive
- **MPLAB PICkit 4**: Mid-range, good performance, affordable
- **MPLAB Snap**: Entry-level, basic features, portable
- **Atmel-ICE**: For AVR/SAM, high performance
- **Atmel Power Debugger**: AVR-focused, power analysis
- **SEGGER J-Link**: Cross-platform, excellent performance
- **SEGGER J-Trace**: With trace capability
- **Lauterbach Trace32**: Professional trace system
- **OpenOCD**: Open-source, flexible

**Programming Tools**:
- **MPLAB IPE**: Standalone programming
- **MPLAB X IDE**: Integrated programming
- **PICkit Programmer**: Simple GUI
- **Atmel Flip**: For AVR via USB
- **Bootloader Support**: PIC/AVR/SAM bootloaders
- **Production**: MPLAB PM3 (high-speed production)

## Peripheral Modules

### Core Peripherals

**Clock System**: Internal/external oscillators, PLL, clock switching, fail-safe monitoring
**GPIO**: Input/output/alternate/analog modes, pull-up/down, interrupts
**Interrupt Controller**: Vectored on 16/32-bit, software polling on 8-bit
**Timers**: 8/16/32-bit, input capture, output compare, PWM
**Watchdog Timer**: Configurable timeout, windowed mode

### Communication

**UART**: Full-duplex, 5-9 bits, parity, flow control, FIFO, DMA
**SPI**: Full-duplex, 4-16 bits, 4 modes, FIFO, DMA
**I2C**: Multi-master, 100/400 kHz/1 MHz, 7/10-bit addressing, DMA
**CAN**: CAN 2.0A/B, CAN FD (5-8 Mbps), filtering, DMA, time stamping
**USB**: Device/Host/OTG, FS/HS, integrated PHY, DMA
**Ethernet**: MII/RMII, DMA, Wake-on-LAN, IEEE 1588
**LIN/IrDA**: Local Interconnect Network, Infrared Data Association

### Analog

**ADC**: 8/10/12/16-bit, 2-48 channels, 50 ksps - 18 MSPS, DMA, triggers
**DAC**: 8/10/12-bit, 1-4 channels, DMA, triggers
**Comparators**: 1-6 channels, programmable reference, hysteresis
**Op-Amps**: 1-4 channels, configurable gain, rail-to-rail

### Advanced Timers/PWM

**Capture/Compare/PWM**: Input capture, output compare, PWM, quadrature decode
**ECCP**: Enhanced CCP with steering, auto-shutdown
**SCT**: State Configurable Timer (SAM), advanced PWM with dead-time
**TC/TCC**: Timer Counter (SAM), PWM with dead-time, fault detection
**Motor Control PWM**: 3-8 channels, dead-time, current sensing, SVM

### Special Peripherals

**RTC**: Calendar, alarms, backup registers, tamper detection
**CRC**: CRC-8/16/32 computation
**RNG**: True/pseudo-random number generation
**Crypto**: AES, DES/TDES, SHA, RSA, ECC, HMAC (PIC32MZ EC/MA, SAM E5x/G5x/V7x)
**HSM**: Hardware Security Module with secure key storage
**DMA**: 4-32 channels, memory-to-memory, peripheral-to-memory
**Memory Controllers**: External NAND/NOR/SRAM, FSMC, SQI
**Capacitive Sensing**: PTC (Peripheral Touch Controller), 256+ channels
**DSPI/I2S**: Enhanced SPI, digital audio interface
**Event System**: Hardware event routing (AVR XMEGA, SAM)
**CLC**: Configurable Logic Cells (4-8 cells)
**NCO**: Numerically Controlled Oscillator

## Power Management

### Low-Power Modes

**Idle/Sleep**: CPU stopped, peripherals running
**Deep Sleep**: CPU and some peripherals stopped
**Backup**: RTC and registers powered
**Hibernate**: Complete power-down with state retention
**Shutdown**: Complete power-down

### Power Features

**XLP Technology**: Ultra-low power for PIC24/dsPIC
**Doze Mode**: CPU at reduced speed
**PMD**: Peripheral Module Disable
**DVFS**: Dynamic Voltage and Frequency Scaling
**Clock Gating**: Disable unused peripheral clocks

## Development Best Practices

### Project Structure

```
project/
├── src/
│   ├── main.c
│   ├── app/
│   ├── system/
│   └── config/
├── include/
├── libraries/
│   ├── mcc_generated/
│   └── harmony/
├── toolchain/
├── nbproject/
└── README.md
```

### Build Systems

**MPLAB X IDE**: Official, comprehensive, free, Java-based
**MPLAB Harmony**: Modular framework, official, comprehensive
**Atmel Studio**: AVR/SAM focused, Windows only
**Microchip Studio**: Unified, modern, cross-platform (experimental)
**Make/CMake**: Cross-platform, custom
**GNU Toolchains**: Free, open-source

### Coding Standards

**Naming**: snake_case or camelCase, UPPER_CASE constants
**Indentation**: 4 spaces
**Braces**: K&R style
**Line Length**: 80-120 characters
**Comments**: //, /* */, /// for Doxygen

**Error Handling**: Use SDK error codes, implement fault handlers
**Resource Management**: Initialize peripherals, keep ISRs short, use DMA
**Optimization**: -O2 for release, -O0 for debug, use DMA, optimize clock tree

### Security Best Practices

**Secure Coding**: Input validation, buffer overflow protection, stack protection
**Cryptography**: Use hardware acceleration, standard algorithms, secure key management
**Secure Boot**: Implement secure bootloader, digital signatures, rollback protection
**Secure Update**: Secure protocols, encryption, authentication, integrity check
**Code Protection**: Configuration bits, MPU protection, bootloader protection

## Standing Rules

1. Verify clock configuration
2. Check pin multiplexing
3. Configure configuration bits
4. Initialize peripherals before use
5. Use SDK libraries when available
6. Keep ISRs short
7. Handle errors gracefully
8. Consider power consumption
9. Test on real hardware
10. Verify timing constraints
11. Enable WDT in production
12. Test low-power modes
13. Document assumptions
14. Use version control
15. Review configuration bits before production

## Common Use Cases

**Motor Control**: dsPIC, PIC32MZ, SAM E/G - Advanced PWM, ADC, encoders
**Industrial Automation**: PIC24, dsPIC, PIC32, SAM E/G/V - Ethernet, CAN, USB
**IoT**: SAM D/L/C, PIC32MZ DA, SAM B/R - BLE, Wi-Fi, LoRa
**Consumer**: PIC16/18, PIC24, dsPIC, PIC32 - Touch, USB, PWM
**Automotive**: PIC18, PIC24, dsPIC, PIC32, SAM R/HA/HC - CAN FD, LIN, Ethernet
**Medical**: PIC24, dsPIC, PIC32, SAM E/G/L - High-res ADC, security
**Audio**: dsPIC, PIC32, SAM E/G - I2S, ADC, DAC
**HMI**: PIC24, dsPIC, PIC32, SAM D/E/G - Graphics, touch
**Security**: PIC32MZ EC/MA, SAM E5x/G5x/V7x - TrustZone, crypto, HSM
**Power Conversion**: dsPIC, PIC24, PIC32 - PWM, ADC, comparators
**Data Acquisition**: dsPIC, PIC24, PIC32, SAM E/G - ADC, DAC, DMA

## Era Notes

### 8-bit PIC
- 1970s-1980s: PIC1650 (first)
- 1980s-1990s: PIC16C5x (first commercial)
- 1990s-2000s: PIC16F84 (most popular)
- 2000s-2010s: PIC16F1xxx (enhanced)
- 2010s-2020s: PIC16F15xx (XLP)
- 2020s-Present: PIC16F17xx (CAN)

### 16-bit PIC
- 1990s-2000s: PIC17Cxxx (first, discontinued)
- 2000s-2010s: PIC18Fxxx (first Flash)
- 2000s: dsPIC30F (first DSC)
- 2000s-2010s: PIC24F (general-purpose)
- 2010s-Present: dsPIC33F/E (CAN FD, Ethernet)
- 2010s-Present: PIC24H (high-performance)

### 32-bit PIC
- 2007-2010: PIC32MX (first, MIPS M4K)
- 2010-2015: PIC32MZ (high-performance, crypto)
- 2015-Present: PIC32MZ DA/EC/MA (ultimate)

### AVR
- 1990s-2000s: AT90S (first)
- 2000s-2010s: ATmega (most popular)
- 2000s-2010s: ATxmega (advanced)
- 2000s-2010s: AVR32 (32-bit, discontinued)

### SAM
- 2010-2012: SAM3/SAM4 (first Cortex-M)
- 2012-2016: SAM D/L (Cortex-M0+)
- 2016-Present: SAM E/G/V (Cortex-M4/M7)
- 2018-Present: SAM B/R (wireless, automotive)

## Additional Resources

### Documentation
- Reference Manuals, Data Sheets, User Manuals, Application Notes, Design Guides

### Community
- Forums: https://www.microchip.com/forums/
- Support: https://www.microchip.com/support
- GitHub: https://github.com/microchip-pic-avr-examples

### Training
- Microchip University: https://mu.microchip.com/
- Online Training: https://www.microchip.com/design/training
- Webinars, Certification Programs

### Tools
- MPLAB X IDE, MPLAB Harmony, MPLAB Code Configurator
- Atmel START, Microchip Studio
- MPLAB Connect, Memory/Register Window Tools
