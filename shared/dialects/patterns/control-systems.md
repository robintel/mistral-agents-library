---
type: pattern
family: control
---

# Control Systems Pattern Contract

**Attaches** to Modelica work, embedded firmware with control algorithms, and any code implementing closed-loop control. Loads alongside `shared/dialects/tools/modelica.md` for Modelica-based systems or the appropriate language dialect for hand-coded implementations.

## The Discipline

Control systems engineering is **feedback discipline**: the system must be stable, the response must meet requirements, and the implementation must respect real-time constraints.

- **Stability first**: A control loop that oscillates or diverges is a finding regardless of feature completeness
- **Timing is a budget**: Sample periods, computation time, and latency are all part of the control design
- **Units are non-negotiable**: Every signal has a unit, every parameter has a unit, and every equation must be dimensionally consistent
- **Anti-windup is mandatory**: Integral windup destroys controllers under sustained error
- **Saturation is expected**: Every actuator has limits, and the control algorithm must handle them gracefully

## Control System Types

### Continuous Control

**PID Control**: The workhorse of industrial control

```
Proportional: output = Kp * error
Integral: output += Ki * integral(error) * dt
Derivative: output += Kd * der(error)

Combined: output = Kp*error + Ki*integral(error) + Kd*der(error)
```

**Pitfalls**:
- Integral windup: When error persists, integral term grows unbounded
- Derivative noise: High-frequency noise amplifies derivative term
- Bumpless transfer: When switching between manual and automatic control

**Mitigations**:
- Clamp integral term when output saturates
- Filter derivative term (low-pass filter)
- Use tracking mode for bumpless transfer

### Discrete Control

**Digital PID**: Discrete-time implementation

```
Integral: integral[n] = integral[n-1] + error[n] * dt
Derivative: derivative[n] = (error[n] - error[n-1]) / dt
Output: output[n] = Kp*error[n] + Ki*integral[n] + Kd*derivative[n]
```

**Pitfalls**:
- Sampling too slow: Loses high-frequency dynamics
- Sampling too fast: Computation overload, numerical issues
- Aliasing: High-frequency signals fold back into low frequencies

**Mitigations**:
- Choose sample rate at 5-10x the system bandwidth
- Use anti-aliasing filters if needed
- Match sample rate to actuator update rate

### State Feedback

**State-space representation**:
```
der(x) = A*x + B*u
y = C*x + D*u
```

**Controller**: u = -K*x + reference

**Pitfalls**:
- Requires full state measurement (often not available)
- Sensitive to modeling errors
- Gain scheduling needed for nonlinear systems

**Mitigations**:
- Use observers to estimate unmeasured states
- Robust control design for model uncertainty
- Adaptive control for nonlinear systems

### Feedforward Control

**Disturbance rejection**: Compensate for known disturbances before they affect the system

**Implementation**:
```
output = feedback_controller(error) + feedforward(measurements)
```

**Pitfalls**:
- Requires accurate disturbance model
- Doesn't handle unmeasured disturbances
- Can amplify noise

**Mitigations**:
- Combine with feedback control
- Use only for measurable disturbances
- Filter feedforward signals

## Control Loop Architecture

### Single Loop

```
[Reference] -> [Error Calc] -> [Controller] -> [Actuator] -> [Plant] -> [Sensor] -> [Error Calc]
```

**Design considerations**:
- Loop rate: 5-10x the system bandwidth
- Sensor noise: Filter or use robust control
- Actuator limits: Implement anti-windup
- Plant dynamics: Must be faster than loop rate

### Cascade Control

```
[Reference] -> [Outer Loop Error] -> [Outer Controller] -> [Inner Reference]
                                                          |
[Inner Loop Error] -> [Inner Controller] -> [Actuator] -> [Plant] -> [Sensor]
```

**Use when**:
- Secondary disturbances need fast rejection
- Inner loop can stabilize outer loop
- Multiple time scales in system

**Example**: Position control with velocity inner loop

### Feedforward + Feedback

```
[Reference] -> [Feedforward] ->+-> [Actuator] -> [Plant] -> [Sensor]
                          ^
[Feedback] <- [Error Calc] <-
```

