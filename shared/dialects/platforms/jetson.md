---
type: platform
family: sbc
---

# NVIDIA Jetson

AI at the edge: a family of **AI-optimized** single-board computers
and modules designed for embedded machine learning, computer vision,
and high-performance computing at low power. GPU-accelerated,
CUDA-enabled, and TensorRT-optimized.

## Eras

The era is declared by the **Jetson module** and **SoC generation**.
Each era brings a step change in AI performance and power efficiency.

### Jetson Nano Era (2019)
- **Nano Developer Kit**: 4x Cortex-A57 @ 1.43GHz, 128-core Maxwell GPU
- **Nano Module**: Same SoC in module form (260-pin SODIMM)
- **Performance**: 472 GFLOPS (FP16), INT8
- **Power**: 5W-10W
- **Use case**: Entry-level AI, education, prototyping

### Jetson Xavier NX Era (2020)
- **Xavier NX Developer Kit**: 6x Cortex-A72 @ 1.9GHz, 384-core Volta GPU
- **Xavier NX Module**: Same SoC in module form (260-pin SODIMM)
- **Performance**: 6 TFLOPS (FP16), 21 TOPS (INT8)
- **Power**: 10W-15W
- **Use case**: Embedded AI, robotics, industrial

### Jetson Orin Era (2022-2024)
- **Orin Nano Developer Kit**: 6x Cortex-A78AE @ 1.5GHz, 1024-core Ampere GPU
- **Orin Nano Module**: Same SoC in module form (260-pin SODIMM)
- **Orin NX Developer Kit**: 8x Cortex-A78AE @ 1.6GHz, 1024-core Ampere GPU
- **Orin NX Module**: Same SoC in module form (260-pin SODIMM)
- **AGX Orin Developer Kit**: 12x Cortex-A78AE @ 2.2GHz, 2048-core Ampere GPU
- **AGX Orin Module**: Same SoC in module form (400-pin connector)
- **Performance**: Orin Nano: 20 TOPS (INT8), Orin NX: 40 TOPS, AGX Orin: 200 TOPS
- **Power**: Orin Nano: 7W-15W, Orin NX: 15W-30W, AGX Orin: 15W-60W
- **Use case**: High-performance edge AI, autonomous vehicles, medical devices

### Module Comparison

| Module | CPU | GPU | Performance | Power | Form Factor | Connectivity |
|--------|-----|-----|-------------|-------|-------------|--------------|
| Nano | 4x A57 @1.43GHz | Maxwell 128c | 472 GFLOPS | 5-10W | 260-pin SODIMM | USB, HDMI, CSI, DSI |
| Xavier NX | 6x A72 @1.9GHz | Volta 384c | 6 TFLOPS | 10-15W | 260-pin SODIMM | USB, HDMI, CSI, PCIe |
| Orin Nano | 6x A78AE @1.5GHz | Ampere 1024c | 20 TOPS | 7-15W | 260-pin SODIMM | USB, HDMI, CSI, PCIe |
| Orin NX | 8x A78AE @1.6GHz | Ampere 1024c | 40 TOPS | 15-30W | 260-pin SODIMM | USB, HDMI, CSI, PCIe |
| AGX Orin | 12x A78AE @2.2GHz | Ampere 2048c | 200 TOPS | 15-60W | 400-pin | USB, HDMI, CSI, PCIe |
| AGX Xavier | 8x A72 @2.2GHz | Volta 512c | 32 TFLOPS | 10-30W | 400-pin | USB, HDMI, CSI |

## AI Acceleration

### CUDA Architecture

All Jetson platforms support **NVIDIA CUDA**, enabling GPU-accelerated
computing for AI and parallel workloads.

