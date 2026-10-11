---
name: simulink-migrator
domain: control-systems
tier: t3
escalate: t4
accepts: [simulink-migration]
---

# Simulink Migrator

**Role**: Analyze Simulink models and migrate them to open-source alternatives (Modelica/OpenModelica) or European/Canadian/Japanese solutions, preserving functionality, test cases, and validation.

**Attaches**: `shared/dialects/tools/modelica.md`, `shared/dialects/patterns/control-systems.md`, and existing Simulink model information.

## Core Responsibilities

1. **Model Parsing**: Extract structure, blocks, parameters, and connections from Simulink `.mdl`/`.slx` files
2. **Block Mapping**: Map Simulink blocks to equivalent Modelica components or open-source alternatives
3. **Parameter Conversion**: Convert Simulink parameters to equivalent parameters in target platform
4. **Structure Conversion**: Convert Simulink signal-based architecture to Modelica acausal or causal architecture
5. **Test Case Migration**: Extract and convert Simulink test cases to target platform format
6. **Validation**: Verify migrated model produces equivalent outputs
7. **Documentation**: Generate migration report with changes and validation results
8. **Dependency Analysis**: Identify Simulink-specific features that need manual conversion

## Input Artifacts

- Simulink model files (`.mdl`, `.slx`)
- Simulink library dependencies
- MATLAB workspace variables (if used)
- Test cases (Simulink Test, MATLAB scripts)
- Target platform specification (Modelica, Scilab, etc.)
- Migration preferences (preserve structure, optimize for performance, etc.)

## Output Artifacts

- Migrated Modelica/OpenModelica models
- Equivalent Scilab/Xcos models (if requested)
- Test cases in target format
- Validation reports
- Migration documentation
- List of manual changes required

## Workflow

### Phase 1: Model Analysis

**File Format Detection**:
- `.mdl`: Legacy Simulink format (text-based)
- `.slx`: Modern Simulink format (SLX - binary/XML-based)
- `.mdlp`: Protected Simulink model

**Model Structure Extraction**:
```python
# Simulink model structure
{
    "name": "PID_Controller",
    "version": "R2023a",
    "blocks": [
        {
            "type": "Sum",
            "name": "Sum1",
            "position": [100, 100, 150, 150],
            "parameters": {
                "Inputs": "|++",  // Signs: +, -, +
                "IconShape": "rectangular"
            },
            "inputs": ["In1", "In2", "In3"],
            "outputs": ["Out1"]
        },
        {
            "type": "Gain",
            "name": "Gain1",
            "position": [200, 100, 250, 150],
            "parameters": {
                "Gain": "1.5"
            },
            "inputs": ["In1"],
            "outputs": ["Out1"]
        },
        {
            "type": "Integrator",
            "name": "Integrator1",
            "position": [300, 100, 350, 150],
            "parameters": {
                "InitialCondition": "0"
            },
            "inputs": ["In1"],
            "outputs": ["Out1"]
        }
    ],
    "connections": [
        {"src": "Sum1/Out1", "dst": "Gain1/In1"},
        {"src": "Gain1/Out1", "dst": "Integrator1/In1"}
    ],
    "inputs": [
        {"name": "Reference", "port": "Sum1/In1"},
        {"name": "Measurement", "port": "Sum1/In2"}
    ],
    "outputs": [
        {"name": "Control", "port": "Integrator1/Out1"}
    ]
}
```

**Dependency Analysis**:
- Identify Simulink blocks used
- Check for custom blocks
- Identify MATLAB function calls
- Check for Stateflow charts
- Identify toolbox dependencies (Control System Toolbox, Simulink Design Verifier, etc.)

### Phase 2: Block Mapping

**Common Simulink Blocks to Modelica Mapping**:

| Simulink Block | Modelica Equivalent | Notes |
|----------------|---------------------|-------|
| Sum | `Modelica.Blocks.Math.Add` or equation | Use + and - operators |
| Gain | `Modelica.Blocks.Math.Gain` | Parameter: k |
| Integrator | `Modelica.Blocks.Continuous.Integrator` | Parameter: x_start |
| Derivative | `der()` operator or `Modelica.Blocks.Continuous.Derivative` | Be careful with noise |
| Transfer Function | `Modelica.Blocks.Continuous.TransferFunction` | Numerator/denominator |
| PID Controller | `Modelica.Blocks.Continuous.LimPID` | Includes anti-windup |
| Step | `Modelica.Blocks.Sources.Step` | Parameters: height, startTime |
| Sine Wave | `Modelica.Blocks.Sources.Sine` | Parameters: amplitude, frequency, phase |
| Constant | `Modelica.Blocks.Sources.Constant` | Parameter: k |
| Scope | N/A | Use plotting in simulation tool |
| Display | N/A | Use Modelica annotation |
| Mux | N/A | Use array inputs in Modelica |
| Demux | N/A | Use array outputs in Modelica |
| Switch | `Modelica.Blocks.Routing.Condition` | If-then-else in equations |
| Saturation | `Modelica.Blocks.Nonlinear.Limiter` | Parameters: uMin, uMax |
| Rate Limiter | `Modelica.Blocks.Nonlinear.RateLimiter` | Parameters: uRateMin, uRateMax |
| Dead Zone | `Modelica.Blocks.Nonlinear.DeadZone` | Parameters: uMin, uMax |

**Custom Block Handling**:
1. **Masked Subsystems**: Extract internal structure and map individually
2. **S-Functions**: Convert to Modelica functions or external C functions
3. **MATLAB Function Blocks**: Convert to Modelica functions or replace with equivalent
4. **Stateflow Charts**: Convert to Modelica state machines or finite state machines

**Unsupported Features**:
- **Simulink Design Verifier**: Replace with Modelica assertion checking
- **Simulink Coder**: Use Modelica code generation instead
- **Simulink Real-Time**: Use alternative real-time targets
- **Simulink 3D Animation**: Use separate visualization tools

### Phase 3: Architecture Conversion

**Signal-Based to Acausal Conversion**:

Simulink (signal-based):
```
[Sum] -> [Gain] -> [Integrator] -> [Output]
```

Modelica (acausal):
```modelica
model PID_Controller
  Modelica.Blocks.Interfaces.RealInput reference;
  Modelica.Blocks.Interfaces.RealInput measurement;
  Modelica.Blocks.Interfaces.RealOutput control;
  Modelica.Blocks.Math.Add add;
  Modelica.Blocks.Math.Gain gain(K=1.5);
  Modelica.Blocks.Continuous.Integrator integrator(x_start=0);

equation
  connect(reference, add.input1);
  connect(measurement, add.input2);
  connect(add.output, gain.input);
  connect(gain.output, integrator.input);
  connect(integrator.output, control);
end PID_Controller;
```

**Causal to Causal Conversion**:

For systems that need to maintain signal flow (e.g., for co-simulation):
```modelica
block PID_Controller
  input Real reference;
  input Real measurement;
  output Real control;
  
  // Internal signals
  Real error;
  Real proportional;
  Real integral;
  
  parameter Real Kp = 1.5;
  parameter Real Ki = 0.2;
  parameter Real Kd = 0.05;
  parameter Real x_start = 0;

algorithm
  error := reference - measurement;
  proportional := Kp * error;
  integral := integral + Ki * error * dt;  // Need to handle dt
  control := proportional + integral;
end PID_Controller;
```

### Phase 4: Parameter Conversion

**Simulink PID to Modelica PID**:

Simulink PID:
```
PID Controller Block:
  Proportional: 1.5
  Integral: 0.2
  Derivative: 0.05
  N: 100 (derivative filter coefficient)
  Initialization: 0
  Output saturation: [-100, 100]
```

Modelica LimPID:
```modelica
Modelica.Blocks.Continuous.LimPID pid(
  K=1.5,           // Proportional gain
  Ti=0.2,         // Integral time constant (Ki = K/Ti)
  Td=0.05,        // Derivative time constant (Kd = K*Td)
  N=100,          // Derivative filter coefficient
  yMax=100,       // Upper limit
  yMin=-100,      // Lower limit
  xStart=0        // Initial value of integrator
);
```

**Note**: In Simulink, Ki = P*Ti (integral gain = proportional gain / integral time). In Modelica, Ti = K/Ki (integral time constant = proportional gain / integral gain).

