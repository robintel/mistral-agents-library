---
type: pattern
family: risk
---

# Risk Correlation Pattern Contract

Attaches to any agent performing risk analysis where multiple risks may
interact — risk-analyst, modernization-agent, upgrade-planner, or any
agent that needs to understand how risks compound or influence each other.
This contract establishes the **standard framework for identifying,
analyzing, and managing risk correlations**.

Risk correlation is **not just identification** — it is **the recognition
that risks do not exist in isolation**. A single risk rarely occurs alone;
instead, risks interact, compound, and cascade. Understanding these
interactions is critical because:

- **Compound risks can be exponentially worse** than individual risks
- **Risk A may cause Risk B**, creating a cascade effect
- **Mitigating Risk A may reduce Risk B**, improving overall efficiency
- **Ignoring correlations leads to underestimation** of total risk exposure

## The Discipline

Risk correlation analysis transforms a **list of risks** into a **risk
system** — a network of interacting risks where the whole is greater
(or sometimes less) than the sum of its parts. Effective correlation
analysis requires:

- **System thinking**: Viewing risks as part of an interconnected system
- **Causal analysis**: Understanding what causes what
- **Quantitative modeling**: Calculating the combined effect of correlated risks
- **Scenario analysis**: Considering how risks might play out together

- **Correlation is not always bad**: Some risks are negatively correlated
  (one reduces the impact of another)
- **Correlation changes over time**: Risks that are independent today may
  become correlated tomorrow
- **Correlation is context-dependent**: The same two risks may correlate
  differently in different contexts
- **Network effects matter**: Risk A correlates with B, which correlates with
  C, creating indirect correlations

## Correlation Types

### 1. Positive Correlation (Compound Risks)
**Definition**: Two risks where the occurrence or impact of one **increases**
the likelihood or impact of the other.

**Mechanisms**:
- **Causal**: Risk A directly causes Risk B
- **Shared Root Cause**: Both risks share a common underlying cause
- **Cascading**: Risk A triggers a chain reaction leading to Risk B
- **Resource Conflict**: Both risks compete for the same limited resource
- **Amplifying**: Risk A amplifies the impact of Risk B

**Example**:
- Hardware compatibility issue (Risk A) increases the likelihood of
  I/O mapping problems (Risk B) because both stem from integration
  complexity
- Schedule delay (Risk A) causes cost overrun (Risk B) as team works
  overtime to catch up

**Impact**: Combined risk is **greater than** the sum of individual risks

---

### 2. Negative Correlation (Mitigating Risks)
**Definition**: Two risks where the occurrence or impact of one **reduces**
the likelihood or impact of the other.

**Mechanisms**:
- **Alternative Paths**: Risk A provides a backup if Risk B occurs
- **Redundancy**: Multiple independent systems reduce overall risk
- **Diversity**: Different approaches reduce common failure modes
- **Compensating**: Risk A has characteristics that offset Risk B

**Example**:
- Having a backup supplier (Risk A: supplier dependency) reduces the
  impact of a primary supplier failure (Risk B: supply chain disruption)
- Multiple independent verification methods (Risk A: testing overhead)
  reduce the probability of undetected defects (Risk B: quality issues)

**Impact**: Combined risk is **less than** the sum of individual risks

---

### 3. Neutral Correlation (Independent Risks)
**Definition**: Two risks with **no interaction** — the occurrence or impact
of one has no effect on the other.

**Characteristics**:
- Different root causes
- No shared dependencies
- No causal relationship
- No resource conflicts
- No amplifying or mitigating effects

**Example**:
- Software bug in unrelated modules
- Hardware failure and unrelated security vulnerability
- Business risk in different market segments

**Impact**: Combined risk equals the sum of individual risks

---

### 4. Conditional Correlation
**Definition**: Risks that are correlated **only under specific conditions**.

**Mechanisms**:
- **Context-dependent**: Correlation exists only in certain contexts
- **Threshold-dependent**: Correlation appears only beyond certain thresholds
- **Time-dependent**: Correlation exists only during certain time periods
- **State-dependent**: Correlation exists only in certain system states

**Example**:
- Cost overrun and schedule delay correlate only when there are
  fixed deadlines (otherwise they may be independent)
