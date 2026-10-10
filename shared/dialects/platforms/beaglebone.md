---
type: platform
family: sbc
---

# BeagleBone

The real-time capable, industrial-friendly single-board computer
from BeagleBoard.org. Open hardware, open software, designed for
embedded applications that need real-time performance and
industrial connectivity.

## Eras

The era is declared by the **board model** and **processor**.

**BeagleBone (Original, 2011)**:
- Processor: AM335x (ARM Cortex-A8, 720MHz)
- RAM: 256MB DDR3
- Storage: 4GB eMMC (on some models)
- Connectivity: 1 x 10/100 Ethernet, USB 2.0
- GPIO: 2 x 46-pin headers

**BeagleBone Black (BBB, 2013)**:
- Processor: AM3358/AM3359 (ARM Cortex-A8, 1GHz)
- RAM: 512MB DDR3L
- Storage: 4GB eMMC (onboard), microSD
- Connectivity: 1 x 10/100 Ethernet, USB 2.0
- GPIO: 2 x 46-pin headers
- **Industrial features**: Onboard HDMI is removed, focus on GPIO

**BeagleBone Black Wireless (BBBW, 2016)**:
- Processor: AM3358 (ARM Cortex-A8, 1GHz)
- RAM: 512MB DDR3L
- Storage: 4GB eMMC, microSD
- Connectivity: Ethernet, USB, WiFi 802.11 b/g/n, Bluetooth 4.1
- GPIO: 2 x 46-pin headers

**BeagleBone Blue (2016)**:
- Processor: AM3358 (ARM Cortex-A8, 1GHz)
- RAM: 512MB DDR3L
- Storage: 4GB eMMC, microSD
- Connectivity: Ethernet, USB, WiFi, Bluetooth, CAN, battery management
- GPIO: 2 x 46-pin headers
- **Robotics focus**: Motor drivers, encoders, IMU, barometer
- **Battery**: LiPo battery support with charging circuit

**BeagleBone AI (2018)**:
- Processor: AM5729 (ARM Cortex-A15, 1.5GHz) + 2x C66x DSP + 4x PRU
- RAM: 1GB DDR3L
- Storage: 16GB eMMC, microSD
- Connectivity: Gigabit Ethernet, USB 3.0, WiFi, Bluetooth
- **AI focus**: TIDL (Texas Instruments Deep Learning)
- **PRU**: 2x Programmable Realtime Units
- **DSP**: 2x C66x DSP cores

**BeagleBone Black Industrial (2020)**:
- **Industrial grade**: -40°C to +85°C operating temperature
- **Long-term availability**: 5+ year production commitment
- **Same as BBB**: AM3358, 512MB RAM, 4GB eMMC
- **Enhanced**: Industrial power supply, DIN rail mount option

**PocketBeagle (2018)**:
- Processor: Octavo OSD3358 (AM3358 + RAM + PMIC in one package)
- RAM: 512MB DDR3L
- Storage: microSD only
- Connectivity: USB (client mode only), no Ethernet
- GPIO: 2 x 46-pin headers (but smaller form factor)
- **Ultra-small**: 56mm x 56mm

## Programmable Realtime Unit (PRU)

The **PRU** is the defining feature of BeagleBone — a **real-time
capable** co-processor that runs independently of the main ARM CPU.

### PRU Architecture

- **Dual PRUs**: PRU0 and PRU1 (BeagleBone Black, AI)
- **Clock**: 200MHz (independent of ARM clock)
- **Instruction set**: 32-bit RISC, custom for PRU
- **Registers**: 32 x 32-bit general purpose registers
- **Memory**: 8KB instruction RAM, 8KB data RAM per PRU
- **Shared memory**: 12KB shared RAM between PRUs

### PRU Capabilities

- **Deterministic timing**: Sub-5ns jitter on GPIO operations
- **Direct GPIO access**: No Linux overhead for GPIO operations
- **Interrupt handling**: Can respond to external events within 20ns
- **Parallel processing**: Both PRUs can run simultaneously
- **Peripheral access**: Direct access to all SoC peripherals