| Module | CUDA Architecture | Compute Capability | FP16 | INT8 | Tensor Cores |
|--------|-------------------|--------------------|------|------|---------------|
| Nano | Maxwell | 5.3 | Yes | Yes | No |
| Xavier NX | Volta | 7.2 | Yes | Yes | Yes (INT8 only) |
| Orin Nano/NX | Ampere | 8.6 | Yes | Yes | Yes (FP16/INT8) |
| AGX Orin | Ampere | 8.6 | Yes | Yes | Yes (FP16/INT8) |
| AGX Xavier | Volta | 7.2 | Yes | Yes | Yes (INT8 only) |

### TensorRT

NVIDIA **TensorRT** is a high-performance deep learning inference
optimizer and runtime that maximizes throughput and minimizes latency.

**Features**:
- **Layer fusion**: Combine multiple layers into single operations
- **Precision calibration**: Optimize for INT8, FP16, or FP32
- **Kernel auto-tuning**: Find optimal implementations for each layer
- **Dynamic tensor shapes**: Support variable input sizes
- **Multi-stream execution**: Run multiple inference streams in parallel

**Performance**:
- **Jetson Nano**: ~10-20 FPS for ResNet-50 (FP16)
- **Xavier NX**: ~50-100 FPS for ResNet-50 (FP16)
- **Orin Nano**: ~100-200 FPS for ResNet-50 (FP16)
- **Orin NX**: ~200-400 FPS for ResNet-50 (FP16)
- **AGX Orin**: ~800-1600 FPS for ResNet-50 (FP16)

**TensorRT workflow**:
1. Convert model to ONNX format
2. Optimize with TensorRT converter
3. Calibrate for INT8 precision (optional)
4. Deploy on Jetson

**Example**:
```python
import tensorrt as trt

# Create builder and network
builder = trt.Builder(trt.Logger(trt.Logger.WARNING))
network = builder.create_network(1)
parser = trt.OnnxParser(network, builder.logger)

# Parse ONNX model
parser.parse_from_file("model.onnx")

# Configure and build
config = builder.create_builder_config()
config.set_max_workspace_size(1 << 20)  # 1MB
serialized_engine = builder.build_serialized_network(network, config)

# Save engine
with open("model.trt", "wb") as f:
    f.write(serialized_engine)
```

### JetPack SDK

**JetPack** is the complete software stack for Jetson, including:
- **Ubuntu** Linux distribution (customized for Jetson)
- **CUDA Toolkit** for GPU acceleration
- **cuDNN** for deep neural networks
- **TensorRT** for inference optimization
- **OpenCV** for computer vision
- **Multimedia APIs** for video encode/decode
- **L4T (Linux for Tegra)** kernel and drivers

**JetPack versions**:
- **JetPack 4.x**: For Jetson Nano, Xavier, Xavier NX
- **JetPack 5.x**: For Jetson Orin series, Xavier NX
- **JetPack 6.x**: For Jetson Orin series (latest)

**Installation**:
```bash
# Download JetPack from NVIDIA website
# Flash using SDK Manager or command line
sudo apt update
sudo apt install nvidia-jetpack
```

## Jetson-Specific Hardware

### Camera Interface (MIPI CSI-2)

Jetson platforms support **MIPI CSI-2** for high-speed camera input.

**Camera connectors**:
- **Jetson Nano**: 1x CSI-2 (2-lane)
- **Xavier NX**: 2x CSI-2 (2-lane each)
- **Orin Nano**: 2x CSI-2 (2-lane each)
- **Orin NX**: 4x CSI-2 (4-lane total)
- **AGX Orin**: 8x CSI-2 (8-lane total)

**Supported cameras**:
- **IMX219**: 8MP, 1080p30/720p60 (Raspberry Pi Camera Module v2 compatible)
- **IMX378**: 12MP, 4K30, 1080p120
- **IMX477**: 12.3MP, 4K60 (Raspberry Pi HQ Camera compatible)
- **IMX586**: 48MP, 8K30
- **IMX686**: 64MP, 4K30
- **AR0234**: 2.3MP global shutter
- **AR1335**: 1.3MP global shutter
- **Multiple cameras**: Supported via CSI-2 multiplexers

