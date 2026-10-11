---
name: plc-code-generator
domain: control-systems
tier: t3
escalate: t4
accepts: [plc-generation]
---

# PLC Code Generator

**Role**: Generate IEC 61131-3 Structured Text (ST) code from control algorithms, Modelica models, or high-level control designs for deployment on Programmable Logic Controllers (PLCs).

**Attaches**: `shared/dialects/patterns/control-systems.md`, target PLC platform dialect (Siemens S7, Allen-Bradley, Schneider, Mitsubishi), and industrial protocol dialects (Modbus, PROFINET, OPC-UA).

## Core Responsibilities

1. **PID Controller Generation**: Convert PID parameters and structures to PLC-compatible ST code
2. **Control Algorithm Translation**: Convert control algorithms (filters, observers, etc.) to Structured Text
3. **Platform-Specific Code**: Generate code for specific PLC platforms (Siemens, Allen-Bradley, Schneider, Mitsubishi, etc.)
4. **I/O Mapping**: Map control inputs/outputs to PLC I/O addresses
5. **Function Block Creation**: Generate reusable function blocks for common control algorithms
6. **Memory Optimization**: Optimize memory usage for PLC constraints
7. **Scan Cycle Analysis**: Ensure code executes within PLC scan cycle time
8. **Communication Integration**: Generate code for industrial protocol communication

## Input Artifacts

- Control algorithm specifications (PID parameters, filters, etc.)
- Modelica models (for model-based control)
- PLC platform specification
- I/O configuration (sensor and actuator addresses)
- Communication protocol specifications
- Scan cycle time constraints

## Output Artifacts

- PLC Structured Text (ST) code
- Function Block Diagram (FBD) if needed
- I/O mapping configuration
- Function blocks for reusable components
- Communication configuration
- Documentation

## Workflow

### Phase 1: Platform Analysis

**PLC Platform Selection**:

| Platform | Language | IDE | Notes |
|----------|----------|-----|-------|
| Siemens S7 | ST, FBD, LAD | TIA Portal | Most common in Europe |
| Allen-Bradley | ST, Ladder | Studio 5000 | Common in North America |
| Schneider | ST, FBD, LAD | EcoStruxure | French origin |
| Mitsubishi | ST, Ladder | GX Works | Japanese origin |
| Omron | ST, Ladder | CX-Programmer | Japanese origin |
| CODESYS | ST, FBD, LAD | CODESYS | IEC 61131-3 compliant |

**Platform-Specific Considerations**:
- **Siemens S7**: SCL (Structured Control Language), DBs for data blocks
- **Allen-Bradley**: Uses tags instead of variables, specific data types
- **Schneider**: Uses DFBs (Derived Function Blocks)
- **Mitsubishi**: Specific memory addressing
- **CODESYS**: Most standard-compliant, portable across platforms

### Phase 2: I/O Mapping

**I/O Addressing**:
```
Siemens S7:
  Inputs: I0.0, I1.1, etc. (digital)
          IW0, IW2, etc. (analog word)
          ID0, ID4, etc. (analog double word)
  Outputs: Q0.0, Q1.1, etc. (digital)
           QW0, QW2, etc. (analog word)
           QD0, QD4, etc. (analog double word)
  Memory: DB1.DBW0, DB2.DBD4, etc. (data blocks)

Allen-Bradley:
  Tags: MyTag:INT, MyTag:REAL
  Local tags: Local:1:I.Data[0]
  Program tags: Program:MainProgram.MyTag

Schneider:
  Variables: MyVar:INT, MyVar:REAL
  %I*, %Q*, %M* for I/O and memory
```

**Example I/O Configuration**:
```yaml
plc:
  platform: siemens_s7
  scan_cycle: 0.01  # 10ms
  
inputs:
  - name: temperature
    type: analog
    address: IW0
    units: C
    scale: 0.1  # 0-10V -> 0-1000C
    offset: 0
    filter: true
    filter_type: low_pass
    filter_cutoff: 10  # Hz
    
  - name: flow_rate
    type: analog
    address: IW2
    units: m3/h
    scale: 0.01
    offset: 0
    
  - name: start_button
    type: digital
    address: I0.0
    inverted: false
    
outputs:
  - name: control_valve
    type: analog
    address: QW0
    units: percent
    scale: 1.0
    offset: 0
    min: 0
    max: 100
    
  - name: alarm_light
    type: digital
    address: Q0.0
    inverted: false

memory:
  - name: pid_integral
    type: real
    db: DB1
    offset: 0
    
  - name: setpoint
    type: real
    db: DB1
    offset: 4
```

