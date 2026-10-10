---
type: platform
family: sbc
---

# Raspberry Pi

The Linux-based single-board computer that brought makers to the
cloud and the cloud to makers. A full computer with GPIO, designed
for education, experimentation, and embedded deployment.

## Eras

The era is declared by the **board model** and **SoC generation**.

**Pi 1 (2012)**: BCM2835 (ARM11, 700MHz), 256-512MB RAM, 26-pin GPIO
**Pi 2 (2015)**: BCM2836/BCM2837 (Cortex-A7, 900MHz), 1GB RAM, 40-pin GPIO
**Pi 3 (2016)**: BCM2837 (Cortex-A53, 1.2-1.4GHz), 1GB RAM, WiFi/BT
**Pi 4 (2019)**: BCM2711 (Cortex-A72, 1.5-1.8GHz), 1-8GB RAM, dual HDMI
**Pi 5 (2023)**: RP1 (Cortex-A76, 2.4GHz), 4-8GB RAM, PCIe 2.0 x1

**Compute Module series**:
- CM1/3/4: Pi 1/3/4 SoC in SODIMM form factor
- CM4S: CM4 without WiFi/BT for industrial use
- CM5: Pi 5 SoC in SODIMM form factor

**Pi Zero series**:
- Zero (2015): BCM2835, 512MB RAM, mini HDMI, micro USB
- Zero W (2017): Zero + WiFi/BT
- Zero 2 W (2021): BCM2837, 512MB RAM, WiFi/BT

**Pico series** (RP2040, not Linux):
- Pico: RP2040 dual-core Cortex-M0+, 2MB Flash, 26-pin GPIO
- Pico W: Pico + WiFi (CYW43439)
- Pico H: Pico with pre-soldered headers

## GPIO (General Purpose Input/Output)

### Pinout

The Raspberry Pi uses **Broadcom (BCM) pin numbering** internally.
Board pin numbers (physical) differ from BCM numbers (logical).

**40-pin header** (Pi 2/3/4/5, Zero, Zero W, Zero 2 W):
```
3V3  (1)  (2)  5V
SDA1 (3)  (4)  5V
SCL1 (5)  (6)  GND
GPIO4 (7)  (8)  TXD0 (GPIO14)
GND  (9)  (10) RXD0 (GPIO15)
GPIO17(11) (12) GPIO18
GPIO27(13) (14) GND
GPIO22(15) (16) GPIO23
3V3  (17) (18) GPIO24
MOSI (19) (20) GND
MISO (21) (22) GPIO25
SCLK (23) (24) CE0  (GPIO8)
GND  (25) (26) CE1  (GPIO7)
ID_SD(27) (28) ID_SC
GPIO5 (29) (30) GND
GPIO6 (31) (32) GPIO12
GPIO13(33) (34) GND
GPIO19(35) (36) GPIO16
GPIO26(37) (38) GPIO20
GND  (39) (40) GPIO21
```

**26-pin header** (Pi 1, early Pi 2):
- Same as top 26 pins of 40-pin header

### Pin Numbering Systems

| System | Example | Usage |
|--------|---------|-------|
| **BCM** | GPIO4, GPIO17 | Software libraries (preferred) |
| **Board** | Pin 7, Pin 11 | Physical pin numbers |
| **WiringPi** | wPi 0, wPi 4 | WiringPi library (deprecated) |

**Always use BCM numbering** in modern code (RPi.GPIO, pigpio, etc.)

### GPIO Voltage Levels

- **Output voltage**: 3.3V (NOT 5V tolerant)
- **Input tolerance**: 3.3V max (5V = damage)
- **Output current**: 16mA max per pin, 50mA total for all GPIO
- **Input leakage**: ~50μA per pin

### GPIO Functions

Each GPIO pin can be configured for different **alternate functions**:

| Pin | BCM | Alt Functions |
|-----|-----|---------------|
| 7,8 | 4,14 | UART0 TXD/RXD |
| 9,10 | 15,17 | UART0 RTS/CTS (Pi 3/4/5) |
| 11,12 | 17,18 | PCM_CLK, PCM_FS, PCM_DIN, PCM_DOUT |
| 19-21 | 10-11,9 | SPI0 MOSI/MISO/SCLK/CE0/CE1 |
| 23,24 | 11,8 | SPI0 CE0/CE1 |
| 26 | 7 | CE1 (SPI0) |
| 28-31 | 1,2,3,4 | I2C1 SDA/SCL, ARM_JTAG |
| 32,33 | 12,13 | PWM0, PWM1 |
| 35-38 | 16,20,26 | SPI1 CE2/CE1/CE0 |
| 36 | 16 | CTS1, RTS1 (UART1) |

**Note**: Alternate functions vary by Pi model and SoC

### Special Pins

| Pin | BCM | Function | Notes |
|-----|-----|----------|-------|
| 1,17 | - | 3V3 Power | 3.3V regulated |
| 2,4 | - | 5V Power | USB input voltage |
| 6,9,14,20,25,30,34,39 | - | Ground | Multiple GND pins |
| 27,28 | ID_SD, ID_SC | EEPROM | HAT identification |

## GPIO Usage Patterns

### Digital I/O

```python
import RPi.GPIO as GPIO

# Setup
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(17, GPIO.OUT)  # GPIO17 as output
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # GPIO18 with pull-up

# Output
GPIO.output(17, GPIO.HIGH)
GPIO.output(17, GPIO.LOW)

# Input
state = GPIO.input(18)

# Cleanup
GPIO.cleanup()
```

**Pitfalls**:
- Forgetting `GPIO.setmode()` causes wrong pins to be used
- Not cleaning up can leave pins in unknown state
- Using WiringPi numbering (deprecated) causes confusion

### PWM (Pulse Width Modulation)

**Hardware PWM**: Available on GPIO12, GPIO13, GPIO18, GPIO19
- **Frequency**: Up to ~19.2MHz (but practical limit lower)
- **Resolution**: 8-12 bits depending on frequency
- **Channel**: 2 channels on Pi 1-3, more on Pi 4/5

**Software PWM**: Available on all pins but less accurate
- **Limitations**: Jitter, CPU overhead, lower max frequency

```python
import pigpio

pi = pigpio.pi()
pi.set_PWM_frequency(18, 1000)  # 1kHz PWM on GPIO18
pi.set_PWM_dutycycle(18, 128)    # 50% duty cycle (0-255)
pi.stop()
```

### UART (Serial)

**UART0**: Primary UART (Linux console on Pi 1-3, Bluetooth on Pi 3-5)
- **Pins**: GPIO14 (TXD), GPIO15 (RXD)
- **Baud rates**: Up to 115200 (software-limited on Pi 1-3)
- **Usage**: Debug console, GPS, serial devices

**UART1**: Mini UART (only on Pi 2-5)
- **Pins**: GPIO14 (TXD), GPIO15 (RXD) — **shared with UART0**
- **Note**: Mini UART has limited FIFO (1 byte vs 16 bytes)

**UART2-6**: Additional UARTs (Pi 4/5, CM4/5)
- **Pins**: Various, check SoC datasheet
- **Usage**: Additional serial ports

**Configuration**:
```bash
# Disable serial console
sudo raspi-config
# Select: Interface Options → Serial → No → Yes

# Enable UART
sudo nano /boot/config.txt
# Add: enable_uart=1

# Reboot
sudo reboot
```

### SPI (Serial Peripheral Interface)

**SPI0**: Primary SPI bus
- **Pins**: MOSI (GPIO10), MISO (GPIO9), SCLK (GPIO11), CE0 (GPIO8), CE1 (GPIO7)
- **Speed**: Up to 125MHz (practical limit ~20MHz)
- **Usage**: Flash memory, displays, sensors

**SPI1**: Secondary SPI bus (Pi 4/5 only)
- **Pins**: MOSI (GPIO20), MISO (GPIO19), SCLK (GPIO21), CE0 (GPIO18), CE1 (GPIO16), CE2 (GPIO17)

**Configuration**:
```bash
# Enable SPI
sudo raspi-config
# Select: Interface Options → SPI → Enable

# Or edit config.txt
sudo nano /boot/config.txt
# Add: dtparam=spi=on

# Reboot
sudo reboot
```