### PRU Use Cases

| Use Case | Description | Benefits |
|----------|-------------|----------|
| **Real-time GPIO** | Precise timing control for GPIO | No Linux latency, deterministic |
| **PWM generation** | High-resolution PWM (sub-ns resolution) | Better than hardware PWM |
| **Encoder reading** | Quadrature encoder counting | No missed counts, high speed |
| **Protocol emulation** | SPI, I2C, UART emulation | Custom protocols, high speed |
| **Stepper motor control** | Precise step generation | Smooth motion, high speed |
| **Data acquisition** | High-speed ADC reading | No CPU overhead |
| **Bus monitoring** | CAN, Ethernet monitoring | Real-time capture |
| **Custom peripherals** | Implement custom hardware interfaces | Flexible, fast |

### PRU Development

**Toolchain**:
- **PRU Assembly**: Native PRU assembly language
- **PRU C**: C compiler for PRU (limited support)
- **PRU Pascal**: Pascal compiler for PRU
- **Remoteproc**: Linux framework for loading PRU firmware

**Example PRU Assembly** (blink LED):
```asm
; PRU0 code to blink GPIO
Origin 0
EntryStart:
    ; Configure GPIO
    LBCO r0, C4, 4, 4   ; Clear GPIO1[15] (P8_15)
    LBBO r0, C4, 4, 4   ; Set GPIO1[15]
    JMP EntryStart
```

**PRU C Example**:
```c
#include <stdint.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include "resource_table_empty.h"

volatile register uint32_t __R30;
volatile register uint32_t __R31;

int main(void) {
    while(1) {
        __R30 ^= (1 << 15);  // Toggle GPIO
    }
    return 0;
}
```

**Loading PRU firmware**:
```bash
# Compile PRU assembly
pasm -b -o pru0.bin pru0.p

# Load PRU firmware
sudo pru_config -f pru0.bin -r

# Or using remoteproc
sudo modprobe pru_rproc
sudo echo pru0_fw > /sys/class/remoteproc/remoteproc1/firmware
```

### PRU-ICSS (PRU Industrial Communication Subsystem)

- **UART**: Up to 12Mbps
- **I2C**: Up to 3.4Mbps
- **SPI**: Up to 48Mbps
- **eCAP**: Enhanced Capture modules (3 on AM335x)
- **ePWM**: Enhanced PWM modules (6 on AM335x)
- **eQEP**: Enhanced Quadrature Encoder Pulse modules (3 on AM335x)

**PRU-ICSS allows**:
- Real-time protocol handling
- Industrial communication (Profibus, CANopen, etc.)
- Custom bus protocols
- High-speed data capture

## Cape System

Capes are **add-on boards** for BeagleBone, similar to Raspberry Pi HATs
but with more flexibility and standardization.

### Cape Identification

- **EEPROM**: 24C256 I2C EEPROM (on most capes)
- **Address**: 0x50-0x57 (configurable via address pins)
- **Format**: Structured data describing cape
- **Auto-configuration**: BeagleBone reads cape EEPROM on boot

**EEPROM layout**:
- Manufacturer, board name, version
- GPIO usage map
- Part number, serial number
- Compatible with BeagleBone versions

### Cape Headers

**P8 Header** (46 pins):
- GPIO: 0-45 (varies by pin)
- Power: 3V3, 5V, VDD_3V3EXP, VDD_5VEXP
- Ground: Multiple GND pins
- Analog: AIN0-AIN7
- Special: PRU, McASP, UART, I2C, SPI, eCAP, ePWM

**P9 Header** (46 pins):
- GPIO: 0-45 (varies by pin)
- Power: 3V3, 5V, VDD_3V3EXP, VDD_5VEXP
- Ground: Multiple GND pins
- USB: USB0_DM, USB0_DP, USB1_DM, USB1_DP
- Ethernet: MDIO, MDC, RGMII
- LCD: LCD_DATA0-15, LCD_VSYNC, LCD_HSYNC, LCD_PCLK

### Popular Capes

