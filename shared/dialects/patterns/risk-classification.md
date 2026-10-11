---
type: pattern
family: risk
---

# Risk Classification Pattern Contract

Attaches to any agent performing risk identification — risk-analyst,
modernization-agent, upgrade-planner, or any agent that needs to categorize
and organize risks systematically. This contract establishes the **standard
risk taxonomy** that ensures risks are consistently categorized across
all domains and assessments.

Risk classification is **not just labeling** — it is **the foundation of
structured risk management**. Without consistent classification,
risks cannot be effectively tracked, correlated, or analyzed. A shared
classification scheme enables:

- **Systematic risk identification**: Ensures all risk types are considered
- **Consistent reporting**: Enables aggregation and comparison across projects
- **Effective correlation**: Allows identification of related risks across domains
- **Targeted mitigation**: Ensures mitigation strategies address the right risk types
- **Knowledge reuse**: Enables learning from past risk assessments

## The Discipline

Risk classification provides a **structured language** for discussing risks.
It transforms vague concerns into specific, categorized issues that can be
systematically addressed. The classification scheme must be:

- **Comprehensive**: Cover all possible risk types
- **Mutually exclusive**: Each risk belongs to exactly one primary category
- **Collectively exhaustive**: Every risk fits into at least one category
- **Hierarchical**: Support multiple levels of detail
- **Extensible**: Allow addition of domain-specific categories
- **Stable**: Categories don't change frequently

- **Classification drives action**: The category determines which agents
  and methodologies are applied
- **Domains have specialized categories**: Control systems have safety risks,
  business systems have financial risks, etc.
- **Context matters**: The same risk type may have different implications
  in different contexts
- **Multiple perspectives**: Consider technical, business, and stakeholder views

## Primary Risk Categories

The six primary risk categories form the foundation of the classification scheme:

### 1. Technical Risk
**Definition**: Risks related to the system's design, implementation, and operation.

**Subcategories**:
- **Architecture**: System structure, component interactions, scalability
- **Technology**: Choice of technologies, frameworks, libraries
- **Compatibility**: Integration with existing systems, standards compliance
- **Performance**: Speed, throughput, latency, resource usage
- **Reliability**: System uptime, failure rates, mean time between failures
- **Maintainability**: Ease of debugging, testing, updating, supporting
- **Complexity**: System understanding, modification difficulty
- **Testing**: Verification and validation effectiveness

**Common Technical Risks**:
- Incompatible dependencies or versions
- Performance bottlenecks or scalability limits
- Architecture not meeting requirements
- Technology obsolescence
- Difficult-to-maintain code
- Insufficient test coverage

**Typical agents**: code-reviewer, architect, upgrade-planner, model-validator

---

### 2. Business Risk
**Definition**: Risks related to financial, market, and organizational impacts.

**Subcategories**:
- **Cost**: Budget overruns, unexpected expenses, ROI not achieved
- **Schedule**: Timeline delays, missed deadlines, resource constraints
- **Market**: Competitive disadvantage, missed opportunities, changing requirements
- **Revenue**: Lost sales, reduced productivity, customer churn
- **Investment**: Sunk costs, opportunity costs, strategic misalignment
- **Organization**: Skills gaps, resistance to change, culture issues

**Common Business Risks**:
- Project cost exceeding budget
- Critical deadlines not met
- Market conditions changing during project
- Competitors releasing similar products first
- Team lacking required skills
- Organizational resistance to new system

**Typical agents**: modernization-agent, intake-analyst, architect

---

### 3. Safety Risk
**Definition**: Risks related to human safety, environmental protection, and
physical asset protection.

**Subcategories**:
- **Human Safety**: Injury, fatality, health impacts
- **Environmental**: Pollution, contamination, ecological damage
- **Equipment**: Physical damage to machinery, facilities, or infrastructure
- **Process Safety**: Chemical reactions, pressure vessels, hazardous operations
- **System Integrity**: Protection against catastrophic system failures