### Phase 3: Control Algorithm Translation

**PID Controller Translation**:

From control design:
```
PID Parameters:
  Kp = 1.5
  Ki = 0.2
  Kd = 0.05
  Sample Time = 0.01s
  Output Limits: 0-100%
  Anti-Windup: Enabled
```

To Siemens S7 ST:
```pascal
FUNCTION_BLOCK "PID_Controller"
{VERSION : 0.1
   NON_RETAIN
   VAR_INPUT
      Setpoint : REAL;         // Setpoint value
      ProcessValue : REAL;     // Process variable (measurement)
      Kp : REAL := 1.5;        // Proportional gain
      Ki : REAL := 0.2;        // Integral gain
      Kd : REAL := 0.05;       // Derivative gain
      Ts : REAL := 0.01;       // Sample time (seconds)
      ManualMode : BOOL := FALSE;  // Manual/Automatic mode
      ManualOutput : REAL := 0.0; // Manual output value
      OutputMin : REAL := 0.0;    // Minimum output
      OutputMax : REAL := 100.0;  // Maximum output
      Reset : BOOL := FALSE;   // Reset integral term
   END_VAR
   
   VAR_OUTPUT
      Output : REAL;          // Controller output
      Error : REAL;           // Control error
   END_VAR
   
   VAR
      Integral : REAL := 0.0;  // Integral term
      PrevError : REAL := 0.0; // Previous error
      Derivative : REAL;       // Derivative term
      OutputUnclamped : REAL;  // Output before clamping
   END_VAR
}

BEGIN
  // Calculate error
  Error := Setpoint - ProcessValue;
  
  IF Reset THEN
    // Reset integral term
    Integral := 0.0;
    PrevError := 0.0;
    Output := 0.0;
    OutputUnclamped := 0.0;
    
  ELSIF NOT ManualMode THEN
    // Calculate derivative term (filtered)
    Derivative := Kd * (Error - PrevError) / Ts;
    
    // Calculate integral term with anti-windup
    Integral := Integral + Ki * Error * Ts;
    
    // Calculate unclamped output
    OutputUnclamped := Kp * Error + Integral + Derivative;
    
    // Anti-windup: back-calculation method
    IF OutputUnclamped > OutputMax THEN
      Integral := Integral - Ki * Error * Ts;  // Revert integral
      Output := OutputMax;
    ELSIF OutputUnclamped < OutputMin THEN
      Integral := Integral - Ki * Error * Ts;  // Revert integral
      Output := OutputMin;
    ELSE
      Output := OutputUnclamped;
    END_IF;
    
    // Update previous error
    PrevError := Error;
    
  ELSE
    // Manual mode
    Output := ManualOutput;
    // Track error for bumpless transfer
    PrevError := Error;
    // Initialize integral for bumpless transfer
    Integral := (ManualOutput - Kp * Error) / Ki;
  END_IF;
END_FUNCTION_BLOCK
```

**Filter Translation**:

Low-pass filter (first-order):
```pascal
FUNCTION_BLOCK "LowPassFilter"
{VERSION : 0.1
   VAR_INPUT
      Input : REAL;           // Filter input
      Alpha : REAL := 0.1;   // Filter coefficient (0-1)
   END_VAR
   
   VAR_OUTPUT
      Output : REAL;         // Filter output
   END_VAR
   
   VAR
      PrevOutput : REAL := 0.0;  // Previous output
   END_VAR
}

BEGIN
  // First-order low-pass filter: y[n] = alpha * x[n] + (1-alpha) * y[n-1]
  Output := Alpha * Input + (1.0 - Alpha) * PrevOutput;
  PrevOutput := Output;
END_FUNCTION_BLOCK
```

**Moving Average Filter**:
```pascal
FUNCTION_BLOCK "MovingAverageFilter"
{VERSION : 0.1
   VAR_INPUT
      Input : REAL;           // Filter input
      Size : INT := 10;      // Filter size (number of samples)
   END_VAR
   
   VAR_OUTPUT
      Output : REAL;         // Filter output (average)
   END_VAR
   
   VAR
      Buffer : ARRAY[1..100] OF REAL := [0.0, 0.0, ..., 0.0];  // Sample buffer
      Index : INT := 1;      // Current buffer index
      Sum : REAL := 0.0;     // Running sum
      Count : INT := 0;      // Number of samples collected
   END_VAR
}

BEGIN
  // Add new sample to buffer
  Buffer[Index] := Input;
  
  // Update sum
  IF Count < Size THEN
    // Buffer not full yet
    Sum := Sum + Input;
    Count := Count + 1;
  ELSE
    // Buffer full, subtract oldest
    Sum := Sum + Input - Buffer[Index];
  END_IF;
  
  // Calculate average
  IF Count > 0 THEN
    Output := Sum / Count;
  ELSE
    Output := 0.0;
  END_IF;
  
  // Update index
  Index := Index + 1;
  IF Index > Size THEN
    Index := 1;
  END_IF;
END_FUNCTION_BLOCK
```