**Python SPI**:
```python
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # Bus 0, CS 0 (CE0)
spi.max_speed_hz = 1000000  # 1MHz
spi.mode = 0b00  # Mode 0

# Write/Read
resp = spi.xfer2([0x80, 0x00])  # Send 2 bytes, receive response

spi.close()
```

### I2C (Inter-Integrated Circuit)

**I2C0**: Primary I2C bus
- **Pins**: SDA (GPIO2), SCL (GPIO3)
- **Speed**: Standard (100kHz), Fast (400kHz), High-speed (3.4MHz)
- **Pull-ups**: 1.8kΩ built-in (can be disabled)

**I2C1**: Secondary I2C bus (Pi 2-5)
- **Pins**: SDA (GPIO0), SCL (GPIO1) — **Note**: GPIO0/1 also used for ID_EEPROM

**Configuration**:
```bash
# Enable I2C
sudo raspi-config
# Select: Interface Options → I2C → Enable

# Or edit config.txt
sudo nano /boot/config.txt
# Add: dtparam=i2c_arm=on,i2c_vc=on

# Install tools
sudo apt install i2c-tools

# Reboot
sudo reboot
```

**Scan I2C bus**:
```bash
sudo i2cdetect -y 0  # Bus 0
sudo i2cdetect -y 1  # Bus 1
```

**Python I2C**:
```python
import smbus2

bus = smbus2.SMBus(1)  # Bus 1
address = 0x68  # Device address

# Read byte
data = bus.read_byte(address)

# Write byte
bus.write_byte(address, 0x10, 0x05)

bus.close()
```

## Display Interfaces

### HDMI
- **Primary display**: HDMI0 (all models)
- **Secondary display**: HDMI1 (Pi 4/5 only)
- **Resolution**: Up to 4K60 (Pi 4/5 with proper configuration)
- **Audio**: HDMI audio output

**Configuration**:
```bash
# Set resolution in config.txt
sudo nano /boot/config.txt
# Add: hdmi_group=2, hdmi_mode=82  # 4K60
# Or: hdmi_group=1, hdmi_mode=16  # 1080p60

# Force HDMI output
sudo nano /boot/config.txt
# Add: hdmi_force_hotplug=1, hdmi_drive=2
```

### DSI (Display Serial Interface)
- **Pins**: 15-pin FPC connector
- **Usage**: Official Raspberry Pi touchscreen display
- **Resolution**: Up to 1080p
- **Touch**: Resistive or capacitive touch support

**Configuration**:
```bash
# Enable DSI display
sudo raspi-config
# Select: Display Options → DSI Display → Enable
```

### CSI (Camera Serial Interface)
- **Pins**: 22-pin FPC connector (CSI-2)
- **Usage**: Raspberry Pi Camera Module
- **Resolution**: Up to 12MP (depending on camera module)
- **Multiple cameras**: Pi 4/5 supports 2 cameras, CM4/5 supports up to 4

**Configuration**:
```bash
# Enable camera
sudo raspi-config
# Select: Interface Options → Camera → Enable

# Or edit config.txt
sudo nano /boot/config.txt
# Add: camera_auto_detect=1
```

**Python camera**:
```python
from picamera2 import Picamera2

picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)

picam2.start()
# Capture image
picam2.capture_file("test.jpg")
picam2.stop()
```

## HATs (Hardware Attached on Top)

### HAT Specification
- **ID EEPROM**: 24C02 I2C EEPROM on ID_SD (GPIO0) and ID_SC (GPIO1)
- **Format**: Structured data in EEPROM describing HAT
- **GPIO usage**: HATs declare which GPIO pins they use
- **Power**: Can request specific power pins

**EEPROM layout**:
- Vendor info, product name, product version
- GPIO map (which pins used and for what)
- Driver location (if applicable)

### Auto-Configuration
- Pi reads HAT EEPROM on boot
- Automatically loads drivers if available
- Prevents GPIO conflicts

**View HAT info**:
```bash
sudo apt install python3-gpiozero python3-pip
pip install raspberrypi-hat
python3 -m raspberrypi_hat
```

### Popular HATs
- **Sense HAT**: Sensor array (IMU, pressure, humidity, temp, joystick, LED matrix)
- **Touch Display HAT**: LCD with touchscreen
- **PoE HAT**: Power over Ethernet
- **Audio HAT**: High-quality audio input/output
- **TV HAT**: DVB-T TV tuner
- **Relay HAT**: Multiple relay outputs