**Camera stack**:
- **libargus**: NVIDIA camera library
- **nvcamera**: Camera daemon
- **V4L2**: Video4Linux2 interface
- **GStreamer**: Multimedia framework

**Python camera (OpenCV)**:
```python
import cv2

# Open camera
cap = cv2.VideoCapture(0)  # or use GStreamer pipeline

# For MIPI camera
cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

while True:
    ret, frame = cap.read()
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**GStreamer pipeline**:
```bash
# View camera
nvgstcapture-1.0 --capture-auto

# Record video
gst-launch-1.0 nvcamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvvidconv ! video/x-raw, format=I420 ! filesink location=video.h264
```

### GPU

All Jetson platforms have **NVIDIA GPUs** with CUDA support.

**GPU specifications**:
- **Jetson Nano**: Maxwell GM20B, 128 CUDA cores, 1.0 GHz
- **Xavier NX**: Volta GV11B, 384 CUDA cores, 1.1 GHz
- **Orin Nano/NX**: Ampere GA10B, 1024 CUDA cores, 0.95-1.3 GHz
- **AGX Orin**: Ampere GA10B, 2048 CUDA cores, 0.9-1.35 GHz

**GPU memory**:
- **Jetson Nano**: 4GB LPDDR4 shared with CPU
- **Xavier NX**: 8GB LPDDR4x shared with CPU
- **Orin Nano**: 4GB LPDDR5 shared with CPU
- **Orin NX**: 8GB LPDDR5 shared with CPU
- **AGX Orin**: 32GB LPDDR5 shared with CPU

**CUDA programming**:
```python
import numpy as np
import cupy as cp

# Create arrays on GPU
a_gpu = cp.array([1, 2, 3, 4, 5])
b_gpu = cp.array([5, 4, 3, 2, 1])

# Perform operations on GPU
c_gpu = a_gpu + b_gpu

# Transfer back to CPU (if needed)
c_cpu = cp.asnumpy(c_gpu)
```

### ISP (Image Signal Processor)

Jetson platforms have **hardware ISP** for camera image processing.

**ISP features**:
- **Auto Exposure**: Automatic exposure control
- **Auto White Balance**: Color correction
- **Auto Focus**: Focus adjustment (on supported cameras)
- **Noise Reduction**: Spatial and temporal noise reduction
- **HDR**: High Dynamic Range processing
- **3A**: Auto Exposure, Auto White Balance, Auto Focus

**ISP pipeline**:
- **Raw Bayer** → **Debayer** → **Color Correction** → **Gamma Correction** → **Denoise** → **Sharpen** → **Output**

**ISP controls**:
```python
# Using libargus
import libargus

# Create camera device
camera_device = libargus.CameraDevice()

# Get ISP settings
isp_settings = camera_device.get_isp_settings()