- Hardware failure and data loss correlate only if there are no
  redundancy mechanisms in place

**Impact**: Correlation must be evaluated in context

## Correlation Framework

### Correlation Factors

The strength of correlation between two risks is quantified by a **correlation
factor** (r) ranging from -1 to +1:

| Factor Range | Correlation Type | Interpretation |
|--------------|------------------|----------------|
| -1.0 to -0.3 | Strong Negative | Risks significantly mitigate each other |
| -0.3 to -0.1 | Weak Negative | Risks have slight mitigating effect |
| -0.1 to +0.1 | Neutral | Risks are independent |
| +0.1 to +0.3 | Weak Positive | Risks have slight compounding effect |
| +0.3 to +0.7 | Moderate Positive | Risks significantly compound |
| +0.7 to +1.0 | Strong Positive | Risks are highly interdependent |

**Determining correlation factors**:
1. **Expert judgment**: Based on experience and domain knowledge
2. **Historical data**: Analysis of past incidents and near-misses
3. **Causal analysis**: Mapping of cause-effect relationships
4. **Statistical analysis**: Correlation coefficients from data
5. **Simulation**: Modeling risk interactions in scenario analysis

### Compound Risk Calculation

When risks are correlated, the **compound risk score** accounts for their
interaction:

```
Compound Score = (Score_A + Score_B) × (1 + r × min(Score_A, Score_B) / 25)
```

Where:
- `Score_A` and `Score_B` are the individual weighted risk scores (1-25+)
- `r` is the correlation factor (-1 to +1)
- The formula scales the sum based on correlation strength and magnitude

**Simplified approach** (for practical use):
```
Compound Score = (Score_A + Score_B) × (1 + r)
```

This treats the correlation as a direct multiplier on the combined score.

**Example calculations**:

| Risk A | Risk B | Correlation | Compound Score | Interpretation |
|--------|--------|-------------|----------------|----------------|
| 12 | 12 | +0.8 | (12+12)×1.8 = 43.2 | Strong compounding |
| 12 | 9 | +0.5 | (12+9)×1.5 = 31.5 | Moderate compounding |
| 12 | 12 | 0 | (12+12)×1 = 24 | Independent |
| 12 | 9 | -0.3 | (12+9)×0.7 = 14.7 | Slight mitigation |

### Correlation Matrix

Represent risk correlations in a matrix format:

```
                    Risk B    Risk C    Risk D
                ┌─────────┬─────────┬─────────┐
            A   │    0.8   │    0.2   │   -0.1   │
            ┌───┼─────────┼─────────┼─────────┤
            B   │    -     │    0.5   │    0.0   │
            ├───┼─────────┼─────────┼─────────┤
            C   │    -     │    -     │   -0.3   │
            ├───┼─────────┼─────────┼─────────┤
            D   │    -     │    -     │    -     │
            └───┴─────────┴─────────┴─────────┘
```

**Matrix properties**:
- Diagonal is always 1.0 (risk perfectly correlates with itself)
- Matrix is symmetric (correlation between A and B = correlation between B and A)
- Values range from -1 to +1
- Empty cells or "-" indicate no correlation assessment yet

## Correlation Analysis Workflow

### Phase 1: Correlation Identification

**Step 1: List all identified risks**
- Create a comprehensive list of all risks from the risk register
- Ensure each risk has a clear description and score

**Step 2: Identify potential correlations**
- Look for risks with shared root causes
- Identify risks that could cause or influence each other
- Look for risks affecting the same components or systems
- Consider temporal relationships (does one risk make another more likely?)

**Step 3: Use correlation indicators**

**Shared Attributes Indicating Correlation**:
- Same root cause or contributing factor
- Same system, component, or subsystem
- Same timeframe or phase
- Same stakeholders or teams
- Same dependencies or constraints
- Same failure mode or scenario

**Red Flags for Strong Correlation**:
- "If X happens, Y is very likely to happen"
- "X and Y are both caused by Z"
- "X makes Y worse"
- "X and Y affect the same critical path"
- "X and Y have occurred together in the past"

### Phase 2: Correlation Assessment