**Benefits**:
- Faster response to known disturbances
- Reduced feedback controller effort
- Better tracking of reference changes

## Implementation Patterns

### Fixed-Point Considerations

**When to use**: MCU targets without FPU, power-constrained systems

**Pattern**:
```c
// Q15 format: -1.0 to +0.99997 (16-bit signed, 15 fractional bits)
typedef int16_t q15_t;

#define Q15_MULT(a, b) ((q15_t)((int32_t)(a) * (int32_t)(b) >> 15))
#define Q15_TO_FLOAT(a) ((float)(a) / 32768.0f)

typedef struct {
    q15_t Kp;    // Q15 format
    q15_t Ki;    // Q15 format
    q15_t Kd;    // Q15 format
    q15_t integral;
    q15_t prev_error;
    q15_t dt_q;   // Q15 format
} PID_FixedPoint;

q15_t pid_update_fixed(PID_FixedPoint* pid, q15_t reference, q15_t measurement) {
    q15_t error = reference - measurement;
    
    // Integral: integral += Ki * error * dt
    // Need to handle overflow
    int32_t integral_temp = (int32_t)pid->integral * 32768;  // Convert to Q30
    integral_temp += (int32_t)pid->Ki * (int32_t)error * (int32_t)pid->dt_q;
    pid->integral = (q15_t)(integral_temp >> 15);  // Convert back to Q15
    
    // Derivative: (error - prev_error) / dt
    q15_t derivative = Q15_MULT(error - pid->prev_error, pid->dt_q);
    
    pid->prev_error = error;
    
    // Output: Kp*error + Ki*integral + Kd*derivative
    int32_t output = (int32_t)pid->Kp * (int32_t)error;
    output += (int32_t)pid->Ki * (int32_t)pid->integral;
    output += (int32_t)pid->Kd * (int32_t)derivative;
    
    return (q15_t)(output >> 15);
}
```

**Scaling strategies**:
- Q format: Qm.n where m+n = bit width
- Choose scaling based on expected value ranges
- Use 64-bit intermediates for multiplications to avoid overflow
- Saturation: Clamp results to min/max values

### Floating-Point Implementation

**When to use**: Targets with FPU, systems requiring high precision

**Pattern**:
```c
typedef struct {
    float Kp;
    float Ki;
    float Kd;
    float integral;
    float prev_error;
    float dt;
    float out_min;
    float out_max;
} PID_Float;

float pid_update_float(PID_Float* pid, float reference, float measurement) {
    float error = reference - measurement;
    
    // Integral with anti-windup
    pid->integral += pid->Ki * error * pid->dt;
    
    // Clamp integral if output would saturate
    float proportional = pid->Kp * error;
    float derivative = pid->Kd * (error - pid->prev_error) / pid->dt;
    float output = proportional + pid->integral + derivative;
    
    // Anti-windup: only integrate if output is within bounds
    if (output > pid->out_max || output < pid->out_min) {
        pid->integral -= pid->Ki * error * pid->dt;  // Revert integral
    } else {
        pid->prev_error = error;
    }
    
    // Clamp output
    return fmaxf(pid->out_min, fminf(pid->out_max, output));
}
```

**Considerations**:
- Use single precision (float) for most MCUs
- Use double precision for high-performance targets
- Check for NaN and Inf in calculations
- Denormal numbers can cause performance issues

### Real-Time Constraints

**Timing analysis**:
```
Sample period (Ts): 1ms
Worst-case execution time (WCET): 0.5ms
Jitter: < 0.1ms
Latency: < 0.5ms
```

**Pattern for RTOS integration**:
```c
// FreeRTOS task for control loop
void vControlTask(void *pvParameters) {
    PID_Controller* pid = (PID_Controller*)pvParameters;
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xPeriod = pdMS_TO_TICKS(1);  // 1ms
    
    while (1) {
        // Wait for next tick
        xTaskDelayUntil(&xLastWakeTime, xPeriod);
        
        // Read sensors
        float measurement = read_sensor();
        float reference = get_reference();
        
        // Compute control
        float output = pid_update(pid, reference, measurement);
        
        // Write to actuators
        set_actuator(output);
        
        // Log for debugging (if there's time)
        log_control_cycle(output, measurement);
    }
}
```