## Power Management

### Power Sources
| Source | Voltage | Current | Notes |
|--------|---------|--------|-------|
| USB-C | 5V | Up to 3A (Pi 4/5) | Primary power source |
| Micro USB | 5V | Up to 2.5A | Pi 1-3, Zero |
| GPIO 5V | 5V | Up to 3A | From USB or other 5V source |
| GPIO 3V3 | 3.3V | Up to 50mA total | Regulated from 5V |
| PoE | 5V | Up to 2.5A | Via PoE HAT |

### Power Requirements

| Model | Idle | Typical | Max |
|-------|------|---------|-----|
| Pi Zero | 150mA | 300mA | 1A |
| Pi 3 | 300mA | 600mA | 2.5A |
| Pi 4 | 400mA | 800mA | 3A |
| Pi 5 | 500mA | 1A | 5A |

**Note**: Current draw increases with CPU load, peripherals, and USB devices

### Power Issues

**Symptoms**:
- Rainbows on HDMI (low voltage)
- SD card corruption
- USB device disconnection
- Ethernet dropout
- Random reboots

**Solutions**:
- Use official power supply (5V/3A for Pi 4/5)
- Use high-quality USB cable
- Avoid powering Pi from PC USB port
- Add decoupling capacitors
- Use PoE HAT for reliable power

## Boot Modes

### SD Card Boot
- **Primary**: Boot from microSD card
- **Requirement**: SD card with Raspberry Pi OS
- **Limitation**: SD card speed can be bottleneck

### USB Mass Storage Boot
- **Pi 4/5, CM4/5**: Boot from USB SSD/HDD
- **Requirement**: USB 3.0 device with bootloader EEPROM update
- **Steps**:
  ```bash
  # Update EEPROM
  sudo apt update
  sudo apt full-upgrade
  sudo rpi-eeprom-update -a
  sudo reboot
  
  # Boot from USB
  sudo raspi-config
  # Select: Advanced Options → Boot Order → USB Boot
  ```

### USB OTG Boot (Pi Zero 2 W, Pi 4/5)
- **Host mode**: Pi acts as USB host
- **Device mode**: Pi acts as USB device

### PXE/Network Boot
- **Pi 3B+/4/5, CM3+/4/5**: Boot from network
- **Requirement**: TFTP server, DHCP, network configuration
- **Use case**: Diskless boot, centralized management

### Bootloader EEPROM
- **Pi 4/5**: Separate EEPROM for bootloader
- **Update**: `rpi-eeprom-update` tool
- **Recovery**: Hold BOOTSEL button while powering on

## Operating Systems

### Raspberry Pi OS
- **Lite**: Headless, minimal (recommended for embedded)
- **Desktop**: Full desktop with GUI
- **Full**: Desktop + recommended software

**32-bit vs 64-bit**:
- **32-bit**: Default, best compatibility
- **64-bit**: Available for Pi 3/4/5, better performance for 64-bit apps

**Installation**:
```bash
# Download imager
sudo apt install rpi-imager

# Or use dd
sudo dd if=2024-03-15-raspios-bookworm-arm64-lite.img.xz of=/dev/sdX bs=4M status=progress
```

### Other OS Options
- **Ubuntu**: Official Raspberry Pi build
- **Debian**: Standard Debian arm64/armhf
- **Fedora**: Fedora for ARM
- **Arch Linux ARM**: Arch for ARM devices
- **Gentoo**: Source-based distribution
- **OpenWrt**: Network router OS
- **FreeBSD**: FreeBSD for ARM
- **RISC OS**: Native ARM OS

## Connectivity

### Ethernet
- **Pi 1/2/3**: 10/100 Mbps (USB 2.0 bus)
- **Pi 4**: 1 Gbps (dedicated controller, USB 3.0 bus)
- **Pi 5**: 1 Gbps (dedicated PCIe controller)
- **PoE**: Supported via PoE HAT