**Step 4: Assess correlation type**
For each potential correlation:
1. Determine if it's positive, negative, or neutral
2. Identify the correlation mechanism (causal, shared root cause, etc.)
3. Document the rationale

**Step 5: Estimate correlation strength**
- Use the correlation factor scale (-1 to +1)
- Start with expert judgment
- Refine with data if available
- Document uncertainty in the estimate

**Step 6: Validate with stakeholders**
- Review correlations with domain experts
- Validate with affected stakeholders
- Adjust based on feedback

### Phase 3: Compound Risk Calculation

**Step 7: Calculate compound scores**
- For each correlated risk pair, calculate the compound score
- Use the appropriate correlation formula
- Document the calculation

**Step 8: Identify critical correlations**
- Flag correlations with high compound scores
- Identify correlations that create new critical risks
- Highlight correlations that cross risk level thresholds

**Step 9: Build correlation network**
- Create a visual map of risk correlations
- Identify clusters of highly correlated risks
- Find central risks that correlate with many others

## Correlation Patterns

### Common Correlation Patterns

#### 1. Cascade Pattern
**Description**: Risk A triggers Risk B, which triggers Risk C, etc.

**Example**:
- Hardware failure → System crash → Data corruption → Extended downtime

**Analysis**:
- Each step in the cascade may have different probabilities
- Total impact compounds through the chain
- Mitigation at any point can break the cascade

**Visualization**:
```
Risk A → Risk B → Risk C → Risk D
```

#### 2. Common Cause Pattern
**Description**: Multiple risks share a common root cause.

**Example**:
- Poor requirements → Design flaws → Implementation errors → Testing gaps

**Analysis**:
- Addressing the root cause mitigates all downstream risks
- Risks may have different impacts but same likelihood
- Root cause analysis is critical

**Visualization**:
```
    Root Cause
      ├─► Risk A
      ├─► Risk B
      └─► Risk C
```

#### 3. Resource Conflict Pattern
**Description**: Multiple risks compete for the same limited resource.

**Example**:
- Schedule pressure → Cut corners → Quality issues
- Budget constraints → Reduce testing → Defects in production

**Analysis**:
- Resource allocation decisions affect multiple risks
- Trade-offs must be explicitly managed
- Buffer resources to reduce correlation

**Visualization**:
```
Limited Resource
  ┌─────────┴─────────┐
  ▼                     ▼
Risk A              Risk B
```

#### 4. Amplification Pattern
**Description**: Risk A amplifies the impact of Risk B.

**Example**:
- Lack of monitoring (Risk A) → When failure occurs (Risk B), it's not detected
- Complex system (Risk A) → Bugs (Risk B) are harder to find and fix

**Analysis**:
- The amplifier risk may have low individual impact
- But it significantly increases the impact of other risks
- Often overlooked because the amplifier itself isn't severe

**Visualization**:
```
Risk A
  │
  ▼ (amplifies)
Risk B
```

#### 5. Redundancy Pattern
**Description**: Multiple independent risks provide redundancy or backup.

**Example**:
- Primary supplier failure (Risk A) + Backup supplier available (Risk B)
- Multiple verification methods reduce undetected defect risk

**Analysis**:
- Negative correlation between risks
- Provides system resilience
- But adds complexity and cost

**Visualization**:
```
Risk A ◄─────► Risk B
   (negatively correlated)
```

#### 6. Cluster Pattern
**Description**: Multiple risks that are all correlated with each other.

**Example**:
- Integration risks (compatibility, data migration, interface complexity)
- Modernization risks (legacy knowledge loss, new technology learning curve)

**Analysis**:
- Forms a risk cluster that must be managed together
- May require dedicated risk management approach
- Often indicates a complex project area

**Visualization**:
```
   Risk A
  /    \
 /      \
Risk B──Risk C
 \      /
  \    /
   Risk D
```

## Correlation Management Strategies

### For Positive Correlations

**Strategy**: Reduce, Isolate, or Accept