**Scheduling strategies**:
- **Periodic**: Fixed sample rate (most common)
- **Event-driven**: Trigger on sensor changes
- **Multi-rate**: Different rates for different loops
- **Hierarchical**: Prioritize critical loops

## Common Control Structures

### PID Controller

**Continuous**:
```
output = Kp * error + Ki * integral(error) + Kd * der(error)
```

**Discrete (Position form)**:
```
output[n] = Kp*error[n] + Ki*Ts*sum(error[0:n]) + Kd/Ts*(error[n] - error[n-1])
```

**Discrete (Velocity form)**:
```
delta_output = Kp*(error[n] - error[n-1]) + Ki*Ts*error[n] + Kd/Ts*(error[n] - 2*error[n-1] + error[n-2])
output[n] = output[n-1] + delta_output
```

**Bumpless transfer**:
```
// When switching from manual to automatic
if (manual_to_auto) {
    // Initialize controller state to match manual output
    pid->integral = (manual_output - Kp * error) / Ki;
    pid->prev_error = error;
}
```

### Lead-Lag Controller

**Transfer function**:
```
C(s) = K * (Ts*s + 1) / (Tp*s + 1)
```

**Discrete implementation**:
```c
typedef struct {
    float K;
    float Ts;
    float Tp;
    float prev_input;
    float prev_output;
} LeadLag;

float lead_lag_update(LeadLag* ll, float input) {
    float output = ll->prev_output + 
                   ll->K * (input - ll->prev_input) * (ll->Ts / ll->Tp) +
                   ll->K * (1 - ll->Ts / ll->Tp) * (input - ll->prev_input);
    
    ll->prev_input = input;
    ll->prev_output = output;
    
    return output;
}
```

### State-Space Controller

**Discrete state-space**:
```
x[k+1] = A*x[k] + B*u[k]
y[k] = C*x[k] + D*u[k]
```

**Implementation**:
```c
typedef struct {
    int state_size;
    int input_size;
    int output_size;
    float* A;  // state_size x state_size
    float* B;  // state_size x input_size
    float* C;  // output_size x state_size
    float* D;  // output_size x input_size
    float* x;  // state vector
} StateSpace;

void state_space_update(StateSpace* ss, float* u, float* y) {
    // y = C*x + D*u
    for (int i = 0; i < ss->output_size; i++) {
        y[i] = 0;
        for (int j = 0; j < ss->state_size; j++) {
            y[i] += ss->C[i * ss->state_size + j] * ss->x[j];
        }
        for (int j = 0; j < ss->input_size; j++) {
            y[i] += ss->D[i * ss->input_size + j] * u[j];
        }
    }
    
    // x[k+1] = A*x[k] + B*u[k]
    float* x_new = malloc(ss->state_size * sizeof(float));
    for (int i = 0; i < ss->state_size; i++) {
        x_new[i] = 0;
        for (int j = 0; j < ss->state_size; j++) {
            x_new[i] += ss->A[i * ss->state_size + j] * ss->x[j];
        }
        for (int j = 0; j < ss->input_size; j++) {
            x_new[i] += ss->B[i * ss->input_size + j] * u[j];
        }
    }
    
    // Copy new state
    memcpy(ss->x, x_new, ss->state_size * sizeof(float));
    free(x_new);
}
```

## Filter Implementation

### Low-Pass Filter

**First-order**:
```
y[n] = alpha * x[n] + (1 - alpha) * y[n-1]
alpha = dt / (tau + dt)
```

**Implementation**:
```c
typedef struct {
    float alpha;
    float prev_output;
} LowPassFilter;

float low_pass_update(LowPassFilter* lpf, float input) {
    lpf->prev_output = lpf->alpha * input + (1 - lpf->alpha) * lpf->prev_output;
    return lpf->prev_output;
}
```

### Moving Average Filter

**N-point moving average**:
```
y[n] = (x[n] + x[n-1] + ... + x[n-N+1]) / N
```