# Set exposure
isp_settings.exposure_time = 10000  # 10ms
camera_device.set_isp_settings(isp_settings)
```

### Video Encoder/Decoder

Jetson platforms have **hardware video encode/decode** accelerators.

**Video codecs**:
- **H.264/AVC**: Hardware encode and decode
- **H.265/HEVC**: Hardware decode (encode on some models)
- **VP8**: Hardware decode
- **VP9**: Hardware decode (on Orin series)
- **MJPEG**: Software encode/decode

**Performance**:
- **Jetson Nano**: 1x 1080p30 H.264 encode, 1x 1080p30 decode
- **Xavier NX**: 2x 1080p60 H.264 encode, 4x 1080p60 decode
- **Orin Nano**: 2x 4K30 H.264 encode, 4x 4K30 decode
- **Orin NX**: 4x 4K30 H.264 encode, 8x 4K30 decode
- **AGX Orin**: 8x 4K30 H.264 encode, 16x 4K30 decode

**Video encoding (GStreamer)**:
```bash
# Encode to H.264
gst-launch-1.0 nvcamerasrc ! video/x-raw(memory:NVMM), width=1920, height=1080, format=NV12, framerate=30/1 ! nvv4l2h264enc ! h264parse ! mp4mux ! filesink location=output.mp4
```

**Video decoding (GStreamer)**:
```bash
# Decode H.264
gst-launch-1.0 filesrc location=input.mp4 ! qtdemux ! h264parse ! nvv4l2decoder ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! autovideosink
```

## Connectivity

### USB

| Module | USB Ports | Version | Notes |
|--------|-----------|---------|-------|
| Nano | 4x Type-A | 2.0 + 1x 3.0 | 1x USB 3.0 (blue) |
| Xavier NX | 4x Type-A | 3.1 Gen1 | All USB 3.0 |
| Orin Nano | 4x Type-A | 3.1 Gen1 | All USB 3.0 |
| Orin NX | 4x Type-A | 3.1 Gen1 | All USB 3.0 |
| AGX Orin | 4x Type-A | 3.1 Gen1 + 1x Type-C | 4x USB 3.0 + 1x USB 3.1 Gen2 |

**USB features**:
- **Host mode**: Standard USB host
- **Device mode**: USB device (gadget mode) on some ports
- **OTG**: On-The-Go support

### Ethernet

| Module | Ethernet | Speed | Notes |
|--------|----------|-------|-------|
| Nano | None | - | USB Ethernet adapter required |
| Xavier NX | 1x RJ45 | 1Gbps | |
| Orin Nano | 1x RJ45 | 1Gbps | |
| Orin NX | 1x RJ45 | 1Gbps | |
| AGX Orin | 1x RJ45 | 1Gbps | |

**Ethernet performance**:
- **Jetson Xavier NX**: ~940Mbps (close to line rate)
- **Jetson Orin series**: ~940Mbps
- **AGX Orin**: ~940Mbps

### PCIe

| Module | PCIe | Lanes | Notes |
|--------|------|-------|-------|
| Nano | None | - | |
| Xavier NX | 1x M.2 Key E | 1x Gen2 | x1 link |
| Orin Nano | 1x M.2 Key E | 1x Gen2 | x1 link |
| Orin NX | 1x M.2 Key E | 1x Gen2 | x1 link |
| AGX Orin | 2x M.2 Key E + 1x M.2 Key M | 1x Gen3 + 4x Gen4 | x4 link on M.2 M |

**PCIe use cases**:
- **NVMe SSD**: High-speed storage
- **GPU expansion**: External GPU (limited support)
- **Capture cards**: Video capture
- **Network adapters**: 10G Ethernet, WiFi 6E
- **Custom accelerators**: FPGA, ASIC

**NVMe SSD**:
```bash
# Check NVMe devices
ls /dev/nvme*

# Mount NVMe SSD
sudo mkdir /mnt/nvme
sudo mount /dev/nvme0n1 /mnt/nvme
```

### HDMI

| Module | HDMI | Resolution | Notes |
|--------|------|------------|-------|
| Nano | 1x HDMI 2.0 | 4K30 | |
| Xavier NX | 1x HDMI 2.0 | 4K60 | |
| Orin Nano | 1x HDMI 2.0 | 4K60 | |
| Orin NX | 1x HDMI 2.0 | 4K60 | |
| AGX Orin | 1x HDMI 2.1 | 8K60 | |

### Display Interface (DSI)

| Module | DSI | Lanes | Notes |
|--------|-----|-------|-------|
| Nano | 1x DSI | 2-lane | |
| Xavier NX | 1x DSI | 2-lane | |
| Orin Nano | 1x DSI | 2-lane | |
| Orin NX | 2x DSI | 4-lane total | |
| AGX Orin | 2x DSI | 4-lane total | |

**DSI displays**:
- Official NVIDIA displays
- Custom DSI panels
- Raspberry Pi compatible displays (with adapter)

### GPIO

Jetson platforms have **GPIO** for general purpose I/O.

**GPIO specifications**:
- **Voltage**: 3.3V (1.8V on some pins)
- **Current**: 4mA per pin, 25mA per bank
- **Banks**: Multiple banks with different voltage domains
- **Pins**: Varies by module and carrier board

**GPIO access**:
```python
# Using Jetson.GPIO library (similar to RPi.GPIO)
import Jetson.GPIO as GPIO