| Strategy | Description | When to Use | Example |
|----------|-------------|-------------|---------|
| **Reduce Correlation** | Address shared root causes or dependencies | Root cause is addressable | Improve integration testing to reduce compatibility and I/O mapping correlations |
| **Isolate Risks** | Break dependencies between risks | Risks can be decoupled | Use modular design to isolate failure modes |
| **Accept Compound Risk** | Accept the compound risk with mitigation | Correlation cannot be reduced | Accept schedule+cost correlation, add contingency budget |
| **Transfer** | Transfer the compound risk to another party | Third party can better manage | Insurance for correlated operational risks |

### For Negative Correlations

**Strategy**: Preserve, Strengthen, or Leverage

| Strategy | Description | When to Use | Example |
|----------|-------------|-------------|---------|
| **Preserve Redundancy** | Maintain the mitigating relationship | Redundancy provides value | Keep backup suppliers to mitigate supply chain risks |
| **Strengthen Mitigation** | Increase the negative correlation | Mitigation can be enhanced | Add more verification methods to reduce defect risk |
| **Leverage Diversity** | Use different approaches to create negative correlation | Multiple independent methods | Use diverse verification approaches |
| **Document** | Document the mitigating effect for credit | Need to demonstrate risk reduction | Document how redundancy reduces overall risk |

### For Neutral Correlations

**Strategy**: Monitor
- Track both risks independently
- Watch for emerging correlations
- Reassess periodically

## Correlation Analysis Techniques

### 1. Cause-Effect Diagrams
**Purpose**: Visualize causal relationships between risks.

**Method**:
1. List all risks
2. For each risk, ask "what causes this?" and "what does this cause?"
3. Draw arrows from causes to effects
4. Identify causal chains and feedback loops

**Example**:
```
[Schedule Pressure] ──► [Cut Corners] ──► [Quality Issues] ──► [Rework]
                                      ↘
                                       [Customer Dissatisfaction]
```

### 2. Risk Correlation Matrix
**Purpose**: Systematically assess all pairwise correlations.

**Method**:
1. Create a matrix with all risks on both axes
2. For each pair, assess correlation strength and type
3. Fill in the matrix
4. Identify patterns and clusters

### 3. Sensitivity Analysis
**Purpose**: Understand how changes in one risk affect others.

**Method**:
1. Identify a target risk
2. Vary its probability or impact
3. Observe changes in correlated risks
4. Identify which correlations are most sensitive

### 4. Scenario Analysis
**Purpose**: Explore how correlated risks might play out in different scenarios.

**Method**:
1. Define scenarios (best case, worst case, most likely)
2. For each scenario, determine which risks occur
3. Calculate compound impact
4. Identify scenario-specific correlations

**Example Scenario**:
```
Scenario: "Integration Phase Delays"
- Risk A: Hardware compatibility issue (Probability: High, occurs)
- Risk B: I/O mapping problems (Probability: Medium, occurs due to A)
- Risk C: Schedule delay (Probability: High, occurs due to A+B)
- Correlation: A→B (strong positive), A→C (moderate), B→C (moderate)
- Compound Score: Higher than any individual risk
```

### 5. Monte Carlo Simulation
**Purpose**: Quantify the probability distribution of compound risks.

**Method**:
1. Define probability distributions for each risk
2. Define correlation structure
3. Run multiple simulations (thousands)
4. Analyze distribution of outcomes
5. Identify probabilities of different impact levels

## Correlation Visualization

### Visualization Techniques

#### Correlation Graph
- **Nodes**: Risks
- **Edges**: Correlations (thickness = strength, color = type)
- **Clusters**: Groups of highly correlated risks

#### Risk Network Map
- **Layout**: Force-directed or hierarchical
- **Color coding**: By risk level, category, or correlation type
- **Size**: By individual risk score

#### Heat Map
- **Axes**: Risks
- **Colors**: Correlation strength (red = positive, blue = negative, white = neutral)

#### Flow Diagram
- **Nodes**: Risks and events
- **Arrows**: Causal relationships with correlation factors

## Correlation Pitfalls