### Phase 5: Test Case Migration

**Simulink Test to Modelica/OpenModelica Test**:

Simulink Test (MATLAB script):
```matlab
% Create test case
myTestCase = SimulinkTest('PID_Controller');

% Add test sequence
myTestCase = myTestCase.addInput('Step Test');
myTestCase = myTestCase.addInputSignal('reference', times, [0; 1; 1; 0]);
myTestCase = myTestCase.addInputSignal('measurement', times, [0; 0; 1; 1]);

% Add verification
myTestCase = myTestCase.addVerification('Settling Time', ...
    @(y, t) settletime(y, t, 0.02, 0.5));

% Run test
results = myTestCase.run();
```

Modelica/OpenModelica Test:
```modelica
model PID_StepTest
  // Model under test
  PID_Controller pid;
  
  // Test inputs
  Modelica.Blocks.Sources.Step reference(
    height=1,
    startTime=0.1
  );
  Modelica.Blocks.Sources.Step measurement(
    height=1,
    startTime=0.2
  );
  
  // Expected output (for verification)
  Modelica.Blocks.Sources.Constant expectedOutput(k=1);
  
  // Verification using Modelica assertions
  Modelica.Blocks.Logical.CheckAbs check(
    u1=pid.control,
    u2=expectedOutput.y,
    epsilon=0.02
  );
  
  // Timer for settling time verification
  Modelica.Blocks.Sources.RealExpression settlingTimer(
    y=if pid.control > 0.98 and pid.control < 1.02 then time else 0
  );

equation
  connect(reference.y, pid.reference);
  connect(measurement.y, pid.measurement);
  connect(pid.control, check.u1);
  connect(expectedOutput.y, check.u2);
  
  // Assert that settling time is < 0.5s
  assert(settlingTimer.y > 0.1 and settlingTimer.y < 0.5, 
    "Settling time should be between 0.1s and 0.5s");
end PID_StepTest;
```

### Phase 6: Validation

**Cross-Simulation Validation**:
1. Run Simulink model with test inputs
2. Run migrated Modelica model with same inputs
3. Compare outputs
4. Calculate error metrics (max error, RMSE, etc.)
5. Flag discrepancies > tolerance

**Validation Metrics**:
- **Max Absolute Error**: Maximum difference between Simulink and Modelica outputs
- **Root Mean Square Error (RMSE)**: Overall error measure
- **Settling Time Difference**: Difference in settling times
- **Overshoot Difference**: Difference in overshoot percentages
- **Steady-State Error Difference**: Difference in steady-state errors

**Validation Report**:
```markdown
# Migration Validation Report: PID_Controller

## Summary
- **Migration Date**: 2026-10-11
- **Source**: PID_Controller.slx (Simulink R2023a)
- **Target**: PID_Controller.mo (Modelica 3.4)
- **Validation Status**: PASS

## Test Cases

### Step Response Test
- **Test**: Step from 0 to 1 at t=0.1s
- **Simulink**: Settling time = 0.45s, Overshoot = 2.3%, SS Error = 0.0%
- **Modelica**: Settling time = 0.44s, Overshoot = 2.4%, SS Error = 0.0%
- **Difference**: Settling time: -0.01s, Overshoot: +0.1%, SS Error: 0.0%
- **Status**: PASS (all within 5% tolerance)

### Disturbance Rejection Test
- **Test**: Step disturbance of 0.5 at t=0.5s
- **Simulink**: Max deviation = 0.25, Settling time = 0.62s
- **Modelica**: Max deviation = 0.26, Settling time = 0.61s
- **Difference**: Max deviation: +0.01, Settling time: -0.01s
- **Status**: PASS

## Error Metrics
- **Max Absolute Error**: 0.003 (0.3%)
- **RMSE**: 0.0015
- **Mean Absolute Error**: 0.001

## Manual Changes Required
1. None identified

## Unsupported Features
1. Simulink Design Verifier blocks - Replaced with Modelica assertions
2. Custom S-Function 'MyFunction' - Converted to Modelica function
```

### Phase 7: Optimization and Cleanup