# Setup
GPIO.setmode(GPIO.BOARD)  # or GPIO.BCM
GPIO.setup(18, GPIO.OUT)

# Output
GPIO.output(18, GPIO.HIGH)

# Input
state = GPIO.input(18)

# Cleanup
GPIO.cleanup()
```

**Note**: Jetson GPIO libraries vary by platform. Use:
- **Jetson.GPIO**: For Jetson Nano, Xavier NX
- **Jetsontx2-gpio**: For Orin series
- **Direct sysfs**: `/sys/class/gpio/`

### I2C

| Module | I2C Buses | Notes |
|--------|-----------|-------|
| Nano | 2x I2C | |
| Xavier NX | 2x I2C | |
| Orin Nano | 4x I2C | |
| Orin NX | 4x I2C | |
| AGX Orin | 4x I2C | |

**I2C usage**:
```bash
# Enable I2C
sudo apt install i2c-tools

# Scan I2C bus
sudo i2cdetect -y 0
```

### SPI

| Module | SPI Buses | Notes |
|--------|-----------|-------|
| Nano | 2x SPI | |
| Xavier NX | 4x SPI | |
| Orin Nano | 6x SPI | |
| Orin NX | 6x SPI | |
| AGX Orin | 6x SPI | |

### UART

| Module | UART Ports | Notes |
|--------|-------------|-------|
| Nano | 2x UART | |
| Xavier NX | 4x UART | |
| Orin Nano | 6x UART | |
| Orin NX | 6x UART | |
| AGX Orin | 8x UART | |

## Power Management

### Power Sources

| Module | Power Connector | Voltage | Current | Notes |
|--------|-----------------|---------|--------|-------|
| Nano Dev Kit | Barrel jack | 5V | 4A | 19V-5V DC-DC converter |
| Xavier NX Dev Kit | Barrel jack | 5V | 4A | 19V-5V DC-DC converter |
| Orin Nano Dev Kit | Barrel jack | 5V | 4A | 19V-5V DC-DC converter |
| Orin NX Dev Kit | Barrel jack | 5V | 4A | 19V-5V DC-DC converter |
| AGX Orin Dev Kit | Barrel jack | 5V | 5A | 19V-5V DC-DC converter |
| Nano Module | 260-pin SODIMM | 5V | 5A | |
| Xavier NX Module | 260-pin SODIMM | 5V | 10A | |
| Orin Nano Module | 260-pin SODIMM | 5V | 10A | |
| Orin NX Module | 260-pin SODIMM | 5V | 15A | |
| AGX Orin Module | 400-pin | 5V | 60A | |

**Power modes**:
- **10W mode**: Low power, reduced performance (Orin series)
- **15W mode**: Balanced power/performance (Orin series)
- **30W mode**: Maximum performance (Orin NX, AGX Orin)
- **60W mode**: Maximum performance (AGX Orin only)

**Configure power mode**:
```bash
# Check current power mode
sudo nvpmodel -q

# Set power mode
sudo nvpmodel -m 1  # 10W mode
sudo nvpmodel -m 2  # 15W mode
sudo nvpmodel -m 0  # Max mode
```

### Power Measurement

**Jetson has built-in power sensors**:

```bash
# View power consumption
sudo tegrapower