**Implementation**:
```c
typedef struct {
    int size;
    int index;
    float* buffer;
    float sum;
} MovingAverage;

void moving_average_init(MovingAverage* ma, int size) {
    ma->size = size;
    ma->index = 0;
    ma->buffer = calloc(size, sizeof(float));
    ma->sum = 0;
}

float moving_average_update(MovingAverage* ma, float input) {
    // Remove oldest value
    ma->sum -= ma->buffer[ma->index];
    
    // Add new value
    ma->sum += input;
    ma->buffer[ma->index] = input;
    
    // Update index
    ma->index = (ma->index + 1) % ma->size;
    
    return ma->sum / ma->size;
}
```

## Stability Analysis Patterns

### Bode Plot Analysis

**What to check**:
- Gain margin > 6 dB (usually)
- Phase margin > 30-45 degrees
- Crossover frequency appropriate for system
- No excessive peaking

**Modelica implementation**:
```modelica
model BodeAnalysis
  Modelica.Blocks.Continuous.TransferFunction TF(
    numerator={1},
    denominator={1, 2, 1},  // s^2 + 2s + 1
    k=1
  );
  Modelica.Blocks.Sources.FrequencySystem freq;
  Modelica.Blocks.Analog.Gain gain(n=20*Modelica.Constants.log10);
  Modelica.Blocks.Analog.AtomicGain phase(n=-Modelica.Constants.pi/180);
  // Connect and analyze
end BodeAnalysis;
```

### Root Locus Analysis

**What to check**:
- All poles in left half-plane (stable)
- Dominant poles have appropriate damping ratio (zeta > 0.7)
- No poles too close to imaginary axis (fast response but sensitive to noise)

### Nyquist Plot Analysis

**What to check**:
- No encirclements of (-1,0) point
- Sufficient distance from critical point

## Digital Twin Patterns

### Co-Simulation Architecture

```
[Physical System] <-> [Sensor Interface] <-> [Digital Twin Model]
                                      ^
[Control Algorithm] <--------------+
```

**Implementation**:
```c
// Digital twin structure
typedef struct {
    // Physical model parameters
    float mass;
    float damping;
    float stiffness;
    
    // State
    float position;
    float velocity;
    
    // Input from physical system
    float force;
    
    // Output to control
    float estimated_position;
    float estimated_velocity;
} DigitalTwin;

void digital_twin_update(DigitalTwin* dt, float sensor_force, float sensor_position, float dt) {
    // Use sensor data to correct model
    // Simple: use sensor position directly
    dt->position = sensor_position;
    
    // Or use observer to estimate state
    // dt->position = observer_update(dt, sensor_force, sensor_position);
    
    // Update velocity
    dt->velocity = (dt->position - dt->estimated_position) / dt;
    
    // Physical model prediction
    float acceleration = (sensor_force - dt->damping * dt->velocity - dt->stiffness * dt->position) / dt->mass;
    dt->velocity += acceleration * dt;
    dt->position += dt->velocity * dt;
    
    // Store estimates for control
    dt->estimated_position = dt->position;
    dt->estimated_velocity = dt->velocity;
}
```

### Model Predictive Control (MPC) Pattern

**Principle**: Solve optimization problem at each time step

```
minimize sum over N: (y_k - r_k)^2 + lambda * (u_k - u_{k-1})^2
subject to:
  x_{k+1} = A*x_k + B*u_k
  y_k = C*x_k
  u_min <= u_k <= u_max
  y_min <= y_k <= y_max
```

**Implementation considerations**:
- Use QP solver for fast computation
- Limit prediction horizon (N) based on compute budget
- Warm-start solver with previous solution
- Use condensed form for efficiency

## Hardware-Specific Patterns

### STM32 with HAL

**PID on STM32**:
```c
#include "stm32f4xx_hal.h"

typedef struct {
    float Kp, Ki, Kd;
    float integral;
    float prev_error;
    uint32_t last_time;
} PID_HandleTypeDef;

float PID_Update(PID_HandleTypeDef* hpid, float reference, float measurement) {
    uint32_t now = HAL_GetTick();
    float dt = (now - hpid->last_time) / 1000.0f;  // Convert ms to s
    hpid->last_time = now;
    
    float error = reference - measurement;
    hpid->integral += hpid->Ki * error * dt;
    float derivative = hpid->Kd * (error - hpid->prev_error) / dt;
    hpid->prev_error = error;
    
    float output = hpid->Kp * error + hpid->integral + derivative;
    return output;
}
```