| Cape | Function | Key Features |
|------|----------|--------------|
| **Display Cape** | LCD display | 4.3" or 7" touchscreen, HDMI pass-through |
| **Audio Cape** | Audio I/O | High-quality stereo audio, microphone input |
| **Wireless Cape** | WiFi/BT | Onboard WiFi and Bluetooth |
| **Motor Cape** | Motor control | 3x motor drivers, encoders |
| **Battery Cape** | Power | LiPo battery, charging circuit |
| **CAN Cape** | CAN bus | MCP2515 CAN controller, DB9 connector |
| **4D Cape** | 4D Systems | LCD, touch, audio, buttons |
| **Replicape** | 3D Printer | Stepper drivers, limit switches, fan control |
| **BBB Mini** | Small form | Breakout for PocketBeagle |

### Cape Development

**Design requirements**:
- EEPROM for identification
- Compatible with BeagleBone headers
- Proper power distribution
- ESD protection on exposed pins

**EEPROM programming**:
```bash
# Write cape EEPROM
sudo config-pin P9.24 gpio  # Enable I2C
sudo i2cset -y 1 0x50 0x00 0xAA  # Write to EEPROM
```

## GPIO System

### GPIO Overview

- **Total GPIO**: 65+ (varies by model)
- **Headers**: P8 and P9 (46 pins each, but not all are GPIO)
- **Bank system**: GPIO grouped into banks (GPIO0, GPIO1, GPIO2, GPIO3)
- **Ball assignment**: Each GPIO has a ball number on the AM335x SoC

### GPIO Banks

**Bank 0 (GPIO0)**:
- Pins: P8_3-16, P8_20-25, P8_27-34, P8_36-46, P9_11-14
- Features: UART, I2C, SPI, eCAP, ePWM, ADC

**Bank 1 (GPIO1)**:
- Pins: P8_17-19, P8_26, P8_35, P9_15-17, P9_19-20, P9_21-30
- Features: UART, McASP, eCAP, ePWM

**Bank 2 (GPIO2)**:
- Pins: P8_1-2, P8_7-10, P8_41-46, P9_41-42
- Features: SPI, I2C, UART, McASP

**Bank 3 (GPIO3)**:
- Pins: P9_18, P9_22-25
- Features: MMC, SPI

### GPIO Configuration

BeagleBone uses **device tree overlays** for GPIO configuration.

**Common configurations**:
- **GPIO input/output**: Basic digital I/O
- **UART**: Serial communication
- **I2C**: I2C bus
- **SPI**: SPI bus
- **PWM**: Pulse Width Modulation
- **ADC**: Analog input
- **eCAP**: Capture input (for encoders)
- **ePWM**: PWM output (for motor control)

**Configuration tools**:
```bash
# List available overlays
ls /lib/firmware/ | grep BB-

# Load overlay
sudo modprobe cape_bone_iio

# Configure pin
sudo config-pin P8.11 gpio  # Set P8.11 as GPIO
sudo config-pin P8.12 uart  # Set P8.12 as UART
sudo config-pin P9.21 pwm   # Set P9.21 as PWM
```

**Device tree overlay example**:
```dts
/ {
    fragment@0 {
        target = <&am33xx_pinmux>;
        __overlay__ {
            pinctrl_p8_11: pinctrl_p8_11 {
                pinctrl-single,pins = <0x034 0x0f>;  // P8.11 as GPIO
            };
        };
    };
};
```

**Python GPIO (using Adafruit_BBIO)**:
```python
import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("P8_11", GPIO.OUT)  # Using pin name
# or
GPIO.setup("GPIO0_13", GPIO.OUT)  # Using GPIO number

GPIO.output("P8_11", GPIO.HIGH)
GPIO.input("P8_12")

GPIO.cleanup()
```

## Analog Input

### ADC (Analog to Digital Converter)

- **ADC**: 12-bit SAR ADC (TLV320AIC3106 on AM335x)
- **Channels**: 8 channels (AIN0-AIN7)
- **Resolution**: 12 bits (0-4095)
- **Reference voltage**: 1.8V internal (can use external)
- **Sample rate**: Up to 200ksps

