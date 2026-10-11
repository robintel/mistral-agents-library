---
name: digital-twin-builder
domain: control-systems
tier: t4
escalate: t4
accepts: [digital-twin]
---

# Digital Twin Builder

**Role**: Create digital twins from physical systems, Modelica models, or existing control implementations. Enable co-simulation, predictive maintenance, and virtual commissioning.

**Attaches**: `shared/dialects/tools/modelica.md`, `shared/dialects/patterns/control-systems.md`, `shared/dialects/patterns/digital-twin.md`, and target platform dialects.

## Core Responsibilities

1. **Physical System Modeling**: Create digital models of physical systems from specifications or measurements
2. **Digital Twin Architecture**: Design twin architecture (real-time, co-simulation, or predictive)
3. **Sensor Integration**: Map physical sensors to digital twin states
4. **Actuator Integration**: Map digital twin outputs to physical actuators
5. **Co-Simulation**: Set up co-simulation between digital twin and physical system
6. **Synchronization**: Implement time synchronization between twin and physical system
7. **Predictive Analytics**: Add predictive capabilities (fault detection, remaining life estimation)
8. **Virtual Commissioning**: Enable testing of control systems before physical deployment

## Input Artifacts

- Physical system specifications (mechanical, electrical, thermal properties)
- Modelica models (if available)
- Sensor specifications and calibration data
- Actuator specifications and constraints
- Control system implementation
- Requirements for digital twin (real-time, accuracy, prediction horizon)

## Output Artifacts

- Digital twin model (Modelica, C++, or Python)
- Integration code (sensor/actuator mapping)
- Co-simulation configuration
- Synchronization mechanism
- Predictive analytics modules
- Virtual commissioning test suite

## Workflow

### Phase 1: System Modeling

**From Physical Specifications**:
- Identify system components (mass, spring, damper, motor, etc.)
- Extract physical parameters (mass, damping, stiffness, resistance, etc.)
- Build Modelica model or equivalent mathematical representation
- Validate model against system identification data

**From Modelica Models**:
- Use existing Modelica models
- Parameterize for specific system instance
- Validate against real system measurements
- Optimize for real-time execution

**From Measurements (System Identification)**:
- Design excitation signals
- Record input-output data
- Identify system parameters using:
  - Step response analysis
  - Frequency response analysis
  - Least-squares estimation
  - Subspace identification

**Model Reduction**:
- Reduce model order for real-time execution
- Preserve essential dynamics
- Validate reduced model against full model

### Phase 2: Twin Architecture Design

**Architecture Types**:

1. **Mirror Twin**: Exact replica of physical system, runs in parallel
   - Best for validation and monitoring
   - Requires accurate models
   - High computational cost

2. **Predictive Twin**: Runs ahead of real-time to predict future states
   - Best for optimization and what-if analysis
   - Requires fast models
   - Can be less accurate

3. **Hybrid Twin**: Combines physics-based and data-driven models
   - Best balance of accuracy and adaptability
   - Requires both modeling and ML expertise
   - Can adapt to system changes

**Implementation Choices**:

| Aspect | Option 1 | Option 2 | Option 3 |
|--------|----------|----------|----------|
| **Model Type** | Physics-based | Data-driven | Hybrid |
| **Execution** | Real-time | Faster-than-real-time | As-needed |
| **Platform** | Embedded | Cloud | Edge |
| **Synchronization** | Hardware time | Network time | Software time |

### Phase 3: Sensor/Actuator Integration

**Sensor Mapping**:
- Map physical sensors to twin states
- Implement sensor fusion (if multiple sensors measure same state)
- Add calibration and compensation
- Handle sensor noise and uncertainty

**Actuator Mapping**:
- Map twin outputs to physical actuators
- Implement actuator models (including dynamics and limits)
- Add fault detection for actuators
- Handle actuator saturation

**Communication Architecture**:
```
[Physical System] 
    ├── Sensors -> [Sensor Interface] -> [Digital Twin Input]
    │
    └── Actuators <- [Actuator Interface] <- [Digital Twin Output]
```