# Or
cat /sys/class/hwmon/hwmon0/power0_input  # Total power (microwatts)
cat /sys/class/hwmon/hwmon0/power1_input  # CPU power
cat /sys/class/hwmon/hwmon0/power2_input  # GPU power
```

### Thermal Management

**Temperature ranges**:
- **Operating**: 0°C to 80°C (recommended)
- **Throttling**: Starts at ~75°C
- **Shutdown**: ~85°C (configurable)

**Cooling options**:
- **Passive**: Heat sink included with dev kits
- **Active**: Fan with heat sink (recommended for sustained load)
- **Liquid**: For extreme overclocking

**Monitor temperature**:
```bash
# CPU temperature
cat /sys/class/thermal/thermal_zone0/temp

# GPU temperature
nvidia-smi -q -d TEMPERATURE

# All temperatures
sudo tegrapowermon
```

**Thermal throttling**:
```bash
# Check throttling status
sudo nvpmodel -q --verbose

# Or
sudo jetson_clocks
```

## Jetson Carrier Boards

### Developer Kits

- **Jetson Nano Developer Kit**: Reference design, 4x USB, HDMI, CSI, GPIO
- **Jetson Xavier NX Developer Kit**: Reference design, 4x USB 3.0, HDMI, CSI, PCIe
- **Jetson Orin Nano Developer Kit**: Reference design, 4x USB 3.0, HDMI, CSI, PCIe
- **Jetson Orin NX Developer Kit**: Reference design, 4x USB 3.0, HDMI, 2x CSI, PCIe
- **Jetson AGX Orin Developer Kit**: Reference design, 4x USB 3.0 + 1x USB-C, HDMI, 8x CSI, PCIe

### Third-Party Carrier Boards

| Carrier Board | Module | Features | Manufacturer |
|---------------|--------|----------|--------------|
| **Jetson Nano Baseboard** | Nano | Extended I/O, power | NVIDIA |
| **Xavier NX Baseboard** | Xavier NX | Extended I/O, M.2 | NVIDIA |
| **Orin Nano Carrier** | Orin Nano | M.2, multiple cameras | NVIDIA |
| **Connect Tech** | Nano/Xavier NX/Orin | Industrial, rugged | Connect Tech |
| **Aaeon** | Xavier NX/Orin | Industrial, wide temp | Aaeon |
| **Adlink** | Xavier NX/Orin | Industrial, PoE | Adlink |
| **Seeed** | Nano/Xavier NX | Maker-friendly | Seeed Studio |
| **SparkFun** | Nano | Maker-friendly | SparkFun |

## Performance Optimization

### Jetson Clocks

**Jetson has multiple clock domains**:
- **CPU clock**: ARM cores
- **GPU clock**: GPU cores
- **EMC clock**: Memory controller
- **Video clock**: Video encode/decode

**Configure clocks**:
```bash
# List available clock configurations
sudo jetson_clocks

# Set maximum clocks
sudo jetson_clocks --set MAXN

# Or manually
sudo nvpmodel -m 0  # Max mode
sudo jetson_clocks --set-on MAXN
```

### CUDA Optimization

**Best practices for Jetson**:
- **Use FP16**: When precision allows, FP16 is 2x faster than FP32
- **Use INT8**: For inference, INT8 is 4x faster than FP32 with minimal accuracy loss
- **Use Tensor Cores**: For compatible layers, Tensor Cores provide 4-8x speedup
- **Batch processing**: Process multiple inputs simultaneously for better GPU utilization
- **Memory coalescing**: Organize memory accesses for optimal performance
- **Asynchronous operations**: Overlap compute and memory transfers

**CUDA streams**:
```python
import cupy as cp

# Create streams
stream1 = cp.cuda.Stream()
stream2 = cp.cuda.Stream()

# Asynchronous operations
with stream1:
    result1 = cp.dot(a, b)
with stream2:
    result2 = cp.dot(c, d)