**Safety Criticality Levels**:
- **SIL 1**: Low safety integrity (minor injuries, localized damage)
- **SIL 2**: Medium safety integrity (serious injuries, significant damage)
- **SIL 3**: High safety integrity (multiple fatalities, major environmental damage)
- **SIL 4**: Very high safety integrity (catastrophic consequences)
- **ASIL A-D**: Automotive Safety Integrity Levels (A lowest, D highest)

**Common Safety Risks**:
- Failure modes causing physical harm
- Inadequate safety certifications (IEC 61508, ISO 26262, etc.)
- Lack of safety monitoring or shutoff mechanisms
- Insufficient safety testing or validation
- Human factors leading to unsafe operations

**Typical agents**: model-validator, hil-test-agent, control-designer

**Escalation**: ALL safety risks in SIL 3-4 or ASIL C-D systems must be
escalated to t4 for review.

---

### 4. Security Risk
**Definition**: Risks related to confidentiality, integrity, and availability
of information and systems.

**Subcategories**:
- **Confidentiality**: Unauthorized data access or disclosure
- **Integrity**: Unauthorized data modification or corruption
- **Availability**: System unavailability, denial of service
- **Authentication**: Weak or bypassed identity verification
- **Authorization**: Improper access control, privilege escalation
- **Auditability**: Inability to track or detect security events
- **Cryptography**: Weak encryption, improper key management

**Common Security Risks**:
- Vulnerabilities in dependencies or libraries
- Insufficient access controls or authentication
- Sensitive data exposure or leakage
- Denial of service attacks
- Supply chain attacks or compromised dependencies
- Insecure communication channels

**Typical agents**: threat-modeler, data-security-auditor, supply-chain-auditor

---

### 5. Operational Risk
**Definition**: Risks related to the day-to-day operation and maintenance of systems.

**Subcategories**:
- **Operability**: Ease of system operation, user experience
- **Supportability**: Availability of support, documentation quality
- **Trainability**: Ease of training users and maintainers
- **Availability**: System uptime, mean time to repair
- **Deployment**: Complexity of deployment, rollback capabilities
- **Monitoring**: Ability to detect and diagnose issues
- **Recovery**: Disaster recovery, backup and restore

**Common Operational Risks**:
- Complex operational procedures requiring expert knowledge
- Insufficient documentation or training materials
- Lack of monitoring or alerting for critical issues
- Long mean time to repair (MTTR)
- Difficult or risky deployment processes
- Inadequate backup and recovery procedures

**Typical agents**: devops, release-manager, modernization-agent

---

### 6. Compliance Risk
**Definition**: Risks related to adherence to laws, regulations, standards,
and internal policies.

**Subcategories**:
- **Regulatory**: Non-compliance with government regulations
- **Standards**: Non-compliance with industry standards
- **Certification**: Failure to achieve or maintain required certifications
- **Contractual**: Breach of contractual obligations
- **Internal Policy**: Violation of organizational policies or procedures
- **Ethical**: Failure to meet ethical guidelines or social responsibilities

**Common Compliance Risks**:
- Non-compliance with GDPR, HIPAA, SOX, or other regulations
- Failure to maintain ISO 9001, IEC 61508, or other certifications
- Contractual penalties for missed deliverables or SLAs
- Violation of internal security or quality policies
- Ethical concerns with AI/ML models or data usage

**Typical agents**: gdpr-auditor, data-auditor, modernization-agent

## Domain-Specific Categories

The primary categories can be extended with domain-specific subcategories:

### Control Systems Domain
- **Control Algorithm**: Stability, performance, robustness
- **Real-Time**: Timing constraints, deadline misses
- **Actuator/Sensor**: Hardware failures, measurement errors
- **Plant Interaction**: Impact on physical processes

### Software Development Domain
- **Code Quality**: Technical debt, code smells
- **Testing**: Test coverage, test effectiveness
- **Integration**: System integration complexity
- **Dependencies**: Library and framework risks

### Data Domain
- **Data Quality**: Accuracy, completeness, consistency
- **Data Privacy**: Personal data protection
- **Data Security**: Data breach, data loss
- **Data Governance**: Ownership, lineage, retention