### WiFi
- **Pi 3/4/5/Zero W/Zero 2 W**: Built-in 2.4GHz/5GHz (varies by model)
- **Pi 3**: BCM43438 (2.4GHz only)
- **Pi 4**: BCM43455 (2.4GHz + 5GHz)
- **Pi 5**: CYW43455 (2.4GHz + 5GHz)
- **Zero W**: BCM43438 (2.4GHz only)
- **Zero 2 W**: BCM43438 (2.4GHz only)

**Configuration**:
```bash
# Configure WiFi
sudo raspi-config
# Select: System Options → Wireless LAN

# Or edit directly
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
# Add:
#   network={
#       ssid="MyNetwork"
#       psk="MyPassword"
#   }
```

### Bluetooth
- **Pi 3/4/5/Zero W/Zero 2 W**: Built-in Bluetooth
- **Pi 3**: Bluetooth 4.1 (Classic + BLE)
- **Pi 4/5**: Bluetooth 5.0
- **Zero W/Zero 2 W**: Bluetooth 4.1

**Configuration**:
```bash
# Enable Bluetooth
sudo raspi-config
# Select: Interface Options → Bluetooth → Enable

# Bluetooth tools
bluetoothctl
#   power on
#   scan on
#   pair <MAC>
#   connect <MAC>
```

### USB
- **Pi 1/2/Zero**: 2 x USB 2.0
- **Pi 3**: 4 x USB 2.0
- **Pi 4**: 2 x USB 2.0 + 2 x USB 3.0
- **Pi 5**: 2 x USB 2.0 + 2 x USB 3.0
- **CM4/5**: 1 x USB 2.0 (on IO board)

### GPIO Connector Variants
- **Standard**: 40-pin header (most models)
- **Pi Zero**: 40-pin header (same as standard but smaller)
- **Compute Module**: 2 x 100-pin connectors (via IO board)

## Storage

### microSD Card
- **Primary storage** for most Pi models
- **Compatibility**: microSD, microSDHC, microSDXC
- **Performance**: Varies by card class (Class 10, UHS-I, UHS-II)
- **Capacity**: Up to 2TB (theoretical), 1TB+ tested

**Recommended cards**:
- **Samsung EVO Select**: Good balance of speed and reliability
- **SanDisk Extreme**: High performance
- **Samsung Pro Endurance**: High endurance for frequent writes

### USB Storage
- **USB 2.0**: Up to ~40MB/s
- **USB 3.0**: Up to ~100MB/s (Pi 4/5)
- **Usage**: External HDD/SSD for additional storage

### NVMe SSD (Pi 5, CM5)
- **PCIe 2.0 x1**: Up to ~500MB/s
- **Requires**: M.2 HAT or adapter
- **Usage**: High-speed storage for data-intensive applications

## Performance

### CPU Performance
| Model | CPU | Cores | Clock | Performance |
|-------|-----|-------|-------|-------------|
| Pi 1 | BCM2835 | 1 | 700MHz | 0.02 DMIPS/MHz |
| Pi 2 | BCM2836 | 4 | 900MHz | 0.05 DMIPS/MHz |
| Pi 3 | BCM2837 | 4 | 1.2-1.4GHz | 0.1 DMIPS/MHz |
| Pi 4 | BCM2711 | 4 | 1.5-1.8GHz | 0.15 DMIPS/MHz |
| Pi 5 | RP1 | 4 | 2.4GHz | 0.25 DMIPS/MHz |

**Note**: Pi 5 uses Cortex-A76 cores, significantly faster than previous models

### Memory Performance
| Model | RAM | Bandwidth | Type |
|-------|-----|-----------|------|
| Pi 1 | 256-512MB | ~1GB/s | LPDDR2 |
| Pi 2 | 1GB | ~2GB/s | LPDDR2 |
| Pi 3 | 1GB | ~2GB/s | LPDDR2 |
| Pi 4 | 1-8GB | ~4GB/s | LPDDR4 |
| Pi 5 | 4-8GB | ~8GB/s | LPDDR4X |

### Graphics Performance
| Model | GPU | OpenGL ES | Vulkan | Performance |
|-------|-----|-----------|--------|-------------|
| Pi 1-3 | VideoCore IV | 2.0 | No | 1-2 GFLOPS |
| Pi 4 | VideoCore VI | 3.1 | No | 6-8 GFLOPS |
| Pi 5 | VideoCore VII | 3.1 | Yes | 15-20 GFLOPS |