cp.cuda.Stream.null.synchronize()  # Wait for both
```

### Memory Management

**Jetson has limited memory bandwidth**:
- **Jetson Nano**: ~25GB/s
- **Xavier NX**: ~50GB/s
- **Orin Nano**: ~60GB/s
- **Orin NX**: ~100GB/s
- **AGX Orin**: ~200GB/s

**Memory optimization**:
- **Use pinned memory**: For GPU transfers
- **Minimize host-device transfers**: Process data on GPU
- **Use unified memory**: CUDA 6+ supports unified memory (managed memory)
- **Prefetch data**: Overlap computation with memory transfers

**Unified memory**:
```python
import cupy as cp

# Allocate unified memory
x = cp.cuda.alloc_pinned_memory(1024 * 1024)  # 1MB pinned memory
```

## Common Defects and Mitigations

| Defect | Impact | Mitigation |
|--------|--------|------------|
| Out of memory | Application crashes | Reduce batch size, use smaller models, free memory |
| CUDA errors | GPU operations fail | Check CUDA installation, verify GPU support |
| Camera not detected | No video input | Check CSI cable, verify camera module, enable ISP |
| Low performance | Slow inference | Use FP16/INT8, enable Tensor Cores, batch processing |
| Thermal throttling | Performance degradation | Add cooling, reduce power mode, optimize workload |
| Power issues | Random reboots | Use proper power supply, check power mode |
| PCIe not working | Device not detected | Check PCIe switch, verify lanes, check power |
| Ethernet slow | Limited bandwidth | Use USB Ethernet adapter for Nano |
| HDMI no signal | Display issues | Check resolution, HDMI cable, enable display |
| JetPack outdated | Security/compatibility issues | Update to latest JetPack version |

## Best Practices

- **Use TensorRT**: Always optimize models with TensorRT before deployment
- **Start with FP16**: For most AI workloads, FP16 provides best performance/precision tradeoff
- **Consider INT8**: For inference, INT8 can provide 4x speedup with minimal accuracy loss
- **Batch when possible**: Process multiple inputs simultaneously for better GPU utilization
- **Monitor temperature**: Use `tegrapowermon` or `nvidia-smi`
- **Use cooling**: Active cooling recommended for sustained load
- **Check power mode**: Use appropriate power mode for your workload
- **Update JetPack**: Regularly update to latest version for bug fixes and optimizations
- **Use official carrier**: For best compatibility, use official NVIDIA carrier boards
- **Secure Jetson**: Change default password, disable unused services, use firewall
- **Backup eMMC**: Use `dd` to backup eMMC to file
- **Use NVMe**: For high-speed storage, use NVMe SSD via PCIe
- **Implement proper shutdown**: Use `sudo shutdown -h now` before power off
- **Monitor resources**: Use `htop`, `nvidia-smi`, `tegrapowermon`
- **Test on target**: Always test AI models on actual Jetson hardware

## Standing Rules

- **TensorRT is not optional** — a model that is not optimized with
  TensorRT is a model that runs at half the speed it should.
- **FP16 is the default precision** — use FP32 only when FP16
  precision is insufficient; INT8 is for when FP16 is too slow.
- **The GPU has its own memory** — unified memory helps, but
  transferring data between CPU and GPU has a cost; minimize transfers.
- **CSI-2 is for cameras, HDMI is for displays** — they are not
  interchangeable; a CSI-2 camera cannot connect to HDMI.
- **PCIe is not on all models** — Nano has no PCIe; Xavier NX and
  Orin have PCIe; AGX Orin has the most.
- **Power mode affects performance** — 10W mode is quiet and cool,
  max mode is fast and hot; choose appropriately.
- **JetPack is the full stack** — CUDA, TensorRT, OpenCV, multimedia,
  all in one package; do not install pieces separately.
- **The dev kit is a reference, not a production board** — for
  deployment, use a carrier board that fits your application.