**Pins**:
- AIN0: P9.39
- AIN1: P9.40
- AIN2: P9.37
- AIN3: P9.38
- AIN4: P9.33
- AIN5: P9.36
- AIN6: P9.35
- AIN7: P9.34

**Reading ADC**:
```bash
# Read ADC value
cat /sys/bus/iio/devices/iio:device0/in_voltage0_raw

# Or with scale
cat /sys/bus/iio/devices/iio:device0/in_voltage_scale
```

**Python ADC**:
```python
import Adafruit_BBIO.ADC as ADC

ADC.setup()
value = ADC.read("P9_39")  # AIN0
voltage = value * 1.8 / 4095  # Convert to voltage

ADC.cleanup()
```

## Industrial Interfaces

### CAN Bus

- **Controller**: DCAN (on AM335x)
- **Pins**: P9.24 (CAN_RX), P9.26 (CAN_TX)
- **Speed**: Up to 1Mbps
- **Transceiver**: Requires external transceiver (TJA1050, etc.)

**Configuration**:
```bash
# Enable CAN
sudo modprobe can
sudo modprobe mttcan

# Configure CAN interface
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up

# Send CAN message
sudo cansend can0 123#1122334455667788

# Receive CAN message
sudo candump can0
```

### PRU CAN

For **real-time CAN** without Linux overhead:
- Use PRU to implement CAN controller
- Direct access to CAN transceiver
- Deterministic timing

### McASP (Multichannel Audio Serial Port)

- **Channels**: 2 x serial ports (McASP0, McASP1)
- **Features**: I2S, TDM, DAC, ADC
- **Use cases**: Audio, high-speed data acquisition

### RGMII (Reduced Gigabit Media Independent Interface)

- **Interface**: Ethernet PHY connection
- **Speed**: Up to 1Gbps
- **Pins**: P9.11-16, P9.18-25 (varies by model)

## Connectivity

### Ethernet

- **BeagleBone Black**: 10/100 Mbps (USB 2.0 bus)
- **BeagleBone AI**: Gigabit Ethernet (dedicated controller)
- **BeagleBone Black Industrial**: 10/100 Mbps (industrial grade)

**Configuration**:
```bash
# Configure network
sudo nano /etc/network/interfaces

# Or use DHCP
sudo dhclient eth0
```

### USB

- **USB 2.0**: All models (480Mbps)
- **USB 3.0**: BeagleBone AI only (5Gbps)
- **OTG**: USB On-The-Go support (device mode)

**USB device mode** (PocketBeagle):
```bash
# Enable device mode
sudo modprobe g_ether

# Or
sudo modprobe g_serial
```

### WiFi (BeagleBone Black Wireless, BeagleBone AI)

- **Chip**: TI WiLink 8 (WL1835MOD on BBBW)
- **Standards**: 802.11 b/g/n
- **Bluetooth**: 4.1 (BBBW), 4.2 (BeagleBone AI)

**Configuration**:
```bash
# Configure WiFi
sudo connmanctl
  connmanctl> enable wifi
  connmanctl> scan wifi
  connmanctl> connect wifi_<SSID>_<MAC> <password>
```

## Performance

### CPU Performance

| Model | CPU | Cores | Clock | Performance |
|-------|-----|-------|-------|-------------|
| BBB | AM3358 | 1 | 720MHz | ~0.1 DMIPS/MHz |
| BBB | AM3358 | 1 | 1GHz | ~0.1 DMIPS/MHz |
| BBBAI | AM5729 | 2x A15 | 1.5GHz | ~0.25 DMIPS/MHz |

**Note**: AM5729 has asymmetric multiprocessing (2x Cortex-A15 + 2x PRU + 2x DSP)

### Memory Performance

| Model | RAM | Bandwidth | Type |
|-------|-----|-----------|------|
| BBB | 256MB | ~2GB/s | DDR3 |
| BBB | 512MB | ~2GB/s | DDR3L |
| BBBAI | 1GB | ~4GB/s | DDR3L |