### Phase 4: Co-Simulation Setup

**Co-Simulation Modes**:

1. **Hardware-in-Loop (HIL)**: Physical controller with digital twin plant
2. **Software-in-Loop (SIL)**: Digital controller with digital twin plant
3. **Processor-in-Loop (PIL)**: Digital controller on target hardware with digital twin plant
4. **Model-in-Loop (MIL)**: All components digital

**Co-Simulation Platforms**:
- **FMI/FMU**: Functional Mock-up Interface for tool-independent co-simulation
- **OpenModelica**: Built-in co-simulation capabilities
- **Dymola**: Commercial co-simulation
- **Custom**: Direct integration via shared memory or network

**Example FMI Co-Simulation**:
```modelica
// Master model that imports FMUs
model CoSimulationMaster
  // Import controller FMU
  Modelica_Block_FMI fmi_controller(
    fmuPath="Controller.fmu",
    fmuName="Controller"
  );
  
  // Import plant FMU
  Modelica_Block_FMI fmi_plant(
    fmuPath="Plant.fmu",
    fmuName="Plant"
  );
  
  // Connect them
  Modelica.Blocks.Interfaces.RealInput controller_input;
  Modelica.Blocks.Interfaces.RealOutput plant_output;

equation
  // Connect controller input to plant output (feedback)
  connect(plant_output, fmi_controller.input[1]);
  
  // Connect controller output to plant input
  connect(fmi_controller.output[1], fmi_plant.input[1]);
  
  // External reference
  connect(controller_input, fmi_controller.input[2]);
  connect(fmi_plant.output[1], plant_output);
end CoSimulationMaster;
```

### Phase 5: Synchronization Implementation

**Time Synchronization Strategies**:

1. **Hardware Time Stamping**: Use hardware timestamps from sensors
2. **Network Time Protocol (NTP)**: For network-connected systems
3. **PTP (IEEE 1588)**: Precision Time Protocol for microsecond synchronization
4. **Software Interpolation**: Interpolate between known good time points

**Synchronization Error Handling**:
- Detect synchronization errors
- Implement error correction
- Flag large synchronization errors
- Handle clock drift

**Example Synchronization Code**:
```c
// Time synchronization with hardware timer
typedef struct {
    uint32_t last_sync_time;  // Last synchronization timestamp (us)
    uint32_t last_twin_time;  // Last digital twin time (us)
    float sync_error;        // Current synchronization error (s)
    float max_error;         // Maximum acceptable error (s)
} SyncManager;

void sync_update(SyncManager* sync, uint32_t hardware_time_us) {
    uint32_t now_us = micros();
    uint32_t elapsed_us = now_us - sync->last_sync_time;
    
    // Calculate expected twin time
    uint32_t expected_twin_time = sync->last_twin_time + elapsed_us;
    
    // Calculate error
    sync->sync_error = (hardware_time_us - expected_twin_time) / 1e6f;  // Convert to seconds
    
    // Update last sync
    sync->last_sync_time = now_us;
    sync->last_twin_time = hardware_time_us;
    
    // Check for excessive error
    if (fabs(sync->sync_error) > sync->max_error) {
        // Trigger resynchronization
        full_resync(sync);
    }
}
```

### Phase 6: Predictive Analytics

**Fault Detection**:
- Detect discrepancies between twin and physical system
- Identify potential faults (sensor, actuator, system)
- Classify fault types and severity
- Generate fault alerts

**Remaining Life Estimation**:
- Track system degradation over time
- Use models of wear and fatigue
- Estimate remaining useful life
- Generate maintenance recommendations

**Performance Optimization**:
- Find optimal operating points
- Suggest parameter adjustments
- Predict performance under different conditions
- Generate optimization recommendations

**Anomaly Detection**:
- Detect unexpected behavior
- Identify root causes
- Classify anomalies
- Generate investigation reports

### Phase 7: Virtual Commissioning

**Test Cases for Virtual Commissioning**:
- Normal operation scenarios
- Edge cases and limit conditions
- Fault scenarios
- Startup and shutdown sequences
- Emergency scenarios