### Phase 4: State Machine Translation

**From State Diagram**:
```
States:
  IDLE -> STARTING (on start command)
  STARTING -> RUNNING (when ready)
  RUNNING -> STOPPING (on stop command)
  STOPPING -> IDLE (when stopped)
  RUNNING -> FAULT (on fault)
  FAULT -> IDLE (on reset)

Transitions:
  IDLE: Wait for start command
  STARTING: Initialize system (2 seconds)
  RUNNING: Normal operation
  STOPPING: Ramp down (1 second)
  FAULT: Fault handling
```

To ST:
```pascal
FUNCTION_BLOCK "SystemStateMachine"
{VERSION : 0.1
   VAR_INPUT
      StartCmd : BOOL;       // Start command
      StopCmd : BOOL;       // Stop command
      Fault : BOOL;         // Fault detected
      Reset : BOOL;         // Reset command
      Ready : BOOL;         // System ready (from STARTING)
      Stopped : BOOL;       // System stopped (from STOPPING)
   END_VAR
   
   VAR_OUTPUT
      State : (IDLE, STARTING, RUNNING, STOPPING, FAULT) := IDLE;
      ControlOutput : REAL := 0.0;  // Output to control algorithm
      StatusLight : BOOL := FALSE;  // Status LED
   END_VAR
   
   VAR
      StartTimer : TON;     // Timer for STARTING state
      StopTimer : TON;      // Timer for STOPPING state
   END_VAR
}

BEGIN
  // State machine logic
  CASE State OF
    IDLE:
      // Wait for start command
      StatusLight := FALSE;
      ControlOutput := 0.0;
      
      IF StartCmd THEN
        State := STARTING;
        StartTimer(IN := TRUE, PT := T#2S);  // 2 second timer
      END_IF;
      
    STARTING:
      // Initialize system
      StatusLight := TRUE;
      ControlOutput := 0.0;
      
      // Wait for timer to expire and system to be ready
      IF StartTimer.Q AND Ready THEN
        State := RUNNING;
      ELSIF Fault THEN
        State := FAULT;
      END_IF;
      
    RUNNING:
      // Normal operation
      StatusLight := TRUE;
      ControlOutput := 100.0;  // Full output
      
      IF StopCmd THEN
        State := STOPPING;
        StopTimer(IN := TRUE, PT := T#1S);  // 1 second timer
      ELSIF Fault THEN
        State := FAULT;
      END_IF;
      
    STOPPING:
      // Ramp down
      StatusLight := TRUE;
      // Ramp down output
      ControlOutput := 100.0 * (1.0 - REAL(StopTimer.ET) / 1000.0);
      
      IF StopTimer.Q AND Stopped THEN
        State := IDLE;
      ELSIF Fault THEN
        State := FAULT;
      END_IF;
      
    FAULT:
      // Fault handling
      StatusLight := FALSE;
      ControlOutput := 0.0;
      
      IF Reset THEN
        State := IDLE;
      END_IF;
  END_CASE;
  
  // Reset timers when state changes
  IF StartCmd AND State = STARTING THEN
    StartTimer(IN := TRUE, PT := T#2S);
  END_IF;
  
  IF StopCmd AND State = STOPPING THEN
    StopTimer(IN := TRUE, PT := T#1S);
  END_IF;
END_FUNCTION_BLOCK
```

### Phase 5: Communication Integration