### PRU Performance

| Feature | Latency | Throughput |
|---------|--------|------------|
| GPIO toggle | 5ns | 200MHz |
| UART (PRU) | < 1µs | 12Mbps |
| SPI (PRU) | < 1µs | 48Mbps |
| eCAP input | < 10ns | 200MHz |

## Real-Time Capabilities

### Real-Time Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **PRU** | Deterministic co-processor | Real-time I/O, protocol handling |
| **eCAP** | Enhanced Capture | Encoder counting, frequency measurement |
| **ePWM** | Enhanced PWM | Motor control, power conversion |
| **eQEP** | Enhanced QEP | Quadrature encoder reading |
| **McASP** | Audio Serial Port | Audio, high-speed data |
| **Hardware timers** | Precise timing | Scheduling, time measurement |
| **Interrupts** | Low-latency response | Event handling |

### Real-Time OS Options

- **Xenomai**: Real-time extension for Linux
- **RTAI**: Real-Time Application Interface
- **PREEMPT_RT**: Real-time patch for Linux kernel
- **FreeRTOS**: On PRU (bare metal)
- **Zephyr**: Real-time OS (can run on PRU)

**Xenomai example**:
```bash
# Install Xenomai
sudo apt install xenomai xenomai-runtime

# Test latency
sudo /usr/xenomai/bin/latency
```

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| PRU not running | Real-time tasks not executing | Check PRU firmware, verify remoteproc |
| Cape not detected | Cape features not available | Check EEPROM, verify I2C pull-ups |
| GPIO not working | Input/output not functioning | Check device tree overlay, verify pinmux |
| ADC noise | Inaccurate readings | Use proper grounding, add capacitors |
| Ethernet slow | Limited to USB bus | Use BeagleBone AI for Gigabit |
| WiFi not working | No connectivity | Check antenna, verify WiFi module |
| Power issues | Random reboots, instability | Use proper power supply, check voltage |
| Thermal throttling | Performance degradation | Add heat sink, improve airflow |
| eMMC corruption | Boot failure | Use proper shutdown, add write protection |
| CAN not working | No communication | Check transceiver, verify bit rate |

## Best Practices

- **Use PRU for real-time tasks**: Offload time-critical operations from Linux
- **Leverage device tree overlays**: Configure pins properly before use
- **Check cape compatibility**: Verify cape works with your BeagleBone model
- **Use proper power**: BeagleBone needs stable 5V power
- **Implement proper shutdown**: Use `sudo shutdown -h now` before power off
- **Monitor temperature**: Use `cat /sys/class/thermal/thermal_zone0/temp`
- **Use heat sinks**: For sustained CPU load
- **Backup eMMC**: Use `dd` to backup eMMC to file
- **Update regularly**: `sudo apt update && sudo apt upgrade`
- **Use UPS**: For gracefully handling power outages
- **Secure SSH**: Disable password login, use SSH keys
- **Use cape EEPROM**: Always include EEPROM for cape identification
- **Test PRU code**: Verify PRU firmware before deployment
- **Document pin usage**: Keep track of which pins are used for what

## Standing Rules

- **PRU is the secret sauce** — if your application needs deterministic
  timing, the PRU is the answer; Linux is not real-time.
- **Device tree overlays are the configuration** — the hardware is
  fixed; the software configures it; get the overlay right first.
- **Cape EEPROM is mandatory** — a cape without EEPROM is a board with
  a manual; a cape with EEPROM configures itself.
- **3.3V on GPIO** — BeagleBone GPIO is 3.3V; 5V requires level shifting
  or special handling.
- **eMMC is not infinite** — it wears; use it wisely, backup
  regularly, and consider read-only mode for embedded.
- **The AM335x has limited RAM** — 512MB is plenty for most tasks,
  but heavy applications need memory management.
- **USB and Ethernet share a bus on BBB** — total bandwidth is
  limited; BeagleBone AI separates them.
- **Real-time means PRU** — for true real-time, the PRU is the only
  option; Linux with PREEMPT_RT is better, but still not hard real-time.