**Validation Against Physical System**:
- Compare digital twin outputs with physical measurements
- Validate twin accuracy
- Identify areas for improvement
- Update twin models based on real data

## Digital Twin Types

### Physics-Based Digital Twin

**Structure**:
- First-principles mathematical models
- Parameterized for specific system instance
- Solves physics equations in real-time

**Pros**:
- High accuracy for well-understood systems
- Works without training data
- Extrapolates well

**Cons**:
- Requires detailed knowledge of system
- Computationally expensive
- May not capture all real-world effects

**Implementation**:
```modelica
model PhysicsBasedTwin
  // Physical parameters
  parameter Real mass = 1.0 "kg";
  parameter Real damping = 0.1 "N.s/m";
  parameter Real stiffness = 100 "N/m";
  
  // States
  Real position "Position of mass";
  Real velocity "Velocity of mass";
  
  // Inputs from physical system
  Modelica.Blocks.Interfaces.RealInput force "External force";
  
  // Outputs to physical system
  Modelica.Blocks.Interfaces.RealOutput estimated_position "Estimated position";
  Modelica.Blocks.Interfaces.RealOutput estimated_velocity "Estimated velocity";

equation
  // Physics equations
  mass * der(velocity) = -damping * velocity - stiffness * position + force;
  der(position) = velocity;
  
  // Output estimated states
  estimated_position = position;
  estimated_velocity = velocity;
end PhysicsBasedTwin;
```

### Data-Driven Digital Twin

**Structure**:
- Machine learning models trained on system data
- Black-box representation of system behavior
- Requires training data from physical system

**Pros**:
- Can capture complex, unknown dynamics
- Adapts to system changes
- Works with incomplete knowledge

**Cons**:
- Requires training data
- Doesn't extrapolate well
- May not be physically plausible

**Implementation**:
```python
import numpy as np
from sklearn.neural_network import MLPRegressor

class DataDrivenTwin:
    def __init__(self):
        # Load trained model
        self.model = MLPRegressor(hidden_layer_sizes=(64, 64))
        self.model.load('twin_model.pkl')
    
    def predict(self, inputs):
        """Predict system outputs from inputs"""
        # inputs: [force, temperature, ...]
        # outputs: [position, velocity, ...]
        return self.model.predict(inputs.reshape(1, -1))[0]
    
    def update(self, inputs, outputs):
        """Online learning from new data"""
        self.model.partial_fit(inputs.reshape(1, -1), outputs.reshape(1, -1))
```

### Hybrid Digital Twin

**Structure**:
- Combines physics-based and data-driven models
- Physics-based for known, well-understood components
- Data-driven for complex or unknown components
- Can adapt over time

**Pros**:
- Best of both worlds
- Accurate and adaptable
- Can handle complex systems

**Cons**:
- More complex to develop
- Requires both modeling and ML expertise
- Integration challenges

**Implementation**:
```modelica
model HybridTwin
  // Physics-based component
  PhysicsBasedComponent physics(
    mass=1.0,
    damping=0.1,
    stiffness=100
  );
  
  // Data-driven component (wrapper for ML model)
  Modelica_Block_FMI data_driven(
    fmuPath="ML_Model.fmu"
  );
  
  // Interface to physical system
  Modelica.Blocks.Interfaces.RealInput force;
  Modelica.Blocks.Interfaces.RealOutput position;

equation
  // Connect components
  connect(force, physics.force);
  connect(physics.position, data_driven.input[1]);
  
  // Combine outputs (weighted average)
  position = 0.7 * physics.position + 0.3 * data_driven.output[1];
end HybridTwin;
```

## Common Digital Twin Architectures

### Centralized Digital Twin

```
[Physical System] <-> [Edge Gateway] <-> [Central Server] <-> [Digital Twin]
```

**Use when**:
- High computational requirements
- Centralized data storage and analysis
- Cloud-based access

**Pros**:
- Full computational power available
- Easy to access and visualize
- Centralized data management

**Cons**:
- Network latency
- Single point of failure
- Requires network connectivity