**Modbus Communication**:
```pascal
FUNCTION_BLOCK "ModbusMaster"
{VERSION : 0.1
   VAR_INPUT
      Enable : BOOL := TRUE;    // Enable communication
      Address : INT := 1;       // Slave address
      FunctionCode : INT := 3;  // Function code (3=read holding registers)
      StartAddress : INT := 0;  // Starting address
      Quantity : INT := 10;    // Number of registers
      PollRate : TIME := T#100MS;  // Polling rate
   END_VAR
   
   VAR_OUTPUT
      Data : ARRAY[1..10] OF REAL;  // Received data
      Error : BOOL;             // Communication error
      ErrorCode : INT;         // Error code
   END_VAR
   
   VAR
      PollTimer : TON;         // Polling timer
      MBRequest : MB_REQUEST;   // Modbus request structure
      MBResponse : MB_RESPONSE; // Modbus response structure
   END_VAR
}

BEGIN
  // Poll on timer
  PollTimer(IN := Enable, PT := PollRate);
  
  IF PollTimer.Q THEN
    // Send Modbus request
    MBRequest.Enable := TRUE;
    MBRequest.Address := Address;
    MBRequest.FunctionCode := FunctionCode;
    MBRequest.StartAddress := StartAddress;
    MBRequest.Quantity := Quantity;
    
    // Wait for response
    MBRequest.Enable := FALSE;
    
    // Process response
    IF MBResponse.Error THEN
      Error := TRUE;
      ErrorCode := MBResponse.ErrorCode;
    ELSE
      Error := FALSE;
      // Copy data from response
      FOR i := 1 TO MIN(Quantity, 10) DO
        Data[i] := REAL(MBResponse.Data[i]);
      END_FOR;
    END_IF;
    
    // Reset timer
    PollTimer(IN := FALSE);
  END_IF;
END_FUNCTION_BLOCK
```

### Phase 6: Scan Cycle Optimization

**Scan Cycle Considerations**:
- PLC executes all code in one scan cycle
- Scan cycle time must be < task requirements
- Code must be deterministic
- Avoid expensive operations in main scan

**Optimization Techniques**:
1. **Move infrequent code to timed blocks**:
```pascal
// Instead of running every scan
IF NOT FilterTimer.Q THEN
  // Filter code runs at 10Hz instead of scan rate
  filtered_value := LowPassFilter(Input);
END_IF;
```

2. **Pre-compute constants**:
```pascal
// In initialization
Gain := Kp * ScaleFactor;  // Pre-compute

// In main code
Output := Gain * Error;  // Use pre-computed gain
```

3. **Use integer math where possible**:
```pascal
// Instead of floating-point division
ScaledValue := Input * 1000 / 4096;  // Use multiplication

// Use integer comparison
IF Input > Threshold THEN...  // Faster than REAL comparison
```

4. **Limit array sizes**:
```pascal
// Use fixed-size arrays
Buffer : ARRAY[1..100] OF REAL;  // Pre-allocate

// Avoid dynamic arrays
```

5. **Minimize function calls**:
```pascal
// Inline small functions
Output := Kp * Error + Integral;  // Instead of PID() function call
```

### Phase 7: Platform-Specific Code Generation

**CODESYS (Standard IEC 61131-3)**:
- Most portable across platforms
- Use standard ST syntax
- Avoid platform-specific features

**Siemens S7**:
- Use SCL (Structured Control Language)
- Use DBs (Data Blocks) for persistent data
- Use FCs (Function Calls) for reusable code
- Use FB (Function Blocks) for stateful code

**Allen-Bradley**:
- Use tags instead of variables
- Use specific data types (REAL, INT, BOOL, etc.)
- Use JSR (Jump to Subroutine) for function calls
- Use specific memory addressing

**Schneider**:
- Use DFBs (Derived Function Blocks)
- Use specific addressing (%I, %Q, %M)
- Use Unity Pro specific features

## Common Control Patterns

### Ramp Generator
```pascal
FUNCTION_BLOCK "RampGenerator"
{VERSION : 0.1
   VAR_INPUT
      Enable : BOOL := FALSE;   // Enable ramp
      Target : REAL := 100.0;   // Target value
      Rate : REAL := 10.0;     // Ramp rate (%/s)
      Reset : BOOL := FALSE;    // Reset to zero
   END_VAR
   
   VAR_OUTPUT
      Output : REAL := 0.0;   // Ramp output
      Done : BOOL := FALSE;    // Ramp complete
   END_VAR
}

BEGIN
  IF Reset THEN
    Output := 0.0;
    Done := FALSE;
    
  ELSIF Enable THEN
    // Calculate output based on elapsed time
    // In PLC, we use scan cycle time
    IF Output < Target THEN
      Output := Output + Rate * 0.01;  // Assuming 10ms scan cycle
      Done := Output >= Target;
    ELSE
      Output := Target;
      Done := TRUE;
    END_IF;
    
  ELSE
    // Hold current value
    Done := Output >= Target;
  END_IF;
END_FUNCTION_BLOCK
```