### Modernization Domain
- **Legacy Integration**: Connecting old and new systems
- **Data Migration**: Moving data between systems
- **Cutover**: Transition from old to new system
- **Rollback**: Ability to revert to legacy system

## Risk Attribute Taxonomy

Beyond categories, risks can be classified by additional attributes:

### Risk Source
- **Internal**: Originating from within the system or organization
- **External**: Originating from outside (vendors, environment, regulations)
- **Human**: Caused by human actions or errors
- **Technical**: Caused by technical failures or limitations
- **Natural**: Caused by natural events (disasters, weather)

### Risk Type
- **Single Event**: One-time occurrence
- **Continuous**: Ongoing condition or situation
- **Cumulative**: Multiple occurrences building up over time
- **Systemic**: Inherent in the system design or architecture

### Risk Timing
- **Immediate**: Risk can materialize at any time
- **Delayed**: Risk materializes after a delay or trigger
- **Deferred**: Risk is pushed to a future date or phase
- **Conditional**: Risk only materializes under specific conditions

### Risk Detectability
- **Obvious**: Risk is easily detectable when it occurs
- **Detectable**: Risk can be detected with monitoring or testing
- **Hidden**: Risk is difficult to detect (may require special tools or expertise)
- **Silent**: Risk may occur without any visible signs

### Risk Controllability
- **Controllable**: Risk can be effectively mitigated or managed
- **Partially Controllable**: Some mitigation possible, but not complete
- **Uncontrollable**: Risk cannot be mitigated (only accepted or transferred)

## Classification Workflow

### Step 1: Identify the Risk
- Describe the risk in clear, specific terms
- Identify what could go wrong and the potential consequences

### Step 2: Determine Primary Category
- Map the risk to one of the six primary categories
- Use the category definitions and examples as guidance
- If uncertain, use the category with the highest potential impact

### Step 3: Identify Subcategories
- Drill down into the specific subcategory or subcategories
- A risk can belong to multiple subcategories
- Document all relevant subcategories

### Step 4: Apply Domain-Specific Categories
- If applicable, apply domain-specific classification
- Control systems: Is it a control algorithm risk? Real-time risk?
- Modernization: Is it a data migration risk? Cutover risk?

### Step 5: Assign Attributes
- Determine risk source, type, timing, detectability, controllability
- Document all relevant attributes

### Step 6: Validate Classification
- Does the classification make sense given the risk description?
- Would other assessors classify it the same way?
- Is there a more appropriate category?

## Classification Decision Tree

```
Is the risk related to...
├── System design, technology, or implementation?
│   └── TECHNICAL
│
├── Money, market, or organization?
│   └── BUSINESS
│
├── Human safety, environment, or physical assets?
│   └── SAFETY
│
├── Information security, confidentiality, or integrity?
│   └── SECURITY
│
├── Day-to-day operation, support, or maintenance?
│   └── OPERATIONAL
│
└── Laws, regulations, standards, or policies?
    └── COMPLIANCE
```

For each primary category, use subcategory decision trees:

**Technical Risk**:
```
Is it about...
├── System architecture or structure? → Architecture
├── Technology choices? → Technology
├── Integration with other systems? → Compatibility
├── Speed or resource usage? → Performance
├── System uptime or failures? → Reliability
├── Code maintenance? → Maintainability
├── Complexity? → Complexity
└── Testing? → Testing
```

**Safety Risk** (in control systems):
```
Does it involve...
├── Potential for human injury? → Human Safety
├── Environmental damage? → Environmental
├── Equipment damage? → Equipment
├── Process safety (chemical, pressure, etc.)? → Process Safety
└── System failure with catastrophic consequences? → System Integrity
```

## Classification Examples