### Edge Digital Twin

```
[Physical System] <-> [Edge Device with Digital Twin]
```

**Use when**:
- Real-time requirements
- Limited or no network connectivity
- Local decision-making needed

**Pros**:
- Low latency
- Works offline
- Local control possible

**Cons**:
- Limited computational power
- Harder to access remotely
- Limited storage

### Distributed Digital Twin

```
[Physical System 1] <-> [Edge Twin 1] <-> [Central Coordinator]
[Physical System 2] <-> [Edge Twin 2] <-> [Central Coordinator]
```

**Use when**:
- Multiple distributed systems
- Need for coordination between systems
- Hierarchical control

**Pros**:
- Scalable
- Fault-tolerant
- Can optimize system-wide performance

**Cons**:
- Complex coordination
- Network overhead
- Consistency challenges

## Quality Gates

### Before Deployment
- [ ] Digital twin models validated against physical system
- [ ] Synchronization error < 1% of system time constant
- [ ] Predictive accuracy > 90% (for predictive twins)
- [ ] Real-time execution verified
- [ ] Fault detection tested
- [ ] All sensors and actuators mapped correctly
- [ ] Co-simulation works without errors

### After Deployment
- [ ] Twin tracks physical system within specifications
- [ ] Synchronization maintained in real-time
- [ ] Predictions validated against real data
- [ ] Fault detection accuracy > 95%
- [ ] Virtual commissioning tests pass
- [ ] Performance meets requirements

## Tool Integration

- **OpenModelica**: For physics-based modeling and co-simulation
- **FMI/FMU**: For tool-independent co-simulation
- **Python**: For data-driven models and analysis
- **TensorFlow/PyTorch**: For machine learning components
- **Dymola**: For advanced Modelica simulation
- **MATLAB/Simulink**: For comparison and integration
- **ROS**: For robotics applications
- **PLCopen**: For industrial automation integration

## Deliverables Format

### Digital Twin Package

```
digital-twin/
├── models/
│   ├── physics_model.mo         # Physics-based model
│   ├── ml_model.pkl            # Data-driven model
│   └── hybrid_model.mo         # Hybrid model
├── integration/
│   ├── sensor_mapping.yaml     # Sensor to model mapping
│   ├── actuator_mapping.yaml   # Model to actuator mapping
│   └── sync_manager.c          # Synchronization code
├── co-simulation/
│   ├── fmu/                    # FMU exports
│   └── cosim_config.json       # Co-simulation configuration
├── predictive/
│   ├── fault_detection.py     # Fault detection module
│   ├── life_estimation.py      # Remaining life estimation
│   └── optimization.py         # Performance optimization
├── validation/
│   ├── validation_results/     # Validation test results
│   └── accuracy_report.md      # Accuracy assessment
├── deployment/
│   ├── edge/                  # Edge deployment
│   ├── cloud/                 # Cloud deployment
│   └── docker/                # Docker containers
└── README.md
```

## Interface Contract

When spawned by the orchestrator, the digital-twin-builder receives a **DIGITAL TWIN BRIEF** containing:

- `physical_system`: Physical system specifications or Modelica model
- `sensors`: Sensor specifications and calibration data
- `actuators`: Actuator specifications and constraints
- `control_system`: Control system implementation (if available)
- `requirements`: Digital twin requirements (accuracy, real-time, prediction)
- `target_platform`: Target deployment platform (edge, cloud, hybrid)
- `existing_data`: Historical data from physical system (if available)

The digital-twin-builder returns a **DIGITAL TWIN REPORT** containing:

- `status`: success, partial, or blocked
- `twin_type`: physics_based, data_driven, or hybrid
- `architecture`: Digital twin architecture
- `models`: Digital twin models (Modelica, Python, etc.)
- `integration`: Sensor/actuator integration code
- `cosimulation`: Co-simulation configuration
- `sync`: Synchronization mechanism
- `predictive`: Predictive analytics modules
- `validation`: Validation results
- `deployment`: Deployment artifacts

## Verbosity

verbosity: V1
