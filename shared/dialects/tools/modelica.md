---
type: language
family: modeling
---

# Modelica Language Contract

**Attaches** when the brief references Modelica (`.mo` files), OpenModelica, or model-based control system design.

## Language Overview

Modelica is an **acausal, equation-based, object-oriented** modeling language for complex physical systems. It is designed for multi-domain modeling (mechanical, electrical, thermal, hydraulic, control) with a focus on **physical correctness** and **reusability**.

Key characteristics:
- **Acausal**: Equations define relationships without explicit direction of computation
- **Equation-based**: Systems are defined by mathematical equations, not assignment statements
- **Object-oriented**: Models are classes that can be extended and instantiated
- **Component-based**: Systems are built by connecting components
- **Multi-domain**: Supports mechanical, electrical, thermal, fluid, control, and other domains

## Eras

**Modelica 1.0-2.2** (1997-2000): Foundational language, basic features
- First public release in 1997
- Basic equation and algorithm sections
- Simple component connections
- Limited library support

**Modelica 3.0-3.2** (2002-2008): Standardization and library expansion
- Modelica Specification 3.0 (2003) - major revision
- Modelica Standard Library (MSL) 1.0
- Improved tool support
- Formal language specification
- Status: Legacy, mostly replaced

**Modelica 3.3-3.4** (2012-2017): Modern features
- Modelica Specification 3.3 (2012)
- MSL 3.2 with comprehensive multi-domain libraries
- Improved optimization support
- Better support for real-time systems
- Status: Current mainstream

**Modelica 3.5+** (2021+): Latest features
- Modelica Specification 3.5 (2021)
- MSL 4.0 with enhanced libraries
- New language features: annotations for FMI/FMU, improved array handling
- Better support for embedded systems
- Status: Current, recommended

**Era detection**: By the `modelicaVersion` annotation or file header comment. Default to 3.4 if unspecified.

## Language Structure

### Model Definition

```modelica
model ModelName "Optional description"
  // Parameters (constants)
  parameter Real Kp = 1.0 "Proportional gain";
  parameter Real Ki = 0.1 "Integral gain";
  
  // Variables (unknowns)
  Real error "Control error";
  Real integral(start=0) "Integral of error";
  
  // Components
  Modelica.Blocks.Interfaces.RealInput reference;
  Modelica.Blocks.Interfaces.RealInput measurement;
  Modelica.Blocks.Interfaces.RealOutput control;

  // Equations
 equation
  error = reference - measurement;
  der(integral) = error;
  control = Kp * error + Ki * integral;

end ModelName;
```

### Component Types

- **model**: Continuous-time model, may contain differential equations
- **block**: Causal block with inputs and outputs (similar to Simulink blocks)
- **type**: Data type definition
- **package**: Container for models and types
- **function**: Mathematical function (algorithmic, not equation-based)
- **record**: Data structure
- **connector**: Defines connection points
- **class**: Generic class (can be specialized)

### Sections

1. **Equation Section** (`equation`): Contains equations that define the model's behavior
2. **Algorithm Section** (`algorithm`): Contains assignment statements (for functions and when statements)
3. **Initial Equation Section** (`initial equation`): Equations only evaluated at initialization
4. **Initial Algorithm Section** (`initial algorithm`): Assignments only executed at initialization

### Variables and Parameters

| Declaration | Description | Example |
|-------------|-------------|---------|
| `parameter` | Constant, known at compile time | `parameter Real Kp=1.0;` |
| `constant` | True constant, cannot be changed | `constant Real pi=3.14159;` |
| `Real` | Real number variable | `Real x;` |
| `Integer` | Integer variable | `Integer n;` |
| `Boolean` | Boolean variable | `Boolean enabled;` |
| `String` | String variable | `String name;` |

**Attributes**:
- `start=value`: Initial guess for solver
- `fixed=true`: Value is fixed, not solved for
- `unit="V"`: Physical unit
- `displayUnit="kV"`: Display unit
- `min=0`, `max=100`: Value constraints
- `nominal=1`: Nominal value for scaling

### Units

**Built-in SI units**:
- `m` (meter), `kg`, `s`, `A`, `K`, `mol`, `cd`
- `N` (Newton), `Pa` (Pascal), `J` (Joule), `W` (Watt)
- `V` (Volt), `Ohm`, `F` (Farad), `H` (Henry)
- `rad` (radian), `Hz` (Hertz)