## Thermal Management

### Temperature Ranges
- **Operating**: 0°C to 70°C (recommended)
- **Extended**: -20°C to 85°C (with derating)
- **Shutdown**: ~85°C (configurable)
- **Throttling**: Starts at ~70°C

### Cooling Options
- **Passive**: Heat sink, thermal pads
- **Active**: Fan with heat sink
- **Liquid**: For extreme overclocking

**Monitor temperature**:
```bash
# CPU temperature
vcgencmd measure_temp

# Or
cat /sys/class/thermal/thermal_zone0/temp

# Throttling status
vcgencmd get_throttled
```

### Overclocking
- **Pi 4**: CPU up to 2.0GHz, GPU up to 750MHz
- **Pi 5**: CPU up to 3.0GHz (with active cooling)
- **Configuration**: Edit `/boot/config.txt`

**Example overclock**:
```
# Pi 4
arm_freq=2000
gpu_freq=750
over_voltage=6

# Pi 5
arm_freq=2800
over_voltage=8
```

**Warning**: Overclocking voids warranty and may reduce lifespan

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| SD card corruption | Boot failure, data loss | Use high-quality card, enable read-only mode, regular backups |
| Power issues | Rainbows, crashes, SD corruption | Use official PSU, high-quality cable, avoid PC USB |
| Thermal throttling | Performance degradation | Add heat sink, fan, improve airflow, reduce load |
| GPIO damage | Permanent damage | Use level shifters for 5V, respect current limits |
| UART conflicts | Serial console not working | Disable serial console, configure UART properly |
| SPI/I2C not working | Communication errors | Enable interfaces in raspi-config, check wiring |
| HDMI no signal | Display issues | Check resolution, HDMI mode, cable, power |
| Camera not detected | No video input | Enable camera, check CSI cable, verify camera module |
| WiFi/Bluetooth issues | No connectivity | Check antenna, interference, channel, power |
| USB device not working | Power or driver issue | Check power supply, use powered hub, install drivers |
| Ethernet slow | Limited to USB 2.0 bus | Use Pi 4/5 for Gigabit, or use USB Ethernet adapter |

## Best Practices

- **Use official power supply**: 5V/3A for Pi 4/5, 5V/2.5A for Pi 3
- **Use high-quality microSD**: Class 10 or UHS-I, minimum 16GB
- **Enable SSH on first boot**: Add `ssh` file to boot partition
- **Configure WiFi on first boot**: Add `wpa_supplicant.conf` to boot partition
- **Use static IP or DHCP reservation**: For reliable network access
- **Set timezone**: `sudo raspi-config` → Localisation Options
- **Update regularly**: `sudo apt update && sudo apt full-upgrade`
- **Backup SD card**: Use `dd` or Raspberry Pi Imager
- **Use read-only filesystem**: For reliability in embedded applications
- **Monitor temperature**: Use `vcgencmd measure_temp`
- **Use heat sinks**: For sustained CPU load
- **Implement proper shutdown**: Use `sudo shutdown -h now` before power off
- **Use UPS**: For gracefully handling power outages
- **Secure SSH**: Disable password login, use SSH keys
- **Firewall**: Use `ufw` for basic protection
- **Regular backups**: Backup important data and configurations

## Standing Rules

- **The BCM number is the truth** — board numbers change between models;
  the Broadcom GPIO number is the constant contract.
- **3.3V only on GPIO** — 5V on GPIO is damage; level shift if
  needed, or use a different approach.
- **SD card is not a hard drive** — expect wear; use read-only mode
  for embedded or add a real filesystem for heavy writes.
- **Power is the first thing to check** — rainbows, SD corruption,
  and random reboots are power problems until proven otherwise.
- **The official power supply is not optional** — a phone charger is
  not a Pi power supply; use the right tool for the job.
- **SSH is the remote shell** — enable it on first boot; a Pi without
  SSH is a Pi you will walk to.
- **Camera and display share CSI/DSI** — but not the same connector;
  CSI is for cameras, DSI is for displays.
- **USB and Ethernet share a bus on Pi 1-3** — total bandwidth is
  limited; Pi 4/5 separates them.