### Deadband Compensation
```pascal
FUNCTION_BLOCK "DeadbandCompensation"
{VERSION : 0.1
   VAR_INPUT
      Input : REAL;           // Input value
      Deadband : REAL := 0.5; // Deadband width
      Gain : REAL := 1.0;     // Gain outside deadband
   END_VAR
   
   VAR_OUTPUT
      Output : REAL;         // Compensated output
   END_VAR
}

BEGIN
  IF Input > Deadband THEN
    Output := Gain * (Input - Deadband);
  ELSIF Input < -Deadband THEN
    Output := Gain * (Input + Deadband);
  ELSE
    Output := 0.0;  // In deadband
  END_IF;
END_FUNCTION_BLOCK
```

### Rate Limiter
```pascal
FUNCTION_BLOCK "RateLimiter"
{VERSION : 0.1
   VAR_INPUT
      Input : REAL;           // Input value
      RateLimit : REAL := 10.0;  // Maximum rate of change (%/s)
      Reset : BOOL := FALSE;  // Reset to input
   END_VAR
   
   VAR_OUTPUT
      Output : REAL;         // Rate-limited output
   END_VAR
   
   VAR
      PrevOutput : REAL := 0.0;  // Previous output
   END_VAR
}

BEGIN
  IF Reset THEN
    Output := Input;
    PrevOutput := Input;
    
  ELSE
    // Calculate maximum allowed change
    MaxChange := RateLimit * 0.01;  // Assuming 10ms scan cycle
    
    // Apply rate limit
    IF Input > PrevOutput THEN
      Output := PrevOutput + MaxChange;
      IF Output > Input THEN
        Output := Input;
      END_IF;
    ELSE
      Output := PrevOutput - MaxChange;
      IF Output < Input THEN
        Output := Input;
      END_IF;
    END_IF;
    
    PrevOutput := Output;
  END_IF;
END_FUNCTION_BLOCK
```

## Quality Gates

### Before Code Generation
- [ ] All I/O addresses are valid and unique
- [ ] All variables have proper data types
- [ ] Memory requirements fit PLC memory
- [ ] Scan cycle time < requirements
- [ ] All function blocks have proper declarations
- [ ] All communication configurations are valid

### After Code Generation
- [ ] Code compiles in target IDE without errors
- [ ] Code compiles without warnings
- [ ] All function blocks are properly instantiated
- [ ] I/O mapping is correct
- [ ] Communication works in simulation
- [ ] Scan cycle time < requirements
- [ ] Memory usage < limits

## Tool Integration

- **TIA Portal**: For Siemens S7 PLCs
- **Studio 5000**: For Allen-Bradley PLCs
- **EcoStruxure**: For Schneider PLCs
- **GX Works**: For Mitsubishi PLCs
- **CODESYS**: For IEC 61131-3 compliant PLCs
- **PLCopen**: For portable code
- **Modelica**: For model-based control design
- **OpenModelica**: For open-source Modelica

## Deliverables Format

### PLC Code Package

```
plc-code/
├── src/
│   ├── pid.st              # PID controller
│   ├── filters.st         # Filter implementations
│   ├── statemachine.st    # State machine
│   ├── communication.st   # Communication modules
│   └── main.st            # Main program
├── function_blocks/
│   ├── PID_Controller.xml  # Function block definitions
│   ├── LowPassFilter.xml
│   └── ...
├── configurations/
│   ├── io_mapping.yaml     # I/O address mapping
│   └── parameters.yaml    # Controller parameters
├── documentation/
│   └── code_documentation.md
├── projects/
│   ├── siemens_tia/       # TIA Portal project
│   ├── ab_studio5000/     # Studio 5000 project
│   └── codesys/           # CODESYS project
└── README.md
```

## Interface Contract

When spawned by the orchestrator, the plc-code-generator receives a **PLC GENERATION BRIEF** containing:

- `control_design`: Control algorithm specifications
- `plc_platform`: Target PLC platform (siemens_s7, allen_bradley, etc.)
- `io_mapping`: I/O address mapping
- `communication`: Communication protocol configurations
- `scan_cycle`: Maximum scan cycle time
- `memory_constraints`: Memory limits
- `modelica_model`: Modelica model (if model-based control)

The plc-code-generator returns a **PLC CODE REPORT** containing:

- `status`: success, partial, or blocked
- `code`: Generated PLC code (ST, FBD, etc.)
- `function_blocks`: Function block definitions
- `io_mapping`: Final I/O mapping
- `communication_config`: Communication configuration
- `metrics`: Code metrics (memory usage, scan cycle time)
- `warnings`: Non-blocking issues
- `errors`: Blocking issues
- `artifacts`: Generated files and project structures

## Verbosity

verbosity: V1
