---
type: pattern
family: risk
---

# Risk Scoring Pattern Contract

Attaches to any agent performing risk assessment — risk-analyst, upgrade-planner,
modernization-agent, threat-modeler, model-validator, or any future risk-evaluating
agent. This contract establishes the **standardized scoring framework** that
enables consistent risk comparison and prioritization across all domains.

Risk scoring is **not just calculation** — it is **the language of risk** that
allows disparate domains (control systems, security, business) to communicate
risk severity in a common currency. A consistent scoring framework ensures
that technical risks can be compared with business risks, and that compound
risks can be calculated across domains.

## The Discipline

Risk scoring transforms qualitative risk assessment into quantitative
comparison. Without standardized scoring, risk discussions become
subjective and incomparable — what one engineer considers "high risk" may
be "medium" to another. The scoring framework must be:

- **Consistent**: Same scoring criteria across all domains
- **Transparent**: Clear how scores are calculated and what they mean
- **Actionable**: Scores map directly to mitigation priorities
- **Comparable**: Scores from different domains can be meaningfully compared
- **Extensible**: Framework supports domain-specific adjustments

- **Probability and impact are multiplicative**: Risk is the product of
  likelihood and consequence, not the sum
- **Weight accounts for context**: Some risk categories matter more in
  certain contexts (safety in aerospace, security in finance)
- **Scores drive decisions**: Scoring must directly inform go/no-go and
  prioritization decisions
- **Calibration is required**: Scoring scales must be consistently applied
  across assessors

## The Scoring Formula

```
Risk Score = Probability × Impact × Category Weight
```

Where:
- **Probability (P)**: 1-5 scale representing likelihood
- **Impact (I)**: 1-5 scale representing consequence severity
- **Category Weight (W)**: 0.1-2.0 multiplier for domain/context adjustment
- **Result**: Typically ranges from 1-25 (before weight adjustment)

This multiplicative formula ensures that:
- High-probability AND high-impact risks get exponentially higher scores
- A risk with probability=1 and impact=5 scores 5, not 6 (avoids additive dilution)
- Category weights can emphasize critical domains without breaking the scale

## Probability Scale

The probability scale measures **likelihood of occurrence** within the project
or system lifecycle:

| Level | Score | Description | Example |
|-------|-------|-------------|---------|
| Rare | 1 | 1-10% chance | Hardware failure in first year of operation |
| Unlikely | 2 | 11-30% chance | Compatibility issue with minor dependency |
| Possible | 3 | 31-60% chance | Schedule delay due to resource constraints |
| Likely | 4 | 61-90% chance | Cost overrun on complex integration project |
| Almost Certain | 5 | 91-100% chance | Need for user training on new system |

**Calibration guidelines**:
- Use historical data when available (past project metrics, industry benchmarks)
- For novel scenarios, use expert judgment with conservative bias
- When in doubt, round up — it's better to overestimate risk than underestimate
- Document the rationale for each probability assessment

**Common probability biases to avoid**:
- **Optimism bias**: Assuming best-case scenarios
- **Confirmation bias**: Only considering evidence that supports preconceived notions
- **Availability bias**: Overweighting recent or memorable events
- **Anchoring**: Fixating on initial estimates without adjustment

## Impact Scale

The impact scale measures **consequence severity** if the risk materializes:

| Level | Score | Description | Example |
|-------|-------|-------------|---------|
| Negligible | 1 | Minimal, localized impact | Temporary minor performance degradation |
| Minor | 2 | Localized impact, quick recovery | Single subsystem requires restart |
| Moderate | 3 | Limited impact, some recovery time | 1-2 days of downtime for non-critical system |
| Major | 4 | Significant impact, extended recovery | Week-long outage, major data loss |
| Catastrophic | 5 | System failure, safety incident, business closure | Loss of life, environmental damage, company bankruptcy |