### Arduino

**PID on Arduino**:
```cpp
#include <PID_v1.h>

// Define Variables
double Setpoint, Input, Output;

// Specify the links and initial tuning parameters
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

void setup() {
    myPID.SetMode(AUTOMATIC);
    myPID.SetOutputLimits(0, 255);  // For 8-bit PWM
}

void loop() {
    Input = readSensor();
    myPID.Compute();
    analogWrite(actuatorPin, Output);
}
```

### PLC (IEC 61131-3 Structured Text)

**PID in Structured Text**:
```pascal
FUNCTION_BLOCK PID
VAR_INPUT
    Setpoint: REAL;
    ProcessVariable: REAL;
    Kp: REAL := 1.0;
    Ki: REAL := 0.1;
    Kd: REAL := 0.01;
    Ts: REAL := 0.01;  // Sample time
    ManualMode: BOOL := FALSE;
    ManualOutput: REAL := 0.0;
END_VAR

VAR_OUTPUT
    Output: REAL;
END_VAR

VAR
    Error: REAL;
    Integral: REAL := 0.0;
    Derivative: REAL;
    PrevError: REAL := 0.0;
END_VAR

METHOD PID : REAL
VAR_INPUT
    Setpoint: REAL;
    ProcessVariable: REAL;
END_VAR

BEGIN
    Error := Setpoint - ProcessVariable;
    
    IF NOT ManualMode THEN
        Integral := Integral + Ki * Error * Ts;
        Derivative := Kd * (Error - PrevError) / Ts;
        PrevError := Error;
        
        PID := Kp * Error + Integral + Derivative;
        
        // Anti-windup
        IF PID > 100.0 THEN
            Integral := Integral - Ki * Error * Ts;  // Revert
            PID := 100.0;
        ELSIF PID < 0.0 THEN
            Integral := Integral - Ki * Error * Ts;  // Revert
            PID := 0.0;
        END_IF;
        
        Output := PID;
    ELSE
        Output := ManualOutput;
        PrevError := Error;  // Track for bumpless transfer
        Integral := (ManualOutput - Kp * Error) / Ki;  // Initialize integral
    END_IF;
END_METHOD
```

## Common Defects and Mitigations

| Defect | Impact | Detection | Mitigation |
|--------|--------|-----------|------------|
| Integral windup | Slow recovery, oscillation | Output saturation | Anti-windup clamping |
| Derivative noise | Erratic control | High-frequency output | Filter derivative term |
| Sample rate too low | Poor performance | Phase lag, slow response | Increase sample rate |
| Sample rate too high | Computation overload | WCET > period | Decrease sample rate |
| Fixed-point overflow | Wraparound, incorrect values | Range analysis | Increase bit width, scale |
| Unit inconsistency | Incorrect calculations | Static analysis | Fix unit annotations |
| Algebraic loop | Solver failure | Causal analysis | Manual tearing |
| No anti-windup | Controller lockup | Manual/auto transfer | Implement anti-windup |
| No saturation handling | Actuator damage | Output > limits | Clamp output |
| Timing violation | Unstable control | WCET > period | Optimize code, reduce complexity |
| Numerical instability | NaN, Inf | Range checking | Use saturation, limit derivatives |
| Bumpless transfer issue | Output jump | Manual/auto switch | Initialize controller state |

## Testing Control Systems

### Unit Testing

**Test cases for PID**:
1. **Zero error**: Output should be zero (with anti-windup)
2. **Constant error**: Output should ramp (integral term)
3. **Step change in reference**: Output should track with overshoot based on tuning
4. **Step change in measurement**: Output should compensate
5. **Saturation**: Integral should stop winding up
6. **Bumpless transfer**: Output should not jump when switching modes

### Integration Testing

**Hardware-in-loop (HIL) testing**:
- Connect control algorithm to simulated plant
- Inject realistic sensor noise
- Test with extreme inputs
- Verify real-time performance

### System Testing

**Full system tests**:
- Stability under various operating conditions
- Disturbance rejection
- Setpoint tracking
- Robustness to sensor noise
- Failure mode handling

## Verbosity

verbosity: V1