**Unit definitions**:
```modelica
type Voltage = Real(unit="V");
type Current = Real(unit="A");
type Resistance = Real(unit="Ohm");
```

**Unit checking**: Modelica enforces dimensional consistency in equations.

### Connections

**Connect statement**: Creates equations between connector variables
```modelica
model ElectricalCircuit
  Modelica.Electrical.Analog.Basic.Resistor R(R=10);
  Modelica.Electrical.Analog.Sources.ConstantVoltage V(V=10);
  Modelica.Electrical.Analog.Basic.Ground G;
 equation
  connect(V.p, R.p);  // V.p = R.p
  connect(R.n, G.p);  // R.n = G.p = 0
end ElectricalCircuit;
```

**Connector classes**: Define what can be connected
```modelica
connector Pin
  Real v "Voltage at pin";
  flow Real i "Current into pin";
end Pin;
```

- `flow` prefix: Variables that sum to zero at connections (Kirchhoff's current law)
- Non-flow: Variables that are equal at connections (Kirchhoff's voltage law)

### Equations

**Basic equations**:
```modelica
equation
  x + y = z;           // Simple equation
  der(x) = v;          // Differential equation
  x^2 + y^2 = r^2;     // Nonlinear equation
  if x > 0 then        // Conditional equation
    y = 1;
  else
    y = -1;
  end if;
```

**Special equation forms**:
- `der(x)`: Time derivative of x
- `pre(x)`: Value of x at previous event
- `edge(x)`: Rising edge of Boolean x
- `change(x)`: x has changed value
- `initial()`: At initialization
- `terminal()`: At end of simulation

### Functions

**Function definition**:
```modelica
function square "Compute square of a number"
  input Real x;
  output Real y;
algorithm
  y := x * x;
end square;
```

**Built-in functions**:
- Mathematical: `abs`, `sqrt`, `exp`, `log`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`
- Vector/matrix: `zeros`, `ones`, `identity`, `transpose`, `inverse`, `solve`
- Special: `der`, `pre`, `edge`, `change`, `initial`, `terminal`

### Arrays

**Array declaration**:
```modelica
Real A[3,3] "3x3 matrix";
Real B[:] "Dynamically sized array";
Real C[5] = {1,2,3,4,5} "Initialized array";
```

**Array operations**:
```modelica
A = zeros(3,3);
B = ones(5);
C = transpose(A);
D = A * B;  // Matrix multiplication
```

### Conditional and Iterative Constructs

**If-then-else**:
```modelica
if x > 0 then
  y = 1;
elseif x == 0 then
  y = 0;
else
  y = -1;
end if;
```

**For loop** (in algorithm sections):
```modelica
for i in 1:10 loop
  A[i] := i * 2;
end for;
```

**While loop** (in algorithm sections):
```modelica
while x < 10 loop
  x := x + 1;
end while;
```

**When statement** (for events):
```modelica
when x > threshold then
  y = 1;
end when;
```

### Inheritance and Modification

**Extends**:
```modelica
model ExtendedModel extends BaseModel
  // Additional equations
end ExtendedModel;
```

**Modification**:
```modelica
model MyResistor extends Modelica.Electrical.Analog.Basic.Resistor(
  R=100  // Modify parameter
);
```

**Redeclaration**:
```modelica
model MyModel
  replaceable Modelica.Electrical.Analog.Basic.Resistor R(R=10);
end MyModel;

// Usage
MyModel myInstance(redeclare Modelica.Electrical.Analog.Basic.Resistor R(R=100));
```

### Annotations

**Standard annotations**:
```modelica
model MyModel "Description"
  annotation (
    Icon(coordinateSystem(preserveAspectRatio=false)),
    Diagram(coordinateSystem(preserveAspectRatio=false)),
    Documentation(info="<html>...</html>", revisions="<html>...</html>"),
    experiment(StopTime=1.0, Tolerance=1e-6)
  );
end MyModel;
```

**FMI/FMU annotations** (for co-simulation):
```modelica
model MyModel
  annotation (
    uses(Modelica(version="3.4")),
    fmiVersion="2.0",
    fmiExport=true
  );
end MyModel;
```

### Modelica Standard Library (MSL)

**Key packages**:
- `Modelica.Bocks`: Control system blocks (PID, transfer functions, sources, etc.)
- `Modelica.Mechanics`: Mechanical systems (rotational, translational)
- `Modelica.Electrical`: Electrical systems (analog, digital, machines)
- `Modelica.Thermal`: Thermal systems (heat transfer, fluid heat flow)
- `Modelica.Fluid`: Fluid systems (hydraulics, pneumatics)
- `Modelica.Magnetic`: Magnetic systems
- `Modelica.SIunits`: SI unit definitions
- `Modelica.Icons`: Standard icons

**Common block types**:
- `Modelica.Blocks.Continuous`: TransferFunction, PID, LimPID, etc.
- `Modelica.Blocks.Discrete`: Sample, Hold, Delay, etc.
- `Modelica.Blocks.Sources`: Constant, Ramp, Sine, etc.
- `Modelica.Blocks.Math`: Add, Multiply, Divide, SquareRoot, etc.
- `Modelica.Blocks.Logical`: And, Or, Not, Compare, etc.

## Common Pitfalls

### Unit Inconsistencies
```modelica
// WRONG: Inconsistent units
parameter Real Kp(unit="1/V") = 1.0;
parameter Real Ki(unit="1/s") = 0.1;
Real error(unit="V");
Real output;
equation
  output = Kp * error + Ki * integral(error);  // ERROR: Ki*integral has unit V*s, not V
```

**Fix**: Ensure all terms in an equation have compatible units.

### Algebraic Loops
```modelica
model AlgebraicLoop
  Real x, y;
equation
  x = y + 1;
  y = x * 2;  // Algebraic loop: x and y depend on each other
end AlgebraicLoop;
```

**Fix**: Use `algorithm` section with assignment statements, or restructure the model.

### High Index DAEs
```modelica
model HighIndex
  Real x, y, z;
  parameter Real k=1;
equation
  der(x) = y;
  der(y) = z;
  z = k * x;  // Index 2 DAE (derivative of constraint appears)
end HighIndex;
```

**Fix**: Use index reduction (Pantelides algorithm) or manual reduction.

### Parameter Binding
```modelica
model UnboundParameter
  parameter Real K;
  Real x;
equation
  x = K * time;  // ERROR: K is unbound
end UnboundParameter;
```

**Fix**: Provide default value or bind when instantiating.

### Initialization Issues
```modelica
model InitProblem
  Real x(start=1);
  Real y;
equation
  x + y = 0;  // Initial equation: 1 + y = 0
  der(x) = y;
end InitProblem;
```

**Fix**: Add initial equations or use `initial equation` section.

## Best Practices

### Model Organization
1. **Use hierarchical structure**: Organize models in packages
2. **Document everything**: Use annotations for documentation
3. **Use meaningful names**: Variables, parameters, models
4. **Keep models focused**: One model, one purpose
5. **Use types**: For parameters and variables with same units

### Physical Modeling
1. **Always use units**: Annotate all physical quantities
2. **Check unit consistency**: Before simulation
3. **Use MSL components**: When available, instead of reinventing
4. **Keep acausal**: Prefer equations over assignments
5. **Avoid algebraic loops**: Restructure or use tearing

### Control Systems
1. **Use Blocks library**: For control system components
2. **Sample appropriately**: Choose sample rate based on system dynamics
3. **Handle anti-windup**: In PID controllers
4. **Check stability**: Before deployment
5. **Validate ranges**: For all signals

### Performance
1. **Minimize state count**: For real-time targets
2. **Use discrete models**: When continuous not needed
3. **Simplify expressions**: For embedded targets
4. **Avoid division**: In fixed-point implementations
5. **Pre-compute constants**: At initialization

## Integration with Other Tools

### OpenModelica
- Open-source Modelica implementation
- Command-line: `omc` compiler
- GUI: OMEdit
- Simulation: OMSimulator

### JModelica.org
- Open-source Modelica implementation
- Focus on optimization and advanced analysis
- Python integration

### FMI/FMU
- Functional Mock-up Interface standard
- Allows co-simulation between tools
- Modelica models can be exported as FMUs

### Python
- PyModelica: Python interface to OpenModelica
- ModelicaPython: Pure Python Modelica interpreter (limited)
- SymPy: For symbolic manipulation of Modelica equations

### MATLAB/Simulink
- Modelica can be imported into Simulink via FMI
- Simulink blocks can be exported to Modelica (limited)
- Modelica Standard Library has Simulink-compatible components

## Common Defects and Findings

| Defect | Impact | Detection | Mitigation |
|--------|--------|-----------|------------|
| Missing unit | Incorrect calculations | Static analysis | Add unit annotation |
| Unit inconsistency | Simulation failure | Type checking | Fix equation or unit |
| Algebraic loop | Solver failure | Causal analysis | Manual tearing, use algorithm |
| High DAE index | Numerical issues | Index analysis | Index reduction |
| Unbound parameter | Compilation error | Static analysis | Add default or binding |
| Initialization issue | Wrong start values | Simulation warning | Add initial equations |
| Division by zero | Runtime error | Range analysis | Add guard clause |
| Array bounds error | Runtime error | Static analysis | Check array sizes |
| Type mismatch | Compilation error | Type checking | Fix type annotations |
| Missing annotation | Poor documentation | Static analysis | Add annotations |

## Example: PID Controller

```modelica
within YourPackage;
model PID "Proportional-Integral-Derivative Controller"
  extends Modelica.Blocks.Icons.Block;
  
  // Parameters
  parameter Real Kp=1.0 "Proportional gain" annotation(Dialog);
  parameter Real Ki=0.1 "Integral gain" annotation(Dialog);
  parameter Real Kd=0.01 "Derivative gain" annotation(Dialog);
  parameter Real Ti=1.0 "Integral time constant" annotation(Dialog);
  parameter Real Td=0.1 "Derivative time constant" annotation(Dialog);
  parameter Real yMax=1e6 "Maximum output" annotation(Dialog);
  parameter Real yMin=-1e6 "Minimum output" annotation(Dialog);
  parameter Real xStart=0 "Initial value of integrator" annotation(Dialog);
  
  // Inputs
  Modelica.Blocks.Interfaces.RealInput u "Input signal";
  Modelica.Blocks.Interfaces.RealInput y "Measurement signal";
  
  // Output
  Modelica.Blocks.Interfaces.RealOutput yCtrl "Control signal";

  // Internal variables
  Real error "Control error";
  Real integral(start=xStart) "Integral of error";
  Real derivative "Derivative of error";
  Real derivative_filtered(start=0) "Filtered derivative";

  // PID algorithm
  Modelica.Blocks.Continuous.LimPID pid(
    K=Kp,
    Ti=Ti,
    Td=Td,
    yMax=yMax,
    yMin=yMin,
    xStart=xStart
  );

 equation
  // Connect signals
  connect(u, pid.u);
  connect(y, pid.y);
  connect(pid.yCtrl, yCtrl);

  annotation (
    Icon(coordinateSystem(preserveAspectRatio=false)),
    Diagram(coordinateSystem(preserveAspectRatio=false)),
    Documentation(info="<html>\n<h4>PID Controller</h4>\n<p>Standard PID controller with anti-windup and filtering.</p>\n</html>")
  );
end PID;
```

## Example: Spring-Mass-Damper System

```modelica
model SpringMassDamper "Mechanical Spring-Mass-Damper System"
  extends Modelica.Mechanics.Translational.Interfaces.PartialCompliant;
  
  // Parameters
  parameter Real m=1.0 "Mass" annotation(Dialog);
  parameter Real c=0.1 "Damping coefficient" annotation(Dialog);
  parameter Real k=10.0 "Spring constant" annotation(Dialog);
  
  // State variables
  Real x "Position"
  Real v "Velocity"
  Real a "Acceleration"

  // Flange for connection
  Modelica.Mechanics.Translational.Interfaces.Flange_a flange_a;
  Modelica.Mechanics.Translational.Interfaces.Flange_b flange_b;

 equation
  // Newton's second law
  m * a = flange_a.f + flange_b.f;
  
  // Kinematics
  v = der(x);
  a = der(v);
  
  // Spring and damper forces
  flange_a.f = k * (x - flange_b.s) + c * (v - flange_b.v);
  flange_b.f = -flange_a.f;
  
  // Connection equations
  flange_a.s = x;
  flange_a.v = v;
  flange_b.s = x;
  flange_b.v = v;
  
  annotation (
    Icon(coordinateSystem(preserveAspectRatio=false)),
    Documentation(info="<html>\n<h4>Spring-Mass-Damper</h4>\n<p>1D translational mechanical system with spring, mass, and damper.</p>\n</html>")
  );
end SpringMassDamper;
```