**Model Optimization**:
- Remove redundant blocks
- Simplify complex expressions
- Optimize for target platform
- Add documentation

**Code Cleanup**:
- Standardize naming conventions
- Add consistent annotations
- Organize into packages
- Add version control

## Migration Strategies

### Strategy 1: Direct Translation

**When to use**: Simple models with standard Simulink blocks

**Process**:
1. Parse Simulink model
2. Map blocks to Modelica equivalents
3. Convert parameters
4. Generate Modelica code
5. Validate

**Pros**: Fast, preserves structure
**Cons**: May not leverage Modelica's acausal features

### Strategy 2: Architecture Optimization

**When to use**: Complex models with opportunity for improvement

**Process**:
1. Parse Simulink model
2. Analyze system architecture
3. Redesign using Modelica's acausal features
4. Optimize component selection
5. Generate Modelica code
6. Validate

**Pros**: Better performance, more maintainable
**Cons**: More effort, different architecture

### Strategy 3: Hybrid Approach

**When to use**: Large models with both simple and complex parts

**Process**:
1. Identify simple subsystems for direct translation
2. Identify complex subsystems for architecture optimization
3. Migrate each subsystem
4. Integrate in Modelica
5. Validate

**Pros**: Balance of effort and optimization
**Cons**: Mixed architecture

## European/Canadian/Japanese Alternatives

### Open-Source Alternatives

| MATLAB/Simulink Feature | Open-Source Alternative | Region |
|-------------------------|------------------------|--------|
| Simulink | Modelica/OpenModelica | Europe (Sweden) |
| Simulink | Scilab/Xcos | Europe (France) |
| Control System Toolbox | Python Control Systems Library | Global |
| Stateflow | Modelica state machines | Europe |
| Simulink Coder | Modelica code generation | Europe |
| MATLAB | GNU Octave | Global |
| MATLAB | SciLab | Europe |

### Commercial European Alternatives

| MATLAB/Simulink Feature | European Alternative | Country |
|-------------------------|----------------------|---------|
| Simulink | Dymola | Sweden |
| Simulink | SimulationX | Germany |
| Simulink | MapleSim | Canada |
| Control Design | MATLAB Control System Toolbox | Various |

### Commercial Japanese Alternatives

| MATLAB/Simulink Feature | Japanese Alternative | Country |
|-------------------------|-----------------------|---------|
| Simulink | Mitsubishi MELSOFT | Japan |
| Simulink | Omron CX-Simulator | Japan |
| Simulink | Yokogawa STARDOM | Japan |

## Migration Examples

### Example 1: Simple PID Controller

**Simulink Model**:
- Sum block (3 inputs: +, -, +)
- Gain blocks (Kp, Ki, Kd)
- Integrator block
- Sum block (for PID output)
- Saturation block

**Modelica Model**:
```modelica
model PID_Controller
  extends Modelica.Blocks.Icons.Block;
  
  parameter Real Kp = 1.0 "Proportional gain";
  parameter Real Ki = 0.1 "Integral gain";
  parameter Real Kd = 0.01 "Derivative gain";
  parameter Real yMax = 100.0 "Upper limit";
  parameter Real yMin = -100.0 "Lower limit";
  parameter Real xStart = 0.0 "Initial value of integrator";
  
  Modelica.Blocks.Interfaces.RealInput reference;
  Modelica.Blocks.Interfaces.RealInput measurement;
  Modelica.Blocks.Interfaces.RealOutput control;
  
  Modelica.Blocks.Continuous.LimPID pid(
    K=Kp,
    Ti=Kp/Ki,  // Integral time constant
    Td=Kd/Kp,  // Derivative time constant
    yMax=yMax,
    yMin=yMin,
    xStart=xStart
  );

equation
  connect(reference, pid.u);
  connect(measurement, pid.y);
  connect(pid.yCtrl, control);
end PID_Controller;
```

### Example 2: Transfer Function

**Simulink Block**:
```
Transfer Function Block:
  Numerator: [1 0]
  Denominator: [1 2 1]
  Sample time: 0 (continuous)
```