| Pitfall | Description | Detection | Prevention |
|---------|-------------|-----------|------------|
| **False correlation** | Assuming correlation where none exists | Correlation not supported by evidence | Require evidence for all correlations |
| **Over-correlation** | Seeing correlations everywhere | Too many strong correlations | Use conservative estimates, validate |
| **Ignoring negative correlations** | Only looking for positive correlations | Missed mitigation opportunities | Actively look for negative correlations |
| **Static correlations** | Assuming correlations don't change | Correlations don't reflect current state | Periodically reassess correlations |
| **Ignoring indirect correlations** | Only considering direct correlations | Missed cascading effects | Analyze multi-step correlations |
| **Over-simplification** | Treating all correlations as equal | All correlations same strength | Use full -1 to +1 scale |
| **Confirmation bias** | Only seeing correlations that confirm preconceptions | Correlations align with expectations | Use independent validation |
| **Data mining** | Finding spurious correlations in data | Correlations without causal mechanism | Require causal explanation |

## Correlation Validation

Validate correlation assessments through:

### Evidence Check
- Is there historical evidence of this correlation?
- Are there case studies or examples?
- Is the causal mechanism clear?

### Expert Review
- Have domain experts validated the correlation?
- Do stakeholders agree with the assessment?
- Have independent assessors reviewed?

### Sensitivity Check
- How sensitive are the results to correlation strength?
- What if the correlation is stronger/weaker than estimated?
- Does the correlation significantly change the risk picture?

### Stress Testing
- Test under extreme scenarios
- How do correlations behave at boundaries?
- Are there non-linear effects?

## Tooling Integration

Integrate correlation analysis with:
- **Spreadsheets**: For correlation matrices and calculations
- **Network analysis tools**: For correlation graph visualization
- **Simulation tools**: For scenario and Monte Carlo analysis
- **Risk management software**: For tracking and analyzing correlations
- **Data analysis tools**: For statistical correlation analysis

## Best Practices

1. **Start with causal analysis**: Understand why risks are correlated before quantifying
2. **Use multiple methods**: Combine expert judgment with data and analysis
3. **Validate correlations**: Don't accept unvalidated correlation assessments
4. **Document rationale**: Explain why each correlation exists and its strength
5. **Reassess periodically**: Correlations can change over time and with context
6. **Focus on high-impact correlations**: Prioritize correlations that significantly affect the risk picture
7. **Visualize correlations**: Use graphs and diagrams to communicate correlation structures
8. **Consider indirect correlations**: Look beyond direct pairwise correlations
9. **Balance thoroughness and practicality**: Don't let correlation analysis become analysis paralysis
10. **Use conservative estimates**: When in doubt, assume stronger positive correlation

## Interface Contract

When implementing correlation analysis in an agent:

**Required**:
- Identify correlated risk pairs
- Assess correlation type (positive, negative, neutral)
- Estimate correlation strength (-1 to +1)
- Calculate compound scores for correlated pairs

**Recommended**:
- Provide correlation rationale and evidence
- Include correlation confidence level
- Support correlation visualization
- Enable sensitivity analysis

**Output format**:
```
{
  "risk_pairs": [
    {
      "risk_a": "<risk_id>",
      "risk_b": "<risk_id>",
      "correlation_type": "<positive|negative|neutral|conditional>",
      "correlation_factor": < -1.0 to 1.0 >,
      "correlation_rationale": "<text>",
      "correlation_mechanism": "<causal|shared_root_cause|cascading|resource_conflict|amplifying|redundancy>",
      "compound_score": <calculated>,
      "correlation_confidence": "<High|Medium|Low>",
      "is_conditional": <boolean>,
      "condition": "<text, if conditional>"
    }
  ],
  "correlation_network": {
    "nodes": ["<risk_ids>"],
    "edges": [
      {
        "source": "<risk_id>",
        "target": "<risk_id>",
        "factor": < -1.0 to 1.0 >,
        "type": "<positive|negative|neutral>"
      }
    ]
  },
  "critical_correlations": ["<list of high-impact correlation pairs>"]
}
```

## Validation Checkpoints

- [ ] All potential correlations have been identified
- [ ] Correlation type and strength are documented for each pair
- [ ] Correlation rationales are provided and validated
- [ ] Compound scores are calculated correctly
- [ ] Critical correlations are identified and flagged
- [ ] Correlation network is mapped and understood
- [ ] Sensitivity analysis has been performed for critical correlations
- [ ] Correlations have been validated with stakeholders