| Risk Description | Primary Category | Subcategories | Domain-Specific |
|-----------------|------------------|---------------|-----------------|
| PLC firmware upgrade fails | Technical | Compatibility, Reliability | Control Systems - Firmware |
| Migration exceeds budget | Business | Cost, Investment | Modernization |
| Loss of SIL 2 certification | Safety | System Integrity | Control Systems - Safety |
| Database breached | Security | Confidentiality, Integrity | Data - Security |
| Complex deployment process | Operational | Deployment, Supportability | DevOps |
| GDPR non-compliance | Compliance | Regulatory | Data - Privacy |
| Control algorithm becomes unstable | Technical | Architecture, Control Algorithm | Control Systems - Control |
| Real-time deadline missed | Technical | Performance, Real-Time | Control Systems - Real-Time |

## Common Classification Pitfalls

| Pitfall | Description | Detection | Prevention |
|---------|-------------|-----------|------------|
| **Category overload** | Too many categories, leading to confusion | Categories rarely used or overlapping | Keep to 6 primary + domain-specific |
| **Inconsistent application** | Same risk type classified differently | Classification varies by assessor | Use decision trees, provide examples |
| **Over-specialization** | Too many domain-specific categories | Categories only used in one context | Limit to truly domain-unique risks |
| **Under-classification** | Risks not assigned to any category | Uncategorized risks in register | Mandatory category assignment |
| **Wrong primary category** | Risk assigned to wrong main category | Risk doesn't fit category definition | Use decision tree, validate |
| **Ignoring context** | Not considering domain-specific factors | Generic classification misses nuances | Apply domain-specific categories |
| **Inconsistent hierarchy** | Subcategories not properly nested | Confusing category structure | Maintain clear hierarchy |

## Classification Validation

Validate risk classification through:

### Consistency Check
- Are similar risks classified the same way?
- Is the classification consistent with category definitions?
- Would stakeholders agree with the classification?

### Completeness Check
- Does every risk have a primary category?
- Are relevant subcategories identified?
- Are domain-specific categories applied where appropriate?

### Usefulness Check
- Does the classification help in understanding the risk?
- Does it inform appropriate mitigation strategies?
- Does it support effective risk correlation?

### Stakeholder Review
- Present classifications to domain experts
- Validate with affected stakeholders
- Adjust based on feedback

## Tooling Integration

Integrate classification with:
- **Risk registers**: Mandatory category fields in risk tracking
- **Reporting**: Group and filter risks by category
- **Analysis**: Identify patterns and trends by category
- **Dashboards**: Visual representation of risk distribution by category

## Best Practices

1. **Use decision trees**: Standardize classification approach
2. **Provide examples**: Help assessors understand category boundaries
3. **Validate classifications**: Don't accept unvalidated classifications
4. **Keep it simple**: Avoid excessive category proliferation
5. **Document rationale**: Explain why a risk was assigned to a particular category
6. **Review periodically**: Update classification scheme as needed
7. **Train assessors**: Ensure consistent application across the organization

## Interface Contract

When implementing risk classification in an agent:

**Required**:
- Assign exactly one primary category from the six main categories
- Allow multiple subcategories
- Support domain-specific category extensions

**Recommended**:
- Use standardized category names and definitions
- Provide classification decision trees
- Include classification confidence level
- Support classification validation

**Output format**:
```
{
  "primary_category": "<technical|business|safety|security|operational|compliance>",
  "subcategories": ["<list of subcategories>"],
  "domain_category": "<domain-specific category, if applicable>",
  "source": "<internal|external|human|technical|natural>",
  "type": "<single_event|continuous|cumulative|systemic>",
  "timing": "<immediate|delayed|deferred|conditional>",
  "detectability": "<obvious|detectable|hidden|silent>",
  "controllability": "<controllable|partially_controllable|uncontrollable>",
  "classification_confidence": "<High|Medium|Low>"
}
```

## Validation Checkpoints

- [ ] All risks have a primary category assigned
- [ ] Subcategories are documented where applicable
- [ ] Domain-specific categories are applied for specialized domains
- [ ] Classification is consistent with definitions and examples
- [ ] Classification has been validated
- [ ] Stakeholders have reviewed and agreed with classifications
- [ ] Classification scheme is documented and accessible