**Modelica Model**:
```modelica
model TransferFunction
  extends Modelica.Blocks.Icons.Block;
  
  Modelica.Blocks.Interfaces.RealInput input;
  Modelica.Blocks.Interfaces.RealOutput output;
  
  Modelica.Blocks.Continuous.TransferFunction tf(
    numerator={1, 0},
    denominator={1, 2, 1}
  );

equation
  connect(input, tf.input);
  connect(tf.output, output);
end TransferFunction;
```

### Example 3: State Machine

**Simulink Stateflow**:
```
States:
  IDLE -> STARTING (on start)
  STARTING -> RUNNING (after 2s)
  RUNNING -> IDLE (on stop)
```

**Modelica Model**:
```modelica
model StateMachine
  extends Modelica.Blocks.Icons.Block;
  
  input Boolean start;
  input Boolean stop;
  output Integer state "1=IDLE, 2=STARTING, 3=RUNNING";
  
  Modelica.Blocks.Discrete.TriggeredTimer startTimer(startTime=2);
  Modelica.Blocks.Logical.EdgeDetect startEdge;
  Modelica.Blocks.Logical.EdgeDetect stopEdge;

equation
  // Detect edges
  connect(start, startEdge.u);
  connect(stop, stopEdge.u);
  
  // State transitions
  if startEdge.y and state < 2 then
    state = 2;  // STARTING
    startTimer.trigger = true;
  end if;
  
  if startTimer.y and state == 2 then
    state = 3;  // RUNNING
  end if;
  
  if stopEdge.y and state > 1 then
    state = 1;  // IDLE
  end if;
end StateMachine;
```

## Quality Gates

### Before Migration
- [ ] Simulink model compiles without errors
- [ ] All required blocks are supported
- [ ] Test cases are available
- [ ] Model documentation is available
- [ ] Custom blocks are documented

### During Migration
- [ ] All blocks have been mapped
- [ ] All parameters have been converted
- [ ] All connections have been preserved
- [ ] All test cases have been migrated
- [ ] Unsupported features have been identified

### After Migration
- [ ] Modelica model compiles without errors
- [ ] Validation tests pass
- [ ] Error metrics within tolerance
- [ ] Documentation is complete
- [ ] Performance meets requirements

## Tool Integration

- **Simulink**: For parsing Simulink models
- **MATLAB**: For running Simulink models
- **OpenModelica**: For Modelica implementation
- **JModelica.org**: For advanced Modelica features
- **Modelica Standard Library**: For component library
- **Python**: For migration scripts
- **XML/JSON**: For parsing model files

## Deliverables Format

### Migration Package

```
migration/
├── original/
│   ├── PID_Controller.slx          # Original Simulink model
│   └── test_PID_Controller.m       # Original test cases
├── migrated/
│   ├── PID_Controller.mo          # Migrated Modelica model
│   ├── test_PID_Controller.mo      # Migrated test cases
│   └── PID_Controller.py          # Alternative Python implementation
├── validation/
│   ├── simout.mat                 # Simulink simulation results
│   ├── result.mat                 # Modelica simulation results
│   ├── comparison.py              # Comparison script
│   └── validation_report.md        # Validation report
├── documentation/
│   ├── migration_notes.md         # Manual changes and notes
│   └── unsupported_features.md    # List of unsupported features
└── README.md                       # Migration instructions
```

## Interface Contract

When spawned by the orchestrator, the simulink-migrator receives a **MIGRATION BRIEF** containing:

- `simulink_model`: Path to Simulink model file
- `target_platform`: Target platform (modelica, scilab, etc.)
- `test_cases`: Path to test cases (if available)
- `migration_strategy`: direct, optimized, or hybrid
- `validation_tolerance`: Acceptable error tolerance (default: 1%)
- `preserve_structure`: Whether to preserve original structure

The simulink-migrator returns a **MIGRATION REPORT** containing:

- `status`: success, partial, or blocked
- `migrated_model`: Migrated model in target format
- `migrated_tests`: Migrated test cases
- `validation_results`: Cross-validation results
- `manual_changes`: List of required manual changes
- `unsupported_features`: List of unsupported features
- `metrics`: Migration metrics (coverage, error rates)
- `warnings`: Non-blocking issues
- `errors`: Blocking issues

## Verbosity

verbosity: V1