**Impact dimensions to consider**:
- **Technical**: System performance, reliability, maintainability
- **Financial**: Cost overruns, revenue loss, liability
- **Safety**: Human injury, environmental damage
- **Reputation**: Brand damage, customer trust loss
- **Compliance**: Regulatory penalties, certification loss
- **Operational**: Productivity loss, workflow disruption

**Impact assessment approach**:
1. Consider worst-case scenario (what's the maximum possible impact?)
2. Consider most likely scenario (what's the expected impact?)
3. Use the higher of the two for conservative assessment
4. Document both for context

## Category Weights

Category weights adjust the base score to reflect **domain importance** and
**context-specific priorities**:

| Category | Default Weight | Range | Rationale |
|----------|---------------|-------|-----------|
| Technical | 1.0 | 0.8-1.5 | Core system functionality |
| Business | 1.0 | 0.8-1.5 | Financial and market impact |
| Safety | 1.5 | 1.2-2.0 | Human life and environmental protection |
| Security | 1.0 | 0.8-1.2 | Data and system protection |
| Operational | 0.9 | 0.8-1.0 | Day-to-day operations impact |
| Compliance | 1.1 | 1.0-1.2 | Regulatory and standards adherence |

**Weight adjustment guidelines**:
- Increase weight for categories critical to the specific project
- Safety weight should always be >= 1.5 for safety-critical systems
- Adjust weights based on stakeholder priorities
- Document all weight adjustments in the risk assessment
- Keep total weighted score interpretable (avoid excessive weight inflation)

**Weight calculation example**:
```
Safety Risk: Probability=3, Impact=5, Weight=1.5
Base Score: 3 × 5 = 15
Weighted Score: 15 × 1.5 = 22.5
Interpretation: High-priority safety risk requiring immediate attention
```

## Score Interpretation

Standard interpretation of weighted risk scores:

| Score Range | Risk Level | Color Code | Action Required |
|-------------|------------|------------|----------------|
| 16-25+ | Critical | Red | Must address before proceeding |
| 12-15 | High | Orange | Should address before proceeding |
| 8-11 | Medium | Yellow | Can proceed with monitoring |
| 4-7 | Low | Light Yellow | Can proceed, monitor periodically |
| 1-3 | Very Low | Green | Accept, no action required |

**Context-specific adjustments**:
- For safety-critical systems (SIL 3-4, ASIL D): Treat scores >= 12 as Critical
- For business-critical systems: Treat scores >= 15 as Critical
- For experimental/low-consequence projects: Can relax thresholds by one level

**Escalation triggers**:
- Any single risk with score >= 15: Automatic escalation to t4
- Compound risk score >= 20: Automatic escalation to t4
- Safety-critical system with any risk score >= 12: Mandatory t4 review
- Multiple Critical risks simultaneously: Strongly recommend t4

## Scoring Workflow

### Step 1: Identify the Risk
- Clearly define the risk in specific, measurable terms
- Avoid vague descriptions like "things might go wrong"
- Example: "Hardware compatibility issue between PLC and new sensor" not "Integration problems"

### Step 2: Assess Probability
- Gather evidence: historical data, expert opinion, similar project experience
- Use the probability scale consistently
- Document the reasoning and any assumptions

### Step 3: Assess Impact
- Consider all impact dimensions
- Use the worst-case or most-likely scenario (whichever is higher)
- Document the expected consequences

### Step 4: Apply Category Weight
- Determine the primary risk category
- Apply the appropriate weight (default or adjusted)
- Document any weight adjustments

### Step 5: Calculate Score
- Multiply Probability × Impact × Weight
- Round to one decimal place for consistency

### Step 6: Validate Score
- Does the score feel right given the risk description?
- Compare with similar risks in the assessment
- Adjust if necessary and document rationale

## Calibration Techniques

### Calibration Workshop
Conduct a calibration session with the assessment team:
1. Select 5-10 example risks with known outcomes
2. Have each team member score them independently
3. Compare scores and discuss discrepancies
4. Establish common understanding of each scale point
5. Document calibration agreements for future reference

### Historical Calibration
Use historical data to calibrate scoring:
- Compare assessed scores with actual outcomes
- Adjust future scoring based on past accuracy
- Track calibration metrics over time

### Cross-Domain Calibration
Ensure consistency across domains:
- Technical team scores a set of risks
- Business team scores the same risks independently
- Compare and align scoring approaches
- Establish cross-domain scoring conventions

## Common Scoring Pitfalls

| Pitfall | Description | Detection | Prevention |
|---------|-------------|-----------|------------|
| **Central tendency** | All scores cluster around the middle | Score distribution is flat | Use full scale range, force distribution |
| **Range compression** | Not using full 1-5 scale | Scores only in 2-4 range | Train assessors on scale extremes |
| **Inconsistent calibration** | Different assessors use scales differently | Wide variance in scores for same risk | Conduct calibration workshops |
| **Anchoring** | First score influences subsequent scores | Scores drift from initial assessment | Score risks independently, then compare |
| **Confirmation bias** | Scores reflect desired outcome | Scores correlate with assessor preferences | Use blind scoring where possible |
| **Over-weighting** | Category weights distort comparisons | Some categories always dominate | Keep weights within reasonable ranges |
| **Under-scoring** | Conservative scoring misses real risks | High-impact risks not flagged | Review high-impact risks carefully |
| **Over-scoring** | Every risk is critical | Too many Critical/High risks | Force prioritization, limit Critical count |

## Scoring Validation

Validate risk scores through:

### Reasonableness Check
- Does the score match the risk description?
- Would stakeholders agree with this assessment?
- Is the score consistent with similar risks?

### Sensitivity Analysis
- How much does the score change with small probability/impact changes?
- Are there threshold effects (crossing Critical/High boundaries)?
- Document score sensitivity for high-priority risks

### Peer Review
- Have another assessor independently score the risk
- Compare and discuss discrepancies
- Reach consensus on final score

### Stakeholder Review
- Present scores to affected stakeholders
- Validate impact assessments
- Adjust based on stakeholder feedback

## Tooling Integration

Integrate scoring with:
- **Spreadsheets**: For simple risk registers with automatic score calculation
- **Risk management software**: For enterprise-wide risk tracking
- **Project management tools**: For tracking risk mitigation progress
- **Decision support systems**: For portfolio-level risk analysis

## Best Practices

1. **Document everything**: Every score must have clear probability, impact, and weight justification
2. **Be consistent**: Use the same scale interpretations across all assessments
3. **Calibrate regularly**: Conduct calibration sessions periodically
4. **Validate scores**: Don't accept scores without validation
5. **Use evidence**: Base scores on data, not just opinions
6. **Be transparent**: Make scoring criteria and methods visible to all stakeholders
7. **Iterate**: Refine scoring approach based on experience and feedback

## Interface Contract

When implementing risk scoring in an agent:

**Required**:
- Use the standard Probability × Impact × Weight formula
- Apply the standard 1-5 scales for Probability and Impact
- Use documented category weights
- Return raw and weighted scores

**Recommended**:
- Include score interpretation (Critical/High/Medium/Low)
- Provide score confidence level (High/Medium/Low)
- Document scoring assumptions and rationale
- Support sensitivity analysis

**Output format**:
```
{
  "probability": <1-5>,
  "probability_rationale": "<text>",
  "impact": <1-5>,
  "impact_rationale": "<text>",
  "category": "<technical|business|safety|security|operational|compliance>",
  "weight": <0.1-2.0>,
  "base_score": <calculated>,
  "weighted_score": <calculated>,
  "score_level": "<Critical|High|Medium|Low|Very Low>",
  "confidence": "<High|Medium|Low>"
}
```

## Validation Checkpoints

- [ ] All risks have documented probability and impact assessments
- [ ] Category weights are documented and justified
- [ ] Scores are calculated correctly (Probability × Impact × Weight)
- [ ] Score interpretations are consistent with the scale
- [ ] High scores have been validated through peer review
- [ ] Scoring assumptions are documented and reasonable
- [ ] Calibration has been performed for new assessment teams
